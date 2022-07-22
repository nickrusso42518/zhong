import json
import random

from colorama import Fore
from colorama import Style

with open("symbols.json", encoding="utf=8") as handle:
    symbols = json.load(handle)

# jsonschema here

print("NOTE: use numeric pinyin format: zhong1, cha2, hao3, jian4, ma\n")
while symbols:
    count = 1
    index = random.randint(0, len(symbols) - 1)
    sym = symbols[index]
    pinyin = sym["pinyin"].lower().strip()
    english = sym["english"].lower().strip()

    attempt = input(f"{count}. Enter pinyin,english for {sym['chinese']}: ")
    in1, in2 = attempt.split(",")

    p_color = Fore.GREEN if in1.lower().strip() == pinyin else Fore.RED
    e_color = Fore.GREEN if in2.lower().strip() == english else Fore.RED
    print(f"pinyin: {p_color}{pinyin}{Style.RESET_ALL}", end="")
    print(f"  /  english: {e_color}{english}{Style.RESET_ALL}\n")

    del symbols[index]
    count += 1
