import os
from modules.mc3dsblang import *

inputFile = input("Enter the file path: ")
blangFile = BlangFile().fromJson(inputFile)

outputDir = input("Enter the output directory: ")
blangFile.export(outputDir)

print("Success!")

if os.name == "nt":
    os.system("pause")