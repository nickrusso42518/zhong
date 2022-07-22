import json
import random
import subprocess

from colorama import Fore
from colorama import Style

# Toggle reading of Chinese symbols
SPEAK = True

with open("symbols.json", encoding="utf=8") as handle:
    symbols = json.load(handle)

# jsonschema here

print("NOTE: use numeric pinyin format: zhong1, cha2, hao3, jian4, ma\n")
count = 1
while symbols:
    index = random.randint(0, len(symbols) - 1)
    sym = symbols[index]
    pinyin = sym["pinyin"].lower().strip()
    english = sym["english"].lower().strip()

    attempt = ""
    while not attempt.strip():
        print(f"\n{count}. Symbols (press ENTER to reprint): {sym['chinese']}")
        if SPEAK:
            subprocess.run(["say", "-v", "Ting-Ting", sym["chinese"]])
        attempt = input(f"Type the pinyin,english: ")

    in1, in2 = attempt.split(",")

    p_color = Fore.GREEN if in1.lower().strip() == pinyin else Fore.RED
    e_color = Fore.GREEN if in2.lower().strip() == english else Fore.RED
    print(f"pinyin: {p_color}{pinyin}{Style.RESET_ALL}", end="")
    print(f"  /  english: {e_color}{english}{Style.RESET_ALL}")

    del symbols[index]
    count += 1
