import csv

path = "../csv/employees.csv"

with open(path, newline="", encoding="utf-8") as f:
    reader = csv.reader(f)
    next(reader)
    rows = list(reader)

names = []
for row in rows:
    if len(row) >= 2:
        names.append(row[0] + " " + row[1])

print(names)

names_with_e = [name for name in names if "e" in name.lower()]
print(names_with_e)