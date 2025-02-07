import os
import json

def listDiff(a, b) -> list:
    c = []
    for element in a:
        if not element in b:
            c.append(element)

    return c

if os.path.exists("./index/text_ids.json"):
    with open("./index/text_ids.json", "r") as f:
        text_ids: dict = json.load(f)
else:
    text_ids = {}

with open("./out/en_US-pocket.json", "r", encoding="utf-8") as f:
    langData: dict = json.load(f)

currentHashes = [value["hash"] for value in text_ids.values()]
allHashes = [int(element) for element in list(langData.keys())]

missingHashes = listDiff(allHashes, currentHashes)

missing = {}
for element in missingHashes:
    missing[str(element)] = langData[str(element)]

with open("./out/missing_ids.json", "w", encoding="utf-8") as f:
    json.dump(missing, f, ensure_ascii=False, indent=4)