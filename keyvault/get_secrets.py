from keyvault.auth import create_keyvault_client


def get_secret_list(client) -> list:
    """

    Parameters
    ----------
    client
        authenticated keyvault client

    Returns
    -------
    secrets: list
        list of secret names that are currently available in keyvault

    """
    secret_properties = client.list_properties_of_secrets()
    secrets = list()
    for secret_property in secret_properties:
        secrets.append(secret_property.name)

    return secrets


def get_secrets(keyvault_name: str) -> dict:
    """
    Parameters
    ----------
    keyvault_name: str
        name of the keyvault containing the secrets

    Returns
    -------
        d: dict
            dictionary containing the secrets in the keyvault
    """

    client = create_keyvault_client(keyvault_name=keyvault_name)
    secret_names = get_secret_list(client)
    d = dict()
    for secret_name in secret_names:
        d[secret_name] = client.get_secret(secret_name).value

    return d


if __name__ == "__main__":

    azure_secrets = get_secrets(keyvault_name="staffing-general")
    print(azure_secrets)
