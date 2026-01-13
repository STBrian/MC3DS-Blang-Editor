import json
from pathlib import Path

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

class MC3DSBlangException(Exception):
    def __init__(self, message):
        super().__init__(message)

class BlangFile:
    def __init__(self):
        return
    
    def open(self, path: str|Path):
        if isinstance(path, str):
            path = Path(path)
        elif isinstance(path, Path):
            pass
        else:
            raise TypeError("path must be a 'str' or 'Path'")
        
        with open(path, "rb") as f:
            file_content = list(f.read())

        # Obtener longitud
        long = []
        for i in range(0, 4):
            long.append(file_content[i])
        long = int.from_bytes(bytearray(long), "little")

        # Obtener los elementos del indice
        idx = 4
        data = []
        for i in range(0, long):
            join = []
            for j in range(0, 4):
                join.append(file_content[idx])
                idx += 1
            data.append(join)
            idx += 4

        # Longitud de los textos
        textlong = []
        for i in range(idx, idx + 4):
            textlong.append(file_content[i])
        textlong = int.from_bytes(bytearray(textlong), "little")

        # Obtener los textos
        idx += 4
        texts = []
        for i in range(0, long):
            join = []
            while file_content[idx] != 0:
                join.append(file_content[idx])
                idx += 1
            texts.append(bytearray(join).decode("utf-8"))
            idx += 1

        self.data = data
        self.texts = texts
        return self
    
    def getData(self):
        return self.data

    def getTexts(self) -> list:
        return self.texts

    def replace(self, idx: int, newtext: str):
        if type(idx) != int:
            raise MC3DSBlangException("idx must be an 'int'")
        if type(newtext) != str:
            raise MC3DSBlangException("newtext must be a 'str'")

        if idx >= 0 and idx < len(self.texts):
            if newtext != "" and newtext != '':
                self.texts[idx] = newtext
            else:
                self.texts[idx] = " "
        return
    
    # TODO: Improve setText, getText and contains methods
    def setText(self, textId: str, text: str):
        dataDict = self.getStringData()
        dataDict[str(get_JOAAT_hash(textId.lower().encode()))] = text
        self.importFromDict(dataDict)

    def getText(self, textId: str) -> str | None:
        dataDict = self.getStringData()
        try:
            if textId.isdigit():
                return dataDict[textId]
            else:
                return dataDict[str(get_JOAAT_hash(textId.lower().encode()))]
        except:
            return None
        
    def contains(self, textId: str):
        dataDict = self.getStringData()
        if textId.isdigit():
            if textId in dataDict:
                return True
        else:
            if str(get_JOAAT_hash(textId.lower().encode)) in dataDict:
                return True
        return False
    
    def export(self, path: str):
        if type(path) != str:
            raise MC3DSBlangException("path must be a 'str'")

        long = len(self.data)
        indexLong = list(long.to_bytes(4, "little"))

        indexData = []
        textData = []
        for i in range(0, long):
            # Copiar los primeros datos del elemento
            indexData.extend(self.data[i])

            # Posición de texto
            indexData.extend(list(len(textData).to_bytes(4, "little")))
            
            # Agregar texto
            textData.extend(list(self.texts[i].encode("utf-8")))

            # Separador/terminador
            textData.append(0)

        textsLong = list(len(textData).to_bytes(4, "little"))

        # Junta todo en una sola lista
        self.exportData = []
        self.exportData.extend(indexLong)
        self.exportData.extend(indexData)
        self.exportData.extend(textsLong)
        self.exportData.extend(textData)

        self.exportData = bytearray(self.exportData)

        with open(path, "wb") as f:
            f.write(self.exportData)
        return

    def getStringData(self):
        long = len(self.data)
        dataDictionary = {}
        for i in range(0, long):
            identifier = bytearray(self.data[i])
            identifier = int.from_bytes(identifier, "little")
            identifier = str(identifier)
            
            dataDictionary[identifier] = self.texts[i]
        return dataDictionary

    def getJson(self):
        dataDictionary = self.getStringData()
        json_str = json.dumps(dataDictionary, indent=4, ensure_ascii=False)
        return json_str
    
    def importFromDict(self, data: dict):
        if type(data) != dict:
            raise MC3DSBlangException("path must be a 'str'")
        
        hashedDict = {}
        stringHashes: list[int] = []
        for key, value in data.items():
            if key.isdigit():
                stringHash = int(key)
            else:
                stringHash = get_JOAAT_hash(key.lower().encode("utf-8"))
            hashedDict[str(stringHash)] = value
            stringHashes.append(stringHash)
        stringHashes.sort()

        sortedData = []
        texts = []

        for key in stringHashes:
            sortedData.append(list(key.to_bytes(4, "little")))
            texts.append(hashedDict[str(key)])

        self.data = sortedData
        self.texts = texts
        return self