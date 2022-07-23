import csv

s = []
with open("symbols.csv", encoding="utf-8") as handle:
    spamreader = csv.reader(handle)
    for row in spamreader:
        if row[0].startswith("#"):
            continue
        s.append(row[0])

print(",".join(s))
