import json
class Section:
    def __init__(self, handle, typ, size):
        self.handle = handle
        self.typ = typ
        self.size = size
        self.data = {}
    def setProperty(self, key, val):
        self.data[key] = val
def countTabs(string):
    i = 0
    while i < len(string) and string[i] == '\t':
        i = i + 1
    return i
def parseHandle(handle):
    return [x.strip() for x in handle.replace('Handle', '').replace('DMI type', '').replace('bytes', '').split(', ')]
def parseDMI(string):
    DMIData = {}
    lasOpenSection = ""
    variableData = ""
    variableName = ""
    for line in string.split('\n')[6:]:
        tabsCount = countTabs(line)
        if variableName != "" and tabsCount != 2:
            DMIData[lastOpenSection].setProperty(variableName, variableData.strip())
            variableName = variableData = ""
        if len(line) == 0:
            continue
        elif len(line) > 6 and line[0:6] == "Handle":
          handleData = parseHandle(line)
        elif tabsCount == 0:
            DMIData[line] = Section(handleData[0], handleData[1], handleData[2])
            lastOpenSection = line
        elif tabsCount == 1:
            splitted = line.split(':')
            variableName = splitted[0].strip()
            variableData = splitted[1].strip() + "\n"
        else:
            variableData += line[2:] + "\n"
    return DMIData


data = open("data.txt", "r").read()
parsed = parseDMI(data)
print json.dumps(parsed, default=lambda o: o.__dict__, indent=2)
