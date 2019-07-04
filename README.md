DMIdecode parser
================

This is a project to parse the result of the linux command dmidecode.

Sample Usage
============

```python
import decoder
sample = """# dmidecode 3.1
Getting SMBIOS data from sysfs.
SMBIOS 2.7 present.
80 structures occupying 3244 bytes.
Table at 0x000E68F0.

Handle 0xDA02, DMI type 219, 11 bytes
OEM-specific Type
\tHeader and Data:
\t\tDB 0B 02 DA 02 01 02 03 FF 04 05
\tStrings:
\t\t00h
\t\t00h
\t\t00h
\t\t00h
\t\t00h"""

result = decoder.DMIParser().parse_dmi(sample)
print(result["OEM-specific Type"].handle) # 0xDA02
print(result["OEM-specific Type"].data["Header and Data"]) # DB 0B 02 DA 02 01 02 03 FF 04 05
```
