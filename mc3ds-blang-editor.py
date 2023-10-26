import os
import sys
from tkinter import Tk
from tkinter import filedialog

def clear():
    os.system("cls")

if __name__ == "__main__":
    Tk().withdraw()

    outputFolder = "MC3DS"

    print("Enter filepath: ")
    filepath = filedialog.askopenfilename()
    print(filepath)

    filename = filepath.split("/")
    filename = filename[len(filename)-1]

    with open(filepath, "rb") as f:
        file_content = f.read()

    # Obtiene la lista de bytes en decimal
    bytes_decimal = []
    for b in file_content:
        bytes_decimal.append(b)

    idx = 3
    time = 0
    elements = []
    text = ''
    element = []
    for i in range(0, 3297 * 8):
        if idx + 1 <= len(bytes_decimal):
            element.append(bytes_decimal[idx])
            time += 1
            if time == 8:
                if len(element) == 0:
                    break
                elements.append(element)
                text = (f"{text}{element}\n")
                element = []
                time = 0
            idx += 1
        else:
            break

    idx = 8 + (3297 * 8)

    joinedText = ''
    joinedBytes = []
    joined = []
    while True:
        if idx + 1 <= len(bytes_decimal):
            if bytes_decimal[idx] != 0:
                joinedText = (f"{joinedText}{chr(bytes_decimal[idx])}")
                joined.append(bytes_decimal[idx])
            else:
                joinedText = (f"{joinedText}\n")
                joinedBytes.append(joined)
                joined = []
            idx += 1
        else:
            break

    texts = joinedText.split("\n")
    
    print(f"Select how to search for a text: \n\t1: By ID\n\t2: By text\n\t0: Exit")
    option = input("Enter an option: ")
    match option:
        case "1":
            i = 0
            for x in elements:
                print(f"{i + 1}: {elements[i]}--{texts[i]}")
                i += 1

            selection = input("Enter the id: ")
            if selection.isdigit() == True:
                print(selection.isdigit())
                selection = int(selection)
            else:
                print("Error: The ID must be a int")
                print("The program will close")
                os.system("pause")
                sys.exit()
        case "2":
            selection = input("Enter the text: ")
            results = []
            i = 0
            for x in texts:
                if selection == texts[i]:
                    results.append(f"{i+1}: {elements[i]}--{texts[i]}")
                i += 1
            clear()
            for x in results:
                print(x)
            selection = input("Enter the ID: ")
            if selection.isdigit() == True:
                print(selection.isdigit())
                selection = int(selection)
            else:
                print("Error: The ID must be a int")
                print("The program will close")
                os.system("pause")
                sys.exit()
        case "0":
            sys.exit()
    
    clear()

    print(f"Selection: {elements[selection-1]}--{texts[selection-1]}")

    replaceText = input("Enter the text to replace: ")

    tempText = []
    for l in replaceText:
        tempText.append(ord(l))

    joinedBytes[selection-1] = tempText

    output_data = [225, 12, 0]
    idx = 0
    byte_1 = 0
    byte_2 = 0
    byte_3 = 0
    for item in elements:
        singleElement = item
        output_data.append(singleElement[0])
        output_data.append(singleElement[1])
        output_data.append(singleElement[2])
        output_data.append(singleElement[3])
        output_data.append(singleElement[4])
        output_data.append(byte_1)
        output_data.append(byte_2)
        output_data.append(byte_3)
        for i in range(0, len(joinedBytes[idx]) + 1):
            if byte_1 == 256:
                byte_2 += 1
                byte_1 = 0
            if byte_2 == 256:
                byte_3 += 1
                byte_2 = 0
            byte_1 += 1
            if byte_1 == 256:
                byte_2 += 1
                byte_1 = 0
            if byte_2 == 256:
                byte_3 += 1
                byte_2 = 0
        idx += 1

    # Insert the lenght of the text part
    output_data.append(0)
    output_data.append(byte_1)
    output_data.append(byte_2)
    output_data.append(byte_3)
    output_data.append(0)
    
    for item in joinedBytes:
        for x in item:
            output_data.append(x)
        output_data.append(0)

    clear()

    byte_arr = bytearray(output_data)

    if not os.path.exists(f"{outputFolder}/"):
        os.mkdir(f"{outputFolder}")

    with open(f"{outputFolder}/{filename}", "wb") as f:
        f.write(byte_arr)

    print("Success. The program will close...")
    os.system("pause")