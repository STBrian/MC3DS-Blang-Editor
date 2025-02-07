from modules.MC3DSBlang import BlangFile
import sys, os, json

def get_JOAAT_hash(string: bytes) -> int:
    hash_ = 0
    for char in string:
        hash_ += char
        hash_ &= 0xFFFFFFFF
        hash_ += (hash_ << 10)
        hash_ &= 0xFFFFFFFF
        hash_ ^= (hash_ >> 6)
    hash_ += (hash_ << 3)
    hash_ &= 0xFFFFFFFF
    hash_ ^= (hash_ >> 11)
    hash_ += (hash_ << 15)
    return hash_ & 0xFFFFFFFF

if len(sys.argv) > 1:
    if os.path.exists(sys.argv[1]) and os.path.isfile(sys.argv[1]):
        blangFile = BlangFile().open(sys.argv[1])
        stringsData = blangFile.getStringData()

        with open("./index/text_ids.json", "r", encoding="utf-8") as f:
            indexData: dict = json.load(f)

        if not os.path.exists("./out"):
            os.makedirs("./out")

        with open("./out/en_US-pocket.lang", "w", encoding="utf-8") as f:
            shortedIDs: list[str] = list(indexData.keys())
            shortedIDs.sort()
            for key in shortedIDs:
                id_hash = get_JOAAT_hash(key.lower().encode("utf-8"))
                if str(id_hash) in stringsData:
                    string = stringsData[str(id_hash)]
                    f.write(f"{key}={string["text"]}\n")
    else:
        print("Usage: python convertBlangToLang.py <input>.blang")
else:
    print("Usage: python convertBlangToLang.py <input>.blang")