from django.http import HttpResponse
import requests


# TODO USE THIS package
from algosdk.v2client import algod

# TODO Feel free to copy-paste the secrets.py file into the Step3 folder and import it here
from secrets import (
    account_private_key,
    account_address,
    PURESTAKE_API_KEY,
    ALGOD_ADDRESS,
    ALGOD_HEADERS
)


PINATA_GATEWAY = "https://gateway.pinata.cloud/ipfs/"

# fill me out
ASSET_ID = 82430632

def serve_image(request):
    # TODO modify this function to:
    # 1. Query the algorand blockchain for your NFT
    client = algod.AlgodClient(PURESTAKE_API_KEY, ALGOD_ADDRESS, ALGOD_HEADERS)
    query = client.asset_info(ASSET_ID);

    # 2. Recover the IPFS Metadata address from the NFT
    ipfs_md_address = query['params']['url']

    # 3. Query the metadata from IPFS
    md_cid = ipfs_md_address[7:]
    url = 'https://gateway.pinata.cloud/ipfs/' + md_cid

    response = requests.get(url)
    print(response)
    response_dict = response.json()
    print(response_dict)

    # 4. Extract the IPFS image address
    image_address = response_dict["image"]

    # 5. Query the image from IPFS
    image_cid = image_address[7:]
    image_url = 'https://gateway.pinata.cloud/ipfs/' + image_cid

    image_response = requests.get(image_url)

    # 6. Serve the image as an HTTP response

    http_image_response = HttpResponse(image_response, content_type=response_dict["image_mimetype"])

    return http_image_response


def home_page(request):
    return HttpResponse("<h1>Visit localhost:8000/nft to view your NFT!</h1>")