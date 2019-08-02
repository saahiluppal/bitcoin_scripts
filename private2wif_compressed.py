import base58
import hashlib
import codecs
from generating_private_key import Key_Generator
import binascii

# 1. Take a private Key
kg = Key_Generator()
kg.seed_input("This is a trutly random string? How are you")
private_key = kg.generate_key()
#private_key = '1e99423a4ed27608a15a2616a2b0e9e52ced330ac530edcc32c8ffc6a526aedd'

# 2. Add a 0x80 byte in front of it for mainnet addresses or 0xef for testnet addresses. Also add a 0x01 byte at the end if the private key will correspond to a compressed public key
extended_key = "80" + private_key + "01"

# 3. Perform SHA256 hash on the extended key.
#first_sha256 = hashlib.sha256(binascii.unhexlify(extended_key)).hexdigest()
first_sha256 = hashlib.sha256(codecs.decode(extended_key,'hex')).hexdigest()

# 4. Perform SHA256 hash on result of SHA256 hash
#second_sha256 = hashlib.sha256(binascii.unhexlify(first_sha256)).hexdigest()
second_sha256 = hashlib.sha256(codecs.decode(first_sha256,'hex')).hexdigest()

# 5. Take first 4 bytes of the second SHA256 hash, this is the checksum
checksum = second_sha256[:8]

# 6. Add the four bytes checksum from point 5 at the end of the extended key from point 2.
final_key = extended_key + checksum

# Wallet Import Format Compressed = base 58 encoding final key
#WIF_compressed = base58.b58encode(binascii.unhexlify(final_key))
WIF_compressed = base58.b58encode(codecs.decode(final_key,'hex'))
WIF_compressed_string = WIF_compressed.decode('utf-8')

print(WIF_compressed)

