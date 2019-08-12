import hashlib
import codecs

def base58(address_hex):
    alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
    b58_string = ''
    leading_zeros = len(address_hex) - len(address_hex.lstrip('0'))
    address_int = int(address_hex,16)
    while address_int > 0:
        digit = address_int % 58
        digit_char = alphabet[digit]
        b58_string = digit_char + b58_string
        address_int//=58
    ones = leading_zeros//2
    for _ in range(ones):
        b58_string = '1' + b58_string
    return b58_string

#public_key = '04621519b911efe17d63c4cf8c4a3dce2e37d6afc7d5e78c44b5ff1b738b12109b5c9c2a68b072db6a64fa7384fe49900043594e56aa8d4ff94bd56c7310876b42'
public_key = ''

public_key_bytes = codecs.decode(public_key,'hex')

# Perform sha256 on public key
sha256_1 = hashlib.sha256(public_key_bytes).digest()

# Perform ripemd160 on sha256 encoded public key
ripemd160 = hashlib.new('ripemd160')
ripemd160.update(sha256_1)
ripemd160_digest = ripemd160.digest()

ripemd160_hex = codecs.encode(ripemd160_digest,'hex')

# performing base58check encoding with 0x00 prefix
network_byte = b'00'
network_bitcoin_public_key = network_byte + ripemd160_hex
network_bitcoin_public_key_bytes = codecs.decode(network_bitcoin_public_key,'hex')

sha256_2 = hashlib.sha256(network_bitcoin_public_key_bytes).digest()
sha256_3 = hashlib.sha256(sha256_2).digest()
sha256_hex = codecs.encode(sha256_3,'hex')

checksum = sha256_hex[:8]
address_hex = (network_bitcoin_public_key + checksum).decode('utf-8')


wallet = base58(address_hex)

print(wallet)