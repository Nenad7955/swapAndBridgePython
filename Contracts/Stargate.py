from ContractBase import ContractBase


class Stargate(ContractBase):
    def __init__(self, web3, priv_key, my_addr, stargate_address):
        super().__init__(web3, priv_key, my_addr, "../abi/stargate.json")

        self.contract = web3.eth.contract(address=stargate_address, abi=self.abi)
        self.lzTxObj = [0, 0, "0x0000000000000000000000000000000000000001"]

    def calculate_fee(self, target_chain_id):
        return self.contract.functions.quoteLayerZeroFee(
            target_chain_id,
            1,  # https://stargateprotocol.gitbook.io/stargate/developers/function-types
            "0x0000000000000000000000000000000000000000".encode(),
            "0x0000000000000000000000000000000000000000".encode(),
            self.lzTxObj
        ).call()[0]

    def swap(self, target_chain_id, src_pool_id, target_pool_id, amount):
        tx = self.contract.functions.swap(
            target_chain_id,
            src_pool_id,
            target_pool_id,
            self.my_addr,  # refund
            amount,
            0,  # min amount... can check router for better
            self.lzTxObj,
            self.my_addr,  # recipient
            "0x".encode(),  # no payload
        ).build_transaction({
            "from": self.my_addr, "nonce": self.get_nonce(), "value": self.calculate_fee(amount)
        })
        self.send_tx(tx)
