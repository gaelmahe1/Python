import bitcoinlib

# Function to check the balance of a given address
def check_balance(address):
    # Use the bitcoinlib service to get the balance of the address
    balance = bitcoinlib.services.blockcypher.get_address_balance(address)
    # Return the balance
    return balance['balance']

# Function to check the first and last seen timestamps of a given address
def check_transactions(address):
    # Use the bitcoinlib service to get the first seen timestamp of the address
    first_seen = bitcoinlib.services.blockcypher.get_address_first_seen(address)
    # Use the bitcoinlib service to get the last seen timestamp of the address
    last_seen = bitcoinlib.services.blockcypher.get_address_last_seen(address)
    # Return the first and last seen timestamps
    return (first_seen, last_seen)

# Function to check if an address has been abandoned
def check_abandoned(address):
    # Get the balance of the address
    balance = check_balance(address)
    # If the balance is 0, return False (the address is not abandoned)
    if balance == 0:
        return False
    # Get the first and last seen timestamps of the address
    first_seen, last_seen = check_transactions(address)
    # Calculate the age of the address
    age = (last_seen - first_seen) / (60 * 60 * 24)
    # If the age of the address is greater than 365 days, return True (the address is abandoned)
    if age > 365:
        return True
    # Otherwise, return False (the address is not abandoned)
    else:
        return False

# Function to transfer funds from one address to another
def transfer_funds(from_address, to_address, amount):
    # Create a PrivateKey object from the private key of the from_address
    priv = bitcoinlib.keys.PrivateKey(from_address)
    # Use the bitcoinlib service to get the unspent outputs of the from_address
    unspent = bitcoinlib.services.blockcypher.get_address_unspent(from_address)
    # Create the inputs for the transaction
    inputs = [{'txid': utxo['txid'], 'vout': utxo['vout']} for utxo in unspent]
    # Create the outputs for the transaction
    outputs = {to_address: amount}
    # Sign the transaction with the private key of the from_address
    signed_tx = priv.sign




################################################################################################



import bitcoinlib
import requests

#Add the API key to the headers
headers = {'Content-Type': 'application/json', 'X-API-Key': 'c1f063a7c0594256b2ec0faaf0878a5c'}

def check_balance(address):
#Make a GET request to the BlockCypher API to get the balance of the address
url = f'https://api.blockcypher.com/v1/btc/main/addrs/{address}'
response = requests.get(url, headers=headers)
balance = response.json()['balance']
return balance

def check_transactions(address):
#Make a GET request to the BlockCypher API to get the first and last seen times of the address
url = f'https://api.blockcypher.com/v1/btc/main/addrs/{address}'
response = requests.get(url, headers=headers)
first_seen = response.json()['first_tx_time']
last_seen = response.json()['last_tx_time']
return (first_seen, last_seen)

def check_abandoned(address):
balance = check_balance(address)
if balance == 0:
return False
first_seen, last_seen = check_transactions(address)
age = (last_seen - first_seen) / (60 * 60 * 24)
if age > 365:
return True
else:
return False

def transfer_funds(from_address, to_address, amount):
priv = bitcoinlib.keys.PrivateKey(from_address)
unspent = bitcoinlib.services.blockcypher.get_address_unspent(from_address)
inputs = [{'txid': utxo['txid'], 'vout': utxo['vout']} for utxo in unspent]
outputs = {to_address: amount}
signed_tx = priv.sign_transaction(inputs, outputs)
bitcoinlib.services.blockcypher.broadcast_signed_transaction(signed_tx)

address =



