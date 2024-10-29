import os
from collections import defaultdict

# ukr_alpha = "АБВГДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЬЮЯабвгдеєжзиіїйклмнопрстуфхцчшщьюя"
ukr_alpha_lower = "абвгдеєжзиіїйклмнопрстуфхцчшщьюя"


encode_helper = {}
for i, l in enumerate(ukr_alpha_lower):
    encode_helper[l] = i

# Return array of indexes of leters in a given text
def encode(text):
    result = []
    for l in text:
        result.append(encode_helper[l])

    return result

# Return leter at index
def decode(indexes):
    result = ""
    for i in indexes:
        result += ukr_alpha_lower[i]

    return result

def main(epsilon = pow(10, -12), precision = 12):
    pass

if __name__ == "__main__":
    main()