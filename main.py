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

def letters_frequency(file_path):
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

if __name__ == "__main__":
    main()