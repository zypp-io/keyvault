import logging
from pprint import pprint
from datetime import datetime, timedelta
from keyvault import delete_keyvault_secrets, dict_to_keyvault, get_keyvault_secrets
from keyvault.tests import test_keyvault
"""
This is the testing suite for twinfield tools.

"""


# #############################
# #### CREATE METHOD TESTS ####
# #############################

def test_create_secrets():
    my_secrets = {"USERNAME": "PYTHON2"}
    expiry_date = datetime.now() + timedelta(days=80)

    dict_to_keyvault(
        keyvault_name=test_keyvault,
        secret_dict=my_secrets,
        expires_on=expiry_date,
        content_type="text/plain"
    )


def test_keyvault_download_upload():
    """
    Test for functions used in this package.
    """

    logging.info("***START TEST UPLOAD DICTIONARY TO KEYVAULT***")

    my_secrets = {"USERNAME": "PYTHON", "PASSWORD": "12kNDi2lm§!"}

    dict_to_keyvault(keyvault_name=test_keyvault, secret_dict=my_secrets)

    logging.info("***START TEST DOWNLOADING SECRETS FROM KEYVAULT***")

    downloaded_secrets = get_keyvault_secrets(keyvault_name=test_keyvault)
    pprint(downloaded_secrets)

    assert my_secrets == downloaded_secrets

    logging.info("***START TEST DELETING SECRETS FROM KEYVAULT***")

    delete_keyvault_secrets(
        keyvault_name=test_keyvault, secret_list=["USERNAME"]
    )
    downloaded_updated_secrets = get_keyvault_secrets(
        keyvault_name=test_keyvault
    )
    pprint(downloaded_updated_secrets)


if __name__ == "__main__":
    test_create_secrets()
    test_keyvault_download_upload()

