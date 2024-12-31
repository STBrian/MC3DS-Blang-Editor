import os, sys
from modules.MC3DSBlang import BlangFile

if len(sys.argv) > 1:
    if os.path.exists(sys.argv[1]) and os.path.isfile(sys.argv[1]):
        with open(sys.argv[1], "r", encoding="utf-8") as f:
            langData = [element.split('\n')[0] for element in f.readlines()]
        listPairs = [(element.split('=')[0], element.split('=', maxsplit=1)[1]) for element in langData]

        dataDict = {}
        for element in listPairs:
            dataDict[element[0]] = element[1]
        blangFile = BlangFile().importFromDict(dataDict)

        if not os.path.exists("./out"):
            os.makedirs("./out")

        blangFile.export("./out/en_US-pocket.blang")
    else:
        print("Usage: python convertLangToBlang.py <input>.lang")
else:
    print("Usage: python convertLangToBlang.py <input>.lang")