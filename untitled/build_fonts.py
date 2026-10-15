import sys
from fontTools.ttLib import TTFont
from fontTools.ttLib.ttCollection import TTCollection

# 1. Read input files from command line arguments using sys.argv
if len(sys.argv) < 3:
    print("\nUsage: python build_fonts.py <Regular_Font.ttf> <Bold_Font.ttf>")
    print("Example: python build_fonts.py UntitledRegular.ttf UntitledBold.ttf\n")
    sys.exit(1)

REGULAR_IN = sys.argv[1]
BOLD_IN = sys.argv[2]

# Standardized output targets
REGULAR_OUT = "UntitledRegular.ttf"
BOLD_OUT = "UntitledBold.ttf"
TTC_OUT = "Untitled.ttc"
VERSION_STRING = f"Version {sys.argv[3]}"  # Standard format expected by OS font managers

def fix_font_metadata(file_path, is_bold=False):
    font = TTFont(file_path)
    name_table = font['name']
    
    family_name = "Untitled"
    subfamily = "Bold" if is_bold else "Regular"
    ps_name = f"{family_name}{subfamily}"
    full_name = f"{family_name} {subfamily}"
    unique_id = f": {family_name} {subfamily}"
    
    target_strings = {
        1: family_name,     # Family Name
        2: subfamily,       # Subfamily Name
        3: unique_id,       # Unique ID
        4: full_name,       # Full Name
        5: VERSION_STRING,  # Font Version
        6: ps_name          # PostScript Name
    }
    
    for name_id, text_value in target_strings.items():
        name_table.names = [n for n in name_table.names if n.nameID != name_id]
        name_table.setName(text_value, name_id, platformID=3, platEncID=1, langID=1033)
        name_table.setName(text_value, name_id, platformID=1, platEncID=0, langID=0)

    os2_table = font['OS/2']
    head_table = font['head']
    
    # Keep the font's internal revision number synchronized if it's a decimal
    try:
        head_table.fontRevision = float(sys.argv[3])
    except ValueError:
        pass  # If version is e.g. "1.0.0-beta", skip head revision updating since it requires a float

    if is_bold:
        os2_table.usWeightClass = 700      
        os2_table.fsSelection |= (1 << 5)  
        os2_table.fsSelection &= ~(1 << 6) 
        head_table.macStyle |= (1 << 0)    
    else:
        os2_table.usWeightClass = 400      
        os2_table.fsSelection |= (1 << 6)  
        os2_table.fsSelection &= ~(1 << 5) 
        head_table.macStyle &= ~(1 << 0)  

    return font

def main():
    print(f"Parsing and patching metadata for: {REGULAR_IN} & {BOLD_IN}...")
    reg_font = fix_font_metadata(REGULAR_IN, is_bold=False)
    bold_font = fix_font_metadata(BOLD_IN, is_bold=True)
    
    # Save optimized independent TTFs
    reg_font.save(REGULAR_OUT)
    bold_font.save(BOLD_OUT)
    print(f" ✔ Saved Web Asset: {REGULAR_OUT}")
    print(f" ✔ Saved Web Asset: {BOLD_OUT}")
    
    # Bundle matching binaries into the desktop TTC package
    print("Compiling directly into TTC container...")
    ttc_source_reg = TTFont(REGULAR_OUT)
    ttc_source_bold = TTFont(BOLD_OUT)
    
    ttc = TTCollection()
    ttc.fonts = [ttc_source_reg, ttc_source_bold]
    ttc.save(TTC_OUT)
    
    print(f" ✔ Saved Desktop Collection: {TTC_OUT}")
    print("\nAll assets compiled successfully!")

if __name__ == "__main__":
    main()