from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential


def create_keyvault_client(keyvault_name: str):
    """

    Parameters
    ----------
    keyvault_name: str
        keyvault name necessary for connecting to the appropriate secrets.

    Returns
    -------
    client: SecretClient
        SecretClient class of azure identity package.
    """

    keyvault_url = f"https://{keyvault_name}.vault.azure.net"
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=keyvault_url, credential=credential)  # noqa

    return client
