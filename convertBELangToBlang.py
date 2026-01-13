# This script attempts to convert a lang file from an old Minecraft PE version to
# a blang for the Minecraft New N3DS Edition
import os, sys, json
from modules.MC3DSBlang import BlangFile, get_JOAAT_hash
from pathlib import Path
from deep_translator import GoogleTranslator
from modules.parseLang import parseLang, exportLang

os.chdir(os.path.dirname(__file__))

GlobalTranslateInstance = None
def new_translate_instance(source_lang, target_lang):
    global GlobalTranslateInstance
    GlobalTranslateInstance = GoogleTranslator(source=source_lang, target=target_lang)

def translate_text(text: str):
    if not isinstance(text, str) or not text.strip():
        raise ValueError("text must be a non-empty string")
    
    translated = GlobalTranslateInstance.translate(text)
    return translated

if len(sys.argv) > 1:
    if os.path.exists(sys.argv[1]) and os.path.isfile(sys.argv[1]):
        with open("./out/en_US-base.lang", "r", encoding="utf-8-sig") as f:
            baseFile = parseLang(f.read())
        with open(sys.argv[1], "r", encoding="utf-8-sig") as f:
            fullDataDict = parseLang(f.read())

        dataDict = {}
        for key, value in fullDataDict.items():
            if key in baseFile:
                dataDict[key] = value

        blangFile = BlangFile().importFromDict(dataDict)
        textIDs: list[str] = list(baseFile.keys())
        sortedIDs: list[int] = [get_JOAAT_hash(f.lower().encode()) for f in textIDs]
        stringsIDs: list[int] = [int(f) for f in blangFile.getStringData().keys()]

        for id in stringsIDs:
            if id in sortedIDs:
                idx = sortedIDs.index(id)
                sortedIDs.pop(idx)
                textIDs.pop(idx)

        if not os.path.exists("./out"):
            os.makedirs("./out")

        # generate a file with all missing texts
        exportMissing = {}
        for i, textID in enumerate(textIDs):
            textData = baseFile[textID]
            exportMissing[textID] = textData
        if os.path.exists("./out/missing_ids.json"):
            with open("./out/missing_ids.json", "r", encoding="utf-8-sig") as f:
                missingHashes: dict = json.loads(f.read())
            for hash, textData in missingHashes.items():
                exportMissing[hash] = textData
        exportLang("./out/missingtexts-en_US.lang", exportMissing)
        sys.exit(0)

        if "language.code" in textIDs:
            lang_code = input("Set the language code: ")
            blangFile.setText("language.code", lang_code)
            idx = sortedIDs.index(get_JOAAT_hash("language.code".encode()))
            sortedIDs.pop(idx)
            textIDs.pop(idx)
        else:
            lang_code = blangFile.getText("language.code")
        if "language.name" in textIDs:
            lang_name = input("Set the language name: ")
            blangFile.setText("language.name", lang_name)
            idx = sortedIDs.index(get_JOAAT_hash("language.name".encode()))
            sortedIDs.pop(idx)
            textIDs.pop(idx)
        if "language.region" in textIDs:
            lang_region = input("Set the language region: ")
            blangFile.setText("language.region", lang_region)
            idx = sortedIDs.index(get_JOAAT_hash("language.region".encode()))
            sortedIDs.pop(idx)
            textIDs.pop(idx)

        lang = None
        autoTranslate = None
        if len(sortedIDs) > 0:
            autoTranslate = input("Some IDs are missing. Do you want to auto translate them? [y/N]").strip().lower()[0]
            if autoTranslate == "y":
                textIDs.sort()
                print("Attempting auto translation")
                lang = input("Enter language to translate: ")
                new_translate_instance("en", lang)
                for i, textID in enumerate(textIDs):
                    textData = baseFile[textID]
                    print(f"{i}: {textID}")
                    try:
                        translatedText = translate_text(textData)
                        print(f"{i}: {textData}")
                        print(f"{i}: {translatedText}")
                        blangFile.setText(textID, translatedText)
                    except Exception as e:
                        print(f"Failed to translate {textData}: {e}")
                    print(f"Progress: {i+1}/{len(textIDs)}")

        if os.path.exists("./out/missing_ids.json"):
            with open("./out/missing_ids.json", "r", encoding="utf-8-sig") as f:
                missingHashes: dict = json.loads(f.read())
            notMissingHashesPresent = {}
            for hash, textData in missingHashes.items():
                if not blangFile.contains(hash):
                    notMissingHashesPresent[hash] = textData
            if len(notMissingHashesPresent) > 0:
                if autoTranslate is None:
                    autoTranslate = input("Some IDs are missing. Do you want to auto translate them? [y/N]").strip().lower()[0]
                if autoTranslate == "y":
                    print("Attempting auto translation for missing IDs from missing_ids.json")
                    if lang is None:
                        lang = input("Enter language to translate: ")
                        new_translate_instance("en", lang)
                    for hash, textData in notMissingHashesPresent.items():
                        try:
                            translatedText = translate_text(textData)
                            print(f"{hex(hash)}: {textData}")
                            print(f"{hex(hash)}: {translatedText}")
                            blangFile.setText(textID, translatedText)
                        except Exception as e:
                            print(f"Failed to translate {textData}: {e}")

        filename = Path(sys.argv[1]).name
        blangFile.export(f"./out/{lang_code}-pocket.blang")
    else:
        print(f"Usage: {sys.argv[0]} <input>.lang")
else:
    print(f"Usage: {sys.argv[0]} <input>.lang")