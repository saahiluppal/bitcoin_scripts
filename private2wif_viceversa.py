import hashlib
import base58
import binascii
from generating_private_key import Key_Generator


def private_2_wif():
    # 1. Take a private Key
    kg = Key_Generator()
    kg.seed_input("This is a truly random string, how are you, feeling bitcoinist")
    private_key = kg.generate_key()
    #private_key = '0C28FCA386C7A227600B2FE50B7CAE11EC86D3BF1FBE471BE89827E19D72AA1D'

    # 2. Add a 0x80 byte in front of it for mainnet addresses or 0xef for testnet addresses. Also add a 0x01 byte at the end if the private key will correspond to a compressed public key
    extended_key = "80" + str(private_key)

    # 3. Perform SHA256 hash on the extended key.
    first_sha256 = hashlib.sha256(binascii.unhexlify(extended_key)).hexdigest()

    # 4. Perform SHA256 hash on result of SHA256 hash
    second_sha256 = hashlib.sha256(binascii.unhexlify(first_sha256)).hexdigest()

    # 5. Take first 4 bytes of the second SHA256 hash, this is the checksum
    checksum = second_sha256[:8]

    # 6. Add the four checksum bytes from point 5 at the end of the extended key from point 2
    final_key = extended_key+checksum

    # Wallet Import Format = base 58 encoding final_key
    WIF = base58.b58encode(binascii.unhexlify(final_key))

    print(WIF)

    #return WIF

def wif_2_private():
    pass


# I refered this site https://en.bitcoin.it/wiki/Wallet_import_format