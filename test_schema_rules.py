# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import re

PPR_ORDER = [
    "pStyle", "keepNext", "keepLines", "pageBreakBefore", "framePr", "widowControl",
    "numPr", "pBdr", "shd", "tabs", "suppressAutoHyphens", "kinsoku", "wordWrap",
    "overflowPunct", "topLinePunct", "autoSpaceDE", "autoSpaceDN", "bidi",
    "adjustRightInd", "snapToGrid", "spacing", "ind", "contextualSpacing",
    "mirrorIndents", "suppressOverlap", "jc", "textDirection", "textAlignment",
    "textboxTightWrap", "outlineLvl", "divId", "cnfStyle", "rPr", "sectPr", "pPrChange"
]

RPR_ORDER = [
    "rStyle", "rFonts", "b", "bCs", "i", "iCs", "caps", "smallCaps", "strike", "dstrike",
    "outline", "shadow", "emboss", "imprint", "noProof", "snapToGrid", "vanish",
    "webHidden", "color", "spacing", "w", "kern", "position", "sz", "szCs", "highlight",
    "u", "effect", "bdr", "shd", "fitText", "vertAlign", "rtl", "cs", "em", "lang"
]

def validate_docx_xml(xml_bytes):
    # 1. Check XML declaration
    assert xml_bytes.startswith(b'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'), "Missing or invalid XML declaration"
    
    # 2. Check XML well-formedness
    root = ET.fromstring(xml_bytes)
    
    xml_str = xml_bytes.decode("utf-8")
    
    # 3. Check mc:Ignorable
    m = re.search(r'mc:Ignorable="([^"]+)"', xml_str)
    if m:
        for p in m.group(1).split():
            assert f'xmlns:{p}=' in xml_str, f"Undeclared prefix '{p}' in mc:Ignorable!"
            
    # 4. Check pPr child order
    pPr_matches = re.finditer(r'<w:pPr>(.*?)</w:pPr>', xml_str)
    for idx, match in enumerate(pPr_matches):
        content = match.group(1)
        tags = re.findall(r'<w:([a-zA-Z0-9]+)[\s/>]', content)
        last_pos = -1
        for tag in tags:
            if tag in PPR_ORDER:
                curr_pos = PPR_ORDER.index(tag)
                if curr_pos < last_pos:
                    raise AssertionError(f"pPr #{idx} order violation: '{tag}' (pos {curr_pos}) appears after tag at pos {last_pos} in: {content}")
                last_pos = curr_pos

    # 5. Check rPr child order
    rPr_matches = re.finditer(r'<w:rPr>(.*?)</w:rPr>', xml_str)
    for idx, match in enumerate(rPr_matches):
        content = match.group(1)
        tags = re.findall(r'<w:([a-zA-Z0-9]+)[\s/>]', content)
        last_pos = -1
        for tag in tags:
            if tag in RPR_ORDER:
                curr_pos = RPR_ORDER.index(tag)
                if curr_pos < last_pos:
                    raise AssertionError(f"rPr #{idx} order violation: '{tag}' (pos {curr_pos}) appears after tag at pos {last_pos} in: {content}")
                last_pos = curr_pos

    print("All schema validation checks PASSED perfectly!")
    return True

if __name__ == "__main__":
    import zipfile
    with zipfile.ZipFile("แบบข้อตกลงในการพัฒนางาน 69_backup.docx", "r") as z:
        validate_docx_xml(z.read("word/document.xml"))
