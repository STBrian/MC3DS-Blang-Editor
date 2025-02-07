import os, sys
from modules.MC3DSBlang import BlangFile

def parseLang(data: str) -> dict:
    lines = data.split("\n")
    length = len(lines)
    for i in range(length-1, -1, -1):
        if len(lines[i]) < 1:
            lines.pop(i)
        elif lines[i].startswith("##"):
            lines.pop(i)
        elif lines[i].find("=") == -1:
            raise SyntaxError(f"Expected at least one '=' in line {i} of file")
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

if len(sys.argv) > 1:
    if os.path.exists(sys.argv[1]) and os.path.isfile(sys.argv[1]):
        with open(sys.argv[1], "r", encoding="utf-8-sig") as f:
            dataDict = parseLang(f.read())

        blangFile = BlangFile().importFromDict(dataDict)

        if not os.path.exists("./out"):
            os.makedirs("./out")

        blangFile.export("./out/en_US-pocket.blang")
    else:
        print("Usage: python convertLangToBlang.py <input>.lang")
else:
    print("Usage: python convertLangToBlang.py <input>.lang")