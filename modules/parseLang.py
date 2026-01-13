def parseLang(data: str) -> dict:
    """
    Returns a dict with a key-value for every string
    
    :param data: Lang string read from a .lang file
    :type data: str
    :return: a dict with a key-value for every string from data
    :rtype: dict
    """
    lines = data.split("\n")
    length = len(lines)
    for i in range(length-1, -1, -1):
        if len(lines[i]) < 1:
            lines.pop(i)
        elif lines[i].startswith("##"):
            lines.pop(i)
        elif lines[i].find("=") == -1:
            raise SyntaxError(f"Expected at least one '=' in line {i} of file")
        else:
            isEmpty = True
            for character in lines[i]:
                if character != " ":
                    isEmpty = False
                    break
            if isEmpty:
                lines.pop(i)

    data_dict = {}
    for line in lines:
        value = line.split("=", 1)
        if value[1].find("\t#") > 0:
            pos = value[1].find("\t#")
            nval = value[1][:pos].rstrip("\t")
            data_dict[value[0]] = nval
        else:
            data_dict[value[0]] = value[1].rstrip("\t")
    
    return data_dict

def exportLang(fp, data: dict):
    with open(fp, "w", encoding="utf-8") as f:
        f.writelines([f"{key}={value}\n" for key, value in data.items()])