class BlangFile:
    def __init__(self):
        return
    
    def open(self, path: str):
        with open(path, "rb") as f:
            file_content = f.read()

        