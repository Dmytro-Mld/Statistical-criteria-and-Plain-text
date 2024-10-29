from string import ascii_letters


# ukr_alpha = "АБВГҐДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЬЮЯабвгґдеєжзиіїйклмнопрстуфхцчшщьюя"
ukr_alpha = "АБВГДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЬЮЯабвгдеєжзиіїйклмнопрстуфхцчшщьюя"

def main():
    with open("pre_text.txt", mode="rt", encoding="utf-8") as ffrom:
        with open("out_text.txt", mode="wt", encoding="utf-8") as fto:
            for line in ffrom:
                for c in line:
                    if c in "Ґґ":
                        fto.write("г")
                    elif c in ukr_alpha:
                        fto.write(c.lower())

if __name__ == "__main__":
    main()