import os
from azure.common.credentials import ServicePrincipalCredentials
import azure.mgmt.subscription
from azure.mgmt.billing import BillingManagementClient
from azure.mgmt.subscription import SubscriptionClient

subscription_id = os.environ['AZURE_SUBSCRIPTION_ID']

credentials = ServicePrincipalCredentials(
    client_id=os.environ['AZURE_CLIENT_ID'],
    secret=os.environ['AZURE_CLIENT_SECRET'],
    tenant=os.environ['AZURE_TENANT_ID']
)

billing_client = BillingManagementClient(credentials, subscription_id)
subscription_client = SubscriptionClient(credentials, subscription_id)

# Obtain the list of accounts within the Enrollment
enrollment_accounts = list(billing_client.enrollment_accounts.list())
print(len(enrollment_accounts))

# The two options for EA are MS-AZR-0017P (production use) and MS-AZR-0148P (dev/test, needs to be turned on using the EA portal).
creation_parameters = azure.mgmt.subscription.models.SubscriptionCreationParameters(offer_type='MS-AZR-0017P')

# Create a new subscription.. This just creates on the first account in the list
creation_result = subscription_client.subscription_factory.create_subscription_in_enrollment_account(enrollment_accounts[0].name,creation_parameters)