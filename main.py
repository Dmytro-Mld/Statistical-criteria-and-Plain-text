import os
import random
from collections import defaultdict

# ukr_alpha = "АБВГДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЬЮЯабвгдеєжзиіїйклмнопрстуфхцчшщьюя"
__UKR_ALPHA_LOWER__ = "абвгдеєжзиіїйклмнопрстуфхцчшщьюя"
__MODULE__ = len(__UKR_ALPHA_LOWER__)


encode_helper = {}
for i, l in enumerate(__UKR_ALPHA_LOWER__):
    encode_helper[l] = i

# Return array of indexes of leters in a given text
def encode(text: str) -> list[int]:
    result = []
    for l in text:
        result.append(encode_helper[l])

    return result

# Return leter at index
def decode(indexes: list[int]) -> str:
    result = ""
    for i in indexes:
        result += __UKR_ALPHA_LOWER__[i]

    return result

def letters_frequency(file_path: str) -> defaultdict[int]:
    frequency = defaultdict(int)

    text_length = 0
    with open(file_path, mode="rt", encoding="utf-8") as file:
        for line in file:
            text_length += len(line)
            for c in line:
                frequency[c] += 1
    
    for k in frequency:
        frequency[k] = frequency[k] / text_length

    return frequency

# Computes all (i, i - 1) bigrams. There might be beter to compute (2i, 2i + 1) bigrams. 
def bigram_frequency(file_path: str) -> defaultdict[int]:
    frequency = defaultdict(int)

    text_length = 0
    with open(file_path, mode="rt", encoding="utf-8") as file:
        text = file.read()
        text_length = len(text)
        
        for i in range(1, text_length):
                frequency[text[i-1] + text[i]] += 1
    
    for k in frequency:
        frequency[k] = frequency[k] / (text_length - 1)

    return frequency

def vigener_distortion(text: str, key: list[int]) -> str:
    r = len(key)
    indexes = encode(text=text)

    for i in range(len(indexes)):
       indexes[i] = (indexes[i] + key[i % r]) % __MODULE__
    
    return decode(indexes)

def main(epsilon = pow(10, -12), precision = 12):
    file_path = "text_preparation/out_text.txt"
    
    fletters = letters_frequency(file_path=file_path)
    for k in fletters:
        print(f"{k}: {fletters[k]:0.{precision}f}")

    sum = 0
    for k in fletters:
        sum += fletters[k]

    # small test for: SUM f_i ~ 1.0
    if sum < 1.0 - epsilon or sum > 1.0 + epsilon: raise ValueError(f"sum of all letters frequency should be equal to 1.0, but it is: {sum}")


    print("")


    fbigrams = bigram_frequency(file_path=file_path)
    for k in fbigrams:
        print(f"{k}: {fbigrams[k]:0.{precision}f}")

    sum = 0
    for k in fbigrams:
        sum += fbigrams[k]

    # small test for: SUM f_i ~ 1.0
    if sum < 1.0 - epsilon or sum > 1.0 + epsilon: raise ValueError(f"sum of all letters frequency should be equal to 1.0, but it is: {sum}")

    print("")
    some_text = "тахлопецьпочувавсятакимображенимщонезвернувнацежодноїувагиідалінарікавіякщобтвійтато"
    print(some_text)

    for i in [1, 5, 10]:
        key = [random.randint(0, __MODULE__ - 1) for _ in range(i)]
        dtext = vigener_distortion(text=some_text, key=key)
        print(dtext)

if __name__ == "__main__":
    main()