import hashlib
import ecdsa
import codecs

def private_to_public(private_key):
    private_key_bytes = codecs.decode(private_key,'hex')
    key = ecdsa.SigningKey.from_string(private_key_bytes,curve=ecdsa.SECP256k1).verifying_key
    key_bytes = key.to_string()
    key_hex = codecs.encode(key_bytes,'hex')
    bitcoin_byte = b'04'
    public_key = bitcoin_byte + key_hex
    return public_key

def private_to_compressed_public(private_key):
    private_hex = codecs.decode(private_key,'hex')
    key = ecdsa.SigningKey.from_string(private_hex,curve=ecdsa.SECP256k1).verifying_key
    key_bytes = key.to_string()
    key_hex = codecs.encode(key_bytes,'hex')
    key_string = key_hex.decode('utf-8')
    half_len = len(key_hex) //2
    key_half = key_hex[:half_len]
    last_byte = int(key_string[-1],16)
    bitcoin_byte = b'02' if last_byte % 2 == 0 else b'03' 
    public_key = bitcoin_byte + key_half
    return public_key

def public_to_address(public_key):
    public_key_bytes = codecs.decode(public_key,'hex')
    sha256_bpk_digest = hashlib.sha256(public_key_bytes).digest()
    ripemd160_bpk = hashlib.new('ripemd160')
    ripemd160_bpk.update(sha256_bpk_digest)
    ripemd160_bpk_digest = ripemd160_bpk.digest()
    ripemd160_bpk_hex = codecs.encode(ripemd160_bpk_digest,'hex')
    network_byte = b'00'
    network_bitcoin_public_key = network_byte + ripemd160_bpk_hex
    network_bitcoin_public_key_bytes = codecs.decode(network_bitcoin_public_key,'hex')
    sha256_nbpk_digest = hashlib.sha256(network_bitcoin_public_key_bytes).digest()
    sha256_2_nbpk_digest = hashlib.sha256(sha256_nbpk_digest).digest()
    sha256_2_hex = codecs.encode(sha256_2_nbpk_digest,'hex')
    checksum = sha256_2_hex[:8]
    address_hex = (network_bitcoin_public_key + checksum).decode('utf-8')
    wallet = base58(address_hex)
    return wallet


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
    for one in range(ones):
        b58_string = '1' + b58_string
    return b58_string


private_key = '690147e965393318528cb062d1885367244342fd50bc56b96e2807f6e62e235e'
compressed_public_key = private_to_compressed_public(private_key)
public_key = private_to_public(private_key)
print(public_to_address(public_key))
print(public_to_address(compressed_public_key))