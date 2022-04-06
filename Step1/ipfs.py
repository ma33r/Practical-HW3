# Doc: https://docs.pinata.cloud/api-pinning/pin-file
import os
import requests
import json
import hashlib
import base64
import mimetypes
from ipfs2bytes32 import ipfscidv0_to_byte32

from secrets import (
    PINATA_API_KEY, 
    PINATA_API_SECRET
)
from art.art_info import (
    FILE_NAME,
    ASSET_NAME,
    ASSET_DESCRIPTION
)


PINATA_IMAGE_URL = "https://api.pinata.cloud/pinning/pinFileToIPFS"
PINATA_JSON_URL = "https://api.pinata.cloud/pinning/pinJSONToIPFS"
PINATA_HEADERS = {
    "pinata_api_key": PINATA_API_KEY,
    "pinata_secret_api_key": PINATA_API_SECRET,
}


def pin_image_to_ipfs(file_path):
    # read the file in binary format
    f = open(file_path, 'rb')

    # replace None with file data
    files = {
        'file': f,
    }

    # make POST request to the correct URL, with files=files, and using the PINATA_HEADERS
    url = 'https://api.pinata.cloud/pinning/pinFileToIPFS'

    response = requests.post(url, files=files, headers=PINATA_HEADERS)

    # examine response extract out the IpfsHash (this is the CID). Return it
    print(response)
    response_dict = response.json()
    print(response_dict)
    return response_dict["IpfsHash"]


def pin_metadata_to_ipfs(metadata):
    # make POST request to the correct URL, with json=metadata, and using the PINATA_HEADERS
    url = 'https://api.pinata.cloud/pinning/pinJSONToIPFS'

    response = requests.post(url, json=metadata, headers=PINATA_HEADERS)

    # examine response extract out the IpfsHash (this is the CID). Return it
    print(response)
    response_dict = response.json()
    print(response_dict)
    return response_dict["IpfsHash"]


def compute_integrity(ipfs_image_cid):
    integrity = ipfscidv0_to_byte32(ipfs_image_cid)
    integrity = base64.b64encode(bytes.fromhex(integrity))
    integrity = "sha256-{}".format(integrity.decode('utf-8'))
    return integrity


def compute_metadata_hash(metadata):
    metadata_json_string = json.dumps(metadata)

    hash = hashlib.sha256()
    hash.update(metadata_json_string.encode("utf-8"))
    ipfs_metadata_hash = hash.digest()
    return ipfs_metadata_hash


def main():
    # compute absolute path to FILE_NAME and use it to pin image to IPFS
    path = os.path.dirname(os.path.realpath(__file__))
    absolute_path = os.path.join(path, 'art', FILE_NAME)

    image_cid = pin_image_to_ipfs(absolute_path)

    # convert the IPFS CID it returns to an IPFS address
    image_ipfsaddress = "ipfs://CID/" + image_cid

    # compute the integrity
    image_integrity = compute_integrity(image_cid)

    # compute the mimetype
    image_mimetype = mimetypes.MimeTypes().guess_type(absolute_path)[0];

    metadata = {
        'name': ASSET_NAME,
        'description': ASSET_DESCRIPTION,
        'image': image_ipfsaddress,
        'image_integrity': image_integrity,
        'image_mimetype': image_mimetype,
    }

    # pin metadata to IPFS
    metadata_cid = pin_metadata_to_ipfs(metadata)

    # convert the IPFS CID it returns to an IPFS address
    metadata_ipfsaddress = "ipfs://CID/" + metadata_cid

    # compute metadata hash
    metadata_hash = compute_metadata_hash(metadata)

    # assign to these variables to print them out
    print("IPFS metadata CID: {}".format(metadata_cid))
    print("IPFS metadata address: {}".format(metadata_ipfsaddress))
    print("IPFS metadata hash: {}".format(metadata_hash))


if __name__ == '__main__':
    main()
