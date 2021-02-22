<p align="center"><img alt="logo" src="https://www.zypp.io/static/assets/img/logos/Main logo - White/Zypp - White - JPG.jpg" width="200"></p>

Azure key vaults
===
> Repository for explaining how to use Azure key vaults in our projects.


## Index
- [Usage](#usage)
    -[get_secrets](#get_secrets)
    -[upload_secrets](#upload_secrets)
- [mandatory .env variables](#mandatory-env-variables)

# Usage
This package is designed for easily pulling and creating secrets in Azure key vaults. There are 2 
functions that can be used:

## get_secrets
This function can be used to pull secrets from the vault. This function will only work if you have
set the [required environment variables](#mandatory-env-variables)

```python
from keyvault import get_secrets

secrets = get_secrets(keyvault_name="my-keyvault-name")

# Returns a dictionary containing secret_name, secret_value pairs
```
     
## upload_secrets
This function is designed for making it easy to upload sensitive project secrets to Azure key vault.
The function reads the `.env` file and uploads the names and values to Azure key vault.

```python
from keyvault import upload_secrets

secrets = upload_secrets(keyvault_name="my-keyvault-name")

# Uploads your current .env variables to azure key vault
```

# mandatory .env variables
There are 4 environment variables that are necessary for authenticating with the azure key vault.
These variables always need to be present in the project in order for the secrets to be retrieved.

```.env
AZURE_KEYVAULT_NAME=my-keyvault-name
AZURE_CLIENT_ID=REPLACE-ME
AZURE_CLIENT_SECRET=REPLACE-ME
AZURE_TENANT_ID=REPLACE-ME
```