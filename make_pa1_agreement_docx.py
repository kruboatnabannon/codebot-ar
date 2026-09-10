# -*- coding: utf-8 -*-
"""
Official Performance Agreement Generator (แบบข้อตกลงในการพัฒนางาน PA 1/ส)
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

def build_pa1_agreement_document():
    elements = []

    # =========================================================================
    # 1. หน้าปกข้อตกลงในการพัฒนางาน (PA 1/ส)
    # =========================================================================
    elements.append(make_p([], align="center", space_before=300, space_after=100))
    elements.append(make_p([
        ("แบบข้อตกลงในการพัฒนางาน (PA)", True, False, 36, "000000")
    ], align="center", space_before=0, space_after=40))
    elements.append(make_p([
        ("สำหรับข้าราชการครูและบุคลากรทางการศึกษา ตำแหน่ง ครู (ไม่มีวิทยฐานะ)", True, False, 30, "000000"),
        ("\nประจำปีงบประมาณ พ.ศ. 2569", True, False, 30, "000000"),
        ("\nรอบการประเมิน ระหว่างวันที่ 1 ตุลาคม พ.ศ. 2568 ถึงวันที่ 30 กันยายน พ.ศ. 2569", False, False, 28, "000000")
    ], align="center", space_before=0, space_after=300, line_spacing=260))

    elements.append(make_p([
        ("ข้อตกลงในการพัฒนางานที่เป็นประเด็นท้าทาย", True, False, 34, "000000"),
        ("\nในการพัฒนาผลลัพธ์การเรียนรู้ของผู้เรียน", True, False, 34, "000000")
    ], align="center", space_before=40, space_after=100, line_spacing=260))

    elements.append(make_p([
        ("เรื่อง", True, False, 32, "000000")
    ], align="center", space_before=20, space_after=40))

    elements.append(make_p([
        ("การพัฒนาทักษะการเรียนรู้รายวิชาเทคโนโลยี (วิทยาการคำนวณ)", True, False, 32, "000000"),
        ("\nกลุ่มสาระการเรียนรู้วิทยาศาสตร์และเทคโนโลยี", True, False, 32, "000000"),
        ("\nโดยใช้กระบวนการ Gamebase learning ร่วมกับเทคนิคการสอนแบบ active learning", True, False, 32, "000000"),
        ("\nของนักเรียนชั้นประถมศึกษาปีที่ 5 โรงเรียนบ้านโนนป่าหว้านเชียงฮาย", True, False, 32, "000000")
    ], align="center", space_before=20, space_after=300, line_spacing=260))

    elements.append(make_p([
        ("ผู้จัดทำข้อตกลง", True, False, 32, "000000")
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
    # 2. เนื้อหาแบบข้อตกลงในการพัฒนางาน (PA 1/ส)
    # =========================================================================
    elements.append(make_p([
        ("แบบข้อตกลงในการพัฒนางาน (PA)", True, False, 34, "000000"),
        ("\nสำหรับข้าราชการครูและบุคลากรทางการศึกษา ตำแหน่ง ครู (ไม่มีวิทยฐานะ)", True, False, 32, "000000"),
        ("\nประจำปีงบประมาณ พ.ศ. 2569", True, False, 32, "000000")
    ], align="center", space_before=60, space_after=100, line_spacing=260, keep_next=True))

    elements.append(make_p([
        ("การจัดทำข้อตกลงในการพัฒนางาน (Performance Agreement : PA) จัดทำขึ้นระหว่าง นายเตชินท์ อินทมล ตำแหน่ง ครู (ไม่มีวิทยฐานะ) โรงเรียนบ้านโนนป่าหว้านเชียงฮาย สังกัดสำนักงานเขตพื้นที่การศึกษาประถมศึกษาหนองบัวลำภู เขต 2 กับ ผู้บริหารสถานศึกษาโรงเรียนบ้านโนนป่าหว้านเชียงฮาย สำหรับรอบการประเมิน ระหว่างวันที่ 1 ตุลาคม พ.ศ. 2568 ถึงวันที่ 30 กันยายน พ.ศ. 2569", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=30, line_spacing=240, first_line=720))

    # ข้อมูลผู้จัดทำข้อตกลง
    elements.append(make_p([
        ("ข้อมูลผู้จัดทำข้อตกลง", True, False, 32, "000000")
    ], align="left", space_before=40, space_after=20, keep_next=True))

    elements.append(make_p([
        ("ชื่อ - นามสกุล: ", True, False, 32, "000000"),
        ("นายเตชินท์  อินทมล", False, False, 32, "000000"),
        ("\nตำแหน่ง: ", True, False, 32, "000000"),
        ("ครู (ไม่มีวิทยฐานะ)", False, False, 32, "000000"),
        ("\nวิทยฐานะ: ", True, False, 32, "000000"),
        ("- (ไม่มีวิทยฐานะ)", False, False, 32, "000000"),
        ("\nสถานศึกษา: ", True, False, 32, "000000"),
        ("โรงเรียนบ้านโนนป่าหว้านเชียงฮาย", False, False, 32, "000000"),
        ("\nสังกัด: ", True, False, 32, "000000"),
        ("สำนักงานเขตพื้นที่การศึกษาประถมศึกษาหนองบัวลำภู เขต 2", False, False, 32, "000000"),
        ("\nกลุ่มสาระการเรียนรู้: ", True, False, 32, "000000"),
        ("วิทยาศาสตร์และเทคโนโลยี", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=30, line_spacing=240, first_line=720))

    # ภาระงานสอน
    elements.append(make_p([
        ("ภาระงานสอนตามที่ ก.ค.ศ. กำหนด (ปีงบประมาณ พ.ศ. 2569)", True, False, 32, "000000")
    ], align="left", space_before=40, space_after=20, keep_next=True))

    elements.append(make_p([
        ("1. ชั่วโมงสอนตามตารางสอน รวมทั้งสิ้น 16 ชั่วโมง/สัปดาห์ ได้แก่:", True, False, 32, "000000"),
        ("\n  • กลุ่มสาระการเรียนรู้วิทยาศาสตร์และเทคโนโลยี รายวิชาวิทยาการคำนวณ ชั้น ป.4-ป.6 จำนวน 3 ชั่วโมง/สัปดาห์", False, False, 32, "000000"),
        ("\n  • กลุ่มสาระการเรียนรู้วิทยาศาสตร์และเทคโนโลยี รายวิชาวิทยาศาสตร์ ชั้น ป.4-ป.6 จำนวน 9 ชั่วโมง/สัปดาห์", False, False, 32, "000000"),
        ("\n  • กิจกรรมพัฒนาผู้เรียน (ลูกเสือ-เนตรนารี, แนะแนว, ชุมนุม) จำนวน 4 ชั่วโมง/สัปดาห์", False, False, 32, "000000"),
        ("\n2. งานส่งเสริมและสนับสนุนการจัดการเรียนรู้ (การวัดผล, การจัดทำแผน, PLC) จำนวน 2 ชั่วโมง/สัปดาห์", True, False, 32, "000000"),
        ("\n3. งานพัฒนาคุณภาพการจัดการศึกษาของสถานศึกษา (งานวิชาการ, เทคโนโลยีสารสนเทศ) จำนวน 3 ชั่วโมง/สัปดาห์", True, False, 32, "000000"),
        ("\n4. งานตอบสนองนโยบายและจุดเน้น จำนวน 1 ชั่วโมง/สัปดาห์", True, False, 32, "000000"),
        ("\nรวมภาระงานทั้งสิ้น 22 ชั่วโมง/สัปดาห์ (เป็นไปตามที่ ก.ค.ศ. กำหนด)", True, False, 32, "000000")
    ], align="both", space_before=0, space_after=40, line_spacing=240, first_line=720))

    # =========================================================================
    # ส่วนที่ 1: ข้อตกลงตามมาตรฐานตำแหน่ง (3 ด้าน 15 ตัวชี้วัด)
    # =========================================================================
    elements.append(make_p([
        ("ส่วนที่ 1: ข้อตกลงในการพัฒนางานตามมาตรฐานตำแหน่ง", True, False, 34, "000000")
    ], align="left", space_before=60, space_after=20, keep_next=True))

    elements.append(make_p([
        ("ข้าพเจ้าได้กำหนดข้อตกลงในการพัฒนางานตามมาตรฐานตำแหน่งครู ครอบคลุมภารกิจ 3 ด้าน 15 ตัวชี้วัด ดังนี้:", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=20, line_spacing=240, first_line=720))

    # ด้านที่ 1
    elements.append(make_p([
        ("1. ด้านการจัดการเรียนรู้ (8 ตัวชี้วัด):", True, False, 32, "000000")
    ], align="left", space_before=20, space_after=10, keep_next=True))

    d1_items = [
        ("1.1 การพัฒนาหลักสูตร", "วิเคราะห์หลักสูตรแกนกลางฯ ตัวชี้วัด ว 4.2 ป.5 จัดทำโครงสร้างรายวิชาและหน่วยการเรียนรู้เรื่อง การใช้เหตุผลเชิงตรรกะและการเขียนโปรแกรมอย่างง่าย"),
        ("1.2 การออกแบบการจัดการเรียนรู้", "จัดทำแผนการจัดการเรียนรู้เชิงรุก (Active Learning) 7 แผน บูรณาการเกม CodeBot AR และโปรแกรม Scratch"),
        ("1.3 การจัดกิจกรรมการเรียนรู้", "จัดการเรียนรู้เชิงรุกโดยใช้เทคนิค Pair Programming (Driver & Navigator) ให้นักเรียนลงมือคิดและปฏิบัติตามสภาพจริง"),
        ("1.4 การสร้างและพัฒนาสื่อ นวัตกรรม", "พัฒนาเว็บเกม AR ร่วมกับชุดแฟลชการ์ดสัญลักษณ์จริง 18 ใบ เพื่อเป็นสะพานเชื่อมโยงรูปธรรมสู่นามธรรม"),
        ("1.5 การวัดและประเมินผลการเรียนรู้", "วัดผลรอบด้านด้วย Pre-test, Post-test, แบบประเมินรูบริกส์วัด CT 4 ด้าน และแบบสอบถามความพึงพอใจ"),
        ("1.6 การศึกษา วิเคราะห์ และสังเคราะห์", "จัดทำรายงานการวิจัยปฏิบัติการในชั้นเรียน (CAR) เพื่อแก้ไขปัญหาความสับสนทิศทางในการเขียนโปรแกรม"),
        ("1.7 การจัดบรรยากาศที่ส่งเสริมและพัฒนา", "สร้างบรรยากาศห้องเรียนคอมพิวเตอร์ที่สนุก ท้าทาย ไม่กลัวความผิดพลาด และส่งเสริมการแก้บั๊ก"),
        ("1.8 การอบรมและพัฒนาคุณลักษณะที่ดี", "ปลูกฝังความมีวินัย ความซื่อสัตย์ การทำงานร่วมกัน และการรับฟังความคิดเห็นผ่านกิจกรรมคู่หู")
    ]
    for code, desc in d1_items:
        elements.append(make_p([
            (f"• {code}: ", True, False, 32, "000000"),
            (desc, False, False, 32, "000000")
        ], align="both", space_before=0, space_after=10, line_spacing=240, first_line=720))

    # ด้านที่ 2
    elements.append(make_p([
        ("2. ด้านการส่งเสริมและสนับสนุนการจัดการเรียนรู้ (4 ตัวชี้วัด):", True, False, 32, "000000")
    ], align="left", space_before=20, space_after=10, keep_next=True))

    d2_items = [
        ("2.1 การจัดทำข้อมูลสารสนเทศของผู้เรียนและรายวิชา", "จัดทำระบบบันทึกคะแนนเก็บ ข้อมูลการเข้าเรียน และสารสนเทศผลสัมฤทธิ์รายบุคคลอย่างเป็นระบบ"),
        ("2.2 การดำเนินการตามระบบดูแลช่วยเหลือนักเรียน", "คัดกรองผู้เรียนรายบุคคล เยี่ยมบ้าน และให้คำปรึกษาช่วยเหลือนักเรียนที่มีปัญหาการเรียนรู้"),
        ("2.3 การปฏิบัติงานวิชาการและงานอื่นๆ ของสถานศึกษา", "ปฏิบัติหน้าที่ครูผู้สอน หัวหน้างานเทคโนโลยีสารสนเทศ (ICT) และงานฝ่ายวิชาการของโรงเรียน"),
        ("2.4 การประสานความร่วมมือกับผู้ปกครองและภาคีเครือข่าย", "ประสานงานกับผู้ปกครองผ่านการประชุมและกลุ่มไลน์ เพื่อติดตามและรายงานความก้าวหน้าของผู้เรียน")
    ]
    for code, desc in d2_items:
        elements.append(make_p([
            (f"• {code}: ", True, False, 32, "000000"),
            (desc, False, False, 32, "000000")
        ], align="both", space_before=0, space_after=10, line_spacing=240, first_line=720))

    # ด้านที่ 3
    elements.append(make_p([
        ("3. ด้านการพัฒนาตนเองและวิชาชีพ (3 ตัวชี้วัด):", True, False, 32, "000000")
    ], align="left", space_before=20, space_after=10, keep_next=True))

    d3_items = [
        ("3.1 การพัฒนาตนเองอย่างเป็นระบบและต่อเนื่อง", "เข้าร่วมการอบรมเชิงปฏิบัติการด้านวิทยาการคำนวณ Coding, AI, และนวัตกรรมดิจิทัลเพื่อการศึกษา"),
        ("3.2 การมีส่วนร่วมในการแลกเปลี่ยนเรียนรู้ทางวิชาชีพ (PLC)", "ร่วมกิจกรรม PLC ในโรงเรียนเพื่อสะท้อนคิด แลกเปลี่ยนเทคนิคการสอน และแก้ปัญหาการเรียนรู้"),
        ("3.3 การนำความรู้และทักษะมาใช้พัฒนาการจัดการเรียนรู้", "นำเทคนิค Game-based Learning และ Active Learning มาบูรณาการสร้างสรรค์นวัตกรรมสื่อการสอน")
    ]
    for code, desc in d3_items:
        elements.append(make_p([
            (f"• {code}: ", True, False, 32, "000000"),
            (desc, False, False, 32, "000000")
        ], align="both", space_before=0, space_after=10, line_spacing=240, first_line=720))

    elements.append(make_page_break())

    # =========================================================================
    # ส่วนที่ 2: ข้อตกลงประเด็นท้าทาย (CHALLENGE ISSUE AGREEMENT)
    # =========================================================================
    elements.append(make_p([
        ("ส่วนที่ 2: ข้อตกลงในการพัฒนางานที่เป็นประเด็นท้าทายในการพัฒนาผลลัพธ์การเรียนรู้ของผู้เรียน", True, False, 34, "000000")
    ], align="left", space_before=40, space_after=30, keep_next=True))

    elements.append(make_p([
        ("ประเด็นท้าทาย เรื่อง: ", True, False, 32, "000000"),
        ("การพัฒนาทักษะการเรียนรู้รายวิชาเทคโนโลยี (วิทยาการคำนวณ) กลุ่มสาระการเรียนรู้วิทยาศาสตร์และเทคโนโลยี โดยใช้กระบวนการ Gamebase learning ร่วมกับเทคนิคการสอนแบบ active learning ของนักเรียนชั้นประถมศึกษาปีที่ 5 โรงเรียนบ้านโนนป่าหว้านเชียงฮาย", True, False, 32, "000000")
    ], align="both", space_before=0, space_after=30, line_spacing=240, first_line=720))

    # 1. สภาพปัญหา
    elements.append(make_p([
        ("1. สภาพปัญหาการจัดการเรียนรู้และคุณภาพการเรียนรู้ของผู้เรียน", True, False, 32, "000000")
    ], align="left", space_before=40, space_after=20, keep_next=True))

    elements.append(make_p([
        ("จากสภาพการจัดการเรียนรู้ในรายวิชาวิทยาการคำนวณ และผลการประเมินคุณภาพผู้เรียนชั้นประถมศึกษาปีที่ 5 โรงเรียนบ้านโนนป่าหว้านเชียงฮาย ในปีการศึกษาที่ผ่านมา พบว่า สาระเทคโนโลยี (วิทยาการคำนวณ) หน่วยการเรียนรู้เรื่อง การใช้เหตุผลเชิงตรรกะและการเขียนโปรแกรมอย่างง่าย (ตามมาตรฐาน ว 4.2 ตัวชี้วัด ป.5/1 และ ป.5/2) เป็นเนื้อหาที่มีลักษณะเป็นนามธรรมและมีความซับซ้อนในการคิดเชิงตรรกะสูงขึ้น ส่งผลให้ผู้เรียนส่วนใหญ่ประสบปัญหาสำคัญ 3 ประการ ได้แก่ 1) ขาดความเข้าใจเชิงมโนทัศน์ สับสนเรื่องทิศทางซ้าย-ขวาเมื่อมุมมองของตัวละครกลับทิศ 2) ขาดทักษะการวางแผนและการคิดอย่างเป็นขั้นตอน มักแก้ปัญหาแบบสุ่มลองผิดลองถูก และ 3) ความเหลื่อมล้ำในการมีส่วนร่วมในกิจกรรมการเรียนรู้ นักเรียนที่กล้าแสดงออกมักมีบทบาทหลัก ส่วนนักเรียนที่คิดช้าหรือขาดความมั่นใจมักขาดโอกาสลงมือปฏิบัติจริง ข้าพเจ้าในฐานะครูผู้สอนจึงได้กำหนดประเด็นท้าทายนี้ขึ้น เพื่อพัฒนาทักษะการคิดเชิงคำนวณและผลสัมฤทธิ์ทางการเรียนของนักเรียนชั้นประถมศึกษาปีที่ 5 ภาคเรียนที่ 1 ปีการศึกษา 2569 จำนวน 8 คน ให้มีคุณภาพตามเกณฑ์มาตรฐานที่หลักสูตรกำหนด", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=30, line_spacing=240, first_line=720))

    # 2. วิธีการดำเนินการ
    elements.append(make_p([
        ("2. วิธีการดำเนินการให้บรรลุผล", True, False, 32, "000000")
    ], align="left", space_before=40, space_after=20, keep_next=True))

    elements.append(make_p([
        ("ข้าพเจ้าได้กำหนดแนวทางการดำเนินงานเพื่อขับเคลื่อนประเด็นท้าทายตามวงจรคุณภาพ PDCA ดังนี้:", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=10, line_spacing=240, first_line=720))

    elements.append(make_p([
        ("1) ขั้นวางแผน (Plan): ศึกษาและวิเคราะห์หลักสูตร มาตรฐานการเรียนรู้ และตัวชี้วัดกลุ่มสาระการเรียนรู้วิทยาศาสตร์และเทคโนโลยี (วิทยาการคำนวณ) ชั้นประถมศึกษาปีที่ 5 เพื่อออกแบบหน่วยการเรียนรู้และแผนการจัดการเรียนรู้เชิงรุก (Active Learning) ตลอดจนวางแผนออกแบบและพัฒนานวัตกรรมสื่อการเรียนรู้โดยใช้เกมเป็นฐาน (Game-based Learning) ร่วมกับเทคโนโลยีความเป็นจริงเสริม (Augmented Reality: AR) และจัดเตรียมเครื่องมือวัดและประเมินผลการเรียนรู้ ได้แก่ แบบทดสอบวัดผลสัมฤทธิ์ แบบประเมินทักษะการคิดเชิงคำนวณ และแบบสอบถามความพึงพอใจ โดยนำเข้าสู่กระบวนการแลกเปลี่ยนเรียนรู้ทางวิชาชีพ (PLC) เพื่อตรวจสอบและปรับปรุงก่อนนำไปใช้", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=10, line_spacing=240, first_line=720))
    elements.append(make_p([
        ("2) ขั้นปฏิบัติการ (Do): ชี้แจงวัตถุประสงค์และดำเนินการทดสอบก่อนเรียน (Pre-test) จากนั้นจัดการเรียนรู้ตามแผนการจัดการเรียนรู้เชิงรุก โดยบูรณาการนวัตกรรมเกมการเรียนรู้และเทคโนโลยี AR ร่วมกับกิจกรรมการเรียนรู้แบบร่วมมือ เพื่อให้นักเรียนได้ลงมือปฏิบัติจริง ฝึกทักษะการคิดวิเคราะห์ และการแก้ปัญหาอย่างเป็นขั้นตอน", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=10, line_spacing=240, first_line=720))
    elements.append(make_p([
        ("3) ขั้นตรวจสอบ (Check): สังเกตพฤติกรรมการเรียนรู้และประเมินทักษะการคิดเชิงคำนวณของผู้เรียนระหว่างจัดกิจกรรม ดำเนินการทดสอบหลังเรียน (Post-test) เพื่อวัดผลสัมฤทธิ์ทางการเรียน และประเมินความพึงพอใจของนักเรียนที่มีต่อการจัดกิจกรรมการเรียนรู้", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=10, line_spacing=240, first_line=720))
    elements.append(make_p([
        ("4) ขั้นปรับปรุงและพัฒนา (Act): วิเคราะห์และสรุปผลการประเมินเพื่อจัดทำรายงานผลการดำเนินงานประเด็นท้าทาย และรายงานการวิจัยในชั้นเรียน (CAR) พร้อมทั้งนำข้อสะท้อนคิดและผลการประเมินเข้าสู่วงแลกเปลี่ยนเรียนรู้ (PLC) เพื่อนำข้อเสนอแนะมาปรับปรุงและพัฒนาการจัดการเรียนรู้ให้มีประสิทธิภาพยิ่งขึ้นต่อไป", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=30, line_spacing=240, first_line=720))

    # 3. ผลลัพธ์ที่คาดหวัง
    elements.append(make_p([
        ("3. ผลลัพธ์การพัฒนาที่คาดหวัง", True, False, 32, "000000")
    ], align="left", space_before=40, space_after=20, keep_next=True))

    elements.append(make_p([
        ("3.1 ผลลัพธ์เชิงปริมาณ (Quantitative Expectations):", True, False, 32, "000000")
    ], align="left", space_before=10, space_after=10, keep_next=True))

    elements.append(make_p([
        ("1) นักเรียนชั้นประถมศึกษาปีที่ 5 ไม่น้อยกว่าร้อยละ 70 มีคะแนนผลสัมฤทธิ์ทางการเรียนรู้วิทยาการคำนวณหลังเรียนสูงกว่าก่อนเรียน", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=10, line_spacing=240, first_line=720))
    elements.append(make_p([
        ("2) นักเรียนชั้นประถมศึกษาปีที่ 5 ไม่น้อยกว่าร้อยละ 80 มีผลการประเมินทักษะการคิดเชิงคำนวณและการเขียนโปรแกรม ผ่านเกณฑ์ในระดับ “ดี” ขึ้นไป", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=20, line_spacing=240, first_line=720))

    elements.append(make_p([
        ("3.2 ผลลัพธ์เชิงคุณภาพ (Qualitative Expectations):", True, False, 32, "000000")
    ], align="left", space_before=10, space_after=10, keep_next=True))

    elements.append(make_p([
        ("1) นักเรียนมีความรู้ความเข้าใจในมโนทัศน์เชิงตรรกะ สามารถวิเคราะห์ แก้ปัญหา และเขียนโปรแกรมอย่างง่ายได้ตามลำดับขั้นตอนที่ถูกต้อง ไม่สับสนทิศทาง", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=10, line_spacing=240, first_line=720))
    elements.append(make_p([
        ("2) นักเรียนเกิดทักษะการคิดเชิงคำนวณ 4 ด้าน และทักษะแห่งศตวรรษที่ 21 (4 Cs) สามารถทำงานร่วมกับผู้อื่นได้อย่างมีประสิทธิภาพ และมีความสุขในการเรียนรู้", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=40, line_spacing=240, first_line=720))

    # ส่วนลงนามข้อตกลง (Signatures)
    elements.append(make_p([
        ("การลงนามข้อตกลงในการพัฒนางาน (PA)", True, False, 32, "000000")
    ], align="left", space_before=60, space_after=30, keep_next=True))

    sig_headers = [
        "ผู้จัดทำข้อตกลงในการพัฒนางาน",
        "ผู้เห็นชอบข้อตกลงในการพัฒนางาน"
    ]
    sig_rows = [
        [
            "(ลงชื่อ).....................................................................\n( นายเตชินท์  อินทมล )\nตำแหน่ง ครู (ไม่มีวิทยฐานะ)\nผู้จัดทำข้อตกลงในการพัฒนางาน\nวันที่ 1 เดือน ตุลาคม พ.ศ. 2568",
            "(ลงชื่อ).....................................................................\n( ..................................................................... )\nตำแหน่ง ผู้อำนวยการโรงเรียนบ้านโนนป่าหว้านเชียงฮาย\nผู้เห็นชอบข้อตกลงในการพัฒนางาน\nวันที่ 1 เดือน ตุลาคม พ.ศ. 2568"
        ]
    ]
    elements.append(make_academic_table(sig_headers, sig_rows, [4500, 4500], ["left", "left"], bordered=True))
    elements.append(make_p([], space_before=20, space_after=20))

    elements.append(make_p([
        ("ความเห็นของผู้บริหารสถานศึกษา:", True, False, 30, "000000")
    ], align="left", space_before=10, space_after=10))
    elements.append(make_p([
        ("(  ) เห็นชอบ ให้เป็นข้อตกลงในการพัฒนางาน (PA) ประจำปีงบประมาณ พ.ศ. 2569", False, False, 30, "000000")
    ], align="left", space_before=0, space_after=10, first_line=720))
    elements.append(make_p([
        ("(  ) ไม่เห็นชอบ เนื่องจาก .............................................................................................................................................................", False, False, 30, "000000")
    ], align="left", space_before=0, space_after=20, first_line=720))

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
    path1 = "แบบข้อตกลงในการพัฒนางาน_PA1_ป5_ครูเตชินท์.docx"
    path2 = os.path.join("docs", "แบบข้อตกลงในการพัฒนางาน_PA1_ป5_ครูเตชินท์.docx")
    
    with open(path1, "wb") as f:
        f.write(data)
    with open(path2, "wb") as f:
        f.write(data)
        
    print(f"Official PA 1 Agreement Document Generated Successfully:\n- {path1}\n- {path2}")

if __name__ == "__main__":
    build_pa1_agreement_document()
