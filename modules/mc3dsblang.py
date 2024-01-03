from pathlib import Path

class BlangFile:
    def __init__(self):
        return
    
    def open(self, path: str):
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
            for j in range(0, 8):
                data.append(file_content[idx])
                idx += 1
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