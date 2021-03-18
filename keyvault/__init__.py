from keyvault.get_secrets import secrets_to_environment
from keyvault.utils import get_dotenv_secrets
from keyvault.get_secrets import get_keyvault_secrets
from keyvault.utils import dotenv_to_keyvault
from keyvault.utils import dict_to_keyvault


import logging

logging.basicConfig(
    format="%(asctime)s.%(msecs)03d [%(levelname)-5s] [%(name)s] - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO,
)
logging.getLogger("azure.core.pipeline.policies.http_logging_policy").setLevel(logging.WARNING)
logging.getLogger("azure.identity").setLevel(logging.WARNING)
