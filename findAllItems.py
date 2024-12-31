from pyBjson.string_hash import get_JOAAT_hash
import json, os

def first_letter_lower(s: str):
    if not s:
        return s
    return s[0].lower() + s[1:]

with open("./patch.txt", "r") as f:
    fileContent = f.readlines()

if os.path.exists("./index/text_ids.json"):
    with open("./index/text_ids.json", "r") as f:
        text_ids = json.load(f)
else:
    text_ids = {}

with open("./out/en_US-pocket.json", "r", encoding="utf-8") as f:
    langData = json.load(f)

for i, element in enumerate(fileContent):
    fileContent[i] = element.split("|")[0]

found = 0
for string in fileContent:
    if not string.isupper():
        id_text = f"{first_letter_lower(string)}"
    else:
        id_text = f"{string.lower()}"
    id_hash = get_JOAAT_hash(id_text.lower().encode("utf-8"))

    if str(id_hash) in langData:
        text_data = langData[str(id_hash)]

        allKeysLower = [stringLower.lower() for stringLower in text_ids.keys()]
        if not id_text.lower() in allKeysLower:
            print(id_text)
            text_ids[id_text] = {"hash": id_hash}
            found += 1

print("Strings that matched:", found)
with open("./index/text_ids.json", "w", encoding="utf-8") as f:
    json.dump(text_ids, f, ensure_ascii=False, indent=4)