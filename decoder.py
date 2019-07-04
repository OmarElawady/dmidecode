import json
class Section:
    def __init__(self, handle, typ, size):
        self.handle = handle
        self.typ = typ
        self.size = size
        self.data = {}
    def set_property(self, key, val):
        """Adds a property to the current section.

        Arguments:
            key {str} -- the name of the key
            val {str} -- the value associated with the key
        """
        self.data[key] = val
    def get_property(self, key):
        """Gets the value associated with the key.

        Arguments:
            key {str} -- the string representing the key

        Raises:
            KeyError -- if the key doesn't exist

        Returns:
            str -- the value of the key
        """
        return self.data[key]

class DMIParser:
    def count_tabs(self, string):
        """Counts the number of the tabs in the beginning of the passed string.

        Arguments:
            string {str} -- the string to be processed

        Returns:
            int -- the number of the tabs
        """
        i = 0
        while i < len(string) and string[i] == '\t':
            i = i + 1
        return i
        
    def parse_handle(self, handle):
        """Parses the line preceding each section which contains the handle, the type and the size.
        
        Assumption:
            The handle is in the form "Handle {handle}, DMI type {type}, {size} bytes"

        Arguments:
            handle {str} -- the string representing the handle

        Returns:
            list -- The parsed data in the form [handle, type, size]
        """
        return [x.strip() for x in handle.replace('Handle', '').replace('DMI type', '').replace('bytes', '').split(', ')]

    def parse_dmi(self, string):
        """Parses the string which should be a result of the running the command dmidecode

        Assumptions:
            The string is formatted in the given way:
                
                The first few lines are a description that is ignored.
               
                The beginning of the data part is preceded by the first blank lines in the string.
               
                Each section starts with an unindented line which contains the handle, type and size.
                
                The second line of the section is unindented and represents the name of the section
                
                The rest of the section is in the form: "key: val"
                
                The line containing the key is indented by 1 tab.
                
                val mught span multiple lines but the indentation of those lines (except the one containing key) is 2 tabs
                
                The sections is separated by a blank line
        Returns:
            dict -- dictionary of sections contained in the string
        """
        DMIData = {}
        last_open_section = ""
        variable_data = ""
        variable_name = ""
        data_start = string.find('\n\n') + 2
        for line in string[data_start:].split('\n'):
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
