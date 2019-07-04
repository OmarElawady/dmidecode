import pytest
import decoder
@pytest.fixture
def parse():
    return decoder.DMIParser().parse_dmi("""# dmidecode 3.1
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
\t\tUSB legacy is supported)

Handle 0xDA02, DMI type 219, 11 bytes
OEM-specific Type
\tHeader and Data:
\t\tDB 0B 02 DA 02 01 02 03 FF 04 05
\tStrings:
\t\t00h
\t\t00h
\t\t00h
\t\t00h
\t\t00h
""")

def test_parse_handle():
    o = decoder.DMIParser()
    assert o.parse_handle("Handle 0x1234, DMI type 13, 244 bytes") == ["0x1234", "13", "244"], "Couldn't parse handle"

def test_parse_props(parse):
    assert parse["BIOS Information"].handle == '0x0000', "handle for BIOS is wrong"
    assert parse["BIOS Information"].typ == '0', "type for BIOS is wrong"
    assert parse["BIOS Information"].size == '24', "size for BIOS is wrong"
    assert parse["OEM-specific Type"].handle == "0xDA02", "handle for OEM is wrong"
    assert parse["OEM-specific Type"].typ == "219", "handle for OEM is wrong"
    assert parse["OEM-specific Type"].size == "11", "handle for OEM is wrong"

def test_parse_data_single(parse):
    assert parse["BIOS Information"].data["Vendor"] == 'Dell Inc.', "handle for BIOS is wrong"
    assert parse["BIOS Information"].data["Version"] == "A14", "Version for BIOS is wrong"
    assert parse["BIOS Information"].data["Release Date"] == "05/13/2013", "!!BIOS's Release Data"
    assert parse["BIOS Information"].data["Address"] == "0xE0000", "!!BIOS's Address"
    assert parse["BIOS Information"].data["Runtime Size"] == "128 kB","!!BIOS's runtime size"
    assert parse["BIOS Information"].data["ROM Size"] == "4608 kB", "!!BIOS's ROM size"
    assert parse["OEM-specific Type"].data["Header and Data"] == "DB 0B 02 DA 02 01 02 03 FF 04 05", "!!OEM's header and data"

def test_parse_multiline_data(parse):
    assert parse["BIOS Information"].data["Characteristics"] == """PCI is supported
PNP is supported
BIOS is upgradeable
BIOS shadowing is allowed
Boot from CD is supported
Selectable boot is supported
EDD is supported
Japanese floppy for NEC 9800 1.2 MB is supported (int 13h)
Japanese floppy for Toshiba 1.2 MB is supported (int 13h)
5.25\"/360 kB floppy services are supported (int 13h)
5.25\"/1.2 MB floppy services are supported (int 13h)
3.5\"/720 kB floppy services are supported (int 13h)
3.5\"/2.88 MB floppy services are supported (int 13h)
Print screen service is supported (int 5h)
8042 keyboard services are supported (int 9h)
Serial services are supported (int 14h)
Printer services are supported (int 17h)
CGA/mono video services are supported (int 10h)
ACPI is supported
USB legacy is supported)""", "!!BIOS's Characteristics"
    assert parse["OEM-specific Type"].data["Strings"] == """00h
00h
00h
00h
00h""", "!!OEM strings"
