from web3 import Web3

# from web3.middleware import geth_poa_middleware

rpc_url = ""
my_priv_key = ""
my_addr = Web3.to_checksum_address("")

router_address = Web3.to_checksum_address("")  # sushiswap v2 router
tokenAaddr = Web3.to_checksum_address("")  # Should be Wrapped NATIVE!
tokenBaddr = Web3.to_checksum_address("")  # random token

stargate_address = ""  # https://stargateprotocol.gitbook.io/stargate/developers/contract-addresses/
token1addr = ""
token2addr = ""
target_chain_id = 0
src_pool_id = 0  # https://stargateprotocol.gitbook.io/stargate/developers/pool-ids
target_pool_id = 0

web3 = Web3(Web3.HTTPProvider(rpc_url))
# web3.middleware_onion.inject(geth_poa_middleware, layer=0)
