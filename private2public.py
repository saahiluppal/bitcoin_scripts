# hex private to hex public key implementation
import codecs
import ecdsa
from generating_private_key import Key_Generator

# 1. Getting a private key
kg = Key_Generator()
kg.seed_input("This is a truly random string, what about you?")
private_key = kg.generate_key()

private_key = '4330c1d018bcef7272d15cbcf74f3a4c6d9024a73d5363ae83a00dbea0610c9e'

# 2. Converting private key from hexadecimal to bytes
private_key_bytes = codecs.decode(private_key,'hex')

# 3. Getting point on the eliptic curve using secp256k1 method
key = ecdsa.SigningKey.from_string(private_key_bytes,curve=ecdsa.SECP256k1).verifying_key

# 4. Converting the object into a bytes
key_bytes = key.to_string()

# 5. Converting from bytes to hexadecimal
key_hex = codecs.encode(key_bytes,'hex')

# 6. Adding bitcoin byte
bitcoin_byte = b'04'

# 7. This is the public key
public_key = bitcoin_byte+key_hex

print(public_key)