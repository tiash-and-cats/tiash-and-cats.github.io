import sys
import os
from PIL import Image
from fontTools.ttLib import TTFont
from fontTools.ttLib.ttCollection import TTCollection
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen

# 1. Parameter Validation
if len(sys.argv) < 4:
    print("\nUsage: python build_pixel_font_collection.py <Regular_Sheet.png> <Bold_Sheet.png> <Version>")
    print("Example: python build_pixel_font_collection.py reg.png bold.png 1.1\n")
    sys.exit(1)

REGULAR_IN_SHEET = sys.argv[1]
BOLD_IN_SHEET = sys.argv[2]
VERSION_INPUT = sys.argv[3]
VERSION_STRING = f"Version {VERSION_INPUT}"

REGULAR_OUT = "UntitledRegular.ttf"
BOLD_OUT = "UntitledBold.ttf"
TTC_OUT = "Untitled.ttc"

# Definitive 3-row x 36-column layout structure from your specifications
LAYOUT = [
    list("ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"),
    list("abcdefghijklmnopqrstuvwxyz?!#*/+-._"),
    list('$%^<>()[]{}=\\,\'":;`|')
]

def trace_character_to_pen(cell, char_w, char_h, pixel_scale):
    """
    Traces raster pixels into vector paths using horizontal span optimization.
    Paths are explicitly drawn counter-clockwise for standard TrueType rendering.
    """
    pen = TTGlyphPen(None)
    
    for y in range(char_h):
        in_span = False
        span_start = 0
        
        ttf_y1 = (char_h - 1 - y) * pixel_scale
        ttf_y2 = (char_h - y) * pixel_scale
        
        for x in range(char_w):
            r, g, b, a = cell.getpixel((x, y))[:4]
            is_solid = (r < 128 and g < 128 and b < 128)
            
            if is_solid and not in_span:
                in_span = True
                span_start = x
            elif not is_solid and in_span:
                ttf_x1 = span_start * pixel_scale
                ttf_x2 = x * pixel_scale
                
                # Counter-Clockwise Winding: Bottom-Left -> Bottom-Right -> Top-Right -> Top-Left
                pen.moveTo((ttf_x1, ttf_y1))
                pen.lineTo((ttf_x2, ttf_y1))
                pen.lineTo((ttf_x2, ttf_y2))
                pen.lineTo((ttf_x1, ttf_y2))
                pen.closePath()
                in_span = False
                
        if in_span:
            ttf_x1 = span_start * pixel_scale
            ttf_x2 = char_w * pixel_scale
            
            pen.moveTo((ttf_x1, ttf_y1))
            pen.lineTo((ttf_x2, ttf_y1))
            pen.lineTo((ttf_x2, ttf_y2))
            pen.lineTo((ttf_x1, ttf_y2))
            pen.closePath()
            
    return pen.glyph()

def generate_vector_font_object(spritesheet_path, is_bold=False):
    if not os.path.exists(spritesheet_path):
        print(f"Error: Spritesheet path missing: {spritesheet_path}")
        sys.exit(1)
        
    img = Image.open(spritesheet_path).convert("RGBA")
    char_w = img.width // 36
    char_h = img.height // 3
    
    # Force the explicit Em Box Size to 1000 matching Image 1
    units_per_em = 1000
    pixel_scale = units_per_em // char_h
    
    metrics = {}
    glyphs = {}
    cmap = {}
    
    # Required missing glyph fallback (.notdef) metric setup
    metrics[".notdef"] = (char_w * pixel_scale, 0)
    notdef_pen = TTGlyphPen(None)
    notdef_pen.moveTo((0, 0))
    notdef_pen.lineTo((char_w * pixel_scale, 0))
    notdef_pen.lineTo((char_w * pixel_scale, char_h * pixel_scale))
    notdef_pen.lineTo((0, char_h * pixel_scale))
    notdef_pen.closePath()
    glyphs[".notdef"] = notdef_pen.glyph()

    # Empty vector box for the standard 'Space' glyph (ASCII 32)
    metrics["space"] = (char_w * pixel_scale, 0)
    glyphs["space"] = TTGlyphPen(None).glyph()
    cmap[32] = "space"

    for row_idx, chars_list in enumerate(LAYOUT):
        for col_idx, char_char in enumerate(chars_list):
            unicode_val = ord(char_char)
            glyph_name = f"uni{unicode_val:04X}"
            cmap[unicode_val] = glyph_name
            
            left = col_idx * char_w
            top = row_idx * char_h
            cell_img = img.crop((left, top, left + char_w, top + char_h))
            
            glyphs[glyph_name] = trace_character_to_pen(cell_img, char_w, char_h, pixel_scale)
            metrics[glyph_name] = (char_w * pixel_scale, 0)

    # Initialize FontBuilder to write standard structures safely
    fb = FontBuilder(unitsPerEm=units_per_em, isTTF=True)
    fb.setupGlyphOrder(list(metrics.keys()))
    fb.setupGlyf(glyphs)
    fb.setupHorizontalMetrics(metrics)
    
    # Default baseline initialization setup (Will be fully hardcoded in Step 2)
    fb.setupHorizontalHeader(ascent=800, descent=-200)
    fb.setupCharacterMap(cmap)
    
    dummy_names = {"familyName": "Untitled", "styleName": "Regular"}
    fb.setupNameTable(dummy_names)
    fb.setupOS2(sTypoAscender=800, sTypoDescender=-200)
    fb.setupPost()
    
    return fb.font

def fix_font_metadata(font, is_bold=False):
    name_table = font['name']
    family_name = "Untitled"
    subfamily = "Bold" if is_bold else "Regular"
    ps_name = f"{family_name}{subfamily}"
    full_name = f"{family_name} {subfamily}"
    unique_id = f": {family_name} {subfamily}"
    copyright_string = (
        "Copyright (c) 2026, Ridwan Bin Mohammad Tiash "
        "(https://tiash.is-cool.dev), with Reserved Font Name Untitled."
    )
    license_description = (
        "This Font Software is licensed under the SIL Open Font License, "
        "Version 1.1. This license is available with a FAQ at: "
        "https://openfontlicense.org"
    )
    license_url = "https://openfontlicense.org"
    
    # 2. MATCH IMAGE 1 & IMAGE 2 (TTF Names Map)
    target_strings = {
        0: copyright_string,                  # Copyright Notice
        1: family_name,                       # Family Name
        2: subfamily,                         # Subfamily Name
        3: unique_id,                         # Unique ID
        4: full_name,                         # Full Name
        5: VERSION_STRING,                    # Font Version string ("Version 1.1")
        6: ps_name,                           # PostScript Name
        13: license_description,              # License Description Field
        14: license_url,                      # License Info URL
        16: family_name,                      # Preferred Family Name
        17: subfamily                         # Preferred Style Name
    }
    
    name_table.names = []
    for name_id, text_value in target_strings.items():
        # Write both Platform 3 (Windows) and Platform 1 (Macintosh) targets cleanly
        name_table.setName(text_value, name_id, platformID=3, platEncID=1, langID=1033)
        name_table.setName(text_value, name_id, platformID=1, platEncID=0, langID=0)

    os2_table = font['OS/2']
    hhea_table = font['hhea']
    head_table = font['head']

    # 3. MATCH IMAGE 4 (Strict OS/2 & hhea Metrics Metrics Overwrites)
    os2_table.usWinAscent = 1429
    os2_table.usWinDescent = 0
    os2_table.sTypoAscender = 1429
    os2_table.sTypoDescender = -1
    os2_table.sTypoLineGap = 0
    os2_table.sxHeight = 1224
    os2_table.sCapHeight = 1224 # Sets cap metrics synchronized to match
    
    hhea_table.ascent = 1429
    hhea_table.descent = -1
    hhea_table.lineGap = 0

    # Ensure Panose configurations match perfectly
    os2_table.panose.bFamilyType = 2       
    os2_table.panose.bSerifStyle = 11      
    os2_table.panose.bWeight = 8 if is_bold else 5  
    os2_table.panose.bProportion = 1       
    os2_table.panose.bContrast = 1         
    os2_table.panose.bStrokeVariation = 1  
    os2_table.panose.bArmStyle = 1         
    os2_table.panose.bLetterForm = 1       
    os2_table.panose.bMidline = 1          
    os2_table.panose.bXHeight = 1          
    
    try:
        head_table.fontRevision = float(VERSION_INPUT)
    except ValueError:
        head_table.fontRevision = 1.0

    if is_bold:
        os2_table.usWeightClass = 700      
        os2_table.fsSelection = 0x0020  
        head_table.macStyle = 0x0001    
    else:
        os2_table.usWeightClass = 400      
        os2_table.fsSelection = 0x0040  
        head_table.macStyle = 0x0000  

    return font

def main():
    print("1. Re-scaling grid units cleanly inside Em 1000 containers...")
    reg_font_obj = generate_vector_font_object(REGULAR_IN_SHEET, is_bold=False)
    bold_font_obj = generate_vector_font_object(BOLD_IN_SHEET, is_bold=True)
    
    print("2. Programmatically hardcoding FontForge window overrides...")
    reg_font = fix_font_metadata(reg_font_obj, is_bold=False)
    bold_font = fix_font_metadata(bold_font_obj, is_bold=True)
    
    reg_font.save(REGULAR_OUT)
    bold_font.save(BOLD_OUT)
    print(f" ✔ Saved Web Asset: {REGULAR_OUT}")
    print(f" ✔ Saved Web Asset: {BOLD_OUT}")
    
    print("3. Compiling binary components straight into Collection container...")
    ttc = TTCollection()
    ttc.fonts = [reg_font, bold_font]
    ttc.save(TTC_OUT)
    
    print(f" ✔ Saved Desktop Collection: {TTC_OUT}")
    print("\nAll systems matching FontForge parameters perfectly!")

if __name__ == "__main__":
    main()