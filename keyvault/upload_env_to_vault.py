import logging
from keyvault.auth import create_keyvault_client
from dotenv import find_dotenv


def get_dotenv_secrets() -> dict:
    """
    This function is designed for easily getting the dictionary of secrets that are currently
    stored in the local .env file. This is useful when you want to create the key value pairs
    in Azure key vaults, using the azure package.

    Returns
    -------
        secrets: dict
            dictionairy containing local secret keys.
    """
    dotenv_location = find_dotenv()
    if dotenv_location == "":
        logging.info("no .env file found")
        return dict()

    with open(dotenv_location, "r") as f:
        lines = f.read().splitlines()  # read all the lines in the .env file

    local_secrets = {}
    ignore_list = [
        "AZURE_KEYVAULT_NAME",
        "AZURE_CLIENT_ID",
        "AZURE_CLIENT_SECRET",
        "AZURE_TENANT_ID",
    ]

    for line in lines:
        if line.find("=") != -1:  # only key value pairs (not the comments)
            secret_key = line.split("=", 1)[0]
            if secret_key in ignore_list:  # some .env settings need to be excluded.
                continue

            secret_value = line.split("=", 1)[1].replace('"', "")
            secret_key = secret_key.replace("_", "-")  # Azure does not accept _ in names. FFS
            local_secrets[secret_key] = secret_value  # save key, values to a the dictionary

    return local_secrets


def upload_secrets(keyvault_name: str):
    """
    Parameters
    ----------
    keyvault_name: str
        name of the keyvault containing the secrets

    Returns
    -------
    None
        creates the secret in the keyvault.
    """

    client = create_keyvault_client(keyvault_name=keyvault_name)
    local_secrets = get_dotenv_secrets()

    if not len(local_secrets):
        logging.info("no secrets found in .env file")
        return None

    print(f"about to create the secrets: {', '.join(local_secrets.keys())}")

    _consent = input("continue? (Y/n)").strip()[0].upper()  # first character only, to upper.

    if _consent != "Y":  # if not equal to yes, abort the creation process.
        return None

    for secret_name, secret_value in local_secrets.items():
        client.set_secret(secret_name, secret_value)

    logging.info(f"succesfully created {len(local_secrets)} secrets!")


if __name__ == "__main__":

    upload_secrets(keyvault_name="staffing-general")
