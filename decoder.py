import json
class Section:
    def __init__(self, handle, typ, size):
        self.handle = handle
        self.typ = typ
        self.size = size
        self.data = {}
    def set_property(self, key, val):
        self.data[key] = val
    def get_property(self, key):
        return self.data[key]

class DMIParser:
    def count_tabs(self, string):
        i = 0
        while i < len(string) and string[i] == '\t':
            i = i + 1
        return i
        
    def parse_handle(self, handle):
        return [x.strip() for x in handle.replace('Handle', '').replace('DMI type', '').replace('bytes', '').split(', ')]

    def parse_dmi(self, string):
        DMIData = {}
        last_open_section = ""
        variable_data = ""
        variable_name = ""
        for line in string.split('\n')[6:]:
            tabs_count = self.count_tabs(line)
            
            if variable_name != "" and tabs_count != 2:
                DMIData[last_open_section].set_property(variable_name, variable_data.strip())
                variable_name = variable_data = ""
            if len(line) == 0:
                continue
            elif len(line) > 6 and line[0:6] == "Handle":
              handle_data = self.parse_handle(line)
            elif tabs_count == 0:
                DMIData[line] = Section(handle_data[0], handle_data[1], handle_data[2])
                last_open_section = line
            elif tabs_count == 1:
                splitted = line.split(':')
                variable_name = splitted[0].strip()
                variable_data = splitted[1].strip() + "\n"
            else:
                variable_data += line[2:] + "\n"
        if variable_name != "":
            DMIData[last_open_section].set_property(variable_name, variable_data.strip())
        return DMIData

if __name__ == "__main__":
    data = open("data.txt", "r").read()
    parsed = DMIParser().parse_dmi(data)
    print(json.dumps(parsed, default=lambda o: o.__dict__, indent=2))
