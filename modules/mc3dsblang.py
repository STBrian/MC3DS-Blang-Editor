import os
from pathlib import Path

class MC3DSBlangException(Exception):
    def __init__(self, message):
        super().__init__(message)

class BlangFile:
    def __init__(self):
        return
    
    def open(self, path: str):
        if type(path) != str:
            MC3DSBlangException("path must be a 'str'")

        self.filename = Path(path).name

        with open(path, "rb") as f:
            file_content = list(f.read())

        # Get header
        byte_1 = file_content[0]
        byte_2 = file_content[1]
        byte_3 = file_content[2]
        byte_4 = file_content[3]

        self.long = byte_1 + (byte_2 * 16 ** 2) + (byte_3 * 16 ** 4) + (byte_4 * 16 ** 8)

        idx = 4
        data = []
        for i in range(0, self.long):
            join = []
            for j in range(0, 8):
                join.append(file_content[idx])
                idx += 1
            data.append(join)
        self.data = data

        byte_1 = file_content[idx]
        byte_2 = file_content[idx + 1]
        byte_3 = file_content[idx + 2]
        byte_4 = file_content[idx + 3]

        self.textlong = byte_1 + (byte_2 * 16 ** 2) + (byte_3 * 16 ** 4) + (byte_4 * 16 ** 8)

        idx += 4
        texts = []
        for i in range(0, self.long):
            join = []
            while file_content[idx] != 0:
                join.append(file_content[idx])
                idx += 1
            texts.append(bytearray(join).decode("utf-8"))
            idx += 1
        self.texts = texts

        print(self.data)
        print(self.texts)
        print(self.long)
        print(self.textlong)
        print(self.filename)

        return self
    
    def getData(self):
        return self.data

    def getTexts(self):
        return self.texts

    def replace(self, text: str, newtext: str):
        if type(text) != str:
            MC3DSBlangException("text must be a 'str'")
        if type(newtext) != str:
            MC3DSBlangException("newtext must be a 'str'")

        if text in self.texts:
            print(True)
            print(self.texts.index(text))
            if newtext != "" and newtext != '':
                self.texts[self.texts.index(text)] = newtext
            else:
                self.texts[self.texts.index(text)] = " "
        else:
            print(False)
        return
    
    def export(self, path: str):
        if type(path) != str:
            MC3DSBlangException("path must be a 'str'")

        indexLong = []
        self.long = len(self.data)
        bytes_list = list(self.long.to_bytes(4))
        for i in range(0, 4):
            indexLong.append(bytes_list[3 - i])

        textsLong = []
        self.textlong = 0
        for i in range(0, len(self.texts)):
            self.textlong += len(self.texts[i].encode("utf-8"))
            self.textlong += 1
        bytes_list = list(self.textlong.to_bytes(4))
        for i in range(0, 4):
            textsLong.append(bytes_list[3 - i])

        print(indexLong)
        print(textsLong, self.textlong)
        indexData = []
        textData = []

        for i in range(0, self.long):
            # Copiar los primeros datos del elemento
            item = self.data[i]
            for j in range(0, 4):
                indexData.append(item[j])

            # Posición de texto
            bytes_list = list(len(textData).to_bytes(4))
            for j in range(0, 4):
                indexData.append(bytes_list[3 - j])
            
            # Agregar texto
            encodedText = list(self.texts[i].encode("utf-8"))
            for j in range(0, len(encodedText)):
                textData.append(encodedText[j])
            # Separador/terminador
            textData.append(0)

        self.exportData = []
        self.exportData.extend(indexLong)
        self.exportData.extend(indexData)
        self.exportData.extend(textsLong)
        self.exportData.extend(textData)

        self.exportData = bytearray(self.exportData)

        with open(os.path.join(path, self.filename), "wb") as f:
            f.write(self.exportData)