from ContractBase import ContractBase


class ERC20(ContractBase):
    def __init__(self, web3, priv_key, my_addr, token_addr):
        super().__init__(web3, priv_key, my_addr, "../abi/erc20.json")

        self.contract = self.web3.eth.contract(address=token_addr, abi=self.abi)

    def approve(self, addr, amount):
        tx = (
            self.contract.functions.approve(addr, amount)
            .build_transaction({
                "from": self.my_addr, "nonce": self.get_nonce()
            }))
        self.send_tx(tx)

    def mint(self, addr, amount):
        tx = (
            self.contract.functions.mint(addr, amount)
            .build_transaction({
                "from": self.my_addr, "nonce": self.get_nonce()
            }))
        self.send_tx(tx)
