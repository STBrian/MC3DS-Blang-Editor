import os
from modules import *

inputFile = input("Enter the file path: ")
with open(inputFile, "r", encoding="utf-8") as f:
    blangFile = BlangFile().importFromJson(f.read())

outputDir = input("Enter the output directory: ")
blangFile.export(outputDir)

print("Success!")

if os.name == "nt":
    os.system("pause")