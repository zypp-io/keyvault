from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential


def create_keyvault_client(keyvault_name: str):

    keyvault_url = f"https://{keyvault_name}.vault.azure.net"
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=keyvault_url, credential=credential)  # noqa

    return client
