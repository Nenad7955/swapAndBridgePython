import json


class ContractBase:
    def __init__(self, web3, account_manager, abi_path):
        self.web3 = web3
        self.account_manager = account_manager

        with open(abi_path, "r") as fp:
            self.abi = json.loads(fp.read())

    def change_account(self):
        self.account_manager.change_account()

    def my_addr(self):
        return self.account_manager.get_account()['address']

    def priv_key(self):
        return self.account_manager.get_account()['key']

    def send_tx(self, tx):
        signed_txn = self.web3.eth.account.sign_transaction(tx, self.priv_key())
        it = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        print(it.hex())

    def get_nonce(self):
        return self.web3.eth.get_transaction_count(self.my_addr())
