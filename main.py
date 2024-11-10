import os
import random
from collections import defaultdict
import numpy as np

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

def encode_l_ary(text: str, l: int) -> list[int]:
    if len(text) % l != 0: raise ValueError(f"Given string is invalid: the size should be divisable by l(={l}) but {len(text)} isn't divisable by {l}")

    result = []
    for i in range(0, len(text), l):
        temp = 0
        multiplyer = 1
        for j in range(l):
            temp += encode_helper[text[i + j]] * multiplyer
            multiplyer *= __MODULE__
        
        result.append(temp)

    return result

def decode_l_ary(indexes: list[int], l: int) -> list[int]:
    # if len(text) % l != 0: raise ValueError(f"Given string is invalid: the size should be divisable by l({l}) but {len(text)} isn't divisable by {l}")

    result = ""
    for i, ind in enumerate(indexes):
        temp = ""
        for j in range(l):
            temp = temp + __UKR_ALPHA_LOWER__[ind % __MODULE__]
            ind = ind // __MODULE__
        
        result += temp

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
        
        for i in range(0, text_length, 2):
                frequency[text[i] + text[i+1]] += 1
    
    for k in frequency:
        frequency[k] = frequency[k] / (text_length // 2)

    return frequency

def vigener_distortion(text: str, key: list[int]) -> str:
    r = len(key)
    indexes = encode(text=text)

    for i in range(len(indexes)):
       indexes[i] = (indexes[i] + key[i % r]) % __MODULE__
    
    return decode(indexes)

# key  = {"a": int, "b": int}
def affine_distortion(text: str, key: dict[str: int], l: int) -> str:
    mod_ = pow(__MODULE__, l)

    indexes = encode_l_ary(text=text, l=l)
    for i, ind in enumerate(indexes):
        indexes[i] = (key["a"] * ind + key["b"]) % mod_
    
    return decode_l_ary(indexes, l=l)

def random_uniform_text(size: int, l: int) -> str:
    size = size // l # because any l-gram gives l symbols instead of 1

    res = []
    mod_ = pow(__MODULE__, 2)

    for _ in range(size):
        res.append(random.randint(0, mod_ - 1))
    
    return decode_l_ary(indexes=res, l=l)

def random_nonuniform_text(size: int, l: int) -> str:
    size = size // l # because any l-gram gives l symbols instead of 1

    mod_ = pow(__MODULE__, 2)
    s = []

    for i in range(2):
        s.append(random.randint(0, mod_))
    
    for i in range(size - 2):
        s.append((s[i] + s[i + 1]) % mod_)

    return decode_l_ary(indexes=s, l=l)

def criteria_2_0(fbigrams: dict, fletters: dict, rand_text: str, l: int):
    l_size = l

    if l_size == 1:
        fbrg = fletters.copy()
        friquent_bigram_dict = defaultdict(int) #A_frq
        bigram_list_of_text = []
        #creating A_frq
        for i in range(32):
            key = max(fbrg, key=fbrg.get)
            value = fbrg.get(key)
            friquent_bigram_dict[key] = value
            del fbrg[key]
        #checking our text
        for i in rand_text:
            if i in bigram_list_of_text:
                continue
            else:
                bigram_list_of_text.append(i)
    else:
        fbrg = fbigrams.copy()
        friquent_bigram_dict = defaultdict(int) #A_frq
        bigram_list_of_text = []
        #creating A_frq
        for i in range(800):
            key = max(fbrg, key=fbrg.get)
            value = fbrg.get(key)
            friquent_bigram_dict[key] = value
            del fbrg[key]

        #checking our text
        for i in range(0, len(rand_text), 2):
            bigram_list_of_text.append(rand_text[i] + rand_text[i+1])

    #checking if our text bigram is in A_frq list
    for i in bigram_list_of_text:
        if i in friquent_bigram_dict:
            continue
        else:
            return "This text makes no sense"

    return "This is plaintext"


def criteria_2_1(fbigrams: dict, fletters: dict, rand_text: str, l: int):
    l_size = l
    fbrg = fbigrams.copy()
    friquent_bigram_dict = {}
    bigram_list_of_text = []

    #creating A_frq 
    for i in range(800):
        key = max(fbrg, key=fbrg.get)
        value = fbrg.get(key)
        friquent_bigram_dict[key] = value
        del fbrg[key]

    #checking our text
    for i in range(0, len(rand_text), 2):
        bigram_list_of_text.append(rand_text[i] + rand_text[i+1])

    a_af_list = []
    #creating A_af list which consists of bigrams that are in text and in A_frq (friquent_bigram_dict)
    for i in range(len(bigram_list_of_text)):
        if bigram_list_of_text[i] in friquent_bigram_dict.keys():
            a_af_list.append(bigram_list_of_text[i])
        else:
            continue
    
    k_f = 300
    count = 0
    for i in range(len(a_af_list)):
        if a_af_list[i] in friquent_bigram_dict:
            count += 1
    if count <= k_f:
        return "This text makes no sense"
    else:
        return "This is plaintext"

def criteria_2_2(fbigrams: dict, fletters: dict, rand_text: str, l: int):
    l_size = l
    fbrg = fbigrams.copy()
    friquent_bigram_dict = {}

    #creating A_frq 
    for i in range(800):
        key = max(fbrg, key=fbrg.get)
        value = fbrg.get(key)
        friquent_bigram_dict[key] = value
        del fbrg[key]

    #checking our text
    frequency = defaultdict(int)

    text_length = 0
    text_length = len(rand_text)
        
    for i in range(0, text_length, 2):
        frequency[rand_text[i] + rand_text[i+1]] += 1
    
    for k in frequency:
        frequency[k] = frequency[k] / (text_length // 2)

    count = 0

    for key in frequency:
        if key in friquent_bigram_dict:
            if frequency[key] < friquent_bigram_dict[key]:
                return "This text makes no sense"
            else:
                continue
        if key not in friquent_bigram_dict:
            count += 1
            
    return "This is plaintext"

def criteria_2_3(fbigrams: dict, fletters: dict, rand_text: str, l: int):
    l_size = l    
    fbrg = fbigrams.copy()
    friquent_bigram_dict = {}

    #creating A_frq 
    for i in range(800):
        key = max(fbrg, key=fbrg.get)
        value = fbrg.get(key)
        friquent_bigram_dict[key] = value
        del fbrg[key]

    #creating a dictionary with bigrams from our bigrams text and its frequency
    frequency = defaultdict(int)

    text_length = 0
    text_length = len(rand_text)
        
    for i in range(0, text_length, 2):
        frequency[rand_text[i] + rand_text[i+1]] += 1
    
    for k in frequency:
        frequency[k] = frequency[k] / (text_length // 2)

    #creating frequency_F array:
    frequency_F = frequency.copy()

    frequency_F = {key: frequency[key] for key in frequency if key in friquent_bigram_dict}

    frequency_F_sum = sum(frequency_F.values())
    frequency_K_sum = sum(friquent_bigram_dict.values())

    if frequency_F_sum < frequency_K_sum:
        return "This text makes no sense"
    else:
        return "This is plaintext"
    
def calculate_index_of_coincidence(cx: dict, L: int) -> float:
    # Рахуємо чисельник: суму cx * (cx - 1) для всіх cx у словнику
    numerator = sum(count * (count - 1) for count in cx.values())
    
    # Рахуємо знаменник
    denominator = L * (L - 1)
    
    # Розраховуємо індекс відповідності
    I_l = numerator / denominator
    return I_l

def criteria_coincidence(fbigrams: dict, fletters: dict, rand_text: str, l: int):
    fbgr = fbigrams.copy()
    l_size = l
    kI = 0.03

    if l_size == 1:
        #checking our text
        frequency = defaultdict(int)
        text_length = 0
        for line in rand_text:
            text_length += len(line)
            for c in line:
                frequency[c] += 1
        for k in frequency:
            frequency[k] = frequency[k] / text_length
    else:
        #checking our text
        frequency = defaultdict(int)

        text_length = 0
        text_length = len(rand_text)
            
        for i in range(0, text_length, 2):
            frequency[rand_text[i] + rand_text[i+1]] += 1
        
        for k in frequency:
            frequency[k] = frequency[k] / (text_length // 2)

    index = calculate_index_of_coincidence(fbgr, len(rand_text))
    index_hatch = calculate_index_of_coincidence(frequency, len(rand_text))
    
    res = abs(index - index_hatch)

    if res > kI:
        return "This text makes no sense"
    else:
        return "This is plaintext"

    


def main(epsilon = pow(10, -12), precision = 12):
    file_path = "text_preparation/out_text.txt"
    
    fletters = letters_frequency(file_path=file_path)
    print("> Letters frequency")
    for k in fletters:
        print(f"{k}: {fletters[k]:0.{precision}f}")

    sum = 0
    for k in fletters:
        sum += fletters[k]

    # small test for: SUM f_i ~ 1.0
    if sum < 1.0 - epsilon or sum > 1.0 + epsilon: raise ValueError(f"sum of all letters frequency should be equal to 1.0, but it is: {sum}")

    print()

    print("> Bigram frequency")
    fbigrams = bigram_frequency(file_path=file_path)
    for k in fbigrams:
        print(f"{k}: {fbigrams[k]:0.{precision}f}")

    sum = 0
    for k in fbigrams:
        sum += fbigrams[k]

    # small test for: SUM f_i ~ 1.0
    if sum < 1.0 - epsilon or sum > 1.0 + epsilon: raise ValueError(f"sum of all letters frequency should be equal to 1.0, but it is: {sum}")
 
    print()
    some_text = "тахлопецьпочувавсятакимображенимщонезвернувнацежодноїувагиідалінарікавіякщобтвійтато"

    print("> Vigener distortion example")
    for i in [1, 5, 10]:
        key = [random.randint(0, __MODULE__ - 1) for _ in range(i)]
        dtext = vigener_distortion(text=some_text, key=key)
        print(dtext)
    
    print()

    print("> Affine distortion example")
    for l in [1, 2]:
        mod_ = pow(__MODULE__, 2)
        key = {"a": random.randint(0, mod_ - 1), "b": random.randint(0, mod_ - 1)}
        dtext = affine_distortion(text=some_text, key=key, l=l)
        print(dtext)

    print()

    print("> Random text creation")
    print(random_uniform_text(size=100, l=1))
    print(random_uniform_text(size=100, l=2))
    print(random_nonuniform_text(size=100, l=1))
    print(random_nonuniform_text(size=100, l=2))

    l = 2

    rand_text_1 = random_uniform_text(size=100, l=2)
    rand_text_2 = random_nonuniform_text(size=100, l=2)

    print("> Criteria 2.0")
    crit_2_0 = criteria_2_0(fbigrams = fbigrams, fletters = fletters, rand_text = rand_text_1, l = l)
    print(crit_2_0)

    print("> Criteria 2.1")
    crit_2_1 = criteria_2_1(fbigrams = fbigrams, fletters = fletters, rand_text = rand_text_1, l = l)
    print(crit_2_1)

    print("> Criteria 2.2")
    crit_2_2 = criteria_2_2(fbigrams = fbigrams, fletters = fletters, rand_text = rand_text_1, l = l)
    print(crit_2_2)

    print("> Criteria 2.3")
    crit_2_3 = criteria_2_3(fbigrams = fbigrams, fletters = fletters, rand_text = rand_text_1, l = l)
    print(crit_2_3)

    print("> Criteria 4.0 Index of Coincidence")
    crit_4_0 = criteria_coincidence(fbigrams = fbigrams, fletters = fletters, rand_text = rand_text_1, l = l)
    print(crit_4_0)



if __name__ == "__main__":
    main()