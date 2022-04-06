from algosdk import mnemonic

PINATA_API_KEY = "0aadebb82c6e1cfe5937"
PINATA_API_SECRET = "17a0ab98997d8dcc910324a56786500dc0a16898423da9c18f18d5bfb4d3085d"

PURESTAKE_API_KEY = "0xYgikhKfl3rKNJ1HnIrc8APysxYcsbm8DyaqNNj"

account_mnemonic = "corn team total buzz forward extend unit shadow buyer ugly creek shove grunt media paper end crash spirit artist people normal local neither abandon gain"
account_private_key = mnemonic.to_private_key(account_mnemonic)
account_address = mnemonic.to_public_key(account_mnemonic)

ALGOD_ADDRESS = "https://testnet-algorand.api.purestake.io/ps2"
ALGOD_HEADERS = {"X-API-Key": PURESTAKE_API_KEY}
