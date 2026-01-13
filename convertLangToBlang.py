import os, sys
from modules.MC3DSBlang import BlangFile
from pathlib import Path
from modules.parseLang import parseLang

if len(sys.argv) > 1:
    if os.path.exists(sys.argv[1]) and os.path.isfile(sys.argv[1]):
        with open(sys.argv[1], "r", encoding="utf-8-sig") as f:
            dataDict = parseLang(f.read())

        blangFile = BlangFile().importFromDict(dataDict)

        if not os.path.exists("./out"):
            os.makedirs("./out")

        filename = Path(sys.argv[1]).name
        blangFile.export(f"./out/{filename.replace('.blang', '.lang')}")
    else:
        print(f"Usage: {sys.argv[0]} <input>.lang")
else:
    print(f"Usage: {sys.argv[0]} <input>.lang")