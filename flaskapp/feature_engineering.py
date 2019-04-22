import pandas as pd
import numpy
import json
import string

colors = [
"BG", "BEIGE",
"BK", "BLACK", "BLCK", "BLK",
"BL", "BLUE", "BLU",
"BN", "BROWN", "BRWN",
"BZ", "BRONZE", "BRNZ",
"CH", "CHARCOAL", "CHRCL",
"CL", "CLEAR", "CLR",
"DK", "DARK", "DRK"
"GD", "GOLD", "GLD",
"GN", "GREEN", "GRN",
"GY", "GRAY", "GRY",
"GT", "GRANITE", "GRNT",
"LT", "LIGHT", "LGHT",
"OR", "ORANGE", "ORNG",
"PK", "PINK", "PNK",
"RD", "RED",
"TL", "TRANSLUCENT", "TRNSLCNT",
"TN", "TAN",
"TP", "TRANSPARENT", "TRNSPRNT",
"VT", "VIOLET", "VLT"
"WT", "WHITE", "WHT"
"YL", "YELLOW", "YLLW", "YLW"]

units = [
        'PACK',
        'PCK',
        'PK'
        'OZ',
        'OUNCE',
        'CT',
        'COUNT',
        'LB',
        'LBS']

with open('../synthetic_data/data/abbreviated_brands.json') as json_file:
    data = json.load(json_file)
    abbreviated_brands = [x[1] for x in data]

with open('../synthetic_data/data/abbreviated_descriptors.json') as json_file:
    data = json.load(json_file)
    abbreviated_descriptors = [x[1] for x in data]


def num_vowels(x):
    num_vowels=0
    for char in x:
        if char in "aeiouAEIOU":
            num_vowels += 1
    return int(num_vowels)


def num_words(x):
    return int(len(x.split()))


def num_chars(x):
    return int(len(x))


def num_digits(x):
    num_digits=0
    for char in x:
        if char.isnumeric():
            num_digits += 1
    return int(num_digits)


def num_symbols(x):
    num_symbols=0
    for char in x:
        if not char.isnumeric() and not char.isspace() and not char.isalpha():
            num_symbols += 1
    return int(num_symbols)


def num_letters(x, letter):
    num_letters=0
    for char in x:
        if char == letter:
            num_letters += 1
    return int(num_letters)


def is_plural(x):
    if x[len(x) - 1] == 'S':
        return 1
    return 0


def has_char_repeat(x):
    for i in range(1, len(x) - 1):
        if x[i - 1] == x[i]:
            return 1
    return 0


def has_color(x):
    words = x.split()
    for word in words:
        if word in colors:
            return 1
    return 0


def has_brand(x):
    for abbr_brand in abbreviated_brands:
        if abbr_brand in x:
            return 1
    return 0


def has_descriptor(x):
    for abbr_descriptor in abbreviated_descriptors:
        if abbr_descriptor in x:
            return 1
    return 0


def has_unit(x):
    words = x.split()
    for word in words:
        if word in units:
            return 1
    return 0


def get_dataframe(items):
    df = pd.DataFrame(data={"x": items, "y": items})
    df["num_vowels"] = df.apply(lambda row: num_vowels(row.x), axis=1)
    df["num_words"] = df.apply(lambda row: num_words(row.x), axis=1)
    df["num_chars"] = df.apply(lambda row: num_chars(row.x), axis=1)
    df["num_digits"] = df.apply(lambda row: num_digits(row.x), axis=1)
    df["num_symbols"] = df.apply(lambda row: num_symbols(row.x), axis=1)
    # for letter in string.ascii_uppercase:
    #     df["num_" + letter] = df.apply(lambda row: num_letters(row.x, letter), axis=1)
    df["is_plural"] = df.apply(lambda row: is_plural(row.x), axis=1)
    df["has_char_repeat"] = df.apply(lambda row: has_char_repeat(row.x), axis=1)
    df["has_color"] = df.apply(lambda row: has_color(row.x), axis=1)
    df["has_brand"] = df.apply(lambda row: has_brand(row.x), axis=1)
    df["has_descriptor"] = df.apply(lambda row: has_descriptor(row.x), axis=1)
    df["has_unit"] = df.apply(lambda row: has_unit(row.x), axis=1)
    return df
