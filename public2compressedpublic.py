# hex public to compressed hex public

public_key = '5c0de3b9c8ab18dd04e3511243ec2952002dbfadc864b9628910169d9b9b00ec243bcefdd4347074d44bd7356d6a53c495737dd96295e2a9374bf5f02ebfc176'

x = public_key[:64]
y = public_key[64:]

if int(y,16) % 2==0:
    compressed_public_key = '02'+x
else:
    compressed_public_key = '03'+x

print(compressed_public_key)