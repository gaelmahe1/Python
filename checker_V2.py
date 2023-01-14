import bitcoinlib

def check_balance(address):
    balance = bitcoinlib.services.blockcypher.get_address_balance(address)
    return balance['balance']

def check_transactions(address):
    first_seen = bitcoinlib.services.blockcypher.get_address_first_seen(address)
    last_seen = bitcoinlib.services.blockcypher.get_address_last_seen(address)
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

address = input("Enter the Bitcoin address to check: ")
if check_abandoned(address):
    print("This address has likely been abandoned.")
    balance = check_balance(address)
    if balance > 0:
        priv = input("Enter the private key of the address: ")
        try:
            transfer_funds(priv, 'YOUR_WALLET_ADDRESS', balance)
            print("Funds transferred successfully.")
        except:
            print("An error occurred while transferring the funds.")
else:
    print("This address is still in use.")
