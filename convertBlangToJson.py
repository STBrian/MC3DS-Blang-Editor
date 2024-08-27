import os
from modules import *

inputFile = input("Enter the file path: ")
blangFile = BlangFile().open(inputFile)

outputDir = input("Enter the output directory: ")
blangFile.exportToJson(outputDir)

print("Success!")

if os.name == "nt":
    os.system("pause")