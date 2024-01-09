import os
import difflib
import tkinter
from tkinter import filedialog

from modules import *

def clear():
    os_type = os.name
    if os_type == "posix":
        os.system("clear")
    elif os_type == "nt":
        os.system("cls")
    else:
        print("Unsupported OS")

if __name__ == "__main__":
    tkinter.Tk().withdraw()

    print("Enter filepath: ")
    filepath = filedialog.askopenfilename()
    print(filepath)

    file = BlangFile().open(filepath)
    clear()
    
    closeMenu1 = False
    while closeMenu1 == False:
        print(f"Enter an option: \n\t1: Search By ID\n\t2: Search By text\n\t3: Export\n\t0: Exit")
        option = input("Enter an option: ")
        match option:
            case "1":
                clear()
                i = 0
                items = file.getTexts()
                for x in items:
                    print(f"{i + 1}: {items[i]}")
                    i += 1

                selection = input("Enter the id: ")
                if selection.isdigit() == True:
                    print(selection.isdigit())
                    selection = int(selection)
                    newText = input("Enter the text to replace to: ")

                    file.replace(items[selection - 1], newText)
                    clear()
                    print("Successfully replaced!")
                else:
                    clear()
                    print("Error: The ID must be a int")
            case "2":
                clear()
                selection = input("Enter the text: ")
                texts = file.getTexts()
                results = []
                matches = difflib.get_close_matches(selection, texts, cutoff=0.4)
                for k in matches:
                    if k in texts:
                        results.append(k)
                clear()
                idx = 1
                for x in results:
                    print(f"{idx}: {x}")
                    idx += 1

                selection = input("Enter the ID: ")
                if selection.isdigit() == True:
                    print(selection.isdigit())
                    selection = int(selection)
                    newText = input("Enter the text to replace to: ")

                    file.replace(texts[selection - 1], newText)
                    clear()
                    print("Successfully replaced!")
                else:
                    clear()
                    print("Error: The ID must be a int")

            case "3":
                # Export
                clear()
                outputFolder = input("Enter the output folder: ")
                if outputFolder != "":
                    file.export(outputFolder)
                    clear()
                    print("Successfully exported!")
                else:
                    clear()
                    print("Error: Folder cannot be empty")

            case "0":
                closeMenu1 = True