import os
from modules.mc3dsblang import *

inputFile = input("Enter the file path: ")
blangFile = BlangFile().open(inputFile)

outputDir = input("Enter the output directory: ")
blangFile.toJson(outputDir)

print("Success!")

if os.name == "nt":
    os.system("pause")