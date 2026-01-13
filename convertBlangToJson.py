import os, sys
from modules.MC3DSBlang import BlangFile
from pathlib import Path

if len(sys.argv) > 1:
    if os.path.exists(sys.argv[1]) and os.path.isfile(sys.argv[1]):
        blangFile = BlangFile().open(sys.argv[1])

        if not os.path.exists("./out"):
            os.makedirs("./out")

        filename = Path(sys.argv[1]).name
        with open(f"./out/{filename.replace('.blang', '.json')}", "w", encoding="utf-8") as f:
            f.write(blangFile.getJson())
    else:
        print(f"Usage: {sys.argv[0]} <input>.blang")
else:
    print(f"Usage: {sys.argv[0]} <input>.blang")