

address_hex = input()

# base58 have every value of base64 except I,l,0,O,+,/ which arises ambiguity
base58_index = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
encoded_string = ''

# Get the number of leading zeros and convert hex to decimal
leading_zeros = len(address_hex) - len(address_hex.lstrip('0'))

# Convert hex to decimal
address_int = int(address_hex,16)

# Append digits to the start of the string
while address_int > 0:
    digit = address_int % 58
    digit_char = base58_index[digit]
    encoded_string = digit_char + encoded_string
    address_int //= 58

# Add '1' for each 2 leading zeros
ones = leading_zeros // 2
for _ in range(ones):
    encoded_string = '1' + encoded_string

print(encoded_string)