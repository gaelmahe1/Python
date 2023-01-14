import requests
import datetime

# Add your BlockCypher API token
api_token = "e83b0d6df34e407e9a506080eb64b40f"

# Add the destination wallet address
destination_address = "3NKys6Wqsz2NWWYKmrCLsHPkQbfjrGatjG"

# Headers for the API request
headers = {"Content-Type": "application/json", "X-API-Key": api_token}


def check_balance(address):
    # Make a GET request to the BlockCypher API to get the balance of the address
    url = f"https://api.blockcypher.com/v1/btc/main/addrs/{address}"
    response = requests.get(url, headers=headers)
    balance = response.json()["balance"]
    return balance


def check_transactions(address):
    # Make a GET request to the BlockCypher API to get the first and last seen times of the address
    url = f"https://api.blockcypher.com/v1/btc/main/addrs/{address}"
    response = requests.get(url, headers=headers)
    txrefs = response.json()["txrefs"]
    if not txrefs:
        return (None, None)
    first_tx = datetime.datetime.strptime(txrefs[0]["confirmed"], "%Y-%m-%dT%H:%M:%SZ")
    last_tx = datetime.datetime.strptime(txrefs[-1]["confirmed"], "%Y-%m-%dT%H:%M:%SZ")

    return (first_tx, last_tx)


def check_abandoned(address):
    balance = check_balance(address)
    if balance <= 0:  # added a check for balance less than or equal to zero
        return False
    first_tx, last_tx = check_transactions(address)
    if not first_tx:  # added a check for None values
        return True
    age = (datetime.datetime.now() - first_tx).days
    if age > 365:
        return True
    else:
        return False


def transfer_funds(from_address, to_address, amount):

    if amount <= 0:  # added a check for amount less than or equal to zero
        return
    # Prepare the data for the API request
    data = {
        "inputs": [{"address": from_address}],
        "outputs": [{"address": to_address, "value": amount}],
    }

    # Make a POST request to the BlockCypher API to create and send the transaction
    url = "https://api.blockcypher.com/v1/btc/main/txs/new"
    response = requests.post(url, json=data, headers=headers)
    print(response.json())
    if response.status_code != 201:
        print(f'Error: {response.json().get("error")}')
    else:
        print(
            f"Transaction sent from {from_address} to {to_address} with amount {amount}"
        )


address = input("Enter the Bitcoin address to check: ")
if check_abandoned(address):
    print(f"This address {address} has likely been abandoned.")
    transfer_amount = check_balance(address)
    transfer_funds(address, destination_address, transfer_amount)
else:
    print(f"This address {address} is still in use.")
