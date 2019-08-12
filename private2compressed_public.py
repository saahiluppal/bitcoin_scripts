import ecdsa
import codecs
from generating_private_key import Key_Generator

# 1. Generating a private key (hex)
kg = Key_Generator()
kg.seed_input('this is a tryly random string, i tossed a dice and got tails. ;)')
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

# 6. Converting hexadecimal to hex string (basically to get string part)
key_string = key_hex.decode('utf-8')

# 7. Getting x and y
x = key_hex[:64]
y = key_hex[64:]

# 8. Checking whether last byte is even or odd
last_byte = int(key_string[-1],16)

# 9. Prefix of 02 if last byte is even else adding 03 is added.
bitcoin_byte = b'02' if last_byte%2==0 else b'03'

# 10. Adding prefix
compressed_public_key = bitcoin_byte + x

print(compressed_public_key)