import os, sys
from modules.MC3DSBlang import BlangFile

if len(sys.argv) > 1:
    if os.path.exists(sys.argv[1]) and os.path.isfile(sys.argv[1]):
        blangFile = BlangFile().open(sys.argv[1])
        stringsData = blangFile.getStringData()

        if not os.path.exists("./out"):
            os.makedirs("./out")

        with open("./out/en_US-pocket.json", "w", encoding="utf-8") as f:
            f.write(blangFile.getJson())
    else:
        print("Usage: python convertBlangToJson.py <input>.blang")
else:
    print("Usage: python convertBlangToJson.py <input>.blang")