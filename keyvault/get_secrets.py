import logging
from azure.core.exceptions import ServiceRequestError
import os
from time import sleep

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
        if secret_property.enabled:
            secrets.append(secret_property.name)

    return secrets


def get_keyvault_secrets(keyvault_name: str) -> dict:
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


def secrets_to_environment(keyvault_name: str) -> None:
    """
    This function the azure keyvault secrets in the environment variables.

    Parameters
    ----------
    keyvault_name: str
        name of the keyvault containing the secrets

    Returns
    -------
    None
    """
    # use retry 5 times for the azure core exception Service request error
    retries = 0
    max_retries = 5
    secrets = None
    while retries < max_retries:
        try:
            secrets = get_keyvault_secrets(keyvault_name)
            break
        except ServiceRequestError:
            logging.warning("Could not connect to the keyvault, try again")
            retries += 1
            if retries >= max_retries:
                raise ServiceRequestError("Could not connect to the keyvault, max retries reached")
            sleep_time = 1 * (2 ** (retries - 1))
            logging.info(f"Request failed. Retrying in {sleep_time} seconds")
            sleep(sleep_time)
    if secrets is not None:
        logging.debug("replacing - characters with _ character")
        secrets = {k.replace("-", "_"): v for k, v in secrets.items()}

        for key, value in secrets.items():
            os.environ[key] = value

        logging.info(f"succesfully stored {len(secrets)} keyvault secrets as environment variables.")
    else:
        logging.error("No secrets were stored in the environment variables")
