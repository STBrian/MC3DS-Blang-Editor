import os
from modules import *

inputFile = input("Enter the file path: ")
blangFile = BlangFile().importFromJson(inputFile)

outputDir = input("Enter the output directory: ")
blangFile.export(outputDir)

print("Success!")

if os.name == "nt":
    os.system("pause")