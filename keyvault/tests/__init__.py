import os

from keyvault import secrets_to_environment

# The keyvault name is stored in github secrets.
secrets_to_environment(keyvault_name=os.environ.get("TEST_KEYVAULT_NAME"))
