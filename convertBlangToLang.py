from modules.MC3DSBlang import BlangFile, get_JOAAT_hash
import sys, os, json

if len(sys.argv) > 1:
    if os.path.exists(sys.argv[1]) and os.path.isfile(sys.argv[1]):
        blangFile = BlangFile().open(sys.argv[1])
        stringsData = blangFile.getStringData()

        with open("./index/text_ids.json", "r", encoding="utf-8") as f:
            indexData: dict = json.load(f)

        if not os.path.exists("./out"):
            os.makedirs("./out")

        with open(sys.argv[1].replace(".blang", ".lang"), "w", encoding="utf-8") as f:
            shortedIDs: list[str] = list(indexData.keys())
            shortedIDs.sort()
            for key in shortedIDs:
                id_hash = get_JOAAT_hash(key.lower().encode("utf-8"))
                if str(id_hash) in stringsData:
                    string = stringsData[str(id_hash)]
                    f.write(f"{key}={string}\n")
    else:
        print(f"Usage: {sys.argv[0]} <input>.blang")
else:
    print(f"Usage: {sys.argv[0]} <input>.blang")