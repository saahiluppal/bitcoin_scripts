import secrets
import hashlib
import binascii
import base58

class Private_key_formats:
    def __init__(self):
        rand_digits = secrets.randbits(256)

        self.private_key_bytes = rand_digits
        self.private_key_bits = bin(rand_digits)[2:]
        self.private_key_hex = hex(rand_digits)[2:]

        while len(self.private_key_hex)<64:
            self.private_key_hex = "0" + self.private_key_hex

        while len(self.private_key_bits)<256:
            self.private_key_bits = "0" + self.private_key_bits

    def get_wif(self):
        extended_key = "80" + self.private_key_hex
        first_sha256 = hashlib.sha256(binascii.unhexlify(extended_key)).hexdigest()
        second_sha256 = hashlib.sha256(binascii.unhexlify(first_sha256)).hexdigest()
        checksum = second_sha256[:8]
        final_key = extended_key+checksum
        self.WIF = base58.b58encode(binascii.unhexlify(final_key)).decode('utf-8')
        return self.WIF
    
    def get_wif_compressed(self):
        extended_key = "80" + self.private_key_hex + "01"
        first_sha256 = hashlib.sha256(binascii.unhexlify(extended_key)).hexdigest()
        second_sha256 = hashlib.sha256(binascii.unhexlify(first_sha256)).hexdigest()
        checksum = second_sha256[:8]
        final_key = extended_key + checksum
        self.WIF_compressed = base58.b58encode(binascii.unhexlify(final_key)).decode('utf-8')
        return self.WIF_compressed

    def get_private_bits(self):
        return self.private_key_bits

    def get_private_bytes(self):
        return self.private_key_bytes

    def get_private_hex(self):
        return self.private_key_hex


keys = Private_key_formats()
print("\nBits:: ",keys.get_private_bits())
print("\nBytes:: ",keys.get_private_bytes())
print("\nHex:: ",keys.get_private_hex())
print("\nWIF:: ",keys.get_wif())
print("\nWIF_compressed:: ",keys.get_wif_compressed())

