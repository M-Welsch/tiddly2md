from pathlib import Path


rename_dict = {
    "mosfet": "mosfet driver"
}

manufacturer_dict = {
    "AD": "Analog Devices",
    "LT": "Analog Devices",
    "LTC": "Analog Devices",
    "NE": "Texas Instruments",
    "we": "Wuerth Elektronik",
    "mcp": "Microchip",
    "atmega": "Microchip",
    "kem": "Kemet",
    "lm": "Texas Instruments",
    "irf": "International Rectifier",
    "infineon": "Infineon"
}


def create_md_file(datasheet: Path):
    prefix = datasheet.stem.split('_')[0]
    if prefix in rename_dict.keys():
        prefix = rename_dict[prefix]
    mf = ""
    for manufacturer in manufacturer_dict.keys():
        if manufacturer.lower() in datasheet.stem.lower():
            mf = manufacturer_dict[manufacturer]
            break
    content = ["---", f"hersteller: {mf}", f"bauteilart: {prefix}", "up: Datenblaetter", "---", "", f"[[{datasheet.stem}.pdf]]", f"![[{datasheet.stem}.pdf]]"]
    with open(datasheet.stem+'.md', 'w') as f:
        f.write('\n'.join(content))


if __name__ == "__main__":
    for datasheet in Path.cwd().glob("*.pdf"):
        create_md_file(datasheet)
