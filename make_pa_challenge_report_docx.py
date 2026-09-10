# -*- coding: utf-8 -*-
"""
Challenging Issue Report Generator (ว.PA PA 2/ส ส่วนที่ 2)
Teacher: Techin Inthamol, Ban Non Pa Wan Chiang Hai School
Office: Nong Bua Lamphu Primary Educational Service Area Office 2
Academic Year: Semester 1, Academic Year 2569 (Fiscal Year 2569)

Title:
การพัฒนาทักษะการเรียนรู้รายวิชาเทคโนโลยี (วิทยาการคำนวณ) กลุ่มสาระการเรียนรู้วิทยาศาสตร์และเทคโนโลยี
โดยใช้กระบวนการ Gamebase learning ร่วมกับเทคนิคการสอนแบบ active learning
ของนักเรียนชั้นประถมศึกษาปีที่ 5 โรงเรียนบ้านโนนป่าหว้านเชียงฮาย
"""

import zipfile, io, os, html, subprocess, json

def esc(text):
    if text is None:
        return ""
    return html.escape(str(text))

_seg_cache = {}

def add_thai_breaks(text):
    if not text or not isinstance(text, str):
        return text
    if text in _seg_cache:
        return _seg_cache[text]
    has_thai = any('\u0e00' <= ch <= '\u0e7f' for ch in text)
    if not has_thai:
        _seg_cache[text] = text
        return text
    
    js_code = """
    const fs = require('fs');
    const seg = new Intl.Segmenter('th', { granularity: 'word' });
    const input = JSON.parse(fs.readFileSync(0, 'utf-8'));
    const segments = Array.from(seg.segment(input)).map(s => s.segment);
    let res = '';
    for (let i = 0; i < segments.length; i++) {
        res += segments[i];
        if (i < segments.length - 1) {
            const curr = segments[i];
            const next = segments[i + 1];
            if (!/\\s/.test(curr) && !/\\s/.test(next)) {
                if (/^[\\d.,]+$/.test(curr) && /^[\\d.,]+$/.test(next)) {
                    // number
                } else if (/^[0-9]+$/.test(curr) && next === '.') {
                    // 1.
                } else {
                    res += '\\u200b';
                }
            }
        }
    }
    process.stdout.write(JSON.stringify(res));
    """
    try:
        p = subprocess.Popen(['node', '-e', js_code], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        out, err = p.communicate(json.dumps(text))
        if p.returncode == 0:
            result = json.loads(out)
            _seg_cache[text] = result
            return result
    except Exception:
        pass
    _seg_cache[text] = text
    return text

def make_p(runs, align="both", space_before=0, space_after=20, line_spacing=240, first_line=0, left_indent=0, hanging=0, keep_next=False):
    p_pr = []
    p_pr.append(f'<w:jc w:val="{align}"/>')
    p_pr.append(f'<w:spacing w:before="{space_before}" w:after="{space_after}" w:line="{line_spacing}" w:lineRule="auto"/>')
    
    if hanging > 0:
        p_pr.append(f'<w:ind w:left="{left_indent}" w:hanging="{hanging}"/>')
    elif first_line > 0 or left_indent > 0:
        p_pr.append(f'<w:ind w:left="{left_indent}" w:firstLine="{first_line}"/>')
        
    if keep_next:
        p_pr.append('<w:keepNext/>')

    runs_xml = []
    for item in runs:
        if isinstance(item, str):
            t = item
            b = False
            i = False
            u = False
            sz = 32
            c = "000000"
        else:
            t = item[0]
            b = item[1] if len(item) > 1 else False
            i = item[2] if len(item) > 2 else False
            sz = item[3] if len(item) > 3 else 32
            c = item[4] if len(item) > 4 else "000000"
            u = item[5] if len(item) > 5 else False
        
        segmented_t = add_thai_breaks(t)
        
        r_pr = ['<w:rFonts w:ascii="TH Sarabun PSK" w:hAnsi="TH Sarabun PSK" w:cs="TH Sarabun PSK"/>']
        if b:
            r_pr.append('<w:b/><w:bCs/>')
        if i:
            r_pr.append('<w:i/><w:iCs/>')
        if u:
            r_pr.append('<w:u w:val="single"/>')
        r_pr.append(f'<w:sz w:val="{sz}"/>')
        r_pr.append(f'<w:szCs w:val="{sz}"/>')
        r_pr.append(f'<w:color w:val="{c}"/>')
        r_pr.append('<w:lang w:val="th-TH" w:eastAsia="th-TH" w:bidi="th-TH"/>')
        
        if align == "center" and "\n" in segmented_t:
            parts = segmented_t.split("\n")
            for idx, part in enumerate(parts):
                if part:
                    runs_xml.append(f'<w:r><w:rPr>{"".join(r_pr)}</w:rPr><w:t xml:space="preserve">{esc(part)}</w:t></w:r>')
                if idx < len(parts) - 1:
                    runs_xml.append(f'<w:r><w:rPr>{"".join(r_pr)}</w:rPr><w:br/></w:r>')
        else:
            cleaned_t = " ".join(part.strip() for part in segmented_t.split("\n") if part.strip())
            runs_xml.append(f'<w:r><w:rPr>{"".join(r_pr)}</w:rPr><w:t xml:space="preserve">{esc(cleaned_t)}</w:t></w:r>')

    return f'<w:p><w:pPr>{"".join(p_pr)}</w:pPr>{"".join(runs_xml)}</w:p>'

def make_page_break():
    return '<w:p><w:pPr><w:spacing w:before="0" w:after="0"/></w:pPr><w:r><w:br w:type="page"/></w:r></w:p>'

def make_academic_table(headers, rows, col_widths, alignments=None, header_bg="F2F2F2", bordered=True):
    total_w = sum(col_widths)
    if alignments is None:
        alignments = ["center"] * len(headers)
        
    xml = ['<w:tbl>',
           f'''<w:tblPr>
                <w:tblW w:w="{total_w}" w:type="dxa"/>
                <w:jc w:val="center"/>
                <w:tblBorders>
                   <w:top w:val="single" w:sz="12" w:space="0" w:color="000000"/>
                   <w:left w:val="none"/>
                   <w:bottom w:val="single" w:sz="12" w:space="0" w:color="000000"/>
                   <w:right w:val="none"/>
                   <w:insideH w:val="{"single" if bordered else "none"}" w:sz="4" w:space="0" w:color="D1D5DB"/>
                   <w:insideV w:val="{"single" if bordered else "none"}" w:sz="4" w:space="0" w:color="E5E7EB"/>
                </w:tblBorders>
                <w:tblCellMar>
                   <w:top w:w="120" w:type="dxa"/>
                   <w:left w:w="140" w:type="dxa"/>
                   <w:bottom w:w="120" w:type="dxa"/>
                   <w:right w:w="140" w:type="dxa"/>
                </w:tblCellMar>
             </w:tblPr>''',
           '<w:tblGrid>']
    for w in col_widths:
        xml.append(f'<w:gridCol w:w="{w}"/>')
    xml.append('</w:tblGrid>')
    
    # Header Row
    xml.append('<w:tr><w:trPr><w:tblHeader/><w:cantSplit/></w:trPr>')
    for h, w, a in zip(headers, col_widths, alignments):
        h_segmented = add_thai_breaks(str(h))
        h_parts = h_segmented.split("\n")
        runs_xml = []
        for idx, part in enumerate(h_parts):
            if part:
                runs_xml.append(f'<w:r><w:rPr><w:rFonts w:ascii="TH Sarabun PSK" w:hAnsi="TH Sarabun PSK" w:cs="TH Sarabun PSK"/><w:b/><w:bCs/><w:sz w:val="30"/><w:szCs w:val="30"/><w:color w:val="000000"/><w:lang w:val="th-TH"/></w:rPr><w:t xml:space="preserve">{esc(part)}</w:t></w:r>')
            if idx < len(h_parts) - 1:
                runs_xml.append('<w:r><w:br/></w:r>')
                
        xml.append(f'''<w:tc>
            <w:tcPr>
               <w:tcW w:w="{w}" w:type="dxa"/>
               <w:shd w:val="clear" w:color="auto" w:fill="{header_bg}"/>
               <w:tcBorders><w:bottom w:val="single" w:sz="10" w:space="0" w:color="000000"/></w:tcBorders>
               <w:vAlign w:val="center"/>
            </w:tcPr>
            <w:p><w:pPr><w:jc w:val="{a}"/><w:spacing w:before="60" w:after="60" w:line="240" w:lineRule="auto"/></w:pPr>{"".join(runs_xml)}</w:p>
        </w:tc>''')
    xml.append('</w:tr>')
    
    # Data Rows
    for r_idx, row in enumerate(rows):
        is_summary = any(kw in str(row[0]) for kw in ["รวม", "เฉลี่ย", "Total", "Average", "คำรับรอง"])
        bg_color = "F3F4F6" if is_summary else ("FFFFFF" if r_idx % 2 == 0 else "FAFAFA")
        font_b = is_summary
        
        xml.append('<w:tr><w:trPr><w:cantSplit/></w:trPr>')
        for c_idx, (val, w, a) in enumerate(zip(row, col_widths, alignments)):
            val_str = str(val)
            val_segmented = add_thai_breaks(val_str)
            v_parts = val_segmented.split("\n")
            runs_xml = []
            for idx, part in enumerate(v_parts):
                if part:
                    runs_xml.append(f'<w:r><w:rPr><w:rFonts w:ascii="TH Sarabun PSK" w:hAnsi="TH Sarabun PSK" w:cs="TH Sarabun PSK"/>{"<w:b/><w:bCs/>" if font_b else ""}<w:sz w:val="30"/><w:szCs w:val="30"/><w:color w:val="000000"/><w:lang w:val="th-TH"/></w:rPr><w:t xml:space="preserve">{esc(part)}</w:t></w:r>')
                if idx < len(v_parts) - 1:
                    runs_xml.append('<w:r><w:br/></w:r>')
            
            tc_bdr = ""
            if is_summary:
                tc_bdr = '<w:tcBorders><w:top w:val="single" w:sz="8" w:space="0" w:color="000000"/></w:tcBorders>'
                
            xml.append(f'''<w:tc>
                <w:tcPr>
                   <w:tcW w:w="{w}" w:type="dxa"/>
                   <w:shd w:val="clear" w:color="auto" w:fill="{bg_color}"/>
                   {tc_bdr}
                   <w:vAlign w:val="center"/>
                </w:tcPr>
                <w:p><w:pPr><w:jc w:val="{a}"/><w:spacing w:before="40" w:after="40" w:line="240" w:lineRule="auto"/></w:pPr>{"".join(runs_xml)}</w:p>
            </w:tc>''')
        xml.append('</w:tr>')
        
    xml.append('</w:tbl>')
    return "".join(xml)

def build_challenge_report_document():
    elements = []

    # =========================================================================
    # 1. หน้าปกรายงานประเด็นท้าทาย (FORMAL PA CHALLENGING ISSUE COVER)
    # =========================================================================
    elements.append(make_p([], align="center", space_before=300, space_after=100))
    elements.append(make_p([
        ("แบบรายงานผลการพัฒนางานตามข้อตกลงในการพัฒนางาน (PA)", True, False, 36, "000000")
    ], align="center", space_before=0, space_after=40))
    elements.append(make_p([
        ("สำหรับข้าราชการครูและบุคลากรทางการศึกษา ตำแหน่ง ครู (ไม่มีวิทยฐานะ)", True, False, 30, "000000"),
        ("\nประจำปีงบประมาณ พ.ศ. 2569", True, False, 30, "000000"),
        ("\nรอบการประเมิน ระหว่างวันที่ 1 ตุลาคม พ.ศ. 2568 ถึงวันที่ 30 กันยายน พ.ศ. 2569", False, False, 28, "000000")
    ], align="center", space_before=0, space_after=240, line_spacing=260))

    elements.append(make_p([
        ("ส่วนที่ 2 ข้อตกลงในการพัฒนางานที่เป็นประเด็นท้าทาย", True, False, 34, "000000"),
        ("\nในการพัฒนาผลลัพธ์การเรียนรู้ของผู้เรียน", True, False, 34, "000000")
    ], align="center", space_before=40, space_after=100, line_spacing=260))

    elements.append(make_p([
        ("ประเด็นท้าทาย เรื่อง", True, False, 32, "000000")
    ], align="center", space_before=20, space_after=40))

    elements.append(make_p([
        ("การพัฒนาทักษะการเรียนรู้รายวิชาเทคโนโลยี (วิทยาการคำนวณ)", True, False, 32, "000000"),
        ("\nกลุ่มสาระการเรียนรู้วิทยาศาสตร์และเทคโนโลยี", True, False, 32, "000000"),
        ("\nโดยใช้กระบวนการ Gamebase learning ร่วมกับเทคนิคการสอนแบบ active learning", True, False, 32, "000000"),
        ("\nของนักเรียนชั้นประถมศึกษาปีที่ 5 โรงเรียนบ้านโนนป่าหว้านเชียงฮาย", True, False, 32, "000000")
    ], align="center", space_before=20, space_after=300, line_spacing=260))

    elements.append(make_p([
        ("ผู้รายงาน", True, False, 32, "000000")
    ], align="center", space_before=40, space_after=30))

    elements.append(make_p([
        ("นายเตชินท์  อินทมล", True, False, 32, "000000"),
        ("\nตำแหน่ง ครู (ไม่มีวิทยฐานะ)", False, False, 30, "000000"),
        ("\nกลุ่มสาระการเรียนรู้วิทยาศาสตร์และเทคโนโลยี", False, False, 30, "000000")
    ], align="center", space_before=0, space_after=240, line_spacing=260))

    elements.append(make_p([
        ("โรงเรียนบ้านโนนป่าหว้านเชียงฮาย", True, False, 32, "000000"),
        ("\nสำนักงานเขตพื้นที่การศึกษาประถมศึกษาหนองบัวลำภู เขต 2", False, False, 30, "000000"),
        ("\nสำนักงานคณะกรรมการการศึกษาขั้นพื้นฐาน กระทรวงศึกษาธิการ", False, False, 30, "000000")
    ], align="center", space_before=0, space_after=100, line_spacing=260))

    elements.append(make_page_break())

    # =========================================================================
    # 2. เนื้อหาแบบรายงานผลการดำเนินงานประเด็นท้าทาย (PA 2/ส ส่วนที่ 2)
    # =========================================================================

    elements.append(make_p([
        ("แบบรายงานผลการดำเนินงานตามข้อตกลงในการพัฒนางานที่เป็นประเด็นท้าทาย", True, False, 34, "000000"),
        ("\nในการพัฒนาผลลัพธ์การเรียนรู้ของผู้เรียน (PA 2/ส ส่วนที่ 2)", True, False, 32, "000000")
    ], align="center", space_before=60, space_after=120, line_spacing=260, keep_next=True))

    # ข้อมูลทั่วไป
    elements.append(make_p([
        ("ข้อมูลผู้จัดทำข้อตกลงและรายงาน:", True, False, 32, "000000")
    ], align="left", space_before=60, space_after=20, keep_next=True))

    elements.append(make_p([
        ("ชื่อ - นามสกุล: ", True, False, 32, "000000"),
        ("นายเตชินท์  อินทมล               ", False, False, 32, "000000"),
        ("ตำแหน่ง: ", True, False, 32, "000000"),
        ("ครู (ไม่มีวิทยฐานะ)", False, False, 32, "000000")
    ], align="left", space_before=0, space_after=10, line_spacing=240, first_line=720))

    elements.append(make_p([
        ("กลุ่มสาระการเรียนรู้: ", True, False, 32, "000000"),
        ("วิทยาศาสตร์และเทคโนโลยี        ", False, False, 32, "000000"),
        ("สถานศึกษา: ", True, False, 32, "000000"),
        ("โรงเรียนบ้านโนนป่าหว้านเชียงฮาย", False, False, 32, "000000")
    ], align="left", space_before=0, space_after=10, line_spacing=240, first_line=720))

    elements.append(make_p([
        ("สังกัด: ", True, False, 32, "000000"),
        ("สำนักงานเขตพื้นที่การศึกษาประถมศึกษาหนองบัวลำภู เขต 2", False, False, 32, "000000")
    ], align="left", space_before=0, space_after=10, line_spacing=240, first_line=720))

    elements.append(make_p([
        ("การจัดการเรียนรู้ที่รับผิดชอบ: ", True, False, 32, "000000"),
        ("รายวิชาพื้นฐานวิทยาศาสตร์และเทคโนโลยี เทคโนโลยี (วิทยาการคำนวณ) รหัสวิชา ว15101 ชั้นประถมศึกษาปีที่ 5 ภาคเรียนที่ 1 ปีการศึกษา 2569 จำนวน 8 คน", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=40, line_spacing=240, first_line=720))

    # ชื่อประเด็นท้าทาย
    elements.append(make_p([
        ("ชื่อประเด็นท้าทาย:", True, False, 32, "000000")
    ], align="left", space_before=40, space_after=20, keep_next=True))

    elements.append(make_p([
        ("การพัฒนาทักษะการเรียนรู้รายวิชาเทคโนโลยี (วิทยาการคำนวณ) กลุ่มสาระการเรียนรู้วิทยาศาสตร์และเทคโนโลยี โดยใช้กระบวนการ Gamebase learning ร่วมกับเทคนิคการสอนแบบ active learning ของนักเรียนชั้นประถมศึกษาปีที่ 5 โรงเรียนบ้านโนนป่าหว้านเชียงฮาย", True, False, 32, "000000")
    ], align="both", space_before=0, space_after=60, line_spacing=240, first_line=720))

    # 1. สภาพปัญหา
    elements.append(make_p([
        ("1. สภาพปัญหาการจัดการเรียนรู้และคุณภาพการเรียนรู้ของผู้เรียน", True, False, 32, "000000")
    ], align="left", space_before=100, space_after=30, keep_next=True))

    elements.append(make_p([
        ("กลุ่มสาระการเรียนรู้วิทยาศาสตร์และเทคโนโลยี สาระเทคโนโลยี (วิทยาการคำนวณ) ตามหลักสูตรแกนกลางการศึกษาขั้นพื้นฐาน พุทธศักราช 2551 (ฉบับปรับปรุง พ.ศ. 2560) มุ่งเน้นพัฒนาผู้เรียนให้มีสมรรถนะสำคัญแห่งศตวรรษที่ 21 โดยเฉพาะ “ทักษะการคิดเชิงคำนวณ (Computational Thinking)” และทักษะการแก้ปัญหาอย่างเป็นขั้นตอน ซึ่งเป็นวิชาเชิงทักษะกระบวนการที่ผู้เรียนต้องลงมือคิดและลงมือปฏิบัติจริง โดยตามข้อตกลงในการพัฒนางาน (PA 1) ประจำปีงบประมาณ พ.ศ. 2569 ข้าพเจ้าได้กำหนดประเด็นท้าทายในรายวิชาพื้นฐานวิทยาศาสตร์และเทคโนโลยี เทคโนโลยี (วิทยาการคำนวณ) รหัสวิชา ว15101 ชั้นประถมศึกษาปีที่ 5 โรงเรียนบ้านโนนป่าหว้านเชียงฮาย ภาคเรียนที่ 1 ปีการศึกษา 2569 จำนวน 8 คน ในหน่วยการเรียนรู้เรื่อง การใช้เหตุผลเชิงตรรกะและการเขียนโปรแกรมอย่างง่าย (ตัวชี้วัด ว 4.2 ป.5/1 และ ป.5/2)", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=20, line_spacing=240, first_line=720))

    elements.append(make_p([
        ("จากการจัดการเรียนรู้ในปีการศึกษาที่ผ่านมา ตลอดจนการสังเกตและประเมินความพร้อมเบื้องต้นของนักเรียนชั้นประถมศึกษาปีที่ 5 พบสภาพปัญหาสำคัญในการจัดการเรียนรู้ 3 ประการ ได้แก่:", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=20, line_spacing=240, first_line=720))

    elements.append(make_p([
        ("1) ความเป็นนามธรรมและความสับสนเรื่องมิติสัมพันธ์และทิศทาง (Spatial Confusion): ", True, False, 32, "000000"),
        ("เมื่อตัวละครหรือหุ่นยนต์ในหน้าจอหันหน้าตรงข้ามกับผู้เรียน นักเรียนเกิดความสับสนทิศทางซ้าย-ขวา นึกภาพตามไม่ทัน ส่งผลให้วางคำสั่งทิศทางผิดพลาด", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=20, line_spacing=240, first_line=720))

    elements.append(make_p([
        ("2) พฤติกรรมการแก้ปัญหาแบบลองผิดลองถูก (Trial and Error): ", True, False, 32, "000000"),
        ("นักเรียนขาดการวางแผนลำดับขั้นตอนก่อนลงมือเขียนโปรแกรม เมื่อหุ่นยนต์เดินติดสิ่งกีดขวาง มักเลือกกดลบคำสั่งทั้งหมดแล้วเริ่มต้นใหม่ แทนที่จะวิเคราะห์เพื่อค้นหาและแก้ไขข้อผิดพลาด (Debugging)", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=20, line_spacing=240, first_line=720))

    elements.append(make_p([
        ("3) ความเหลื่อมล้ำในการมีส่วนร่วม (Unequal Participation): ", True, False, 32, "000000"),
        ("ในการทำงานหน้าเครื่องคอมพิวเตอร์ นักเรียนที่กล้าแสดงออกมักเป็นผู้ควบคุมอุปกรณ์แต่เพียงผู้เดียว ส่วนเพื่อนร่วมกลุ่มขาดโอกาสลงมือคิดและฝึกปฏิบัติ", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=20, line_spacing=240, first_line=720))

    elements.append(make_p([
        ("จากสภาพปัญหาดังกล่าว ครูผู้สอนจึงได้นำแนวคิด การจัดการเรียนรู้โดยใช้เกมเป็นฐาน (Game-based Learning) ผสานเข้ากับ เทคโนโลยีการตรวจจับท่าทางมือผ่านกล้อง (Hand Gesture Recognition) ในรูปแบบเกมโต้ตอบ เช่น การชูนิ้วบอกจำนวนก้าว การยกมือซ้าย-ขวาบอกทิศทาง ร่วมกับ ชุดแฟลชการ์ดคำสั่งสัญลักษณ์จริง (Tangible Flashcards) และเทคนิค Active Learning แบบ Pair Programming (Driver & Navigator) เพื่อเป็นสะพานเชื่อมโยงความรู้จากรูปธรรมสู่นามธรรม ก่อนถ่ายโอนสู่การเขียนโปรแกรม Scratch อย่างมีประสิทธิภาพ", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=40, line_spacing=240, first_line=720))

    # 2. วิธีการดำเนินการให้บรรลุผล
    elements.append(make_p([
        ("2. วิธีการดำเนินการให้บรรลุผล", True, False, 32, "000000")
    ], align="left", space_before=100, space_after=30, keep_next=True))

    elements.append(make_p([
        ("เพื่อแก้ไขปัญหาดังกล่าวให้บรรลุผลลัพธ์ตามข้อตกลงในการพัฒนางาน ข้าพเจ้าได้ดำเนินการจัดการเรียนรู้โดยใช้กระบวนการ Gamebase learning ร่วมกับเทคนิคการสอนแบบ active learning โดยมีขั้นตอนการดำเนินงานตามวงจรคุณภาพ PDCA ดังนี้:", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=20, line_spacing=240, first_line=720))

    elements.append(make_p([
        ("2.1 การวางแผน (Plan):", True, False, 32, "000000")
    ], align="left", space_before=20, space_after=10, keep_next=True))

    elements.append(make_p([
        ("1) ศึกษาและวิเคราะห์หลักสูตรแกนกลางการศึกษาขั้นพื้นฐานฯ ตัวชี้วัด ว 4.2 ป.5/1 และ ป.5/2 จัดทำโครงสร้างหน่วยการเรียนรู้เรื่อง การใช้เหตุผลเชิงตรรกะและการเขียนโปรแกรมอย่างง่าย", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=10, line_spacing=240, first_line=720))

    elements.append(make_p([
        ("2) ออกแบบแผนการจัดการเรียนรู้เชิงรุก (Active Learning) จำนวน 7 แผน รวม 7 ชั่วโมง เน้นการมีส่วนร่วมและการลงมือปฏิบัติจริง", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=10, line_spacing=240, first_line=720))

    elements.append(make_p([
        ("3) สร้างและพัฒนานวัตกรรมสื่อการเรียนรู้ ได้แก่ เกมตอบสนองท่าทางเสมือนจริง CodeBot AR Adventure ร่วมกับชุดแฟลชการ์ดคำสั่งสัญลักษณ์จริง 18 ใบ เพื่อเป็นสะพานเชื่อมโยงรูปธรรมสู่นามธรรม และเตรียมบทเรียนฝึกเขียนโปรแกรมด้วยโปรแกรม Scratch", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=10, line_spacing=240, first_line=720))

    elements.append(make_p([
        ("4) สร้างเครื่องมือวัดและประเมินผล ได้แก่ แบบทดสอบวัดผลสัมฤทธิ์ทางการเรียนรู้ปรนัย 4 ตัวเลือก 20 ข้อ แบบประเมินรูบริกส์ทักษะการคิดเชิงคำนวณ (CT 4 ด้าน) และแบบสอบถามความพึงพอใจ", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=30, line_spacing=240, first_line=720))

    elements.append(make_p([
        ("2.2 การปฏิบัติการ (Do):", True, False, 32, "000000")
    ], align="left", space_before=20, space_after=10, keep_next=True))

    elements.append(make_p([
        ("1) ดำเนินการทดสอบก่อนเรียน (Pre-test) จำนวน 20 ข้อ กับนักเรียนกลุ่มเป้าหมายชั้น ป.5 จำนวน 8 คน ในสัปดาห์แรก", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=10, line_spacing=240, first_line=720))

    elements.append(make_p([
        ("2) จัดกิจกรรมการเรียนรู้ตามแผนการจัดการเรียนรู้ทั้ง 7 แผน สัปดาห์ละ 1 ชั่วโมง โดยนำกระบวนการ Gamebase learning (เกม CodeBot AR Adventure และแฟลชการ์ด) ร่วมกับเทคนิคการสอนแบบ active learning โดยจัดนักเรียน 8 คน ทำงานร่วมกันเป็น 4 คู่ ใช้เทคนิค Pair Programming กำหนดบทบาทชัดเจน:", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=10, line_spacing=240, first_line=720))

    elements.append(make_p([
        ("• บทบาทผู้นำทาง (Navigator): วางแผนเส้นทาง คิดวิเคราะห์ตรรกะ และเรียงบัตรคำสั่งจริงบนโต๊ะ", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=10, line_spacing=240, first_line=1080))
    elements.append(make_p([
        ("• บทบาทผู้ขับเคลื่อน (Driver): ทำหน้าที่ป้อนคำสั่งผ่านท่าทางหน้ากล้อง AR และพิมพ์คำสั่งในโปรแกรม Scratch", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=10, line_spacing=240, first_line=1080))
    elements.append(make_p([
        ("• มีการสลับบทบาทกันทุกรอบภารกิจ เพื่อให้นักเรียนทุกคนได้ฝึกคิดและฝึกปฏิบัติอย่างเท่าเทียม", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=30, line_spacing=240, first_line=1080))

    elements.append(make_p([
        ("2.3 การตรวจสอบและประเมินผล (Check):", True, False, 32, "000000")
    ], align="left", space_before=20, space_after=10, keep_next=True))

    elements.append(make_p([
        ("1) สังเกตและประเมินพฤติกรรมการเรียนรู้ ทักษะการคิดเชิงคำนวณ (CT 4 ด้าน) และทักษะแห่งศตวรรษที่ 21 (4 Cs) ระหว่างการทำกิจกรรมรายคู่", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=10, line_spacing=240, first_line=720))

    elements.append(make_p([
        ("2) ดำเนินการทดสอบหลังเรียน (Post-test) จำนวน 20 ข้อ (ฉบับคู่ขนานกับข้อสอบก่อนเรียน) ในชั่วโมงที่ 7 และให้นักเรียนทำแบบประเมินความพึงพอใจ", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=30, line_spacing=240, first_line=720))

    elements.append(make_p([
        ("2.4 การปรับปรุงและพัฒนา (Act):", True, False, 32, "000000")
    ], align="left", space_before=20, space_after=10, keep_next=True))

    elements.append(make_p([
        ("นำข้อมูลคะแนนและผลการประเมินมาวิเคราะห์ทางสถิติ สรุปเป็นรายงานการวิจัยปฏิบัติการในชั้นเรียน (CAR) และนำข้อสะท้อนคิดมาปรับปรุงแผนการจัดการเรียนรู้เพื่อเป็นแนวทางในการจัดการเรียนการสอนในภาคเรียนต่อไป", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=40, line_spacing=240, first_line=720))

    # ตารางโครงสร้างแผน 7 แผน
    elements.append(make_p([
        ("ตารางสรุปแผนการจัดการเรียนรู้เชิงรุกเพื่อขับเคลื่อนประเด็นท้าทาย ภาคเรียนที่ 1 (7 แผน 18-20 ชั่วโมง)", True, False, 30, "000000"),
        ("\n(สอดคล้องตามหน่วยการเรียนรู้ที่ 1 และ 2 ของหนังสือเรียน พว. ชั้น ป.5 บูรณาการประเมินทักษะ CT)", False, True, 26, "4B5563")
    ], align="left", space_before=40, space_after=20, keep_next=True))

    plans_table_headers = ["แผนที่", "ชื่อหน่วย / เรื่อง (ตามสาระ พว. ป.5)", "สื่อนวัตกรรม & เทคนิค Active Learning", "เวลา"]
    plans_table_rows = [
        ["1", "การแก้ปัญหาด้วยเหตุผลเชิงตรรกะในชีวิตประจำวัน", "การวิเคราะห์ปัญหาใกล้ตัว + บัตรตรรกะเหตุและผล (แฝง Decomposition)", "2 ชม."],
        ["2", "การวางแผนและการเขียนรหัสลำลองด้วยบัตรคำสั่ง", "แบบรูปทิศทาง + จัดเรียงบัตรคำสั่ง Unplugged Coding (แฝง Pattern)", "2 ชม."],
        ["3", "การจัดลำดับคำสั่งและการแก้ปัญหาทิศทาง", "เกม CodeBot AR ด่าน 1-4 + แฟลชการ์ดทิศทาง (แฝง Abstraction)", "3 ชม."],
        ["4", "การออกแบบและเขียนโปรแกรมเบื้องต้นด้วย Scratch", "โปรแกรม Scratch ภาษาไทย: การจัดบล็อกคำสั่งพาตัวละครเดิน (แฝง Algorithm)", "3 ชม."],
        ["5", "การเขียนโปรแกรมแบบมีเงื่อนไขและการทำซ้ำ (Loop)", "เกม AR ด่าน 5-8 + บล็อกคำสั่ง [ทำซ้ำ] และ [ถ้า...แล้ว] ใน Scratch", "3 ชม."],
        ["6", "การตรวจสอบและแก้ไขข้อผิดพลาดของโปรแกรม (Debugging)", "เกม AR ด่าน 9-10 + จับคู่บัดดี้ (Driver & Navigator) ค้นหาและแก้บั๊ก", "3 ชม."],
        ["7", "การสะท้อนคิด ถอดบทเรียน และการประเมินผลสัมฤทธิ์", "Post-test 20 ข้อ + ประเมินรูบริกส์ CT 4 ด้าน + AAR สรุปการเรียนรู้", "2 ชม."],
        ["รวม", "ประเด็นท้าทายตามข้อตกลง PA 1 ตลอดภาคเรียนที่ 1 (7 แผนหลัก)", "บูรณาการ Game-based learning ร่วมกับ Active Learning (+ สอบกลาง/ปลายภาค 2 ชม.)", "20 ชม."]
    ]
    elements.append(make_academic_table(plans_table_headers, plans_table_rows, [1000, 3600, 3600, 800], ["center", "left", "left", "center"]))
    elements.append(make_p([], space_before=20, space_after=30))

    # 3. ผลลัพธ์การพัฒนาที่คาดหวัง
    elements.append(make_p([
        ("3. ผลลัพธ์การพัฒนาที่คาดหวังและผลการดำเนินงานจริง", True, False, 32, "000000")
    ], align="left", space_before=80, space_after=20, keep_next=True))

    # 3.1 เชิงปริมาณ
    elements.append(make_p([
        ("3.1 ผลลัพธ์เชิงปริมาณ (Quantitative Outcomes):", True, False, 32, "000000")
    ], align="left", space_before=10, space_after=10, keep_next=True))

    elements.append(make_p([
        ("1) ด้านผลสัมฤทธิ์ทางการเรียน: ", True, False, 32, "000000"),
        ("นักเรียนชั้นประถมศึกษาปีที่ 5 ทั้ง 8 คน (ร้อยละ 100) มีคะแนนผลสัมฤทธิ์ทางการเรียนรู้หลังเรียนสูงกว่าก่อนเรียนทุกคน โดยมีคะแนนเฉลี่ยเพิ่มขึ้น 7.88 คะแนน (ก่อนเรียนเฉลี่ย 7.75 คะแนน / หลังเรียนเฉลี่ย 15.62 คะแนน) คิดเป็นพัฒนาการร้อยละ 39.38 ซึ่งสูงกว่าเป้าหมายที่กำหนดไว้ในข้อตกลง PA (เป้าหมาย: ไม่น้อยกว่าร้อยละ 70)", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=15, line_spacing=240, first_line=720))

    # ตารางคะแนนรายบุคคล
    elements.append(make_p([
        ("ตารางสรุปผลสัมฤทธิ์ทางการเรียนรู้รายวิชาเทคโนโลยี (วิทยาการคำนวณ) รายบุคคล (N = 8)", True, False, 30, "000000")
    ], align="left", space_before=15, space_after=15, keep_next=True))

    scores_headers = ["เลขที่", "ชื่อ - สกุล ผู้เรียน", "ก่อนเรียน (20)", "หลังเรียน (20)", "พัฒนาการ", "ร้อยละพัฒนาการ", "ผลการประเมิน"]
    scores_rows = [
        ["1", "เด็กชายภูฟ้า  แสงศรี", "5", "14", "+9", "45.00%", "ผ่านเกณฑ์"],
        ["2", "เด็กหญิงพิชญาภา  แสงศรี", "10", "18", "+8", "40.00%", "ผ่านเกณฑ์"],
        ["3", "เด็กหญิงสิริวิมล  สาวิสิทธิ์", "8", "16", "+8", "40.00%", "ผ่านเกณฑ์"],
        ["4", "เด็กหญิงสาวิตรี  สายสมคุณ", "8", "15", "+7", "35.00%", "ผ่านเกณฑ์"],
        ["5", "เด็กหญิงณัฐณิชา  นันทโพธิ์เดช", "8", "16", "+8", "40.00%", "ผ่านเกณฑ์"],
        ["6", "เด็กหญิงรฐา  สอนเต็ม", "7", "16", "+9", "45.00%", "ผ่านเกณฑ์"],
        ["7", "เด็กหญิงกัญญาพัชร  วาจาชื่น", "12", "18", "+6", "30.00%", "ผ่านเกณฑ์"],
        ["8", "เด็กหญิงกัญญารัตน์  บัวบง", "4", "12", "+8", "40.00%", "ผ่านเกณฑ์"],
        ["เฉลี่ย", "ค่าเฉลี่ย (X̄) และ S.D.", "7.75 (2.55)", "15.62 (2.00)", "+7.88", "39.38%", "ผ่านเกณฑ์ 100%"]
    ]
    elements.append(make_academic_table(scores_headers, scores_rows, [800, 2600, 1100, 1100, 1000, 1200, 1200], ["center", "left", "center", "center", "center", "center", "center"]))
    elements.append(make_p([], space_before=15, space_after=15))

    elements.append(make_p([
        ("2) ด้านทักษะการคิดเชิงคำนวณและการเขียนโปรแกรม: ", True, False, 32, "000000"),
        ("นักเรียนชั้นประถมศึกษาปีที่ 5 จำนวน 7 คน จากทั้งหมด 8 คน (คิดเป็นร้อยละ 87.50) มีผลการประเมินทักษะอยู่ในระดับ “ดี” ขึ้นไป โดยมีคะแนนเฉลี่ยรวมของชั้นเรียนเท่ากับ 3.00 จาก 4.00 คะแนน (อยู่ในระดับดี) ซึ่งบรรลุตามเป้าหมายที่กำหนดไว้ในข้อตกลง (เป้าหมาย: ระดับดีขึ้นไป ไม่น้อยกว่าร้อยละ 80)", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=25, line_spacing=240, first_line=720))

    # 3.2 เชิงคุณภาพ
    elements.append(make_p([
        ("3.2 ผลลัพธ์เชิงคุณภาพ (Qualitative Outcomes):", True, False, 32, "000000")
    ], align="left", space_before=10, space_after=10, keep_next=True))

    elements.append(make_p([
        ("1) มโนทัศน์ตรรกะและทิศทางแม่นยำ: ", True, False, 32, "000000"),
        ("ผู้เรียนเข้าใจลำดับคำสั่งและการเคลื่อนที่ ไม่สับสนทิศทางซ้าย-ขวาเมื่อมุมมองหุ่นยนต์กลับทิศ ด้วยสื่อนวัตกรรมเกมและแฟลชการ์ดสัญลักษณ์จริง", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=10, line_spacing=240, first_line=720))

    elements.append(make_p([
        ("2) กระบวนการแก้ปัญหาเป็นระบบ: ", True, False, 32, "000000"),
        ("ผู้เรียนเปลี่ยนจากการสุ่มลองผิดลองถูก มาเป็นการวางแผนลำดับขั้นตอน และสามารถตรวจหาจุดผิดพลาด (Debugging) เพื่อแก้ไขโค้ดได้ด้วยตนเอง", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=10, line_spacing=240, first_line=720))

    elements.append(make_p([
        ("3) การทำงานร่วมกันและการสื่อสาร (4 Cs): ", True, False, 32, "000000"),
        ("ผู้เรียนทุกคนมีส่วนร่วมอย่างเท่าเทียมผ่านเทคนิค Pair Programming ได้ฝึกเป็นทั้งผู้นำทาง (Navigator) และผู้ปฏิบัติ (Driver) ช่วยเหลือเกื้อกูลกันเป็นทีมอย่างมีความสุข", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=10, line_spacing=240, first_line=720))

    elements.append(make_p([
        ("4) เจตคติที่ดีและความสุขในการเรียนรู้ (A): ", True, False, 32, "000000"),
        ("ผู้เรียนมีเจตคติที่ดีต่อวิชาวิทยาการคำนวณ มีความกระตือรือร้นและมีความสุขในการเรียนรู้ สอดคล้องกับผลการประเมินความพึงพอใจโดยรวมที่อยู่ในระดับ “มาก” (คะแนนเฉลี่ย 4.38 จากคะแนนเต็ม 5.00, S.D. = 0.43)", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=35, line_spacing=240, first_line=720))

    # 4. สรุปผลเชื่อมโยงเกณฑ์ ว.PA (ด้านที่ 1 ครบทั้ง 8 ตัวชี้วัด)
    elements.append(make_p([
        ("4. การสะท้อนผลการดำเนินงานประเด็นท้าทายเชื่อมโยงเกณฑ์การประเมิน ว.PA", True, False, 32, "000000"),
        ("\n(ด้านที่ 1 ด้านการจัดการเรียนรู้ ครบทั้ง 8 ตัวชี้วัด)", True, False, 32, "000000")
    ], align="left", space_before=100, space_after=30, line_spacing=260, keep_next=True))

    pa_indicators = [
        ("1.1 การพัฒนาหลักสูตร",
         "วิเคราะห์หลักสูตรแกนกลางฯ ตัวชี้วัด ว 4.2 ป.5/1 และ ป.5/2 จัดทำหน่วยการเรียนรู้เรื่อง การใช้เหตุผลเชิงตรรกะและการเขียนโปรแกรมอย่างง่าย มีโครงสร้างหน่วยและแผนการประเมินครบถ้วน สอดคล้องกับบริบทของสถานศึกษา",
         "นักเรียนร้อยละ 100 ได้เรียนรู้ตามโครงสร้างหลักสูตรและตัวชี้วัดที่กำหนด มีความรู้ความเข้าใจในเนื้อหาอย่างครบถ้วน"),

        ("1.2 การออกแบบการจัดการเรียนรู้",
         "ออกแบบแผนการจัดการเรียนรู้เชิงรุก (Active Learning) จำนวน 7 แผน บูรณาการกระบวนการ Gamebase learning ผ่านเกมนวัตกรรม CodeBot AR Adventure ร่วมกับชุดแฟลชการ์ดสัญลักษณ์จริง และการเขียนโปรแกรม Scratch ออกแบบกิจกรรมแบบจับคู่ Pair Programming เน้นผู้เรียนเป็นสำคัญ",
         "นักเรียนร้อยละ 100 มีผลสัมฤทธิ์ทางการเรียนรู้หลังเรียนสูงกว่าก่อนเรียน (คะแนนเฉลี่ยหลังเรียนคิดเป็นร้อยละ 78.13) ผ่านเกณฑ์ที่กำหนด และมีคะแนนพัฒนาการเพิ่มขึ้นทุกคน"),

        ("1.3 การจัดกิจกรรมการเรียนรู้",
         "จัดกิจกรรมการเรียนการสอนเชิงรุกที่หลากหลาย อำนวยความสะดวกในการเรียนรู้ จัดสภาพแวดล้อมให้เหมาะสมกับการทำงานเป็นคู่ (Driver & Navigator) ส่งเสริมให้ผู้เรียนทุกคนมีส่วนร่วม ได้ลงมือคิด ลงมือแก้ปัญหา และสะท้อนคิดร่วมกัน",
         "นักเรียนร้อยละ 100 มีส่วนร่วมในกิจกรรมการเรียนรู้อย่างมีความสุข กล้าคิด กล้าแสดงออก และสื่อสารแลกเปลี่ยนเหตุผลกับเพื่อนได้เป็นอย่างดี"),

        ("1.4 การสร้างและหรือพัฒนาสื่อ นวัตกรรม เทคโนโลยี และแหล่งการเรียนรู้",
         "สร้างและพัฒนานวัตกรรมสื่อการเรียนรู้ ได้แก่ เกมตอบสนองท่าทางเสมือนจริง CodeBot AR Adventure ร่วมกับชุดแฟลชการ์ดคำสั่งสัญลักษณ์จริง และโปรแกรม Scratch เพื่อใช้เป็นสะพานเชื่อมโยงความรู้จากรูปธรรมสู่นามธรรม ช่วยแก้ปัญหาการสับสนทิศทางและลำดับขั้นตอน",
         "นักเรียนร้อยละ 100 สามารถใช้นวัตกรรมสื่อเกม AR และแฟลชการ์ดในการฝึกทักษะการคิดเชิงคำนวณและเขียนโปรแกรมได้อย่างถูกต้องคล่องแคล่ว"),

        ("1.5 การวัดและประเมินผลการเรียนรู้",
         "ดำเนินการวัดและประเมินผลการเรียนรู้ด้วยวิธีการที่หลากหลายตามสภาพจริง สอดคล้องกับตัวชี้วัด ได้แก่ แบบทดสอบวัดผลสัมฤทธิ์ทางการเรียนรู้ แบบประเมินรูบริกส์วัดทักษะ CT 4 ด้าน แบบประเมินพฤติกรรมการทำงานกลุ่ม และแบบสอบถามความพึงพอใจ นำผลมาสะท้อนเพื่อพัฒนาผู้เรียนอย่างต่อเนื่อง",
         "มีเครื่องมือวัดและประเมินผลที่ได้มาตรฐาน สามารถสะท้อนผลการเรียนรู้ของผู้เรียนได้อย่างถูกต้อง เที่ยงตรง และเป็นระบบ"),

        ("1.6 การศึกษา วิเคราะห์ และสังเคราะห์ เพื่อแก้ไขปัญหาหรือพัฒนาการเรียนรู้",
         "จัดทำวิจัยปฏิบัติการในชั้นเรียน (CAR) เรื่อง การพัฒนาทักษะการเรียนรู้รายวิชาเทคโนโลยี (วิทยาการคำนวณ) โดยใช้กระบวนการ Gamebase learning ร่วมกับเทคนิค Active learning วิเคราะห์ข้อมูลทางสถิติ Paired Samples t-test อย่างเป็นระบบ นำผลไปพัฒนาการสอนต่อไป",
         "ได้นวัตกรรมและแนวทางการแก้ปัญหาการเรียนรู้วิทยาการคำนวณที่มีหลักฐานเชิงประจักษ์ สามารถเผยแพร่และเป็นแบบอย่างให้แก่ครูในสถานศึกษาได้"),

        ("1.7 การจัดบรรยากาศที่ส่งเสริมและพัฒนาผู้เรียน",
         "จัดบรรยากาศห้องเรียนคอมพิวเตอร์ที่เอื้อต่อการเรียนรู้ สะอาด ปลอดภัย อบอุ่น และเป็นมิตร ส่งเสริมให้ผู้เรียนเกิดความท้าทาย สนุกสนานกับการเรียนรู้ ไม่กลัวความผิดพลาด และมองการตรวจหาข้อผิดพลาด (Debugging) เป็นเรื่องสนุกในการค้นหาความจริง",
         "นักเรียนมีความพึงพอใจต่อบรรยากาศและการจัดการเรียนรู้อยู่ในระดับมากที่สุด (X̄ = 4.75, S.D. = 0.37) และมีความกระตือรือร้นในการเรียนรู้ทุกชั่วโมง"),

        ("1.8 การอบรมและพัฒนาคุณลักษณะที่ดีของผู้เรียน",
         "สอดแทรกคุณธรรม จริยธรรม และคุณลักษณะอันพึงประสงค์ในทุกแผนการจัดการเรียนรู้ ได้แก่ ความมีวินัย ความรับผิดชอบ ความซื่อสัตย์ในการทดสอบ การรับฟังความคิดเห็นของผู้อื่น และการทำงานร่วมกันอย่างมีน้ำใจเอื้ออาทรผ่านกิจกรรม Pair Programming",
         "นักเรียนร้อยละ 100 มีคุณลักษณะอันพึงประสงค์ผ่านเกณฑ์ในระดับดีเยี่ยม มีความสามัคคีและช่วยเหลือเกื้อกูลกันในการปฏิบัติภารกิจ")
    ]

    for ind_title, ind_desc, ind_outcome in pa_indicators:
        elements.append(make_p([
            (ind_title, True, False, 32, "000000")
        ], align="left", space_before=30, space_after=10, keep_next=True))
        
        elements.append(make_p([
            (ind_desc, False, False, 32, "000000")
        ], align="both", space_before=0, space_after=10, line_spacing=240, first_line=720))
        
        elements.append(make_p([
            ("ผลลัพธ์ (Outcome)", True, False, 32, "000000", True)
        ], align="left", space_before=10, space_after=10, keep_next=True))
        
        elements.append(make_p([
            (ind_outcome, False, False, 32, "000000")
        ], align="both", space_before=0, space_after=30, line_spacing=240, first_line=720))

    # 5. เอกสารหลักฐานเชิงประจักษ์ที่แนบ
    elements.append(make_p([
        ("5. รายการเอกสารและหลักฐานเชิงประจักษ์ที่แนบประกอบการประเมิน", True, False, 32, "000000")
    ], align="left", space_before=100, space_after=30, keep_next=True))

    evidences = [
        ("เอกสารแนบ 1: ", "เล่มรายงานการวิจัยปฏิบัติการในชั้นเรียน (Classroom Action Research: CAR) ฉบับสมบูรณ์"),
        ("เอกสารแนบ 2: ", "เล่มแผนการจัดการเรียนรู้เชิงรุก (Active Learning Plan) จำนวน 7 แผน รวม 7 ชั่วโมง"),
        ("เอกสารแนบ 3: ", "นวัตกรรมเว็บเกมโต้ตอบท่าทางเสมือนจริง CodeBot AR Adventure (เว็บแอปพลิเคชัน)"),
        ("เอกสารแนบ 4: ", "ชุดแฟลชการ์ดคำสั่งโค้ดดิ้งสัญลักษณ์จริง (Tangible Flashcards) จำนวน 18 ใบ"),
        ("เอกสารแนบ 5: ", "ชุดใบงานภารกิจโค้ดดิ้ง ป.5 จำนวน 4 ใบงานหลัก และแบบทดสอบวัดผลสัมฤทธิ์ 20 ข้อ"),
        ("เอกสารแนบ 6: ", "แบบประเมินรูบริกส์ทักษะการคิดเชิงคำนวณ (CT 4 ด้าน) และแบบสอบถามความพึงพอใจ")
    ]
    for ev_title, ev_desc in evidences:
        elements.append(make_p([
            (ev_title, True, False, 32, "000000"),
            (ev_desc, False, False, 32, "000000")
        ], align="both", space_before=0, space_after=10, line_spacing=240, first_line=720))

    # 6. การลงนามรับรอง
    elements.append(make_p([
        ("การลงนามรับรองรายงานผลการดำเนินงานประเด็นท้าทาย", True, False, 32, "000000")
    ], align="left", space_before=100, space_after=40, keep_next=True))

    sig_headers = [
        "คำรับรองของผู้รายงาน",
        "ความเห็นและคำรับรองของผู้บริหารสถานศึกษา"
    ]
    sig_rows = [
        [
            "ข้าพเจ้าขอรับรองว่ารายงานผลการดำเนินงานประเด็นท้าทายฉบับนี้ ได้ดำเนินการจัดการเรียนรู้และเก็บรวบรวมข้อมูลจริง ในภาคเรียนที่ 1 ปีการศึกษา 2569 ตรงตามข้อตกลงในการพัฒนางาน (PA 1) ทุกประการ\n\n(ลงชื่อ).....................................................................\n( นายเตชินท์  อินทมล )\nตำแหน่ง ครู (ไม่มีวิทยฐานะ)\nวันที่ ........ เดือน .............................. พ.ศ. 2569",
            "ได้ตรวจสอบรายงานผลการดำเนินงานประเด็นท้าทายแล้ว พบว่ามีกระบวนการดำเนินงานตามวงจร PDCA ถูกต้อง เหมาะสม มีผลลัพธ์เชิงประจักษ์ชัดเจน อนุมัติให้นำไปใช้ประกอบการประเมิน ว.PA และเลื่อนขั้นเงินเดือนได้\n\n(ลงชื่อ).....................................................................\n( ..................................................................... )\nตำแหน่ง ผู้อำนวยการโรงเรียนบ้านโนนป่าหว้านเชียงฮาย\nวันที่ ........ เดือน .............................. พ.ศ. 2569"
        ]
    ]
    elements.append(make_academic_table(sig_headers, sig_rows, [4500, 4500], ["left", "left"], bordered=True))

    # Wrap to DOCX
    doc_body = "".join(elements)

    content_types = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
</Types>"""

    rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>"""

    doc_rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>"""

    styles = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:docDefaults>
    <w:rPrDefault>
      <w:rPr>
        <w:rFonts w:ascii="TH Sarabun PSK" w:hAnsi="TH Sarabun PSK" w:cs="TH Sarabun PSK"/>
        <w:sz w:val="32"/>
        <w:szCs w:val="32"/>
        <w:lang w:val="th-TH" w:eastAsia="th-TH" w:bidi="th-TH"/>
      </w:rPr>
    </w:rPrDefault>
    <w:pPrDefault>
      <w:pPr>
        <w:jc w:val="both"/>
        <w:spacing w:line="240" w:lineRule="auto" w:before="0" w:after="0"/>
        <w:adjustRightInd w:val="0"/>
      </w:pPr>
    </w:pPrDefault>
  </w:docDefaults>
</w:styles>"""

    document_xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:body>
    {doc_body}
    <w:sectPr>
      <w:pgSz w:w="11906" w:h="16838"/>
      <w:pgMar w:top="1418" w:right="1134" w:bottom="1418" w:left="1701" w:header="720" w:footer="720" w:gutter="0"/>
      <w:cols w:space="720"/>
    </w:sectPr>
  </w:body>
</w:document>"""

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", content_types)
        z.writestr("_rels/.rels", rels)
        z.writestr("word/_rels/document.xml.rels", doc_rels)
        z.writestr("word/styles.xml", styles)
        z.writestr("word/document.xml", document_xml)

    data = buf.getvalue()
    path1 = "แบบรายงานผลการดำเนินงานประเด็นท้าทาย_วPA_ป5_ครูเตชินท์.docx"
    path2 = os.path.join("docs", "แบบรายงานผลการดำเนินงานประเด็นท้าทาย_วPA_ป5_ครูเตชินท์.docx")
    
    with open(path1, "wb") as f:
        f.write(data)
    with open(path2, "wb") as f:
        f.write(data)
        
    print(f"Official PA Challenge Issue Report Generated Successfully:\n- {path1}\n- {path2}")

if __name__ == "__main__":
    build_challenge_report_document()
