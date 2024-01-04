from modules.mc3dsblang import *

inputFile = input("Enter the file path: ")
blangFile = BlangFile().fromJson(inputFile)

outputDir = input("Enter the output directory: ")
blangFile.export(outputDir)