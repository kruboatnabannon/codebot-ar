# -*- coding: utf-8 -*-
import zipfile, io, os, html

def esc(text):
    if text is None: return ""
    return html.escape(str(text))

def make_page_break():
    return '<w:p><w:r><w:br w:type="page"/></w:r></w:p>'

def make_p(runs, align="left", space_before=60, space_after=60, line_spacing=260, bullet=False):
    p_props = [f'<w:jc w:val="{align}"/>']
    p_props.append(f'<w:spacing w:before="{space_before}" w:after="{space_after}" w:line="{line_spacing}" w:lineRule="auto"/>')
    if bullet:
        p_props.append('<w:ind w:left="480" w:hanging="240"/>')

    runs_xml = []
    if bullet:
        runs_xml.append('''<w:r><w:rPr><w:rFonts w:ascii="TH Sarabun PSK" w:hAnsi="TH Sarabun PSK" w:cs="TH Sarabun PSK"/><w:sz w:val="28"/><w:szCs w:val="28"/></w:rPr><w:t>• </w:t></w:r>''')

    for item in runs:
        if isinstance(item, str):
            t, b, i, sz, c = item, False, False, 28, "000000"
        else:
            t = item[0]
            b = item[1] if len(item) > 1 else False
            i = item[2] if len(item) > 2 else False
            sz = item[3] if len(item) > 3 else 28
            c = item[4] if len(item) > 4 else "000000"
        
        r_pr = ['<w:rFonts w:ascii="TH Sarabun PSK" w:hAnsi="TH Sarabun PSK" w:cs="TH Sarabun PSK"/>']
        if b: r_pr.append('<w:b/><w:bCs/>')
        if i: r_pr.append('<w:i/><w:iCs/>')
        r_pr.append(f'<w:sz w:val="{sz}"/><w:szCs w:val="{sz}"/>')
        if c and c != "000000": r_pr.append(f'<w:color w:val="{c}"/>')
        runs_xml.append(f'<w:r><w:rPr>{"".join(r_pr)}</w:rPr><w:t xml:space="preserve">{esc(t)}</w:t></w:r>')
    return f'<w:p><w:pPr>{"".join(p_props)}</w:pPr>{"".join(runs_xml)}</w:p>'

def make_callout(text, title=None, bg="F1F5F9", bdr="1E3A8A"):
    p_pr = f'''<w:pPr>
        <w:pBdr><w:left w:val="single" w:sz="24" w:space="15" w:color="{bdr}"/></w:pBdr>
        <w:shd w:val="clear" w:color="auto" w:fill="{bg}"/>
        <w:ind w:left="360" w:right="360"/>
        <w:spacing w:before="100" w:after="100" w:line="240" w:lineRule="auto"/>
    </w:pPr>'''
    runs_xml = []
    if title:
        runs_xml.append(f'''<w:r><w:rPr><w:rFonts w:ascii="TH Sarabun PSK" w:hAnsi="TH Sarabun PSK" w:cs="TH Sarabun PSK"/><w:b/><w:bCs/><w:sz w:val="28"/><w:szCs w:val="28"/><w:color w:val="{bdr}"/></w:rPr><w:t xml:space="preserve">{esc(title)}&#10;</w:t></w:r>''')
    
    text_escaped = esc(text).replace("\n", '</w:t></w:r></w:p><w:p>' + p_pr + '<w:r><w:rPr><w:rFonts w:ascii="TH Sarabun PSK" w:hAnsi="TH Sarabun PSK" w:cs="TH Sarabun PSK"/><w:sz w:val="26"/><w:szCs w:val="26"/><w:color w:val="333333"/></w:rPr><w:t xml:space="preserve">')
    runs_xml.append(f'''<w:r><w:rPr><w:rFonts w:ascii="TH Sarabun PSK" w:hAnsi="TH Sarabun PSK" w:cs="TH Sarabun PSK"/><w:sz w:val="26"/><w:szCs w:val="26"/><w:color w:val="333333"/></w:rPr><w:t xml:space="preserve">{text_escaped}</w:t></w:r>''')
    return f'<w:p>{p_pr}{"".join(runs_xml)}</w:p>'

def make_table(headers, rows, col_widths, alignments=None, font_size=24, header_bg="1E3A8A"):
    total_w = sum(col_widths)
    if alignments is None: alignments = ["center"] * len(headers)
    xml = ['<w:tbl>',
           f'''<w:tblPr>
               <w:tblW w:w="{total_w}" w:type="dxa"/><w:tblInd w:w="0" w:type="dxa"/>
               <w:tblBorders>
                   <w:top w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>
                   <w:left w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>
                   <w:bottom w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>
                   <w:right w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>
                   <w:insideH w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/>
                   <w:insideV w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/>
               </w:tblBorders>
               <w:tblCellMar><w:top w:w="60" w:type="dxa"/><w:left w:w="100" w:type="dxa"/><w:bottom w:w="60" w:type="dxa"/><w:right w:w="100" w:type="dxa"/></w:tblCellMar>
           </w:tblPr>''',
           '<w:tblGrid>']
    for w in col_widths: xml.append(f'<w:gridCol w:w="{w}"/>')
    xml.append('</w:tblGrid>')
    # Header
    xml.append('<w:tr><w:trPr><w:tblHeader/><w:trHeight w:val="280" w:hRule="atLeast"/></w:trPr>')
    for i, h in enumerate(headers):
        al = alignments[i] if i < len(alignments) else "center"
        xml.append(f'''<w:tc><w:tcPr><w:tcW w:w="{col_widths[i]}" w:type="dxa"/><w:shd w:val="clear" w:color="auto" w:fill="{header_bg}"/><w:vAlign w:val="center"/></w:tcPr>
            <w:p><w:pPr><w:jc w:val="{al}"/><w:spacing w:before="30" w:after="30" w:line="210" w:lineRule="auto"/></w:pPr>
            <w:r><w:rPr><w:rFonts w:ascii="TH Sarabun PSK" w:hAnsi="TH Sarabun PSK" w:cs="TH Sarabun PSK"/><w:b/><w:bCs/><w:sz w:val="{font_size}"/><w:szCs w:val="{font_size}"/><w:color w:val="FFFFFF"/></w:rPr><w:t xml:space="preserve">{esc(h)}</w:t></w:r></w:p></w:tc>''')
    xml.append('</w:tr>')
    for row in rows:
        xml.append('<w:tr><w:trPr><w:trHeight w:val="280" w:hRule="atLeast"/></w:trPr>')
        for i, val in enumerate(row):
            al = alignments[i] if i < len(alignments) else "left"
            val_escaped = esc(val).replace("\n", '</w:t></w:r></w:p><w:p><w:pPr><w:jc w:val="' + al + '"/><w:spacing w:before="20" w:after="20" w:line="210" w:lineRule="auto"/></w:pPr><w:r><w:rPr><w:rFonts w:ascii="TH Sarabun PSK" w:hAnsi="TH Sarabun PSK" w:cs="TH Sarabun PSK"/><w:sz w:val="' + str(font_size) + '"/><w:szCs w:val="' + str(font_size) + '"/><w:color w:val="1E293B"/></w:rPr><w:t xml:space="preserve">')
            xml.append(f'''<w:tc><w:tcPr><w:tcW w:w="{col_widths[i]}" w:type="dxa"/><w:vAlign w:val="center"/></w:tcPr>
                <w:p><w:pPr><w:jc w:val="{al}"/><w:spacing w:before="20" w:after="20" w:line="210" w:lineRule="auto"/></w:pPr>
                <w:r><w:rPr><w:rFonts w:ascii="TH Sarabun PSK" w:hAnsi="TH Sarabun PSK" w:cs="TH Sarabun PSK"/><w:sz w:val="{font_size}"/><w:szCs w:val="{font_size}"/><w:color w:val="1E293B"/></w:rPr><w:t xml:space="preserve">{val_escaped}</w:t></w:r></w:p></w:tc>''')
        xml.append('</w:tr>')
    xml.append('</w:tbl>')
    return "".join(xml)

def heading_1(text):
    return make_p([(text, True, False, 30, "1E3A8A")], align="left", space_before=140, space_after=40)

def heading_2(text):
    return make_p([(text, True, False, 28, "0369A1")], align="left", space_before=100, space_after=30)

def heading_3(text):
    return make_p([(text, True, False, 26, "1F2937")], align="left", space_before=60, space_after=20)

def body_text(text, bold_prefix=None, bullet=False):
    runs = []
    if bold_prefix:
        runs.append((bold_prefix, True, False, 26, "1E293B"))
    runs.append((text, False, False, 26, "334155"))
    return make_p(runs, align="left", space_before=20, space_after=20, line_spacing=240, bullet=bullet)

print("Base XML functions initialized")
