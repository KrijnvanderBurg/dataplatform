...


1. Remote Backend: Deployment Steps:
Terraform requires a storage account in Azure for a remote backend, it is used to store the state files of terraform deployments to track infrastructure state and plan changes.

    1. Create resource group: rg-init-dev-gwc-01
    2. Add management lock to resource group: rg-init-dev-gwc-01-lock, CanNotDelete
    3. Create storage account sttfbackenddevgwc01
    4. Create storage container tfbackend