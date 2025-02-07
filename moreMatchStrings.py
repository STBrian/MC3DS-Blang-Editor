import os
import json

from pyBjson.string_hash import get_JOAAT_hash

def listDiff(a, b) -> list:
    c = []
    for element in a:
        if not element in b:
            c.append(element)

    return c

def parseLang(data: str) -> dict:
    lines = data.split("\n")
    length = len(lines)
    for i in range(length-1, -1, -1):
        if len(lines[i]) < 1:
            lines.pop(i)
        elif lines[i].startswith("##") or lines[i].startswith("\ufeff##"):
            lines.pop(i)
        else:
            isEmpty = True
            for character in lines[i]:
                if character != " ":
                    isEmpty = False
                    break
            if isEmpty:
                lines.pop(i)

    data_dict = {}
    for line in lines:
        value = line.split("=", 1)
        data_dict[value[0]] = value[1]
    
    return data_dict

def main():
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

    with open("./en_US-pocket.lang", "r", encoding="utf-8") as f:
        parsedLang = parseLang(f.read())

    for element in parsedLang.keys():
        generated_hash = get_JOAAT_hash(str(element).lower().encode("utf-8"))
        if generated_hash in missingHashes:
            print(f"{element}: {generated_hash}")
            text_ids[element] = {"hash": generated_hash}
            missingHashes.remove(generated_hash)

    with open("./index/text_ids.json", "w", encoding="utf-8") as f:
        json.dump(text_ids, f, ensure_ascii=False, indent=4)
    
    print(f"Missing hashes: {len(missingHashes)}")

if __name__ == "__main__":
    main()