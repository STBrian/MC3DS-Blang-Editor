from pyBjson.string_hash import get_JOAAT_hash
import json, os

if os.path.exists("./index/text_ids.json"):
    with open("./index/text_ids.json", "r") as f:
        text_ids = json.load(f)
else:
    text_ids = {}

with open("./MC3DS/en_US-pocket.json", "r", encoding="utf-8") as f:
    langData = json.load(f)

while True:
    id_text = input("Enter text id: ")
    id_hash = get_JOAAT_hash(id_text.lower().encode("utf-8"))

    if str(id_hash) in langData:
        text_data = langData[str(id_hash)]

        print(text_data)
        text_ids[id_text] = {"hash": id_hash}
    else:
        print("Hash not found for text:", id_text)

    with open("./index/text_ids.json", "w", encoding="utf-8") as f:
        json.dump(text_ids, f, ensure_ascii=False, indent=4)