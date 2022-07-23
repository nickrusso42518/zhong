import json
with open("symbols.json", encoding="utf-8") as handle:
    d = json.load(handle)
for data in d:
    print(f'{data["chinese"]},{data["pinyin"]},{data["english"]}')
