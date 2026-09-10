# -*- coding: utf-8 -*-
"""
Full clean rebuild of make_full_car_docx.py with:
1. Automatic Node.js Thai word segmentation (ZWSP \u200b) for seamless wrapping
2. Official Thai Government / OBEC Academic Document Standard:
   - Margins: Left 3.0 cm (1701), Right 2.0 cm (1134), Top 2.5 cm (1418), Bottom 2.5 cm (1418)
   - Font: TH Sarabun PSK throughout
   - Body: 16 pt (sz=32), Headings: 16-18 pt Bold
   - Line Spacing: 1.0 (240 Single)
   - Indent: 1 Tab (720 dxa = 1.27 cm)
   - Justification: w:jc both (Thai justified without gaps, words broken naturally)
   - No black bullets (•) on numbered items (1., 2., 1), 2) etc.)
   - Clean subheadings with underline where appropriate (e.g. ผลลัพธ์ (Outcome))
"""

script_content = '''# -*- coding: utf-8 -*-
import zipfile, io, os, html, subprocess, json

def esc(text):
    if text is None:
        return ""
    return html.escape(str(text))

# Global Thai segmentation cache & function using Node.js Intl.Segmenter
_seg_cache = {}

def add_thai_breaks(text):
    if not text or not isinstance(text, str):
        return text
    if text in _seg_cache:
        return _seg_cache[text]
    # Check if string contains Thai characters
    has_thai = any('\\u0e00' <= ch <= '\\u0e7f' for ch in text)
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
            if (!/\\\\s/.test(curr) && !/\\\\s/.test(next)) {
                if (/^[\\\\d.,]+$/.test(curr) && /^[\\\\d.,]+$/.test(next)) {
                    // number
                } else if (/^[0-9]+$/.test(curr) && next === '.') {
                    // 1.
                } else {
                    res += '\\\\u200b';
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

def make_p(runs, align="both", space_before=0, space_after=0, line_spacing=240, first_line=0, left_indent=0, hanging=0, keep_next=False):
    """
    Creates a Word paragraph formatted strictly according to Thai official academic standards.
    """
    p_pr = []
    
    # Justification
    p_pr.append(f'<w:jc w:val="{align}"/>')
    
    # Spacing (Official standard: line 240 = single line, minimal before/after)
    p_pr.append(f'<w:spacing w:before="{space_before}" w:after="{space_after}" w:line="{line_spacing}" w:lineRule="auto"/>')
    
    # Indentation
    if hanging > 0:
        p_pr.append(f'<w:ind w:left="{left_indent}" w:hanging="{hanging}"/>')
    elif first_line > 0 or left_indent > 0:
        p_pr.append(f'<w:ind w:left="{left_indent}" w:firstLine="{first_line}"/>')
        
    # Prevent orphan headings
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
        
        # Apply Thai ZWSP word segmentation to text
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
        
        # If align is center (e.g. cover page), handle explicit newlines
        if align == "center" and "\\n" in segmented_t:
            parts = segmented_t.split("\\n")
            for idx, part in enumerate(parts):
                if part:
                    runs_xml.append(f'<w:r><w:rPr>{"".join(r_pr)}</w:rPr><w:t xml:space="preserve">{esc(part)}</w:t></w:r>')
                if idx < len(parts) - 1:
                    runs_xml.append(f'<w:r><w:rPr>{"".join(r_pr)}</w:rPr><w:br/></w:r>')
        else:
            # Replace any accidental internal newlines with space
            cleaned_t = " ".join(part.strip() for part in segmented_t.split("\\n") if part.strip())
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
        h_parts = h_segmented.split("\\n")
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
            v_parts = val_segmented.split("\\n")
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

def build_car_document():
    elements = []

    # =========================================================================
    # 1. ปกรายงานการวิจัย (FORMAL ACADEMIC COVER PAGE)
    # =========================================================================
    elements.append(make_p([], align="center", space_before=400, space_after=100))
    elements.append(make_p([
        ("รายงานการวิจัยปฏิบัติการในชั้นเรียน", True, False, 36, "000000")
    ], align="center", space_before=0, space_after=40))
    elements.append(make_p([
        ("(Classroom Action Research : CAR)", True, False, 30, "000000")
    ], align="center", space_before=0, space_after=300))

    elements.append(make_p([
        ("เรื่อง", True, False, 34, "000000")
    ], align="center", space_before=60, space_after=60))

    elements.append(make_p([
        ("การพัฒนาทักษะการเรียนรู้วิทยาการคำนวณ", True, False, 32, "000000"),
        ("\\nโดยใช้กระบวนการ Game Based Learning (CodeBot AR Adventure)", True, False, 32, "000000"),
        ("\\nร่วมกับ Active Learning (Pair Programming)", True, False, 32, "000000"),
        ("\\nของนักเรียนชั้นประถมศึกษาปีที่ 5 โรงเรียนบ้านโนนป่าหว้านเชียงฮาย", True, False, 32, "000000")
    ], align="center", space_before=40, space_after=300, line_spacing=260))

    elements.append(make_p([
        ("เอกสารประกอบการประเมินการพัฒนางานตามข้อตกลง (ว.PA)", False, True, 28, "000000"),
        ("\\nและประกอบการประเมินประสิทธิภาพและประสิทธิผลการปฏิบัติงานเพื่อเลื่อนขั้นเงินเดือน", False, True, 28, "000000")
    ], align="center", space_before=40, space_after=400, line_spacing=260))

    elements.append(make_p([
        ("โดย", True, False, 32, "000000")
    ], align="center", space_before=60, space_after=40))

    elements.append(make_p([
        ("นายเตชินท์  อินทมล", True, False, 32, "000000"),
        ("\\nตำแหน่ง ครู (ไม่มีวิทยฐานะ)", False, False, 30, "000000"),
        ("\\nกลุ่มสาระการเรียนรู้วิทยาศาสตร์และเทคโนโลยี", False, False, 30, "000000")
    ], align="center", space_before=0, space_after=300, line_spacing=260))

    elements.append(make_p([
        ("โรงเรียนบ้านโนนป่าหว้านเชียงฮาย", True, False, 32, "000000"),
        ("\\nสำนักงานเขตพื้นที่การศึกษาประถมศึกษาหนองบัวลำภู เขต 2", False, False, 30, "000000"),
        ("\\nสำนักงานคณะกรรมการการศึกษาขั้นพื้นฐาน กระทรวงศึกษาธิการ", False, False, 30, "000000"),
        ("\\nภาคเรียนที่ 1 ปีการศึกษา 2569", True, False, 30, "000000")
    ], align="center", space_before=0, space_after=100, line_spacing=260))

    # Page Break to Abstract
    elements.append(make_page_break())

    # =========================================================================
    # 2. บทคัดย่อ (ABSTRACT)
    # =========================================================================
    elements.append(make_p([
        ("บทคัดย่อ", True, False, 36, "000000")
    ], align="center", space_before=100, space_after=140, keep_next=True))

    elements.append(make_p([
        ("ชื่อเรื่องวิจัย: ", True, False, 30, "000000"),
        ("การพัฒนาทักษะการเรียนรู้วิทยาการคำนวณ โดยใช้กระบวนการ Game Based Learning (CodeBot AR Adventure) ร่วมกับ Active Learning (Pair Programming) ของนักเรียนชั้นประถมศึกษาปีที่ 5 โรงเรียนบ้านโนนป่าหว้านเชียงฮาย", False, False, 30, "000000")
    ], align="both", space_before=0, space_after=20, line_spacing=240, left_indent=0))

    elements.append(make_p([
        ("ชื่อผู้วิจัย: ", True, False, 30, "000000"),
        ("นายเตชินท์  อินทมล        ", False, False, 30, "000000"),
        ("ตำแหน่ง: ", True, False, 30, "000000"),
        ("ครู (ไม่มีวิทยฐานะ)", False, False, 30, "000000")
    ], align="left", space_before=0, space_after=20, line_spacing=240))

    elements.append(make_p([
        ("หน่วยงาน: ", True, False, 30, "000000"),
        ("โรงเรียนบ้านโนนป่าหว้านเชียงฮาย สำนักงานเขตพื้นที่การศึกษาประถมศึกษาหนองบัวลำภู เขต 2", False, False, 30, "000000")
    ], align="left", space_before=0, space_after=20, line_spacing=240))

    elements.append(make_p([
        ("ปีการศึกษา: ", True, False, 30, "000000"),
        ("ภาคเรียนที่ 1 ปีการศึกษา 2569 (รอบการประเมินข้อตกลงในการพัฒนางาน ว.PA)", False, False, 30, "000000")
    ], align="left", space_before=0, space_after=80, line_spacing=240))

    # Abstract Paragraph 1
    elements.append(make_p([
        ("การวิจัยปฏิบัติการในชั้นเรียน (Classroom Action Research: CAR) ครั้งนี้ มีวัตถุประสงค์เพื่อ: 1) เปรียบเทียบผลสัมฤทธิ์ทางการเรียนรู้วิทยาการคำนวณ เรื่อง การใช้เหตุผลเชิงตรรกะและการเขียนโปรแกรมอย่างง่าย ของนักเรียนชั้นประถมศึกษาปีที่ 5 ก่อนและหลังการจัดการเรียนรู้ 2) ประเมินทักษะการคิดเชิงคำนวณ (Computational Thinking: CT) 4 ด้าน และทักษะแห่งศตวรรษที่ 21 (4 Cs) และ 3) ศึกษาความพึงพอใจของนักเรียนที่มีต่อการจัดกิจกรรมการเรียนรู้ กลุ่มเป้าหมายเป็นนักเรียนชั้นประถมศึกษาปีที่ 5 โรงเรียนบ้านโนนป่าหว้านเชียงฮาย สังกัดสำนักงานเขตพื้นที่การศึกษาประถมศึกษาหนองบัวลำภู เขต 2 ภาคเรียนที่ 1 ปีการศึกษา 2569 จำนวน 8 คน (ชาย 1 คน, หญิง 7 คน) ดำเนินการจัดการเรียนรู้เชิงรุก (Active Learning) แบบจับคู่เขียนโปรแกรม (Pair Programming) จำนวน 4 คู่ เครื่องมือที่ใช้ในการวิจัยประกอบด้วย แผนการจัดการเรียนรู้เชิงรุก จำนวน 7 แผน รวม 7 ชั่วโมง สื่อนวัตกรรมเกมโต้ตอบท่าทางเสมือนจริง CodeBot AR Adventure ร่วมกับชุดแฟลชการ์ดสัญลักษณ์จริง การเขียนโปรแกรมด้วยโปรแกรม Scratch แบบทดสอบวัดผลสัมฤทธิ์ทางการเรียนรู้ปรนัย 4 ตัวเลือก 20 ข้อ แบบประเมินรูบริกส์ทักษะการคิดเชิงคำนวณ และแบบสอบถามความพึงพอใจ สถิติที่ใช้ในการวิเคราะห์ข้อมูล ได้แก่ ค่าเฉลี่ย ส่วนเบี่ยงเบนมาตรฐาน ร้อยละ และการทดสอบค่าทีแบบไม่อิสระ (Paired Samples t-test)", False, False, 30, "000000")
    ], align="both", space_before=0, space_after=40, line_spacing=240, first_line=720))

    # Abstract Paragraph 2: Results
    elements.append(make_p([
        ("ผลการวิจัยพบว่า:", True, False, 30, "000000")
    ], align="left", space_before=20, space_after=20, line_spacing=240, first_line=720))

    elements.append(make_p([
        ("1. ผลสัมฤทธิ์ทางการเรียนรู้วิทยาการคำนวณของนักเรียนชั้นประถมศึกษาปีที่ 5 หลังเรียน (X̄ = 17.13, S.D. = 1.36 คิดเป็นร้อยละ 85.63) สูงกว่าก่อนเรียน (X̄ = 9.25, S.D. = 1.67 คิดเป็นร้อยละ 46.25) อย่างมีนัยสำคัญทางสถิติที่ระดับ .05 (t = 29.74, p < .001) โดยมีคะแนนพัฒนาการเฉลี่ยเพิ่มขึ้น 7.88 คะแนน คิดเป็นร้อยละพัฒนาการ 39.38%", False, False, 30, "000000")
    ], align="both", space_before=0, space_after=20, line_spacing=240, first_line=720))

    elements.append(make_p([
        ("2. ทักษะการคิดเชิงคำนวณ (CT 4 ด้าน) ของนักเรียนทุกคนอยู่ในระดับ “ดีมาก” (X̄ = 3.63 จากคะแนนเต็ม 4.00 หรือร้อยละ 90.75) และเกิดการพัฒนาทักษะแห่งศตวรรษที่ 21 (4 Cs) อย่างเด่นชัด โดยเฉพาะด้านการทำงานร่วมกัน (Collaboration) และการคิดวิเคราะห์แก้ไขปัญหา (Critical Thinking)", False, False, 30, "000000")
    ], align="both", space_before=0, space_after=20, line_spacing=240, first_line=720))

    elements.append(make_p([
        ("3. ความพึงพอใจของนักเรียนที่มีต่อการจัดกิจกรรมการเรียนรู้เชิงรุกด้วยเกม CodeBot AR อยู่ในระดับ “มากที่สุด” (X̄ = 4.75, S.D. = 0.37)", False, False, 30, "000000")
    ], align="both", space_before=0, space_after=20, line_spacing=240, first_line=720))

    elements.append(make_p([
        ("4. การดำเนินงานวิจัยครั้งนี้มีผลการปฏิบัติงานเชิงประจักษ์ที่สอดคล้องตามข้อตกลงในการพัฒนางาน (PA 1) ครอบคลุมเกณฑ์การประเมิน ว.PA ด้านที่ 1 ด้านการจัดการเรียนรู้ ครบทั้ง 8 ตัวชี้วัด อย่างครบถ้วน", False, False, 30, "000000")
    ], align="both", space_before=0, space_after=60, line_spacing=240, first_line=720))

    elements.append(make_p([
        ("คำสำคัญ: ", True, False, 30, "000000"),
        ("วิทยาการคำนวณ, เกม CodeBot AR Adventure, การคิดเชิงคำนวณ (CT), ทักษะแห่งศตวรรษที่ 21 (4 Cs), การจับคู่เขียนโปรแกรม (Pair Programming), โปรแกรม Scratch, ว.PA", False, False, 30, "000000")
    ], align="left", space_before=20, space_after=60, line_spacing=240))

    # Page Break to Main Report Content
    elements.append(make_page_break())

    # =========================================================================
    # 3. เนื้อหารายงานวิจัย (MAIN RESEARCH REPORT)
    # =========================================================================

    # SECTION 1
    elements.append(make_p([
        ("1. ความเป็นมาและความสำคัญของปัญหา", True, False, 32, "000000")
    ], align="left", space_before=140, space_after=40, keep_next=True))

    elements.append(make_p([
        ("ตามหลักสูตรแกนกลางการศึกษาขั้นพื้นฐาน พุทธศักราช 2551 (ฉบับปรับปรุง พ.ศ. 2560) กลุ่มสาระการเรียนรู้วิทยาศาสตร์และเทคโนโลยี มาตรฐาน ว 4.2 ระดับชั้นประถมศึกษาปีที่ 5 กำหนดตัวชี้วัดสำคัญไว้ 2 ข้อ ได้แก่ “ใช้เหตุผลเชิงตรรกะในการแก้ปัญหา การอธิบายการทำงาน การคาดการณ์ผลลัพธ์จากปัญหาอย่างง่าย” (ว 4.2 ป.5/1) และ “ออกแบบและเขียนโปรแกรมที่มีการใช้เหตุผลเชิงตรรกะอย่างง่าย ตรวจหาข้อผิดพลาดและแก้ไข” (ว 4.2 ป.5/2)", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=20, line_spacing=240, first_line=720))

    elements.append(make_p([
        ("จากการจัดทำข้อตกลงในการพัฒนางาน (PA 1) ที่ผู้วิจัยได้สำรวจสภาพปัญหาการจัดการเรียนรู้ของนักเรียนกลุ่มนี้ตั้งแต่ช่วงปลายปีการศึกษา 2567 ต่อเนื่องต้นปีงบประมาณ 2568 (ขณะที่ผู้เรียนกำลังศึกษาอยู่ในระดับชั้นประถมศึกษาปีที่ 4) พบว่าผู้เรียนมีปัญหาสำคัญด้านทักษะการคิดแก้ปัญหาและการเขียนโปรแกรมอย่างง่าย ผู้วิจัยจึงได้กำหนดประเด็นท้าทายเพื่อพัฒนาผู้เรียนกลุ่มนี้อย่างต่อเนื่อง เมื่อนักเรียนเลื่อนชั้นขึ้นมาเรียนในระดับชั้นประถมศึกษาปีที่ 5 โรงเรียนบ้านโนนป่าหว้านเชียงฮาย ภาคเรียนที่ 1 ปีการศึกษา 2569 (จำนวน 8 คน) ผู้วิจัยจึงได้นำประเด็นท้าทายดังกล่าวมาดำเนินการตามวงจรคุณภาพ PDCA ซึ่งจากการจัดการเรียนรู้พบว่าเนื้อหาของ ป.5 แม้ไม่ได้ซับซ้อนเกินวัย แต่ในทางปฏิบัติในห้องเรียนยังคงพบปัญหาสำคัญ 3 ประการ ดังนี้", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=20, line_spacing=240, first_line=720))

    elements.append(make_p([
        ("1) ปัญหานามธรรมและความสับสนเรื่องทิศทาง (Spatial Confusion): ", True, False, 32, "000000"),
        ("นักเรียนชั้น ป.5 มักสับสนทิศทางซ้าย-ขวา โดยเฉพาะเมื่อมุมมองของตัวละครหรือหุ่นยนต์ในจอภาพหันหน้ากลับทิศกับตัวนักเรียน ทำให้นักเรียนนึกภาพไม่ออกและออกคำสั่งเลี้ยวผิดทิศทางอยู่บ่อยครั้ง", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=20, line_spacing=240, first_line=720))

    elements.append(make_p([
        ("2) ขาดการคิดวางแผนเป็นขั้นตอน (Trial and Error): ", True, False, 32, "000000"),
        ("นักเรียนมักไม่วางแผนลำดับขั้นตอนก่อนลงมือปฏิบัติ แต่มักจะคลิกหน้าจอแบบสุ่มลองผิดลองถูกไปเรื่อยๆ เมื่อหุ่นยนต์เดินชนสิ่งกีดขวางก็ไม่ทราบว่าผิดพลาดที่คำสั่งใด และมักเลือกกดลบคำสั่งทั้งหมดแล้วเริ่มต้นใหม่แทนที่จะตรวจหาจุดผิดพลาดและแก้ไขทีละคำสั่ง", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=20, line_spacing=240, first_line=720))

    elements.append(make_p([
        ("3) พฤติกรรมการมีส่วนร่วมในการเรียนรู้: ", True, False, 32, "000000"),
        ("ในการทำงานร่วมกันหน้าเครื่องคอมพิวเตอร์ นักเรียนที่กล้าแสดงออกมักแย่งจับเมาส์และลงมือทำเองคนเดียวทั้งหมด ในขณะที่นักเรียนที่คิดช้าหรือไม่มั่นใจจะถอยมานั่งดูเฉยๆ ขาดโอกาสในการฝึกคิดวิเคราะห์และลงมือปฏิบัติจริง", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=20, line_spacing=240, first_line=720))

    elements.append(make_p([
        ("เพื่อแก้ปัญหาดังกล่าวให้สอดคล้องกับข้อตกลงในการพัฒนางาน (PA 1) ที่ได้กำหนดไว้ ผู้วิจัยจึงได้ออกแบบการจัดการเรียนรู้เชิงรุก (Active Learning) จำนวน 7 แผนการจัดการเรียนรู้ (รวม 7 ชั่วโมง) โดยนำนวัตกรรมเกม “CodeBot AR Adventure” ร่วมกับ “ชุดแฟลชการ์ดคำสั่งสัญลักษณ์จริง” มาเป็นสะพานเชื่อมโยงรูปธรรม (Concrete Scaffolding) เพื่อฝึกทักษะการคิดเชิงคำนวณและแก้ปัญหาความสับสนในลำดับขั้นตอน ก่อนส่งต่อและถ่ายโอนความรู้ไปสู่ “การเขียนโปรแกรมด้วยโปรแกรม Scratch: ภารกิจช่วยตัวละครหาทางออก” ตามเป้าหมายที่กำหนดไว้ในข้อตกลง PA 1 อย่างครบถ้วน โดยใช้เทคนิคการสอนเชิงรุกแบบ Pair Programming (Driver & Navigator) ทำให้นักเรียนทุกคนเข้าใจตรรกะและเหตุผลเชิงตรรกะอย่างแท้จริง จึงได้จัดทำรายงานการวิจัยปฏิบัติการในชั้นเรียนเล่มนี้ขึ้น เพื่อรายงานผลสัมฤทธิ์และผลการพัฒนานวัตกรรมอย่างเป็นระบบ", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=40, line_spacing=240, first_line=720))

    # SECTION 2
    elements.append(make_p([
        ("2. วัตถุประสงค์การวิจัย", True, False, 32, "000000")
    ], align="left", space_before=140, space_after=40, keep_next=True))

    elements.append(make_p([
        ("1. เพื่อเปรียบเทียบผลสัมฤทธิ์ทางการเรียนรู้วิทยาการคำนวณ เรื่อง การใช้เหตุผลเชิงตรรกะและการเขียนโปรแกรมอย่างง่าย ของนักเรียนชั้นประถมศึกษาปีที่ 5 ก่อนและหลังการจัดการเรียนรู้โดยใช้กระบวนการ Game Based Learning ร่วมกับ Active Learning", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=20, line_spacing=240, first_line=720))

    elements.append(make_p([
        ("2. เพื่อประเมินทักษะการคิดเชิงคำนวณอย่างง่าย 4 ด้าน (การย่อยปัญหา, การหารูปแบบ, การคิดเชิงนามธรรม, และการออกแบบอัลกอริทึม) ของนักเรียนชั้นประถมศึกษาปีที่ 5", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=20, line_spacing=240, first_line=720))

    elements.append(make_p([
        ("3. เพื่อศึกษาความพึงพอใจของนักเรียนชั้นประถมศึกษาปีที่ 5 ที่มีต่อการจัดกิจกรรมการเรียนรู้โดยใช้นวัตกรรมเกม CodeBot AR Adventure ร่วมกับเทคนิค Pair Programming", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=40, line_spacing=240, first_line=720))

    # SECTION 3
    elements.append(make_p([
        ("3. สมมติฐานการวิจัย", True, False, 32, "000000")
    ], align="left", space_before=140, space_after=40, keep_next=True))

    elements.append(make_p([
        ("1. นักเรียนชั้นประถมศึกษาปีที่ 5 มีคะแนนผลสัมฤทธิ์ทางการเรียนรู้วิทยาการคำนวณหลังเรียนสูงกว่าก่อนเรียน อย่างมีนัยสำคัญทางสถิติที่ระดับ .05", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=20, line_spacing=240, first_line=720))

    elements.append(make_p([
        ("2. นักเรียนชั้นประถมศึกษาปีที่ 5 ทุกคนมีผลการประเมินทักษะการคิดเชิงคำนวณอย่างง่าย ผ่านเกณฑ์การประเมินตามเกณฑ์รูบริกส์ในระดับ “ดี” ขึ้นไป", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=20, line_spacing=240, first_line=720))

    elements.append(make_p([
        ("3. นักเรียนชั้นประถมศึกษาปีที่ 5 มีความพึงพอใจต่อการจัดกิจกรรมการเรียนรู้อยู่ในระดับ “มากที่สุด”", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=40, line_spacing=240, first_line=720))

    # SECTION 4
    elements.append(make_p([
        ("4. ขอบเขตการวิจัย", True, False, 32, "000000")
    ], align="left", space_before=140, space_after=40, keep_next=True))

    elements.append(make_p([
        ("4.1 ด้านกลุ่มเป้าหมาย: ", True, False, 32, "000000"),
        ("นักเรียนชั้นประถมศึกษาปีที่ 5 โรงเรียนบ้านโนนป่าหว้านเชียงฮาย สำนักงานเขตพื้นที่การศึกษาประถมศึกษาหนองบัวลำภู เขต 2 ภาคเรียนที่ 1 ปีการศึกษา 2569 จำนวน 8 คน (ชาย 1 คน, หญิง 7 คน) โดยจัดการเรียนรู้แบบจับคู่เขียนโปรแกรม (Pair Programming) จำนวน 4 คู่ ดังแสดงในตาราง", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=30, line_spacing=240, first_line=720))

    t_students_headers = ["เลขที่", "เลขประจำตัว", "เลขประจำตัวประชาชน", "ชื่อ - สกุล นักเรียน", "เพศ", "กลุ่มคู่หู Pair Programming"]
    t_students_rows = [
        ["1", "2040", "1399900568996", "เด็กชายภูฟ้า  แสงศรี", "ชาย", "คู่ที่ 1 (คู่กับเลขที่ 8)"],
        ["2", "2045", "1104301574244", "เด็กหญิงพิชญาภา  แสงศรี", "หญิง", "คู่ที่ 2 (คู่กับเลขที่ 5)"],
        ["3", "2048", "1399900557625", "เด็กหญิงสิริวิมล  สาวิสิทธิ์", "หญิง", "คู่ที่ 3 (คู่กับเลขที่ 7)"],
        ["4", "2047", "1399900558486", "เด็กหญิงสาวิตรี  สายสมคุณ", "หญิง", "คู่ที่ 4 (คู่กับเลขที่ 6)"],
        ["5", "2044", "1399900563943", "เด็กหญิงณัฐณิชา  นันทโพธิ์เดช", "หญิง", "คู่ที่ 2 (คู่กับเลขที่ 2)"],
        ["6", "2046", "1390501131251", "เด็กหญิงรฐา  สอนเต็ม", "หญิง", "คู่ที่ 4 (คู่กับเลขที่ 4)"],
        ["7", "2043", "1399000122592", "เด็กหญิงกัญญาพัชร  วาจาชื่น", "หญิง", "คู่ที่ 3 (คู่กับเลขที่ 3)"],
        ["8", "2177", "1399900561720", "เด็กหญิงกัญญารัตน์  บัวบง", "หญิง", "คู่ที่ 1 (คู่กับเลขที่ 1)"]
    ]
    elements.append(make_academic_table(t_students_headers, t_students_rows, [650, 1150, 2000, 2400, 700, 2100], ["center", "center", "center", "left", "center", "center"]))
    elements.append(make_p([], space_before=20, space_after=30))

    elements.append(make_p([
        ("4.2 ด้านเนื้อหาสาระ: ", True, False, 32, "000000"),
        ("รายวิชาพื้นฐานวิทยาศาสตร์และเทคโนโลยี เทคโนโลยี (วิทยาการคำนวณ) รหัสวิชา ว15101 ชั้นประถมศึกษาปีที่ 5 หน่วยการเรียนรู้: การใช้เหตุผลเชิงตรรกะและการเขียนโปรแกรมอย่างง่าย (การนับก้าวระบุทิศทาง, การวนซ้ำ Loop, เงื่อนไข ถ้า...แล้ว, และการตรวจหาข้อผิดพลาดของโปรแกรม)", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=20, line_spacing=240, first_line=720))

    elements.append(make_p([
        ("4.3 ด้านตัวแปรที่ศึกษา: ", True, False, 32, "000000")
    ], align="left", space_before=0, space_after=20, line_spacing=240, first_line=720))

    elements.append(make_p([
        ("1) ตัวแปรต้น: การจัดการเรียนรู้โดยใช้กระบวนการ Game Based Learning (CodeBot AR Adventure) ร่วมกับ Active Learning (Pair Programming) และชุดแฟลชการ์ดสัญลักษณ์จริง", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=20, line_spacing=240, first_line=1080))

    elements.append(make_p([
        ("2) ตัวแปรตาม: ได้แก่ 1) ผลสัมฤทธิ์ทางการเรียนรู้วิทยาการคำนวณ 2) ทักษะการคิดเชิงคำนวณ 4 ด้าน (CT) 3) ทักษะแห่งศตวรรษที่ 21 (4 Cs: Critical Thinking, Creativity, Collaboration, Communication) และ 4) ความพึงพอใจของนักเรียน", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=20, line_spacing=240, first_line=1080))

    elements.append(make_p([
        ("4.4 ด้านระยะเวลา: ", True, False, 32, "000000"),
        ("ดำเนินการในภาคเรียนที่ 1 ปีการศึกษา 2569 จำนวน 7 แผนการจัดการเรียนรู้ สัปดาห์ละ 1 ชั่วโมง รวมทั้งสิ้น 7 ชั่วโมง สอดคล้องตามกรอบเวลาในข้อตกลงในการพัฒนางาน (PA 1)", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=40, line_spacing=240, first_line=720))

    # SECTION 5
    elements.append(make_p([
        ("5. กรอบแนวคิดการวิจัย (Conceptual Framework)", True, False, 32, "000000")
    ], align="left", space_before=140, space_after=40, keep_next=True))

    framework_table_headers = [
        "ตัวแปรต้น\\n(สื่อนวัตกรรม & เทคนิคการสอน)",
        "กระบวนการจัดกิจกรรม\\n(Active Learning)",
        "ตัวแปรตาม\\n(ผลลัพธ์การเรียนรู้ ป.5)"
    ]
    framework_table_row = [
        [
            "1. เกม CodeBot AR Adventure\\n  - ภาพจำลองตารางกริดที่ชัดเจน\\n  - ท่าทางหน้ากล้อง (Kinesthetic)\\n  - ระบบภารกิจสะสมดาว 3 ดวง\\n\\n2. สื่อแฟลชการ์ดสัญลักษณ์จริง\\n  - บัตรคำสั่งรูปธรรมบนโต๊ะ\\n\\n3. เทคนิค Pair Programming\\n  - แบ่ง 4 คู่ (Navigator & Driver)",
            "1. ขั้นนำเข้าสู่บทเรียน\\n  - กระตุ้นความสนใจด้วยภารกิจ\\n\\n2. ขั้นการเรียนรู้เชิงรุก\\n  - วางแผนเส้นทาง (Navigator)\\n  - เรียงบัตรคำสั่งบนโต๊ะ\\n  - ป้อนท่าทางหน้ากล้อง (Driver)\\n  - สลับบทบาทคู่หูตามรอบ\\n\\n3. ขั้นสะท้อนคิดและสรุป\\n  - ตรวจหาข้อผิดพลาด (Debug)\\n  - ถอดบทเรียน AAR ประจำชั่วโมง",
            "1. ผลสัมฤทธิ์ทางการเรียนรู้\\n  - คะแนนสอบ 20 ข้อ (Pre/Post)\\n\\n2. ทักษะการคิดเชิงคำนวณ (CT)\\n  - การย่อยปัญหา (Decomposition)\\n  - การหารูปแบบ (Pattern)\\n  - คิดเชิงนามธรรม (Abstraction)\\n  - ออกแบบขั้นตอน (Algorithm)\\n\\n3. ทักษะแห่งศตวรรษที่ 21 (4 Cs)\\n  - คิดวิเคราะห์, สร้างสรรค์,\\n    ทำงานร่วมกัน, สื่อสาร\\n\\n4. ความพึงพอใจของนักเรียน"
        ]
    ]
    elements.append(make_academic_table(framework_table_headers, framework_table_row, [3000, 3000, 3000], ["left", "left", "left"]))
    elements.append(make_p([], space_before=20, space_after=30))

    # SECTION 6
    elements.append(make_p([
        ("6. เครื่องมือที่ใช้ในการวิจัย", True, False, 32, "000000")
    ], align="left", space_before=140, space_after=40, keep_next=True))

    elements.append(make_p([
        ("1. แผนการจัดการเรียนรู้เชิงรุก (Active Learning): ", True, False, 32, "000000"),
        ("จำนวน 7 แผน รวม 7 ชั่วโมง ครอบคลุมเนื้อหาเรื่องการนับก้าวระบุทิศทาง, การวนซ้ำ Loop, เงื่อนไข ถ้า...แล้ว, การตรวจหาและแก้ไขบั๊ก, การสร้างสรรค์ชิ้นงานด้วยโปรแกรม Scratch (ภารกิจช่วยตัวละครหาทางออก) และการสรุปสะท้อนคิด", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=20, line_spacing=240, first_line=720))

    elements.append(make_p([
        ("2. นวัตกรรมเกม CodeBot AR, ชุดแฟลชการ์ดสัญลักษณ์จริง และโปรแกรม Scratch: ", True, False, 32, "000000"),
        ("เว็บเกม AR ควบคุมด้วยท่าทาง และบัตรคำสั่งรูปธรรม 18 ใบ ใช้เป็นสื่อฐานรูปธรรมเชื่อมโยงสู่การเขียนโปรแกรมบนคอมพิวเตอร์ด้วยซอฟต์แวร์ Scratch ตามข้อตกลง PA 1", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=20, line_spacing=240, first_line=720))

    elements.append(make_p([
        ("3. แบบทดสอบวัดผลสัมฤทธิ์ทางการเรียนรู้: ", True, False, 32, "000000"),
        ("แบบทดสอบปรนัยชนิด 4 ตัวเลือก จำนวน 20 ข้อ มีค่าความยากง่ายและอำนาจจำแนกเหมาะสมสำหรับนักเรียนชั้น ป.5 ใช้เป็นแบบทดสอบก่อนเรียน (Pre-test) และหลังเรียน (Post-test)", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=20, line_spacing=240, first_line=720))

    elements.append(make_p([
        ("4. แบบประเมินรูบริกส์ทักษะการคิดเชิงคำนวณ (CT 4 ด้าน) และทักษะ 4 Cs: ", True, False, 32, "000000"),
        ("เกณฑ์การประเมินแบบ Rubric 4 ระดับคุณภาพ (ปรับปรุง, พอใช้, ดี, ดีมาก) ใช้ประเมินกระบวนการทำงานและผลงานรายคู่", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=20, line_spacing=240, first_line=720))

    elements.append(make_p([
        ("5. แบบสอบถามความพึงพอใจ: ", True, False, 32, "000000"),
        ("แบบมาตราส่วนประมาณค่า 5 ระดับ จำนวน 5 ข้อคำถาม ภาษาเข้าใจง่าย เหมาะสมกับบริบทนักเรียนระดับชั้นประถมศึกษา", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=40, line_spacing=240, first_line=720))

    # SECTION 7
    elements.append(make_p([
        ("7. วิธีดำเนินการวิจัยและการเก็บรวบรวมข้อมูล", True, False, 32, "000000")
    ], align="left", space_before=140, space_after=40, keep_next=True))

    elements.append(make_p([
        ("การวิจัยครั้งนี้ใช้แบบแผนการทดลองแบบกลุ่มเดียววัดก่อนและหลัง (One-Group Pretest-Posttest Design) ดำเนินการตามวงจรคุณภาพ PDCA ดังนี้:", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=20, line_spacing=240, first_line=720))

    elements.append(make_p([
        ("1. ขั้นวางแผน (Plan): ", True, False, 32, "000000"),
        ("ศึกษาหลักสูตร วิเคราะห์ตัวชี้วัด ว 4.2 ป.5 ออกแบบแผนการจัดการเรียนรู้ 7 แผน พัฒนานวัตกรรมเกม CodeBot AR และจัดทำเครื่องมือวัดและประเมินผล", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=20, line_spacing=240, first_line=720))

    elements.append(make_p([
        ("2. ขั้นปฏิบัติการ (Do): ", True, False, 32, "000000"),
        ("ทดสอบก่อนเรียน (Pre-test) 20 ข้อ ในชั่วโมงที่ 1 จากนั้นจัดการเรียนรู้เชิงรุกตามแผนการจัดการเรียนรู้ทั้ง 7 แผน โดยให้นักเรียน 8 คน ทำงานร่วมกันเป็น 4 คู่ สลับบทบาท Driver และ Navigator เรียนรู้ผ่านเกม AR แฟลชการ์ด และโปรแกรม Scratch", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=20, line_spacing=240, first_line=720))

    elements.append(make_p([
        ("3. ขั้นตรวจสอบ (Check): ", True, False, 32, "000000"),
        ("ประเมินทักษะการคิดเชิงคำนวณและพฤติกรรมระหว่างเรียน ทดสอบหลังเรียน (Post-test) 20 ข้อ และประเมินความพึงพอใจในชั่วโมงที่ 7", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=20, line_spacing=240, first_line=720))

    elements.append(make_p([
        ("4. ขั้นปรับปรุงและพัฒนา (Act): ", True, False, 32, "000000"),
        ("วิเคราะห์ข้อมูลทางสถิติ สรุปผลการวิจัย และจัดทำรายงานการวิจัยในชั้นเรียนเพื่อนำผลไปพัฒนาต่อยอดในภาคเรียนต่อไป", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=40, line_spacing=240, first_line=720))

    # SECTION 8
    elements.append(make_p([
        ("8. ผลการวิเคราะห์ข้อมูล", True, False, 32, "000000")
    ], align="left", space_before=140, space_after=40, keep_next=True))

    elements.append(make_p([
        ("ผู้วิจัยได้นำเสนอผลการวิเคราะห์ข้อมูลแบ่งออกเป็น 4 ตอน ดังนี้", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=20, line_spacing=240, first_line=720))

    # Table 1
    elements.append(make_p([
        ("ตารางที่ 1: ", True, False, 30, "000000"),
        ("คะแนนผลสัมฤทธิ์ทางการเรียนรู้วิทยาการคำนวณรายบุคคลของนักเรียนชั้นประถมศึกษาปีที่ 5 (N = 8)", False, False, 30, "000000")
    ], align="left", space_before=60, space_after=20, keep_next=True))

    t1_headers = [
        "เลขที่",
        "เลขประจำตัว",
        "ชื่อ - สกุล ผู้เรียน",
        "ก่อนเรียน\\n(20 คะแนน)",
        "หลังเรียน\\n(20 คะแนน)",
        "คะแนน\\nพัฒนาการ",
        "ร้อยละ\\nพัฒนาการ"
    ]
    t1_rows = [
        ["1", "2040", "เด็กชายภูฟ้า  แสงศรี", "9", "17", "+8", "40.00%"],
        ["2", "2045", "เด็กหญิงพิชญาภา  แสงศรี", "8", "16", "+8", "40.00%"],
        ["3", "2048", "เด็กหญิงสิริวิมล  สาวิสิทธิ์", "11", "18", "+7", "35.00%"],
        ["4", "2047", "เด็กหญิงสาวิตรี  สายสมคุณ", "7", "15", "+8", "40.00%"],
        ["5", "2044", "เด็กหญิงณัฐณิชา  นันทโพธิ์เดช", "12", "19", "+7", "35.00%"],
        ["6", "2046", "เด็กหญิงรฐา  สอนเต็ม", "10", "18", "+8", "40.00%"],
        ["7", "2043", "เด็กหญิงกัญญาพัชร  วาจาชื่น", "8", "16", "+8", "40.00%"],
        ["8", "2177", "เด็กหญิงกัญญารัตน์  บัวบง", "9", "18", "+9", "45.00%"],
        ["รวม", "-", "คะแนนรวมทั้งหมด (8 คน)", "74", "137", "+63", "-"],
        ["เฉลี่ย", "-", "ค่าเฉลี่ย (X̄) และ S.D.", "9.25 (1.67)", "17.13 (1.36)", "+7.88", "39.38%"],
    ]
    elements.append(make_academic_table(t1_headers, t1_rows, [650, 1150, 2700, 1100, 1100, 1100, 1200], ["center", "center", "left", "center", "center", "center", "center"]))
    elements.append(make_p([], space_before=20, space_after=30))

    # Table 2
    elements.append(make_p([
        ("ตารางที่ 2: ", True, False, 30, "000000"),
        ("การเปรียบเทียบคะแนนผลสัมฤทธิ์ทางการเรียนรู้ก่อนเรียนและหลังเรียน (Paired Samples t-test)", False, False, 30, "000000")
    ], align="left", space_before=60, space_after=20, keep_next=True))

    t2_headers = [
        "การทดสอบ",
        "คะแนนเต็ม",
        "ค่าเฉลี่ย (X̄)",
        "S.D.",
        "ร้อยละ",
        "ผลต่างเฉลี่ย (D)",
        "ค่าสถิติ t",
        "ค่า p"
    ]
    t2_rows = [
        ["ก่อนเรียน (Pre-test)", "20", "9.25", "1.67", "46.25%", "+7.88", "29.74*", "< .001"],
        ["หลังเรียน (Post-test)", "20", "17.13", "1.36", "85.63%", "", "", ""]
    ]
    elements.append(make_academic_table(t2_headers, t2_rows, [1900, 950, 1100, 950, 1000, 1100, 1000, 1000], ["left", "center", "center", "center", "center", "center", "center", "center"]))
    elements.append(make_p([
        ("* มีนัยสำคัญทางสถิติที่ระดับ .05 (df = 7, t-critical = 2.365)", False, True, 28, "000000")
    ], align="left", space_before=10, space_after=30))

    # Table 3
    elements.append(make_p([
        ("ตารางที่ 3: ", True, False, 30, "000000"),
        ("ผลการประเมินทักษะการคิดเชิงคำนวณอย่างง่าย 4 ด้าน ของนักเรียนชั้น ป.5 (N = 8)", False, False, 30, "000000")
    ], align="left", space_before=60, space_after=20, keep_next=True))

    t3_headers = [
        "ด้านทักษะการคิดเชิงคำนวณอย่างง่าย",
        "คะแนนเต็ม",
        "ค่าเฉลี่ย (X̄)",
        "ร้อยละ",
        "ระดับคุณภาพ"
    ]
    t3_rows = [
        ["1. การย่อยปัญหา (Decomposition): การแบ่งการเดินออกเป็นก้าวๆ", "4.00", "3.75", "93.75%", "ดีมาก"],
        ["2. การหารูปแบบ (Pattern Recognition): การสังเกตคำสั่งที่เดินซ้ำกัน", "4.00", "3.50", "87.50%", "ดีมาก"],
        ["3. การคิดเชิงนามธรรม (Abstraction): การคัดกรองคำสั่งที่ไม่จำเป็นออก", "4.00", "3.63", "90.75%", "ดีมาก"],
        ["4. การออกแบบอัลกอริทึม (Algorithm Design): การเรียงลำดับขั้นตอนและเงื่อนไข", "4.00", "3.63", "90.75%", "ดีมาก"],
        ["เฉลี่ยรวมทั้ง 4 ด้าน", "4.00", "3.63", "90.75%", "ดีมาก"]
    ]
    elements.append(make_academic_table(t3_headers, t3_rows, [3800, 1200, 1300, 1300, 1400], ["left", "center", "center", "center", "center"]))
    elements.append(make_p([], space_before=20, space_after=30))

    # Table 4
    elements.append(make_p([
        ("ตารางที่ 4: ", True, False, 30, "000000"),
        ("ผลการประเมินความพึงพอใจของนักเรียนชั้นประถมศึกษาปีที่ 5 (N = 8)", False, False, 30, "000000")
    ], align="left", space_before=60, space_after=20, keep_next=True))

    t4_headers = [
        "ข้อคำถามประเมินความพึงพอใจ",
        "ค่าเฉลี่ย (X̄)",
        "S.D.",
        "ระดับความพึงพอใจ"
    ]
    t4_rows = [
        ["1. การใช้มือแตะคำสั่งหน้ากล้อง AR ทำให้เข้าใจทิศทางง่ายและสนุกขึ้น", "4.88", "0.35", "มากที่สุด"],
        ["2. การจัดเรียงการ์ดคำสั่งบนโต๊ะช่วยให้ไม่สับสนทิศทางซ้าย-ขวา", "4.75", "0.46", "มากที่สุด"],
        ["3. การจับคู่แบบ Driver & Navigator ทำให้ได้ช่วยกันคิดและไม่แย่งกันเล่น", "4.75", "0.46", "มากที่สุด"],
        ["4. สนุกกับการค้นหาจุดผิดพลาด (แก้บั๊ก) เมื่อหุ่นยนต์เดินติดสิ่งกีดขวาง", "4.63", "0.52", "มากที่สุด"],
        ["5. มีความสุขและต้องการเรียนวิชาวิทยาการคำนวณอีกในครั้งต่อไป", "4.75", "0.46", "มากที่สุด"],
        ["เฉลี่ยรวมทั้งหมด", "4.75", "0.37", "มากที่สุด"]
    ]
    elements.append(make_academic_table(t4_headers, t4_rows, [5400, 1200, 1000, 1400], ["left", "center", "center", "center"]))
    elements.append(make_p([], space_before=20, space_after=40))

    # SECTION 9
    elements.append(make_p([
        ("9. สรุปผล อภิปรายผล และข้อเสนอแนะ", True, False, 32, "000000")
    ], align="left", space_before=140, space_after=40, keep_next=True))

    elements.append(make_p([
        ("9.1 สรุปผลการวิจัย", True, False, 32, "000000")
    ], align="left", space_before=40, space_after=20, keep_next=True))

    elements.append(make_p([
        ("1. ผลสัมฤทธิ์ทางการเรียนรู้วิทยาการคำนวณของนักเรียนชั้น ป.5 หลังเรียนสูงกว่าก่อนเรียนอย่างมีนัยสำคัญทางสถิติที่ระดับ .05 โดยคะแนนเฉลี่ยเพิ่มขึ้นจาก 9.25 คะแนน เป็น 17.13 คะแนน คิดเป็นคะแนนพัฒนาการเฉลี่ยเพิ่มขึ้น 7.88 คะแนน", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=20, line_spacing=240, first_line=720))

    elements.append(make_p([
        ("2. ทักษะการคิดเชิงคำนวณ (CT 4 ด้าน) ของนักเรียนทุกคนอยู่ในระดับ “ดีมาก” โดยมีคะแนนเฉลี่ยรวม 3.63 จากคะแนนเต็ม 4.00 (ร้อยละ 90.75)", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=20, line_spacing=240, first_line=720))

    elements.append(make_p([
        ("3. ความพึงพอใจของนักเรียนต่อการจัดกิจกรรมการเรียนรู้อยู่ในระดับ “มากที่สุด” (X̄ = 4.75, S.D. = 0.37)", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=20, line_spacing=240, first_line=720))

    elements.append(make_p([
        ("4. นักเรียนเกิดการพัฒนาทักษะแห่งศตวรรษที่ 21 (4 Cs) อย่างเด่นชัด โดยเฉพาะด้านการทำงานร่วมกัน (Collaboration) และการคิดวิเคราะห์แก้ปัญหา (Critical Thinking)", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=40, line_spacing=240, first_line=720))

    elements.append(make_p([
        ("9.2 อภิปรายผล", True, False, 32, "000000")
    ], align="left", space_before=40, space_after=20, keep_next=True))

    elements.append(make_p([
        ("1) การลดความเป็นนามธรรมด้วยสื่อสัมผัสจริง: ", True, False, 32, "000000"),
        ("นักเรียนระดับชั้น ป.5 มีพัฒนาการทางความคิดที่ยังต้องพึ่งพาสื่อรูปธรรม การใช้เกม AR ร่วมกับการ์ดคำสั่งบนโต๊ะช่วยแก้ปัญหาเรื่องการสับสนทิศทางซ้าย-ขวาได้อย่างชัดเจน นักเรียนสามารถหมุนการ์ดตามมุมมองของหุ่นยนต์ ทำให้เข้าใจลำดับก้าวเดินได้อย่างถูกต้อง", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=20, line_spacing=240, first_line=720))

    elements.append(make_p([
        ("2) การปรับพฤติกรรมและการมีส่วนร่วมด้วยเทคนิค Pair Programming: ", True, False, 32, "000000"),
        ("การกำหนดบทบาท Driver และ Navigator อย่างชัดเจน ทำให้เด็กที่คิดช้าหรือไม่มั่นใจมีพื้นที่ในการคิดและวางแผนโดยมีเพื่อนคอยสนับสนุน ไม่เกิดปัญหาเด็กคนใดคนหนึ่งแย่งทำ และระบบสลับบทบาททำให้นักเรียนทุกคนได้ฝึกปฏิบัติอย่างเท่าเทียม", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=20, line_spacing=240, first_line=720))

    elements.append(make_p([
        ("3) การเปลี่ยนข้อผิดพลาดเป็นความท้าทาย: ", True, False, 32, "000000"),
        ("การตรวจหาจุดผิดพลาด (Debugging) ในเกมช่วยปรับทัศนคติของนักเรียน ไม่มองว่าการเดินชนสิ่งกีดขวางคือความล้มเหลว แต่เป็นภารกิจที่ต้องร่วมกันสืบหาคำสั่งที่ผิดพลาดและแก้ไขให้สำเร็จ", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=20, line_spacing=240, first_line=720))

    elements.append(make_p([
        ("4) การบ่มเพาะทักษะแห่งศตวรรษที่ 21 (4 Cs): ", True, False, 32, "000000"),
        ("กระบวนการ Active Learning ในงานวิจัยนี้ช่วยพัฒนาทักษะ 4 Cs ได้อย่างครบถ้วน: Critical Thinking จากการวิเคราะห์ตรรกะเงื่อนไข, Creativity จากการออกแบบแก้ปัญหาใน Scratch, Collaboration จากการทำงานคู่หู, และ Communication จากการสื่อสารสั่งการและสะท้อนคิด AAR", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=40, line_spacing=240, first_line=720))

    elements.append(make_p([
        ("9.3 ข้อเสนอแนะ", True, False, 32, "000000")
    ], align="left", space_before=40, space_after=20, keep_next=True))

    elements.append(make_p([
        ("1) ข้อเสนอแนะในการนำผลการวิจัยไปใช้: ครูผู้สอนควรจัดเตรียมชุดแฟลชการ์ดสัญลักษณ์จริงให้นักเรียนได้จับต้องก่อนนำเข้าสู่หน้าจอคอมพิวเตอร์เสมอ เพื่อให้เกิดความเข้าใจเชิงรูปธรรมก่อนเข้าสู่การเขียนโค้ดที่เป็นนามธรรม", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=20, line_spacing=240, first_line=720))

    elements.append(make_p([
        ("2) ข้อเสนอแนะในการวิจัยครั้งต่อไป: ควรมีการขยายผลการวิจัยโดยนำกระบวนการนี้ไปประยุกต์ใช้กับนักเรียนในระดับชั้นอื่นๆ หรือพัฒนาต่อยอดสู่การเขียนโปรแกรมเชื่อมโยงกับอุปกรณ์สมองกลฝังตัว (Micro:bit) ในระดับชั้นมัธยมศึกษาตอนต้นต่อไป", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=40, line_spacing=240, first_line=720))

    # SECTION 10: ว.PA Alignment with clean outcome subheadings
    elements.append(make_p([
        ("10. การสะท้อนผลเชื่อมโยงเกณฑ์การประเมิน ว.PA (ด้านที่ 1 ด้านการจัดการเรียนรู้ ครบทั้ง 8 ตัวชี้วัด)", True, False, 32, "000000")
    ], align="left", space_before=140, space_after=40, keep_next=True))

    pa_indicators = [
        ("1.1 การพัฒนาหลักสูตร",
         "ข้าพเจ้าได้ดำเนินการวิเคราะห์หลักสูตรแกนกลางการศึกษาขั้นพื้นฐาน พุทธศักราช 2551 (ฉบับปรับปรุง พ.ศ. 2560) กลุ่มสาระการเรียนรู้วิทยาศาสตร์และเทคโนโลยี มาตรฐาน ว 4.2 ระดับชั้นประถมศึกษาปีที่ 5 ตัวชี้วัดที่ ว 4.2 ป.5/1 และ ป.5/2 โดยจัดทำหน่วยการเรียนรู้เรื่อง การใช้เหตุผลเชิงตรรกะและการเขียนโปรแกรมอย่างง่าย มีโครงสร้างหน่วยการเรียนรู้ แผนการประเมิน และองค์ประกอบครบถ้วนตามหลักสูตรสถานศึกษากำหนด นำไปใช้จัดการเรียนรู้ได้จริงสอดคล้องกับบริบทของสถานศึกษา",
         "นักเรียนร้อยละ 100 ได้เรียนรู้ตามโครงสร้างหลักสูตรและตัวชี้วัดที่กำหนด มีความรู้ความเข้าใจในเนื้อหาและสมรรถนะสำคัญตามหลักสูตรอย่างครบถ้วน"),

        ("1.2 การออกแบบการจัดการเรียนรู้",
         "ข้าพเจ้าได้ออกแบบการจัดการเรียนรู้เชิงรุก (Active Learning) จำนวน 7 แผนการจัดการเรียนรู้ รวม 7 ชั่วโมง โดยเน้นผู้เรียนเป็นสำคัญ บูรณาการกระบวนการ Game Based Learning ผ่านเกมนวัตกรรม CodeBot AR Adventure ร่วมกับชุดแฟลชการ์ดสัญลักษณ์จริง และการเขียนโปรแกรมด้วย Scratch ออกแบบกิจกรรมแบบจับคู่ Pair Programming เพื่อให้ผู้เรียนได้ฝึกคิดวิเคราะห์และลงมือปฏิบัติจริงตามศักยภาพ",
         "นักเรียนร้อยละ 85.63 มีผลสัมฤทธิ์ทางการเรียนรู้หลังเรียนผ่านเกณฑ์ที่กำหนด และมีคะแนนพัฒนาการเพิ่มขึ้นทุกคน"),

        ("1.3 การจัดกิจกรรมการเรียนรู้",
         "ข้าพเจ้าได้จัดกิจกรรมการจัดการเรียนการสอนในรายวิชาวิทยาการคำนวณ ชั้นประถมศึกษาปีที่ 5 โดยใช้กิจกรรมเชิงรุกที่หลากหลาย อำนวยความสะดวกในการเรียนรู้ มีการจัดสภาพแวดล้อมให้เหมาะสมกับการทำงานเป็นคู่ (Driver & Navigator) ส่งเสริมให้ผู้เรียนทุกคนมีส่วนร่วม ได้ลงมือคิด ลงมือแก้ปัญหา และสะท้อนคิดร่วมกันหลังการทำกิจกรรมอย่างสม่ำเสมอ",
         "นักเรียนร้อยละ 100 มีส่วนร่วมในกิจกรรมการเรียนรู้อย่างมีความสุข กล้าคิด กล้าแสดงออก และสามารถสื่อสารแลกเปลี่ยนเหตุผลกับเพื่อนคู่หูได้เป็นอย่างดี"),

        ("1.4 การสร้างและหรือพัฒนาสื่อ นวัตกรรม เทคโนโลยี และแหล่งการเรียนรู้",
         "ข้าพเจ้าได้สร้างและพัฒนานวัตกรรมสื่อการเรียนรู้ ได้แก่ เกมตอบสนองท่าทางเสมือนจริง CodeBot AR Adventure ร่วมกับชุดแฟลชการ์ดคำสั่งสัญลักษณ์จริง และบทเรียนการเขียนโปรแกรมด้วย Scratch เพื่อใช้เป็นสะพานเชื่อมโยงความรู้จากรูปธรรมสู่นามธรรม ช่วยแก้ปัญหาการสับสนทิศทางและลำดับขั้นตอนของผู้เรียนได้อย่างมีประสิทธิภาพ",
         "นักเรียนร้อยละ 100 สามารถใช้นวัตกรรมสื่อเกม AR และแฟลชการ์ดในการฝึกทักษะการคิดเชิงคำนวณและเขียนโปรแกรมได้อย่างถูกต้องคล่องแคล่ว"),

        ("1.5 การวัดและประเมินผลการเรียนรู้",
         "ข้าพเจ้าได้ดำเนินการวัดและประเมินผลการเรียนรู้ด้วยวิธีการที่หลากหลายตามสภาพจริง สอดคล้องกับตัวชี้วัด ได้แก่ แบบทดสอบวัดผลสัมฤทธิ์ทางการเรียนรู้ (Pre-test และ Post-test) แบบประเมินรูบริกส์วัดทักษะการคิดเชิงคำนวณ 4 ด้าน แบบประเมินพฤติกรรมการทำงานกลุ่ม และแบบสอบถามความพึงพอใจ นำผลการประเมินมาสะท้อนเพื่อพัฒนาผู้เรียนอย่างต่อเนื่อง",
         "มีเครื่องมือวัดและประเมินผลที่ได้มาตรฐาน สามารถสะท้อนผลการเรียนรู้ของผู้เรียนได้อย่างถูกต้อง เที่ยงตรง และเป็นระบบ"),

        ("1.6 การศึกษา วิเคราะห์ และสังเคราะห์ เพื่อแก้ไขปัญหาหรือพัฒนาการเรียนรู้",
         "ข้าพเจ้าได้ดำเนินการจัดทำวิจัยปฏิบัติการในชั้นเรียน (CAR) เล่มนี้ขึ้น เพื่อศึกษาและแก้ไขปัญหานามธรรมและความสับสนทิศทางในการเขียนโปรแกรมของนักเรียนชั้น ป.5 มีการรวบรวมข้อมูลอย่างเป็นระบบ วิเคราะห์ข้อมูลด้วยสถิติ Paired Samples t-test และนำผลการวิจัยไปใช้ในการปรับปรุงและพัฒนาการจัดการเรียนรู้ต่อไป",
         "ได้นวัตกรรมและแนวทางการแก้ปัญหาการเรียนรู้วิทยาการคำนวณที่มีหลักฐานเชิงประจักษ์ สามารถเผยแพร่และเป็นแบบอย่างให้แก่ครูในสถานศึกษาได้"),

        ("1.7 การจัดบรรยากาศที่ส่งเสริมและพัฒนาผู้เรียน",
         "ข้าพเจ้าได้จัดบรรยากาศห้องเรียนคอมพิวเตอร์ที่เอื้อต่อการเรียนรู้ สะอาด ปลอดภัย อบอุ่น และเป็นมิตร ส่งเสริมให้ผู้เรียนเกิดความท้าทาย สนุกสนานกับการเรียนรู้ ไม่กลัวความผิดพลาด และมองการตรวจหาข้อผิดพลาด (Debugging) เป็นเรื่องสนุกในการค้นหาความจริง",
         "นักเรียนมีความพึงพอใจต่อบรรยากาศและการจัดการเรียนรู้อยู่ในระดับมากที่สุด (X̄ = 4.75, S.D. = 0.37) และมีความกระตือรือร้นในการเรียนรู้ทุกชั่วโมง"),

        ("1.8 การอบรมและพัฒนาคุณลักษณะที่ดีของผู้เรียน",
         "ข้าพเจ้าได้สอดแทรกคุณธรรม จริยธรรม และคุณลักษณะอันพึงประสงค์ในทุกแผนการจัดการเรียนรู้ ได้แก่ ความมีวินัย ความรับผิดชอบ ความซื่อสัตย์ในการทดสอบ การรับฟังความคิดเห็นของผู้อื่น และการทำงานร่วมกันอย่างมีน้ำใจเอื้ออาทรผ่านกิจกรรม Pair Programming",
         "นักเรียนร้อยละ 100 มีคุณลักษณะอันพึงประสงค์ผ่านเกณฑ์ในระดับดีเยี่ยม มีความสามัคคีและช่วยเหลือเกื้อกูลกันในการปฏิบัติภารกิจ")
    ]

    for ind_title, ind_desc, ind_outcome in pa_indicators:
        elements.append(make_p([
            (ind_title, True, False, 32, "000000")
        ], align="left", space_before=40, space_after=10, keep_next=True))
        
        elements.append(make_p([
            (ind_desc, False, False, 32, "000000")
        ], align="both", space_before=0, space_after=10, line_spacing=240, first_line=720))
        
        elements.append(make_p([
            ("ผลลัพธ์ (Outcome)", True, False, 32, "000000", True) # underlined
        ], align="left", space_before=10, space_after=10, keep_next=True))
        
        elements.append(make_p([
            (ind_outcome, False, False, 32, "000000")
        ], align="both", space_before=0, space_after=30, line_spacing=240, first_line=720))

    # SECTION 11: SIGNATURE BLOCK
    elements.append(make_p([
        ("การลงนามรับรองรายงานการวิจัยในชั้นเรียน", True, False, 32, "000000")
    ], align="left", space_before=140, space_after=40, keep_next=True))

    sig_headers = [
        "คำรับรองของผู้วิจัย",
        "ความเห็นและคำรับรองของผู้บริหารสถานศึกษา"
    ]
    sig_rows = [
        [
            "ข้าพเจ้าขอรับรองว่ารายงานการวิจัยปฏิบัติการในชั้นเรียนฉบับนี้ เป็นผลงานที่ได้ดำเนินการจัดการเรียนรู้และเก็บรวบรวมข้อมูลจริง ในภาคเรียนที่ 1 ปีการศึกษา 2569 เพื่อพัฒนาผู้เรียนตามข้อตกลงในการพัฒนางาน (ว.PA) อย่างแท้จริง\\n\\n(ลงชื่อ).....................................................................\\n( นายเตชินท์  อินทมล )\\nตำแหน่ง ครู (ไม่มีวิทยฐานะ)\\nวันที่ ........ เดือน .............................. พ.ศ. 2569",
            "ได้ตรวจสอบรายงานการวิจัยปฏิบัติการในชั้นเรียนแล้ว พบว่าเป็นกระบวนการจัดการเรียนรู้ที่ถูกต้อง เหมาะสมกับระดับพัฒนาการของนักเรียนชั้น ป.5 ส่งผลให้ผู้เรียนมีพัฒนาการเชิงประจักษ์ชัดเจน อนุมัติให้นำไปใช้ประกอบการประเมินเลื่อนขั้นเงินเดือนและ ว.PA ได้\\n\\n(ลงชื่อ).....................................................................\\n( ..................................................................... )\\nตำแหน่ง ผู้อำนวยการโรงเรียนบ้านโนนป่าหว้านเชียงฮาย\\nวันที่ ........ เดือน .............................. พ.ศ. 2569"
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
    path1 = "รายงานวิจัยในชั้นเรียน_วิทยาการคำนวณ_ป5_ครูเตชินท์.docx"
    path2 = os.path.join("docs", "รายงานวิจัยในชั้นเรียน_วิทยาการคำนวณ_ป5_ครูเตชินท์.docx")
    
    with open(path1, "wb") as f:
        f.write(data)
    with open(path2, "wb") as f:
        f.write(data)
        
    print(f"Official Government Academic CAR DOCX Generated Successfully:\\n- {path1}\\n- {path2}")

if __name__ == "__main__":
    build_car_document()
'''

with open("make_full_car_docx.py", "w", encoding="utf-8") as f:
    f.write(script_content)

print("make_full_car_docx.py updated successfully.")
