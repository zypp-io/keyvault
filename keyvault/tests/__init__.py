import os

# The keyvault name is stored in github secrets.
try:
    from dotenv import load_dotenv

    load_dotenv(override=True)
    print("keyvault", os.environ.get("TEST_KEYVAULT_NAME"))
except ImportError:
    print("dotenv not installed")

test_keyvault = os.environ.get("TEST_KEYVAULT_NAME")
