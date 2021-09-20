import logging

from keyvault.get_secrets import get_keyvault_secrets, secrets_to_environment
from keyvault.utils import (
    delete_keyvault_secrets,
    dict_to_keyvault,
    dotenv_to_keyvault,
    get_dotenv_secrets,
)

logging.getLogger("azure.core.pipeline.policies.http_logging_policy").setLevel(logging.WARNING)
logging.getLogger("azure.identity").setLevel(logging.WARNING)
