import logging
from time import sleep

from azure.core.exceptions import ResourceExistsError
from azure.keyvault.secrets import SecretClient
from tqdm import tqdm

from keyvault.auth import create_keyvault_client


def get_dotenv_secrets(dotenv_file: str) -> dict:
    """
    This function is designed for easily getting the dictionary of secrets that are currently
    stored in the local .env file. This is useful when you want to create the key value pairs
    in Azure key vaults, using the azure package.

    Parameters
    ----------
    dotenv_file: str
        dotenv file containing the local secrets

    Returns
    -------
        secrets: dict
            dictionairy containing local secret keys.
    """

    if dotenv_file == "":
        logging.info("no .env file found")
        return dict()

    with open(dotenv_file, "r") as f:
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
            local_secrets[secret_key] = secret_value  # save key, values to a the dictionary

    return local_secrets


def dict_to_keyvault(keyvault_name: str, secret_dict: dict) -> None:
    """
    Parameters
    ----------
    keyvault_name: str
        name of the keyvault containing the secrets
    secret_dict: dict
        dictionary containing secrets

    Returns
    -------
    None
        creates the secret in the keyvault.
    """

    client = create_keyvault_client(keyvault_name=keyvault_name)
    send_secrets(client, secret_dict)


def send_secrets(client: SecretClient, secrets: dict) -> None:
    """

    Parameters
    ----------
    client : SecretClient
        keyvault client

    secrets: dict
        dictionary containing the secrets

    Returns
    -------
        None. Uploads the secrets to azure keyvault.

    """

    for secret_name, secret_value in tqdm(secrets.items(), desc="creating secrets"):
        secret_name = secret_name.replace("_", "-")  # Azure does not accept _ in names. FFS
        logging.debug(f"creating secret name {secret_name}")
        try:
            client.set_secret(secret_name, secret_value)
        except ResourceExistsError:
            # if the secret already exists, first recover the secret and then update the secret.
            client.begin_recover_deleted_secret(secret_name)
            # it takes some time to recover the secret.

            for _ in tqdm(range(10), desc="Secret is in soft delete state: Waiting to recover..."):
                sleep(1)

            client.set_secret(secret_name, secret_value)

    logging.info(f"succesfully created {len(secrets)} secrets!")


def dotenv_to_keyvault(keyvault_name: str, dotenv_file: str) -> None:
    """
    Parameters
    ----------
    dotenv_file: str
        file location of the .env file
    keyvault_name: str
        name of the keyvault containing the secrets

    Returns
    -------
    None
        creates the secret in the keyvault.
    """

    client = create_keyvault_client(keyvault_name=keyvault_name)
    local_secrets = get_dotenv_secrets(dotenv_file)

    if not len(local_secrets):
        logging.info("no secrets found in .env file")
        return None
    send_secrets(client, local_secrets)


def delete_keyvault_secrets(keyvault_name: str, secret_list: list) -> None:
    """
    Function for deleting a list of secrets in the keyvault.
    Parameters
    ----------
    keyvault_name: str
        name of the keyvault containing the secrets
    secret_list: list
        dictionary containing secrets that need to be deleted.

    Returns
    -------
    None
        creates the secret in the keyvault.
    """

    client = create_keyvault_client(keyvault_name=keyvault_name)
    for secret in secret_list:
        client.begin_delete_secret(secret).result()

    logging.info(f"succesfully deleted secrets {''.join(secret_list)}")
