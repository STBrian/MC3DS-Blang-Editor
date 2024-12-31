from pyBjson.string_hash import get_JOAAT_hash
import json, os

with open("./extracted_texts.txt", "r") as f:
    fileContent = f.readlines()

if os.path.exists("./index/text_ids.json"):
    with open("./index/text_ids.json", "r") as f:
        text_ids = json.load(f)
else:
    text_ids = {}

with open("./MC3DS/en_US-pocket.json", "r", encoding="utf-8") as f:
    langData = json.load(f)

for i, element in enumerate(fileContent):
    fileContent[i] = element.split("\n")[0]

found = 0
for string in fileContent:
    id_text = string
    id_hash = get_JOAAT_hash(id_text.lower().encode("utf-8"))

    if str(id_hash) in langData:
        text_data = langData[str(id_hash)]

        print(string)
        text_ids[id_text] = {"hash": id_hash}
        found += 1

print("Strings that matched:", found)
with open("./index/text_ids.json", "w", encoding="utf-8") as f:
        json.dump(text_ids, f, ensure_ascii=False, indent=4)