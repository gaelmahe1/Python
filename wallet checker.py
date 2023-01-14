import requests

def check_balance(address):
    url = 'https://blockchain.info/q/addressbalance/' + address
    response = requests.get(url)
    balance = int(response.text) / 100000000
    return balance

def check_transactions(address):
    url = 'https://blockchain.info/q/addressfirstseen/' + address
    response = requests.get(url)
    first_seen = int(response.text)
    url = 'https://blockchain.info/q/addresslastseen/' + address
    response = requests.get(url)
    last_seen = int(response.text)
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

    from bitcoin import *

def transfer_funds(from_address, to_address, amount):
    priv = privkey_to_wif(from_address) # import the private key
    unspent = listunspent(priv) # get the unspent outputs
    inputs = [{'txid':utxo['txid'], 'vout':utxo['vout']} for utxo in unspent] # create inputs
    outputs = {to_address: amount} # create outputs
    signed_tx = signrawtransaction(createrawtransaction(inputs, outputs), priv) # sign the transaction
    sendrawtransaction(signed_tx) # broadcast the transaction
    pass

address = input("Enter the Bitcoin address to check: ")
if check_abandoned(address):
    print("This address has likely been abandoned.")
    transfer_funds(address, 'YOUR_WALLET_ADDRESS', check_balance(address))
else:
    print("This address is still in use.")








from bitcoin import *

def transfer_funds(from_address, to_address, amount):
    priv = privkey_to_wif(from_address) # import the private key
    unspent = listunspent(priv) # get the unspent outputs
    inputs = [{'txid':utxo['txid'], 'vout':utxo['vout']} for utxo in unspent] # create inputs
    outputs = {to_address: amount} # create outputs
    signed_tx = signrawtransaction(createrawtransaction(inputs, outputs), priv) # sign the transaction
    sendrawtransaction(signed_tx) # broadcast the transaction
