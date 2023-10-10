import json
import time

from web3 import Web3

from AccountManager import AccountManager
from Contracts.ERC20 import ERC20
from Contracts.Stargate import Stargate
from Contracts.SushiSwap import SushiSwap

# from web3.middleware import geth_poa_middleware

rpc_url = "http://127.0.0.1:7545"

# swap
# https://dev.sushi.com/docs/Products/Classic%20AMM/Deployment%20Addresses
router_address = Web3.to_checksum_address("")
factory_address = Web3.to_checksum_address("")
tokenAaddr = Web3.to_checksum_address("")  # Should be Wrapped token!
tokenBaddr = Web3.to_checksum_address("")  # USDT

# stargate
# https://stargateprotocol.gitbook.io/stargate/developers/contract-addresses/
stargate_address = ""  # mumbai testnet
token1addr = tokenBaddr

target_chain_id = 0  # fuji - avalanche testnet
src_pool_id = 1  # USDT https://stargateprotocol.gitbook.io/stargate/developers/pool-ids
target_pool_id = 1  # USDT

web3 = Web3(Web3.HTTPProvider(rpc_url))
# web3.middleware_onion.inject(geth_poa_middleware, layer=0)

am = AccountManager(should_shuffle=False)
token = ERC20(web3, am, token1addr)
stargate = Stargate(web3, am, stargate_address)
swap = SushiSwap(web3, am, tokenAaddr, tokenBaddr, router_address)


def prepare():
    # create pool on sushi
    my_addr = token.my_addr()
    priv_key = token.priv_key()

    mint_self_all()
    approve_all(router_address)
    approve_all(stargate_address)

    # creating pair on swap
    with open("./abi/factory.json") as fp:
        abi = json.loads(fp.read())
    factory = web3.eth.contract(address=factory_address, abi=abi)

    tx = factory.functions.createPair(tokenAaddr, tokenBaddr).build_transaction({
        "from": my_addr, "nonce": web3.eth.get_transaction_count(my_addr)
    })
    signed_txn = web3.eth.account.sign_transaction(tx, priv_key)
    web3.eth.send_raw_transaction(signed_txn.rawTransaction)

    # add liquidity
    tx = swap.contract.functions.addLiquidityETH(
        tokenBaddr, 10 ** 18, 1, 1, my_addr, 10**18
    ).build_transaction({
        "from": my_addr, "nonce": web3.eth.get_transaction_count(my_addr), "value": 10 ** 18
    })
    signed_txn = web3.eth.account.sign_transaction(tx, priv_key)
    web3.eth.send_raw_transaction(signed_txn.rawTransaction)


def approve_all(addr):
    for i in range(am.accounts_length()):
        token.approve(addr, 2 ** 255)
        am.change_account()


def get_balance_all():
    for i in range(am.accounts_length()):
        token.print_balance()
        am.change_account()


def mint_all(addr):
    for i in range(am.accounts_length()):
        token.mint(addr, 10 ** 20)
        am.change_account()


def mint_self_all():
    for i in range(am.accounts_length()):
        token.mint(token.my_addr(), 10 ** 20)
        am.change_account()


prepare()

# do ops
while True:
    for i in range(am.accounts_length()):
        swap.eth_to_token_by_token_amount(10 ** 6)
        swap.token_to_eth(10 ** 6)
        print(stargate.calculate_fee(target_chain_id))
        stargate.swap(target_chain_id, src_pool_id, target_pool_id, 10 ** 6)
        am.change_account()
