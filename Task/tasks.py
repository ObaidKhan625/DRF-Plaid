from .models import Item
from celery import shared_task
from plaid import Client
import datetime

# from .config import PLAID_CLIENT_ID, PLAID_SECRET, PLAID_ENV
PLAID_CLIENT_ID = '6373e3838186650013202d02'
PLAID_SECRET = '18a24ec488686aa1cd2a0801258bd8'
PLAID_ENV = 'sandbox'

def get_plaid_client():
    return Client(client_id=PLAID_CLIENT_ID, secret=PLAID_SECRET, environment=PLAID_ENV)

# # Get the account
@shared_task
def get_accounts(access_token):
    client = get_plaid_client()
    accounts = client.Accounts.get(access_token)
    return accounts

# # Acquire access token
@shared_task
def get_access_token(public_token):
    client = get_plaid_client()
    exchange_response = client.Item.public_token.exchange(public_token)
    return exchange_response

# # Get transactions between these dates
@shared_task
def get_transactions(access_token, start_date, end_date):
    client = get_plaid_client()
    transactions = client.Transactions.get(access_token, start_date, end_date)
    return transactions

@shared_task
def fetch_transactions(item_id=None, new_transactions=500):
    # transactions of two years
    start_date = '{:%Y-%m-%d}'.format(
    datetime.datetime.now() + datetime.timedelta(-2*365))
    end_date = '{:%Y-%m-%d}'.format(datetime.datetime.now())
    access_token = Item.objects.filter(item_id=item_id)[0].access_token
    client = get_plaid_client()
    transactions = client.Transactions.get(access_token, start_date, end_date)
    return transactions