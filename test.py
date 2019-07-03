import pytest
import decoder
def test_parse_handle():
    o = decoder.DMIParser()
    assert o.parse_handle("Handle 0x1234, DMI type 13, 244 bytes") == ["0x1234", "13", "244"], "Couldn't parse handle"

def test_parse_dmi():
    o = decoder.DMIParser().parse_dmi("""# dmidecode 3.1
Getting SMBIOS data from sysfs.
SMBIOS 2.7 present.
80 structures occupying 3244 bytes.
Table at 0x000E68F0.

Handle 0x0000, DMI type 0, 24 bytes
BIOS Information
\tVendor: Dell Inc.
\tVersion: A14
\tRelease Date: 05/13/2013
\tAddress: 0xE0000
\tRuntime Size: 128 kB
\tROM Size: 4608 kB
\tCharacteristics:
\t\tPCI is supported
\t\tPNP is supported
\t\tBIOS is upgradeable
\t\tBIOS shadowing is allowed
\t\tBoot from CD is supported
\t\tSelectable boot is supported
\t\tEDD is supported
\t\tJapanese floppy for NEC 9800 1.2 MB is supported (int 13h)
\t\tJapanese floppy for Toshiba 1.2 MB is supported (int 13h)
\t\t5.25"/360 kB floppy services are supported (int 13h)
\t\t5.25"/1.2 MB floppy services are supported (int 13h)
\t\t3.5"/720 kB floppy services are supported (int 13h)
\t\t3.5"/2.88 MB floppy services are supported (int 13h)
\t\tPrint screen service is supported (int 5h)
\t\t8042 keyboard services are supported (int 9h)
\t\tSerial services are supported (int 14h)
\t\tPrinter services are supported (int 17h)
\t\tCGA/mono video services are supported (int 10h)
\t\tACPI is supported
\t\tUSB legacy is supported)""")
    import json
    print(json.dumps(o, default=lambda o: o.__dict__, indent=2))
    assert len(o) == 1, "length is not calculated right"
    assert o["BIOS Information"].handle == '0x0000', "hand;e is wrong"
    assert o["BIOS Information"].typ == '0', "type is wrong"
    assert o["BIOS Information"].size == '24', "size is wrong"
    assert o["BIOS Information"].get_property('Vendor') == 'Dell Inc.', "Vendor is wrong"
    assert o["BIOS Information"].get_property('Characteristics') == """PCI is supported
PNP is supported
BIOS is upgradeable
BIOS shadowing is allowed
Boot from CD is supported
Selectable boot is supported
EDD is supported
Japanese floppy for NEC 9800 1.2 MB is supported (int 13h)
Japanese floppy for Toshiba 1.2 MB is supported (int 13h)
5.25"/360 kB floppy services are supported (int 13h)
5.25"/1.2 MB floppy services are supported (int 13h)
3.5"/720 kB floppy services are supported (int 13h)
3.5"/2.88 MB floppy services are supported (int 13h)
Print screen service is supported (int 5h)
8042 keyboard services are supported (int 9h)
Serial services are supported (int 14h)
Printer services are supported (int 17h)
CGA/mono video services are supported (int 10h)
ACPI is supported
USB legacy is supported)""", "Characteristics is wrong"
