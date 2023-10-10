from Contracts.ContractBase import ContractBase


class ERC20(ContractBase):
    def __init__(self, web3, accounts, token_addr):
        super().__init__(web3, accounts, "./abi/erc20.json")

        self.contract = self.web3.eth.contract(address=token_addr, abi=self.abi)

    def approve(self, addr, amount):
        tx = (
            self.contract.functions.approve(addr, amount)
            .build_transaction({
                "from": self.my_addr(), "nonce": self.get_nonce()
            }))
        self.send_tx(tx)

    def mint(self, addr, amount):
        tx = (
            self.contract.functions.mint(addr, amount)
            .build_transaction({
                "from": self.my_addr(), "nonce": self.get_nonce()
            }))
        self.send_tx(tx)

    def print_balance(self):
        balance = self.contract.functions.balanceOf(self.my_addr()).call()
        print(f"account: {self.my_addr()} has {balance} balance of tokens (not regarding decimals)")

    def get_balance(self):
        return self.contract.functions.balanceOf(self.my_addr()).call()
