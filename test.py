import requests
import json

# Add your own API key for the blockchain.info API
API_KEY = 'YOUR_API_KEY'

# Function to check the balance of a wallet address
def check_balance(address):
    url = f'https://blockchain.info/q/addressbalance/{address}?api_code={API_KEY}'
    response = requests.get(url)
    balance = int(response.text) / 100000000
    return balance

# Function to check the first and last seen times of a wallet address
def check_transactions(address):
    url = f'https://blockchain.info/q/addressfirstseen/{address}?api_code={API_KEY}'
    response = requests.get(url)
    first_seen = int(response.text)
    url = f'https://blockchain.info/q/addresslastseen/{address}?api_code={API_KEY}'
    response = requests.get(url)
    last_seen = int(response.text)
    return (first_seen, last_seen)

# Function to check if a wallet address has been abandoned
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

# Function to transfer funds from one wallet address to another
def transfer_funds(from_address, to_address, priv, amount):
    url = f'https://blockchain.info/merchant/{from_address}/payment?password={priv}&to={to_address}&amount={amount}&api_code={API_KEY}'
    response = requests.get(url)
    result = json.loads(response.text)
    if 'error' in result:
        print(result['error'])
    else:
        print("Funds transferred successfully.")

# Ask the user to enter a
