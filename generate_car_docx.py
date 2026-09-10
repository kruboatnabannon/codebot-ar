# -*- coding: utf-8 -*-
import zipfile, io, os, html

def esc(text):
    if text is None:
        return ""
    return html.escape(str(text))

def make_p(runs, align="left", space_before=100, space_after=100, line_spacing=276, bullet=False):
    """
    runs is a list of tuples: (text, bold, italic, size, color)
    size in half-points (e.g. 32 = 16pt, 36 = 18pt)
    """
    p_props = [f'<w:jc w:val="{align}"/>']
    p_props.append(f'<w:spacing w:before="{space_before}" w:after="{space_after}" w:line="{line_spacing}" w:lineRule="auto"/>')
    
    if bullet:
        p_props.append('<w:pPrChange><w:pPr/></w:pPrChange>')
        p_props.append('<w:ind w:left="480" w:hanging="240"/>')

    runs_xml = []
    if bullet:
        runs_xml.append('''<w:r><w:rPr><w:rFonts w:ascii="TH Sarabun PSK" w:hAnsi="TH Sarabun PSK" w:cs="TH Sarabun PSK"/><w:sz w:val="32"/><w:szCs w:val="32"/></w:rPr><w:t>• </w:t></w:r>''')

    for item in runs:
        if isinstance(item, str):
            t = item
            b = False
            i = False
            sz = 32
            c = "000000"
        else:
            t = item[0]
            b = item[1] if len(item) > 1 else False
            i = item[2] if len(item) > 2 else False
            sz = item[3] if len(item) > 3 else 32
            c = item[4] if len(item) > 4 else "000000"
        
        r_pr = ['<w:rFonts w:ascii="TH Sarabun PSK" w:hAnsi="TH Sarabun PSK" w:cs="TH Sarabun PSK"/>']
        if b:
            r_pr.append('<w:b/><w:bCs/>')
        if i:
            r_pr.append('<w:i/><w:iCs/>')
        r_pr.append(f'<w:sz w:val="{sz}"/>')
        r_pr.append(f'<w:szCs w:val="{sz}"/>')
        if c and c != "000000":
            r_pr.append(f'<w:color w:val="{c}"/>')
        
        runs_xml.append(f'<w:r><w:rPr>{"".join(r_pr)}</w:rPr><w:t xml:space="preserve">{esc(t)}</w:t></w:r>')

    return f'<w:p><w:pPr>{"".join(p_props)}</w:pPr>{"".join(runs_xml)}</w:p>'

def make_callout(text, title=None):
    runs = []
    if title:
        runs.append((f"{title}\n", True, False, 30, "1E3A8A"))
    runs.append((text, False, False, 30, "333333"))
    
    p_pr = '''<w:pPr>
        <w:pBdr>
            <w:left w:val="single" w:sz="24" w:space="15" w:color="1E3A8A"/>
        </w:pBdr>
        <w:shd w:val="clear" w:color="auto" w:fill="F0F4F8"/>
        <w:ind w:left="360" w:right="360"/>
        <w:spacing w:before="160" w:after="160" w:line="260" w:lineRule="auto"/>
    </w:pPr>'''
    
    r_xml = []
    for item in runs:
        r_xml.append(f'''<w:r>
            <w:rPr>
                <w:rFonts w:ascii="TH Sarabun PSK" w:hAnsi="TH Sarabun PSK" w:cs="TH Sarabun PSK"/>
                {"<w:b/><w:bCs/>" if item[1] else ""}
                <w:sz w:val="{item[3]}"/>
                <w:szCs w:val="{item[3]}"/>
                <w:color w:val="{item[4]}"/>
            </w:rPr>
            <w:t xml:space="preserve">{esc(item[0])}</w:t>
        </w:r>''')
    return f'<w:p>{p_pr}{"".join(r_xml)}</w:p>'

def make_table(headers, rows, col_widths, alignments=None):
    """
    col_widths: list of int in dxa (total around 9000 dxa for A4)
    alignments: list of "left", "center", "right"
    """
    total_w = sum(col_widths)
    if alignments is None:
        alignments = ["center"] * len(headers)
        
    xml = ['<w:tbl>',
           f'''<w:tblPr>
               <w:tblW w:w="{total_w}" w:type="dxa"/>
               <w:tblInd w:w="0" w:type="dxa"/>
               <w:tblBorders>
                   <w:top w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/>
                   <w:left w:val="none"/>
                   <w:bottom w:val="single" w:sz="12" w:space="0" w:color="1E3A8A"/>
                   <w:right w:val="none"/>
                   <w:insideH w:val="single" w:sz="4" w:space="0" w:color="E5E7EB"/>
                   <w:insideV w:val="none"/>
               </w:tblBorders>
               <w:tblCellMar>
                   <w:top w:w="120" w:type="dxa"/>
                   <w:left w:w="160" w:type="dxa"/>
                   <w:bottom w:w="120" w:type="dxa"/>
                   <w:right w:w="160" w:type="dxa"/>
               </w:tblCellMar>
           </w:tblPr>''']
    
    # Grid
    xml.append('<w:tblGrid>')
    for w in col_widths:
        xml.append(f'<w:gridCol w:w="{w}"/>')
    xml.append('</w:tblGrid>')

    # Header Row
    xml.append('<w:tr><w:trPr><w:tblHeader/></w:trPr>')
    for i, h in enumerate(headers):
        w = col_widths[i]
        al = alignments[i] if i < len(alignments) else "center"
        xml.append(f'''<w:tc>
            <w:tcPr>
                <w:tcW w:w="{w}" w:type="dxa"/>
                <w:shd w:val="clear" w:color="auto" w:fill="1E3A8A"/>
                <w:vAlign w:val="center"/>
            </w:tcPr>
            <w:p>
                <w:pPr>
                    <w:jc w:val="{al}"/>
                    <w:spacing w:before="80" w:after="80"/>
                </w:pPr>
                <w:r>
                    <w:rPr>
                        <w:rFonts w:ascii="TH Sarabun PSK" w:hAnsi="TH Sarabun PSK" w:cs="TH Sarabun PSK"/>
                        <w:b/><w:bCs/>
                        <w:sz w:val="28"/>
                        <w:szCs w:val="28"/>
                        <w:color w:val="FFFFFF"/>
                    </w:rPr>
                    <w:t xml:space="preserve">{esc(h)}</w:t>
                </w:r>
            </w:p>
        </w:tc>''')
    xml.append('</w:tr>')

    # Data Rows
    for r_idx, row in enumerate(rows):
        bg = "F9FAFB" if r_idx % 2 == 1 else "FFFFFF"
        xml.append('<w:tr>')
        for c_idx, val in enumerate(row):
            w = col_widths[c_idx]
            al = alignments[c_idx] if c_idx < len(alignments) else "left"
            is_bold = (r_idx >= len(rows) - 2 and ("รวม" in str(row[0]) or "เฉลี่ย" in str(row[0])))
            text_color = "1E3A8A" if is_bold else "111827"
            
            xml.append(f'''<w:tc>
                <w:tcPr>
                    <w:tcW w:w="{w}" w:type="dxa"/>
                    <w:shd w:val="clear" w:color="auto" w:fill="{bg}"/>
                    <w:vAlign w:val="center"/>
                </w:tcPr>
                <w:p>
                    <w:pPr>
                        <w:jc w:val="{al}"/>
                        <w:spacing w:before="60" w:after="60"/>
                    </w:pPr>
                    <w:r>
                        <w:rPr>
                            <w:rFonts w:ascii="TH Sarabun PSK" w:hAnsi="TH Sarabun PSK" w:cs="TH Sarabun PSK"/>
                            {"<w:b/><w:bCs/>" if is_bold else ""}
                            <w:sz w:val="28"/>
                            <w:szCs w:val="28"/>
                            <w:color w:val="{text_color}"/>
                        </w:rPr>
                        <w:t xml:space="preserve">{esc(str(val))}</w:t>
                    </w:r>
                </w:p>
            </w:tc>''')
        xml.append('</w:tr>')

    xml.append('</w:tbl>')
    return "".join(xml)

print("Helper definitions loaded successfully.")
