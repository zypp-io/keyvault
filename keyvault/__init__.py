from dotenv import load_dotenv, find_dotenv
from keyvault.get_secrets import get_secrets
from keyvault.upload_env_to_vault import upload_secrets

import logging

logging.basicConfig(
    format="%(asctime)s.%(msecs)03d [%(levelname)-5s] [%(name)s] - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO,
)
logging.getLogger("azure.core.pipeline.policies.http_logging_policy").setLevel(logging.WARNING)
logging.getLogger("azure.identity").setLevel(logging.WARNING)

load_dotenv(find_dotenv(), verbose=True)
