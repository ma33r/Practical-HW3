import requests
from algosdk.v2client import algod
from algosdk.future import transaction
from algosdk.future.transaction import PaymentTxn, AssetConfigTxn, AssetTransferTxn, LogicSigTransaction
from algosdk import mnemonic, encoding

from secrets import (
    account_private_key,
    account_address,
    PURESTAKE_API_KEY,
    ALGOD_ADDRESS,
    ALGOD_HEADERS
)


def wait_for_confirmation(client, transaction_id, timeout):
    start_round = client.status()["last-round"] + 1
    current_round = start_round

    while current_round < start_round + timeout:
        try:
            pending_txn = client.pending_transaction_info(transaction_id)
        except Exception:
            return

        if pending_txn.get("confirmed-round", 0) > 0:
            return pending_txn
        elif pending_txn["pool-error"]:
            raise Exception('pool error: {}'.format(pending_txn["pool-error"]))

        client.status_after_block(current_round)
        current_round += 1

    raise Exception('pending tx not found in timeout rounds, timeout value = : {}'.format(timeout))


def main():
    # Recepient Approval
    url = "https://distracted-varahamihira-80f55c.netlify.app/.netlify/functions/approval"

    body = {
        "asset_id":82592770,
    }

    response = requests.post(url, json=body)

    print(response.text)

    # Transfer Asset
    client = algod.AlgodClient(PURESTAKE_API_KEY, ALGOD_ADDRESS, ALGOD_HEADERS)

    params = client.suggested_params()

    txn = AssetTransferTxn(
        sender=account_address,
        sp=params,
        receiver="UAHTM3EC3PTNDYBA5AGPHVBMXOK4YQE3N23VQEUFAMTHY3AXHBUXDHIWKE",
        amt=0,
        index=82592770)
    stxn = txn.sign(account_private_key)

    try:
        txid = client.send_transaction(stxn)
        print("Signed transaction with txID: {}".format(txid))
        # Wait for the transaction to be confirmed
        confirmed_txn = wait_for_confirmation(client, txid, 4)
        print("TXID: ", txid)
        print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))
    except Exception as err:
        print(err)


if __name__ == '__main__':
    main()

