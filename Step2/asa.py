from algosdk.v2client import algod
from algosdk.future import transaction
from algosdk.future.transaction import PaymentTxn, AssetConfigTxn, AssetTransferTxn, LogicSigTransaction
from algosdk import mnemonic, encoding
from utils import wait_for_confirmation, get_default_params

from ipfs_info import (
    ASSET_NAME,
    IPFS_METADATA_ADDRESS,
    IPFS_METADATA_HASH
)

from secrets import (
    account_private_key,
    account_address,
    PURESTAKE_API_KEY,
    ALGOD_ADDRESS,
    ALGOD_HEADERS
)


def create_ASA(client, address, private_key):
    # NFTs in Algorand can be represented on-chain as assets.
    # In HW1, you used AssetConfigTxn to create an asset. Here, you will use
    # the same class, but with different arguments. Refer to
    # https://developer.algorand.org/docs/get-started/tokenization/nft/
    # on how to create an NFT using AssetConfigTxn

    # You will need to pass strict_empty_address_check=False as an argument
    # to AssetConfigTxn

    params = get_default_params(client)

    txn = AssetConfigTxn(
        sender=address,
        sp=params,
        total=1, # NFTs have totalIssuance of exactly 1
        default_frozen = False,
        unit_name = "CoolUnit",
        asset_name = ASSET_NAME,
        manager = address,
        reserve = None,
        freeze = None,
        clawback = None,
        strict_empty_address_check=False,
        url = IPFS_METADATA_ADDRESS + "#arc3",
        metadata_hash = IPFS_METADATA_HASH,
        decimals = 0) # NFTs have decimals of exactly 0

    # sign and send transaction, and wait_for_confirmation like in the previous homeworks
    # Feel free to use functions from utils.py
    stxn = txn.sign(private_key)
    txid = client.send_transaction(stxn)
    print("Asset Creation Transaction ID: {}".format(txid))
    confirmed_txn = wait_for_confirmation(client, txid, 4)

    try:
        ptx = client.pending_transaction_info(txid)
        asset_id = ptx["asset-index"]
    except Exception as e:
        print(e)

    # Assign to these variables to print out the Transaction ID and Asset ID
    print("Transaction ID: {}".format(txid))
    print("Asset ID: {}".format(asset_id))


def main():
    client = algod.AlgodClient(PURESTAKE_API_KEY, ALGOD_ADDRESS, ALGOD_HEADERS)
    # call create_ASA with the correct arguments

    create_ASA(client, account_address, account_private_key)


if __name__ == '__main__':
    main()
