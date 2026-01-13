import sys, os
from pathlib import Path
from modules.parseLang import parseLang

unused_words = ["realm", "Realm", "screenshot", "vsync", "renderDistance",
                "keyboardLayout", "invertMouse", "guiScale", "gamma", "framerateLimit", 
                "fov", "fboEnable", "forceUnicodeFont", "farWarning", "entityShadows",
                "chat", "changeGamertag", "animatetextures", "advancedOpengl", "playdemo",
                "livingroom", "fireworksCharge", "invite", "createWorld.customize", "controllerLayoutScreen",
                "commands.", "chalkboardScreen", "fullscreen", "msaa", "texelAA", "swapJumpAndSneak", 
                "fancyskies", "destroyvibration", "usetouchpad", "lefthanded", "hidegui", 
                "transparentleaves", "particleRenderDistance", "selectServer.", "authserver",
                "translation.test", "soundCategory", "selectWorld.tab", "riftControls"]

def checkKey(tkey: str):
    """
    Returns True if the key doesn't contain any unused_words
    
    :param tkey: Key to check
    :type tkey: str
    """
    for element in unused_words:
        if element in tkey:
            return False
    return True

if len(sys.argv) > 1:
    if os.path.exists(sys.argv[1]) and os.path.isfile(sys.argv[1]):
        with open(sys.argv[1], "r", encoding="utf-8-sig") as f:
            dataDict = parseLang(f.read())

        newDatDict = {}
        for key, value in dataDict.items():
            if checkKey(key):
                newDatDict[key] = value

        if not os.path.exists("./out"):
            os.makedirs("./out")

        filename = Path(sys.argv[1]).stem
        with open(f"./out/{filename}_new.lang", "w", encoding="utf-8-sig") as f:
            f.writelines([f"{key}={value}\n" for key, value in newDatDict.items()])
    else:
        print(f"Usage: {sys.argv[0]} <input>.lang")
else:
    print(f"Usage: {sys.argv[0]} <input>.lang")