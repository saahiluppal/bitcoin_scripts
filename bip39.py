import sys
import binascii
import hashlib
import random
import hmac
import pbkdf2

PBKDF2_ROUNDS = 2048

# Custom implementation of BIP 39: https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki

RADIX = 2048
MAP_MS_CS = dict([(12, 4), (15, 5), (18, 6), (21, 7), (24, 8)])
MAP_ENT_CS = dict([(128, 4), (160, 5), (192, 6), (224, 7), (256, 8)])
MAP_ENT_MS = dict([(128, 12), (160, 15), (192, 18), (224, 21), (256, 24)])


def LoadWords(words_file_path):
    with open(words_file_path, "r") as f:
        words = [w.strip() for w in f.readlines()]
    if len(words) != RADIX:
        raise ValueError(
            "Word list must contain %d words, however it contains %d words." % (RADIX, len(words)))
    return words


def PrefixChoice(words, prefix):
    if not isinstance(words, list):
        raise ValueError(
            "Error. Word list must be provided as a list data type.")
    if len(words) != RADIX:
        raise ValueError(
            "Error. Word list must contain %d words, however it contains %d words." % (RADIX, len(words)))
    return [word for word in words if word.startswith(prefix)]


def CalcChecksum(entropy):
    CS = len(entropy) // 32
    checksum_hash = hashlib.sha256(binascii.unhexlify(
        hex(int(entropy, 2))[2:])).hexdigest()
    return bin(int(checksum_hash, 16))[2:].zfill(256)[:CS]


def EntropyToMnemonic(words, entropy):
    if not isinstance(words, list):
        raise ValueError(
            "Error. Word list must be provided as a list data type.")
    if len(words) != RADIX:
        raise ValueError(
            "Error. Word list must contain %d words, however it contains %d words." % (RADIX, len(words)))
    if len(entropy) not in [128, 160, 192, 224, 256]:
        raise ValueError("Error. Incorrect entropy input length.")
    b = entropy + CalcChecksum(entropy)
    result = []
    for i in range(len(b) // 11):
        idx = int(b[i * 11:(i + 1) * 11], 2)
        result.append(words[idx])
    if len(result) not in [12, 15, 18, 21, 24]:
        raise ValueError("Error. Incorrect word sentence output length.")
    return result


def MnemonicToEntropy(words, mnemonic):
    if not isinstance(words, list):
        raise ValueError(
            "Error. Word list must be provided as a list data type.")
    if len(words) != RADIX:
        raise ValueError(
            "Error. Word list must contain %d words, however it contains %d words." % (RADIX, len(words)))
    if not isinstance(mnemonic, list):
        mnemonic = mnemonic.split()
    if len(mnemonic) not in [12, 15, 18, 21, 24]:
        raise ValueError("Error. Incorrect word senence input length.")
    bit_string = ""
    for word in mnemonic:
        i = words.index(word)
        for j in range(11):
            if (i & (1 << (10 - j))) == 0:
                bit_string = bit_string + "0"
            else:
                bit_string = bit_string + "1"
    bit_check_string = bit_string[-MAP_MS_CS[len(mnemonic)]:]
    entropy = bit_string[:-MAP_MS_CS[len(mnemonic)]]
    if bit_check_string != CalcChecksum(entropy):
        raise ValueError("Error. Incorrect checksum.")
    return entropy


def MakeSeed(mnemonic, passphrase=""):
    if isinstance(mnemonic, list):
        mnemonic = " ".join(mnemonic)
    return pbkdf2.PBKDF2(mnemonic, "mnemonic" + passphrase, iterations=PBKDF2_ROUNDS, macmodule=hmac, digestmodule=hashlib.sha512).read(64)


if __name__ == "__main__":
    test = False
    generate = False

    for arg in sys.argv:
        if arg == "-t":
            test = True
        if arg == "-g":
            generate = True

    if test == True:
        device = LoadWords("english.txt")
        subset = PrefixChoice(device, "an")
        assert subset[0] == "analyst", "Test failed. Invalid prefix option."
        assert subset[1] == "anchor", "Test failed. Invalid prefix option."

        entropy = bin(int("68a79eaca2324873eacc50cb9c6eca8cc68ea5d936f98787c60c7ebc74e6ce7c", 16))[
            2:].zfill(256)
        sentence = EntropyToMnemonic(device, entropy)
        expected = "hamster diagram private dutch cause delay private meat slide toddler razor book happy fancy gospel tennis maple dilemma loan word shrug inflict delay length".split()
        assert sentence == expected, "Test failed. Invalid sentence."

        entropy_from_sentence = MnemonicToEntropy(device, sentence)
        assert entropy_from_sentence == entropy, "Test failed. Incorrect entropy."

        MakeSeed(sentence, passphrase="KALPANA")

        print("Tests passed.")

    if generate == True:
        device = LoadWords("english.txt")
        weak_private_key = "".join(random.choice(
            "0123456789abcdef") for n in range(64))
        entropy = bin(int(weak_private_key, 16))[2:].zfill(256)
        sentence = EntropyToMnemonic(device, entropy)
        print("Weak private key: " + weak_private_key)
        print("Mnemonic: " + " ".join(sentence))
