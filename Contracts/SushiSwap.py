from ContractBase import ContractBase

DEADLINE = 10000000000000


class SushiSwap(ContractBase):

    def __init__(self, web3, priv_key, my_addr, tokenA, tokenB, router):
        super().__init__(web3, priv_key, my_addr, "../abi/abi.json")
        self.tokenA = tokenA  # can change to path = [tokenA, tokenB]
        self.tokenB = tokenB
        self.router = router
        self.my_addr = my_addr

        self.contract = self.web3.eth.contract(address=router, abi=self.abi)

    def calc_amount_out(self, amount):
        return int(self.contract.functions.getAmountsOut(amount, [self.tokenB, self.tokenA]).call()[-1])

    def calc_amount_in(self, amount):
        return int(self.contract.functions.getAmountsIn(amount, [self.tokenA, self.tokenB]).call()[0])

    def token_to_eth(self, amount):
        amount_out = self.calc_amount_out(amount)
        tx = (
            # error shows up with the other function without FeeOnTransferTokens
            self.contract.functions.swapExactTokensForETHSupportingFeeOnTransferTokens(
                amount, amount_out, [self.tokenB, self.tokenA], self.my_addr, DEADLINE)
            .build_transaction({
                "from": self.my_addr, "nonce": self.get_nonce()
            }))
        self.send_tx(tx)

    def eth_to_token(self, amount):
        amount_out = self.calc_amount_out(amount)
        tx = (
            self.contract.functions.swapExactETHForTokens(
                amount_out, [self.tokenA, self.tokenB], self.my_addr, DEADLINE)
            .build_transaction({
                "from": self.my_addr, "nonce": self.get_nonce(), "value": amount
            }))
        self.send_tx(tx)

    def eth_to_token_by_token_amount(self, amount):
        value = self.calc_amount_in(amount)
        tx = (
            self.contract.functions.swapETHForExactTokens(
                amount, [self.tokenA, self.tokenB], self.my_addr, DEADLINE)
            .build_transaction({
                "from": self.my_addr, "nonce": self.get_nonce(), "value": value
            }))
        self.send_tx(tx)
