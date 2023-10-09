import json


class ContractBase:
    def __init__(self, web3, priv_key, my_addr, abi_path):
        self.web3 = web3
        self.priv_key = priv_key
        self.my_addr = my_addr

        with open(abi_path, "r") as fp:
            self.abi = json.loads(fp.read())

    def send_tx(self, tx):
        signed_txn = self.web3.eth.account.sign_transaction(tx, self.priv_key)
        it = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        print(it.hex())

    def get_nonce(self):
        return self.web3.eth.get_transaction_count(self.my_addr)
