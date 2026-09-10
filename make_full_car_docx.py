# -*- coding: utf-8 -*-
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

def make_p(runs, align="both", space_before=0, space_after=0, line_spacing=240, first_line=0, left_indent=0, hanging=0, keep_next=False):
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

def build_car_document():
    elements = []

    # 1. ปกรายงานการวิจัย
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
        ("การพัฒนาทักษะการเรียนรู้รายวิชาเทคโนโลยี (วิทยาการคำนวณ)", True, False, 32, "000000"),
        ("\nกลุ่มสาระการเรียนรู้วิทยาศาสตร์และเทคโนโลยี", True, False, 32, "000000"),
        ("\nโดยใช้กระบวนการ Gamebase learning ร่วมกับเทคนิคการสอนแบบ active learning", True, False, 32, "000000"),
        ("\nของนักเรียนชั้นประถมศึกษาปีที่ 5 โรงเรียนบ้านโนนป่าหว้านเชียงฮาย", True, False, 32, "000000")
    ], align="center", space_before=40, space_after=300, line_spacing=260))

    elements.append(make_p([
        ("เอกสารประกอบการประเมินการพัฒนางานตามข้อตกลง (ว.PA)", False, True, 28, "000000"),
        ("\nและประกอบการประเมินประสิทธิภาพและประสิทธิผลการปฏิบัติงานเพื่อเลื่อนขั้นเงินเดือน", False, True, 28, "000000")
    ], align="center", space_before=40, space_after=400, line_spacing=260))

    elements.append(make_p([
        ("โดย", True, False, 32, "000000")
    ], align="center", space_before=60, space_after=40))

    elements.append(make_p([
        ("นายเตชินท์  อินทมล", True, False, 32, "000000"),
        ("\nตำแหน่ง ครู (ไม่มีวิทยฐานะ)", False, False, 30, "000000"),
        ("\nกลุ่มสาระการเรียนรู้วิทยาศาสตร์และเทคโนโลยี", False, False, 30, "000000")
    ], align="center", space_before=0, space_after=300, line_spacing=260))

    elements.append(make_p([
        ("โรงเรียนบ้านโนนป่าหว้านเชียงฮาย", True, False, 32, "000000"),
        ("\nสำนักงานเขตพื้นที่การศึกษาประถมศึกษาหนองบัวลำภู เขต 2", False, False, 30, "000000"),
        ("\nสำนักงานคณะกรรมการการศึกษาขั้นพื้นฐาน กระทรวงศึกษาธิการ", False, False, 30, "000000"),
        ("\nภาคเรียนที่ 1 ปีการศึกษา 2569", True, False, 30, "000000")
    ], align="center", space_before=0, space_after=100, line_spacing=260))

    elements.append(make_page_break())

    # 2. บทคัดย่อ
    elements.append(make_p([
        ("บทคัดย่อ", True, False, 36, "000000")
    ], align="center", space_before=100, space_after=140, keep_next=True))

    elements.append(make_p([
        ("ชื่อเรื่องวิจัย: ", True, False, 30, "000000"),
        ("การพัฒนาทักษะการเรียนรู้รายวิชาเทคโนโลยี (วิทยาการคำนวณ) กลุ่มสาระการเรียนรู้วิทยาศาสตร์และเทคโนโลยี โดยใช้กระบวนการ Gamebase learning ร่วมกับเทคนิคการสอนแบบ active learning ของนักเรียนชั้นประถมศึกษาปีที่ 5 โรงเรียนบ้านโนนป่าหว้านเชียงฮาย", False, False, 30, "000000")
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

    elements.append(make_p([
        ("การวิจัยปฏิบัติการในชั้นเรียนครั้งนี้ มีวัตถุประสงค์เพื่อ: 1) เปรียบเทียบผลสัมฤทธิ์ทางการเรียนรู้รายวิชาเทคโนโลยี (วิทยาการคำนวณ) เรื่อง การใช้เหตุผลเชิงตรรกะและการเขียนโปรแกรมอย่างง่าย ของนักเรียนชั้นประถมศึกษาปีที่ 5 ก่อนและหลังการจัดการเรียนรู้ 2) ประเมินทักษะการคิดเชิงคำนวณและการเขียนโปรแกรมตามตัวชี้วัด ว 4.2 ป.5/1 และ ป.5/2 และ 3) ศึกษาความพึงพอใจของนักเรียนที่มีต่อการจัดกิจกรรมการเรียนรู้ กลุ่มเป้าหมายเป็นนักเรียนชั้นประถมศึกษาปีที่ 5 โรงเรียนบ้านโนนป่าหว้านเชียงฮาย สังกัดสำนักงานเขตพื้นที่การศึกษาประถมศึกษาหนองบัวลำภู เขต 2 ภาคเรียนที่ 1 ปีการศึกษา 2569 จำนวน 8 คน ดำเนินการจัดการเรียนรู้เชิงรุก (Active Learning) แบบจับคู่เขียนโปรแกรม (Pair Programming) จำนวน 4 คู่ เครื่องมือที่ใช้ในการวิจัยประกอบด้วย แผนการจัดการเรียนรู้เชิงรุก จำนวน 7 แผน รวม 7 ชั่วโมง สื่อนวัตกรรมเกมตอบสนองท่าทางเสมือนจริง CodeBot AR Adventure แผ่นแผนที่ภารกิจตารางเดินช่อง ชุดแฟลชการ์ดคำสั่งสัญลักษณ์ และโปรแกรม Scratch แบบทดสอบวัดผลสัมฤทธิ์ทางการเรียนรู้ 20 ข้อ แบบประเมินรูบริกส์ทักษะการคิดเชิงคำนวณและการเขียนโปรแกรม และแบบสอบถามความพึงพอใจ สถิติที่ใช้ในการวิเคราะห์ข้อมูล ได้แก่ ค่าเฉลี่ย ส่วนเบี่ยงเบนมาตรฐาน ร้อยละ และการทดสอบค่าทีแบบไม่อิสระ (Paired Samples t-test)", False, False, 30, "000000")
    ], align="both", space_before=0, space_after=40, line_spacing=240, first_line=720))

    elements.append(make_p([
        ("ผลการวิจัยพบว่า:", True, False, 30, "000000")
    ], align="left", space_before=20, space_after=20, line_spacing=240, first_line=720))

    elements.append(make_p([
        ("1. ผลสัมฤทธิ์ทางการเรียนรู้ของนักเรียนชั้นประถมศึกษาปีที่ 5 จำนวน 8 คน มีคะแนนผลสัมฤทธิ์ทางการเรียนรู้หลังเรียนสูงกว่าก่อนเรียนทุกคน คิดเป็นร้อยละ 100 โดยมีคะแนนเฉลี่ยเพิ่มขึ้น 7.88 คะแนน (ก่อนเรียนเฉลี่ย 7.75 คะแนน และหลังเรียนเฉลี่ย 15.62 คะแนน) อย่างมีนัยสำคัญทางสถิติที่ระดับ .05 ซึ่งสูงกว่าเป้าหมายที่กำหนดไว้ในข้อตกลง", False, False, 30, "000000")
    ], align="both", space_before=0, space_after=20, line_spacing=240, first_line=720))

    elements.append(make_p([
        ("2. ทักษะการคิดเชิงคำนวณและการเขียนโปรแกรมของนักเรียนผ่านเกณฑ์ในระดับ “ดี” ขึ้นไป จำนวน 7 คน คิดเป็นร้อยละ 87.50 โดยมีคะแนนเฉลี่ยชั้นเรียนเท่ากับ 3.00 เต็ม 4.00 คะแนน ซึ่งสูงกว่าเป้าหมายที่กำหนดไว้ในข้อตกลง", False, False, 30, "000000")
    ], align="both", space_before=0, space_after=20, line_spacing=240, first_line=720))

    elements.append(make_p([
        ("3. ความพึงพอใจของนักเรียนที่มีต่อการจัดกิจกรรมการเรียนรู้อยู่ในระดับ “มาก” โดยมีคะแนนเฉลี่ยรวมเท่ากับ 4.38 จากคะแนนเต็ม 5.00", False, False, 30, "000000")
    ], align="both", space_before=0, space_after=20, line_spacing=240, first_line=720))

    elements.append(make_p([
        ("คำสำคัญ: ", True, False, 30, "000000"),
        ("วิทยาการคำนวณ, Gamebase Learning, Active Learning, Pair Programming, โปรแกรม Scratch, ว.PA", False, False, 30, "000000")
    ], align="left", space_before=20, space_after=60, line_spacing=240))

    elements.append(make_page_break())

    # 3. เนื้อหารายงานวิจัย (MAIN RESEARCH REPORT)
    elements.append(make_p([
        ("1. สภาพปัญหาของผู้เรียนและการจัดการเรียนรู้", True, False, 32, "000000")
    ], align="left", space_before=140, space_after=40, keep_next=True))

    elements.append(make_p([
        ("กลุ่มสาระการเรียนรู้วิทยาศาสตร์และเทคโนโลยี สาระเทคโนโลยี (วิทยาการคำนวณ) ตามหลักสูตรแกนกลางการศึกษาขั้นพื้นฐาน พุทธศักราช 2551 (ฉบับปรับปรุง พ.ศ. 2560) มุ่งเน้นพัฒนาผู้เรียนให้มีสมรรถนะสำคัญแห่งศตวรรษที่ 21 โดยเฉพาะ “ทักษะการคิดเชิงคำนวณ (Computational Thinking)” และทักษะการแก้ปัญหาอย่างเป็นขั้นตอน โดยธรรมชาติของสาระวิชานี้เป็นวิชาเชิงทักษะกระบวนการที่ผู้เรียนต้องสร้างองค์ความรู้ผ่านประสบการณ์ตรงและการลงมือปฏิบัติจริง มิใช่การจัดการเรียนรู้ที่มุ่งเน้นการถ่ายทอดเนื้อหา การทำแบบฝึกหัด หรือการจดจำทฤษฎี โดยเฉพาะในระดับชั้นประถมศึกษาปีที่ 5 ซึ่งหลักสูตรกำหนดตัวชี้วัดสำคัญตามมาตรฐาน ว 4.2 ได้แก่ การใช้เหตุผลเชิงตรรกะในการแก้ปัญหาและการคาดการณ์ผลลัพธ์ (ว 4.2 ป.5/1) ตลอดจนการออกแบบและเขียนโปรแกรมที่มีการใช้เหตุผลเชิงตรรกะอย่างง่าย พร้อมทั้งการตรวจหาข้อผิดพลาดและแก้ไข (ว 4.2 ป.5/2)", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=20, line_spacing=240, first_line=720))

    elements.append(make_p([
        ("จากการจัดการเรียนรู้ในรายวิชาวิทยาการคำนวณ รหัสวิชา ว15101 แก่นักเรียนชั้นประถมศึกษาปีที่ 5 โรงเรียนบ้านโนนป่าหว้านเชียงฮาย สำนักงานเขตพื้นที่การศึกษาประถมศึกษาหนองบัวลำภู เขต 2 ในภาคเรียนที่ 1 ปีการศึกษา 2569 พบสภาพปัญหาที่เป็นอุปสรรคสำคัญต่อการบรรลุเป้าหมายของหลักสูตร 3 ประการ ได้แก่:", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=20, line_spacing=240, first_line=720))

    elements.append(make_p([
        ("1) อุปสรรคด้านมโนทัศน์เชิงนามธรรมและมิติสัมพันธ์: ", True, False, 32, "000000"),
        ("ตามทฤษฎีพัฒนาการทางสติปัญญา ผู้เรียนในระดับประถมศึกษายังต้องการสื่อรูปธรรมในการเชื่อมโยงความคิด แต่เนื้อหาการเขียนโปรแกรมมีลักษณะเป็นนามธรรมสูง เมื่อผู้เรียนต้องสั่งการตัวละครในจอภาพที่มีมุมมองกลับทิศทางกับตนเอง ผู้เรียนจะเกิดความสับสนทิศทางซ้าย-ขวาอย่างชัดเจน ไม่สามารถแปลงจินตภาพเชิงพื้นที่ให้เป็นคำสั่งทางตรรกะได้ ส่งผลให้เขียนคำสั่งผิดพลาดและเกิดความท้อแท้ต่อการเรียนรู้", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=20, line_spacing=240, first_line=720))

    elements.append(make_p([
        ("2) อุปสรรคด้านกระบวนการคิดเชิงอัลกอริทึม: ", True, False, 32, "000000"),
        ("ผู้เรียนขาดทักษะการวางแผนลำดับขั้นตอนก่อนลงมือปฏิบัติ มักใช้วิธีการแก้ปัญหาแบบสุ่มลองผิดลองถูก และเมื่อโปรแกรมประมวลผลไม่สำเร็จหรือตัวละครเดินติดสิ่งกีดขวาง ผู้เรียนขาดทักษะในการวิเคราะห์เพื่อสืบค้นและระบุจุดผิดพลาด (Debugging) แต่มักเลือกที่จะลบชุดคำสั่งทั้งหมดทิ้งแล้วเริ่มต้นใหม่ ซึ่งสะท้อนถึงการขาดกระบวนการคิดวิเคราะห์อย่างมีเหตุผลและเป็นระบบ", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=20, line_spacing=240, first_line=720))

    elements.append(make_p([
        ("3) อุปสรรคด้านการมีส่วนร่วมในชั้นเรียน: ", True, False, 32, "000000"),
        ("ในการทำกิจกรรมหน้าเครื่องคอมพิวเตอร์ พบปัญหานักเรียนที่มีความมั่นใจหรือกล้าแสดงออกมักมีบทบาทหลักในการควบคุมอุปกรณ์และตัดสินใจเพียงลำพัง ขณะที่นักเรียนที่มีทักษะช้ากว่าหรือขาดความมั่นใจจะถอยตัวออกห่างและกลายเป็นเพียงผู้สังเกตการณ์ ทำให้ขาดโอกาสในการฝึกคิดวิเคราะห์และลงมือปฏิบัติจริง ส่งผลให้เกิดช่องว่างความก้าวหน้าทางการเรียนรู้ระหว่างบุคคล", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=20, line_spacing=240, first_line=720))

    elements.append(make_p([
        ("จากสภาพปัญหาและความท้าทายดังกล่าว ครูผู้สอนจึงตระหนักถึงความจำเป็นเร่งด่วนในการเปลี่ยนกระบวนทัศน์การจัดการเรียนรู้จาก Passive Learning สู่ Active Learning อย่างเป็นรูปธรรม โดยนำแนวคิด การจัดการเรียนรู้โดยใช้เกมเป็นฐาน (Game-based Learning) ผสานเข้ากับ เทคโนโลยีการตรวจจับท่าทางผ่านกล้อง (Hand Gesture Recognition) แผ่นแผนที่ภารกิจตารางเดินช่อง และ ชุดแฟลชการ์ดคำสั่งสัญลักษณ์ เพื่อเปลี่ยนการเขียนโค้ดที่เป็นนามธรรมให้กลายเป็นการลงมือปฏิบัติที่สนุกสนาน โดยเปิดโอกาสให้ผู้เรียนได้ใช้การเคลื่อนไหวร่างกาย เช่น การยกมือซ้าย-มือขวาเพื่อกำหนดทิศทาง และการใช้สัญลักษณ์มือสั่งการคำสั่งโค้ดดิ้งผ่านกล้อง ควบคู่กับการนำเทคนิค Pair Programming (การจับคู่เขียนโปรแกรม: บทบาท Driver & Navigator) มาใช้ส่งเสริมการทำงานร่วมกัน การสื่อสารแลกเปลี่ยนเหตุผล และสร้างความเท่าเทียมในการลงมือปฏิบัติ", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=20, line_spacing=240, first_line=720))

    elements.append(make_p([
        ("ด้วยเหตุนี้ ข้าพเจ้าจึงได้ขับเคลื่อนการวิจัยปฏิบัติการในชั้นเรียน เรื่อง “การพัฒนาทักษะการเรียนรู้รายวิชาเทคโนโลยี (วิทยาการคำนวณ) กลุ่มสาระการเรียนรู้วิทยาศาสตร์และเทคโนโลยี โดยใช้กระบวนการ Gamebase learning ร่วมกับเทคนิคการสอนแบบ active learning ของนักเรียนชั้นประถมศึกษาปีที่ 5 โรงเรียนบ้านโนนป่าหว้านเชียงฮาย” เพื่อเป็นแนวทางในการแก้ไขปัญหาเชิงประจักษ์ ยกระดับผลสัมฤทธิ์ทางการเรียนรู้ และบ่มเพาะสมรรถนะการคิดเชิงคำนวณของผู้เรียนให้บรรลุตามมาตรฐานของหลักสูตรได้อย่างมีประสิทธิภาพและยั่งยืน", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=40, line_spacing=240, first_line=720))

    # SECTION 2
    elements.append(make_p([
        ("2. วัตถุประสงค์การวิจัย", True, False, 32, "000000")
    ], align="left", space_before=140, space_after=40, keep_next=True))

    elements.append(make_p([
        ("1. เพื่อเปรียบเทียบผลสัมฤทธิ์ทางการเรียนรู้รายวิชาเทคโนโลยี (วิทยาการคำนวณ) เรื่อง การใช้เหตุผลเชิงตรรกะและการเขียนโปรแกรมอย่างง่าย ของนักเรียนชั้นประถมศึกษาปีที่ 5 ก่อนและหลังการจัดการเรียนรู้โดยใช้กระบวนการ Gamebase learning ร่วมกับเทคนิคการสอนแบบ active learning", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=20, line_spacing=240, first_line=720))

    elements.append(make_p([
        ("2. เพื่อประเมินทักษะการคิดเชิงคำนวณและการเขียนโปรแกรม ตามตัวชี้วัด ว 4.2 ป.5/1 และ ป.5/2 ของนักเรียนชั้นประถมศึกษาปีที่ 5", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=20, line_spacing=240, first_line=720))

    elements.append(make_p([
        ("3. เพื่อศึกษาความพึงพอใจของนักเรียนชั้นประถมศึกษาปีที่ 5 ที่มีต่อการจัดกิจกรรมการเรียนรู้โดยใช้กระบวนการ Gamebase learning ร่วมกับเทคนิคการสอนแบบ active learning", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=40, line_spacing=240, first_line=720))

    # SECTION 3
    elements.append(make_p([
        ("3. สมมติฐานการวิจัย", True, False, 32, "000000")
    ], align="left", space_before=140, space_after=40, keep_next=True))

    elements.append(make_p([
        ("1. นักเรียนชั้นประถมศึกษาปีที่ 5 มีคะแนนผลสัมฤทธิ์ทางการเรียนรู้หลังเรียนสูงกว่าก่อนเรียน อย่างมีนัยสำคัญทางสถิติที่ระดับ .05", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=20, line_spacing=240, first_line=720))

    elements.append(make_p([
        ("2. นักเรียนชั้นประถมศึกษาปีที่ 5 มีผลการประเมินทักษะการคิดเชิงคำนวณและการเขียนโปรแกรมในระดับ “ดี” ขึ้นไป ไม่น้อยกว่าร้อยละ 80", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=20, line_spacing=240, first_line=720))

    elements.append(make_p([
        ("3. นักเรียนชั้นประถมศึกษาปีที่ 5 มีความพึงพอใจต่อการจัดกิจกรรมการเรียนรู้เฉลี่ยอยู่ในระดับ “มาก” ขึ้นไป", False, False, 32, "000000")
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
        ("รายวิชาพื้นฐานวิทยาศาสตร์และเทคโนโลยี เทคโนโลยี (วิทยาการคำนวณ) รหัสวิชา ว15101 ชั้นประถมศึกษาปีที่ 5 หน่วยการเรียนรู้: การใช้เหตุผลเชิงตรรกะและการเขียนโปรแกรมอย่างง่าย ตามมาตรฐาน ว 4.2 ตัวชี้วัด ป.5/1 และ ป.5/2", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=20, line_spacing=240, first_line=720))

    elements.append(make_p([
        ("4.3 ด้านตัวแปรที่ศึกษา: ", True, False, 32, "000000")
    ], align="left", space_before=0, space_after=20, line_spacing=240, first_line=720))

    elements.append(make_p([
        ("1) ตัวแปรต้น: การจัดการเรียนรู้โดยใช้กระบวนการ Gamebase learning ร่วมกับเทคนิคการสอนแบบ active learning (Pair Programming) สื่อเกม CodeBot AR Adventure แผ่นแผนที่ภารกิจตารางเดินช่อง ชุดแฟลชการ์ดคำสั่งสัญลักษณ์ และโปรแกรม Scratch", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=20, line_spacing=240, first_line=1080))

    elements.append(make_p([
        ("2) ตัวแปรตาม: ได้แก่ 1) ผลสัมฤทธิ์ทางการเรียนรู้ 2) ทักษะการคิดเชิงคำนวณและการเขียนโปรแกรม และ 3) ความพึงพอใจของนักเรียน", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=20, line_spacing=240, first_line=1080))

    elements.append(make_p([
        ("4.4 ด้านระยะเวลา: ", True, False, 32, "000000"),
        ("ดำเนินการในภาคเรียนที่ 1 ปีการศึกษา 2569 จำนวน 7 แผนการจัดการเรียนรู้ สัปดาห์ละ 1 ชั่วโมง รวม 7 ชั่วโมง", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=40, line_spacing=240, first_line=720))

    # SECTION 5: กรอบแนวคิดการวิจัย
    elements.append(make_p([
        ("5. กรอบแนวคิดการวิจัย", True, False, 32, "000000")
    ], align="left", space_before=140, space_after=40, keep_next=True))

    framework_table_headers = [
        "ตัวแปรต้น\n(นวัตกรรม & เทคนิคการจัดการเรียนรู้)",
        "กระบวนการจัดการเรียนรู้\n(Active Learning)",
        "ตัวแปรตาม\n(ผลลัพธ์การเรียนรู้ ป.5)"
    ]
    framework_table_row = [
        [
            "1. กระบวนการ Gamebase Learning\n  - เกม CodeBot AR Adventure\n  - แผ่นแผนที่ภารกิจตารางเดินช่อง\n  - ชุดแฟลชการ์ดคำสั่งสัญลักษณ์\n\n2. การเขียนโปรแกรม Scratch\n  - การจัดลำดับบล็อกคำสั่ง\n  - การตรวจหาและแก้บั๊ก\n\n3. เทคนิค Pair Programming\n  - จับคู่ 4 คู่ (Navigator & Driver)",
            "1. ขั้นวางแผน (Plan)\n  - วิเคราะห์ตัวชี้วัด ว 4.2\n  - ออกแบบ 7 แผนการเรียนรู้\n\n2. ขั้นปฏิบัติการ (Do)\n  - ทดสอบก่อนเรียน Pre-test\n  - วางแผนเส้นทาง (Navigator)\n  - ป้อนคำสั่งท่าทาง (Driver)\n  - สลับบทบาททุกรอบภารกิจ\n\n3. ขั้นตรวจสอบ (Check)\n  - ประเมินทักษะการคิดและโค้ดดิ้ง\n  - ทดสอบหลังเรียน Post-test\n  - ประเมินความพึงพอใจ\n\n4. ขั้นพัฒนา (Act)\n  - สรุปผลและพัฒนาต่อเนื่อง",
            "1. ผลสัมฤทธิ์ทางการเรียนรู้\n  - คะแนนทดสอบ 20 ข้อ\n  - พัฒนาการร้อยละ 100\n\n2. ทักษะการคิดเชิงคำนวณ\nและการเขียนโปรแกรม\n  - การใช้เหตุผลเชิงตรรกะ\n  - การวางแผนขั้นตอน\n  - การเขียนโปรแกรมอย่างง่าย\n  - การตรวจแก้ข้อผิดพลาด\n\n3. ความพึงพอใจของผู้เรียน\n  - ต่อกิจกรรมและสื่อการเรียนรู้"
        ]
    ]
    elements.append(make_academic_table(framework_table_headers, framework_table_row, [3000, 3000, 3000], ["left", "left", "left"]))
    elements.append(make_p([], space_before=20, space_after=30))

    # SECTION 6: เครื่องมือที่ใช้ในการวิจัย
    elements.append(make_p([
        ("6. เครื่องมือที่ใช้ในการวิจัย", True, False, 32, "000000")
    ], align="left", space_before=140, space_after=40, keep_next=True))

    elements.append(make_p([
        ("1. แผนการจัดการเรียนรู้เชิงรุก (Active Learning): ", True, False, 32, "000000"),
        ("จำนวน 7 แผนการจัดการเรียนรู้ รวม 7 ชั่วโมง ครอบคลุมเนื้อหาเรื่องการใช้เหตุผลเชิงตรรกะ การจัดลำดับขั้นตอน การเขียนโปรแกรมด้วย Scratch และการตรวจหาและแก้ไขข้อผิดพลาด", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=20, line_spacing=240, first_line=720))

    elements.append(make_p([
        ("2. สื่อนวัตกรรมการเรียนรู้: ", True, False, 32, "000000"),
        ("ได้แก่ เกมตอบสนองท่าทางเสมือนจริง CodeBot AR Adventure แผ่นแผนที่ภารกิจตารางเดินช่อง (Unplugged Coding) ชุดแฟลชการ์ดคำสั่งสัญลักษณ์ และบทเรียนการเขียนโปรแกรมอย่างง่ายด้วยโปรแกรม Scratch", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=20, line_spacing=240, first_line=720))

    elements.append(make_p([
        ("3. แบบทดสอบวัดผลสัมฤทธิ์ทางการเรียนรู้: ", True, False, 32, "000000"),
        ("แบบทดสอบปรนัยชนิด 4 ตัวเลือก จำนวน 20 ข้อ ตรงตามตัวชี้วัด ว 4.2 ป.5/1 และ ป.5/2 ใช้ทดสอบก่อนเรียน (Pre-test) และหลังเรียน (Post-test)", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=20, line_spacing=240, first_line=720))

    elements.append(make_p([
        ("4. แบบประเมินรูบริกส์ทักษะการคิดเชิงคำนวณและการเขียนโปรแกรม: ", True, False, 32, "000000"),
        ("เกณฑ์การประเมินแบบ Rubric 4 ระดับคุณภาพ ประเมิน 4 ด้าน ได้แก่ 1) การใช้เหตุผลเชิงตรรกะ 2) การวางแผนขั้นตอน 3) การออกแบบและเขียนโปรแกรม และ 4) การตรวจหาและแก้ไขข้อผิดพลาด", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=20, line_spacing=240, first_line=720))

    elements.append(make_p([
        ("5. แบบสอบถามความพึงพอใจ: ", True, False, 32, "000000"),
        ("แบบมาตราส่วนประมาณค่า 5 ระดับ จำนวน 5 ข้อคำถาม ภาษาเข้าใจง่าย เหมาะสมกับนักเรียนชั้นประถมศึกษา", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=40, line_spacing=240, first_line=720))

    # SECTION 7: วิธีดำเนินการวิจัย (PDCA)
    elements.append(make_p([
        ("7. วิธีดำเนินการวิจัยและการเก็บรวบรวมข้อมูล", True, False, 32, "000000")
    ], align="left", space_before=140, space_after=40, keep_next=True))

    elements.append(make_p([
        ("การวิจัยดำเนินการตามวงจรคุณภาพ PDCA ร่วมกับการจัดการเรียนรู้แบบ Active Learning ดังนี้:", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=20, line_spacing=240, first_line=720))

    elements.append(make_p([
        ("7.1 การวางแผน (Plan): ", True, False, 32, "000000"),
        ("ศึกษาและวิเคราะห์หลักสูตรแกนกลางการศึกษาขั้นพื้นฐานฯ ตัวชี้วัด ว 4.2 ป.5/1 และ ป.5/2 จัดทำโครงสร้างหน่วยการเรียนรู้เรื่อง การใช้เหตุผลเชิงตรรกะและการเขียนโปรแกรมอย่างง่าย ออกแบบแผนการจัดการเรียนรู้เชิงรุก 7 แผน รวม 7 ชั่วโมง สร้างและพัฒนานวัตกรรมสื่อเกม CodeBot AR Adventure แผ่นแผนที่ภารกิจตารางเดินช่อง และชุดแฟลชการ์ดคำสั่งสัญลักษณ์ ตลอดจนจัดเตรียมเครื่องมือวัดและประเมินผลการเรียนรู้", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=20, line_spacing=240, first_line=720))

    elements.append(make_p([
        ("7.2 การปฏิบัติการ (Do): ", True, False, 32, "000000"),
        ("1) ดำเนินการทดสอบก่อนเรียน (Pre-test) จำนวน 20 ข้อ กับนักเรียนกลุ่มเป้าหมายชั้น ป.5 จำนวน 8 คน ในสัปดาห์แรก 2) จัดกิจกรรมการเรียนรู้ตามแผนการจัดการเรียนรู้ทั้ง 7 แผน สัปดาห์ละ 1 ชั่วโมง โดยนำกระบวนการ Gamebase learning ร่วมกับเทคนิค active learning โดยจัดนักเรียน 8 คน ทำงานร่วมกันเป็น 4 คู่ ใช้เทคนิค Pair Programming กำหนดบทบาทชัดเจน คือ บทบาทผู้นำทาง (Navigator) วางแผนเส้นทาง คิดวิเคราะห์ตรรกะ และเรียงบัตรคำสั่งบนโต๊ะ และบทบาทผู้ขับเคลื่อน (Driver) ทำหน้าที่ป้อนคำสั่งผ่านท่าทางหน้ากล้อง AR และป้อนคำสั่งใน Scratch โดยมีการสลับบทบาทกันทุกรอบภารกิจ", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=20, line_spacing=240, first_line=720))

    elements.append(make_p([
        ("7.3 การตรวจสอบและประเมินผล (Check): ", True, False, 32, "000000"),
        ("สังเกตและประเมินพฤติกรรมการเรียนรู้ ทักษะการคิดเชิงคำนวณและการเขียนโปรแกรมระหว่างการทำกิจกรรมรายคู่ ดำเนินการทดสอบหลังเรียน (Post-test) จำนวน 20 ข้อ ในชั่วโมงที่ 7 และให้นักเรียนทำแบบประเมินความพึงพอใจ", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=20, line_spacing=240, first_line=720))

    elements.append(make_p([
        ("7.4 การปรับปรุงและพัฒนา (Act): ", True, False, 32, "000000"),
        ("นำข้อมูลคะแนนและผลการประเมินมาวิเคราะห์ทางสถิติ สรุปเป็นรายงานการวิจัยปฏิบัติการในชั้นเรียน และนำข้อสะท้อนคิดมาปรับปรุงแผนการจัดการเรียนรู้เพื่อเป็นแนวทางในการจัดการเรียนการสอนต่อไป", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=40, line_spacing=240, first_line=720))

    # SECTION 8: ผลการวิเคราะห์ข้อมูล
    elements.append(make_p([
        ("8. ผลการวิเคราะห์ข้อมูล", True, False, 32, "000000")
    ], align="left", space_before=140, space_after=40, keep_next=True))

    elements.append(make_p([
        ("ผู้วิจัยได้นำเสนอผลการวิเคราะห์ข้อมูลแบ่งออกเป็น 4 ตอน ดังนี้", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=20, line_spacing=240, first_line=720))

    # Table 1: Authentic Pre/Post matching PA 2 exactly
    elements.append(make_p([
        ("ตารางที่ 1: ", True, False, 30, "000000"),
        ("ผลสัมฤทธิ์ทางการเรียนรู้รายวิชาเทคโนโลยี (วิทยาการคำนวณ) รายบุคคลของนักเรียนชั้น ป.5 (N = 8)", False, False, 30, "000000")
    ], align="left", space_before=60, space_after=20, keep_next=True))

    t1_headers = [
        "เลขที่",
        "ชื่อ - สกุล ผู้เรียน",
        "ก่อนเรียน\n(20 คะแนน)",
        "หลังเรียน\n(20 คะแนน)",
        "คะแนน\nพัฒนาการ",
        "ร้อยละ\nพัฒนาการ",
        "ผลการประเมิน"
    ]
    t1_rows = [
        ["1", "เด็กชายภูฟ้า  แสงศรี", "5", "14", "+9", "45.00%", "ผ่านเกณฑ์"],
        ["2", "เด็กหญิงพิชญาภา  แสงศรี", "10", "18", "+8", "40.00%", "ผ่านเกณฑ์"],
        ["3", "เด็กหญิงสิริวิมล  สาวิสิทธิ์", "8", "16", "+8", "40.00%", "ผ่านเกณฑ์"],
        ["4", "เด็กหญิงสาวิตรี  สายสมคุณ", "8", "15", "+7", "35.00%", "ผ่านเกณฑ์"],
        ["5", "เด็กหญิงณัฐณิชา  นันทโพธิ์เดช", "8", "16", "+8", "40.00%", "ผ่านเกณฑ์"],
        ["6", "เด็กหญิงรฐา  สอนเต็ม", "7", "16", "+9", "45.00%", "ผ่านเกณฑ์"],
        ["7", "เด็กหญิงกัญญาพัชร  วาจาชื่น", "12", "18", "+6", "30.00%", "ผ่านเกณฑ์"],
        ["8", "เด็กหญิงกัญญารัตน์  บัวบง", "4", "12", "+8", "40.00%", "ผ่านเกณฑ์"],
        ["รวม", "คะแนนรวมทั้งหมด (8 คน)", "62", "125", "+63", "-", "-"],
        ["เฉลี่ย", "ค่าเฉลี่ย (X̄) และ S.D.", "7.75 (2.55)", "15.62 (2.00)", "+7.88", "39.38%", "ผ่านเกณฑ์ 100%"]
    ]
    elements.append(make_academic_table(t1_headers, t1_rows, [800, 2600, 1100, 1100, 1000, 1200, 1200], ["center", "left", "center", "center", "center", "center", "center"]))
    elements.append(make_p([], space_before=20, space_after=30))

    # Table 2: t-test
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
        ["ก่อนเรียน (Pre-test)", "20", "7.75", "2.55", "38.75%", "+7.88", "22.47*", "< .001"],
        ["หลังเรียน (Post-test)", "20", "15.62", "2.00", "78.13%", "", "", ""]
    ]
    elements.append(make_academic_table(t2_headers, t2_rows, [1900, 950, 1100, 950, 1000, 1100, 1000, 1000], ["left", "center", "center", "center", "center", "center", "center", "center"]))
    elements.append(make_p([
        ("* มีนัยสำคัญทางสถิติที่ระดับ .05 (df = 7, t-critical = 2.365)", False, True, 28, "000000")
    ], align="left", space_before=10, space_after=30))

    # Table 3: Rubric Assessment matching PA 2 exactly (X̄ = 3.00, 87.50% at Good+)
    elements.append(make_p([
        ("ตารางที่ 3: ", True, False, 30, "000000"),
        ("ผลการประเมินทักษะการคิดเชิงคำนวณและการเขียนโปรแกรม ตามตัวชี้วัด ว 4.2 ป.5 (N = 8)", False, False, 30, "000000")
    ], align="left", space_before=60, space_after=20, keep_next=True))

    t3_headers = [
        "ด้านทักษะที่ประเมิน (ตามตัวชี้วัด ป.5)",
        "คะแนนเต็ม",
        "ค่าเฉลี่ย (X̄)",
        "ร้อยละ",
        "ระดับคุณภาพ"
    ]
    t3_rows = [
        ["1. การใช้เหตุผลเชิงตรรกะในการแก้ปัญหา (ว 4.2 ป.5/1)", "4.00", "2.75", "68.75%", "ดี"],
        ["2. การวางแผนและอธิบายขั้นตอนการทำงาน (ว 4.2 ป.5/1)", "4.00", "3.38", "84.50%", "ดี"],
        ["3. การออกแบบและเขียนโปรแกรมอย่างง่าย (ว 4.2 ป.5/2)", "4.00", "3.00", "75.00%", "ดี"],
        ["4. การตรวจหาและแก้ไขข้อผิดพลาด (Debugging) (ว 4.2 ป.5/2)", "4.00", "2.88", "72.00%", "ดี"],
        ["เฉลี่ยรวมทั้ง 4 ด้าน", "4.00", "3.00", "75.00%", "ดี"]
    ]
    elements.append(make_academic_table(t3_headers, t3_rows, [4000, 1200, 1200, 1200, 1400], ["left", "center", "center", "center", "center"]))
    elements.append(make_p([
        ("หมายเหตุ: นักเรียนมีผลการประเมินทักษะในระดับ “ดี” ขึ้นไป จำนวน 7 คน จากทั้งหมด 8 คน คิดเป็นร้อยละ 87.50 (สูงกว่าเป้าหมายข้อตกลงที่กำหนดไว้ร้อยละ 80)", False, True, 28, "000000")
    ], align="left", space_before=10, space_after=30))

    # Table 4: Satisfaction matching PA 2 exactly (X̄ = 4.38)
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
        ["1. การใช้สื่อการเรียนรู้ผ่านกล้องและการสั่งการด้วยท่าทางมือ ทำให้เข้าใจคำสั่งได้ง่ายและสนุก", "4.50", "0.53", "มากที่สุด"],
        ["2. การจัดวางแฟลชการ์ดคำสั่งและแผ่นตารางเดินช่องบนโต๊ะ ช่วยให้ไม่สับสนเรื่องทิศทาง", "4.38", "0.52", "มาก"],
        ["3. การจับคู่แบบ Pair Programming (ผู้นำทาง Navigator และผู้ขับเคลื่อน Driver) ทำให้ได้ช่วยเหลือกัน", "4.50", "0.53", "มากที่สุด"],
        ["4. สนุกกับการได้ร่วมมือกับเพื่อนช่วยกันตรวจหาจุดผิดและแก้ไขข้อผิดพลาด (แก้บั๊ก)", "4.25", "0.46", "มาก"],
        ["5. มีความสุขในการเรียน และอยากเรียนวิชาวิทยาการคำนวณด้วยกิจกรรมเชิงรุกแบบนี้อีกในครั้งต่อไป", "4.25", "0.46", "มาก"],
        ["เฉลี่ยรวมทั้งหมด", "4.38", "0.43", "มาก"]
    ]
    elements.append(make_academic_table(t4_headers, t4_rows, [5400, 1200, 1000, 1400], ["left", "center", "center", "center"]))
    elements.append(make_p([], space_before=20, space_after=40))

    # SECTION 9: สรุปผล อภิปรายผล และข้อเสนอแนะ
    elements.append(make_p([
        ("9. สรุปผล อภิปรายผล และข้อเสนอแนะ", True, False, 32, "000000")
    ], align="left", space_before=140, space_after=40, keep_next=True))

    elements.append(make_p([
        ("9.1 สรุปผลการวิจัย", True, False, 32, "000000")
    ], align="left", space_before=40, space_after=20, keep_next=True))

    elements.append(make_p([
        ("1. ด้านผลสัมฤทธิ์ทางการเรียน: นักเรียนชั้นประถมศึกษาปีที่ 5 จำนวน 8 คน มีคะแนนผลสัมฤทธิ์ทางการเรียนรู้หลังเรียนสูงกว่าก่อนเรียนทุกคน คิดเป็นร้อยละ 100 โดยมีคะแนนเฉลี่ยเพิ่มขึ้น 7.88 คะแนน (ก่อนเรียนเฉลี่ย 7.75 คะแนน และหลังเรียนเฉลี่ย 15.62 คะแนน) อย่างมีนัยสำคัญทางสถิติที่ระดับ .05 ซึ่งสูงกว่าเป้าหมายที่กำหนดไว้ในข้อตกลง (เป้าหมาย: ไม่น้อยกว่าร้อยละ 70)", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=20, line_spacing=240, first_line=720))

    elements.append(make_p([
        ("2. ด้านทักษะการคิดเชิงคำนวณและการเขียนโปรแกรม: นักเรียนชั้นประถมศึกษาปีที่ 5 มีผลการประเมินทักษะในระดับ “ดี” ขึ้นไป จำนวน 7 คน คิดเป็นร้อยละ 87.50 โดยมีคะแนนเฉลี่ยชั้นเรียนเท่ากับ 3.00 จาก 4.00 คะแนน ซึ่งสูงกว่าเป้าหมายที่กำหนดไว้ในข้อตกลง (เป้าหมาย: ร้อยละ 80)", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=20, line_spacing=240, first_line=720))

    elements.append(make_p([
        ("3. ด้านความพึงพอใจ: นักเรียนมีความพึงพอใจต่อการจัดกิจกรรมการเรียนรู้อยู่ในระดับ “มาก” โดยมีคะแนนเฉลี่ยรวมเท่ากับ 4.38 จากคะแนนเต็ม 5.00 (S.D. = 0.43)", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=20, line_spacing=240, first_line=720))

    elements.append(make_p([
        ("4. ด้านผลลัพธ์เชิงคุณภาพ: นักเรียนมีความรู้ความเข้าใจในหลักการแก้ปัญหาเชิงตรรกะ สามารถวางแผนขั้นตอนการทำงาน และเขียนโปรแกรมอย่างง่ายด้วยโปรแกรม Scratch ได้อย่างถูกต้องตามลำดับขั้นตอน มีทักษะในการแก้ปัญหาอย่างเป็นระบบ สามารถทำงานร่วมกับผู้อื่นได้ดีผ่านกิจกรรมคู่หู มีความมุ่งมั่นช่วยกันแก้ไขจุดผิดพลาดของโปรแกรมจนสำเร็จ และมีความสุขในการเรียนรู้", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=40, line_spacing=240, first_line=720))

    elements.append(make_p([
        ("9.2 อภิปรายผล", True, False, 32, "000000")
    ], align="left", space_before=40, space_after=20, keep_next=True))

    elements.append(make_p([
        ("1) การลดความเป็นนามธรรมด้วยสื่อรูปธรรม: นักเรียนระดับชั้นประถมศึกษายังต้องการสื่อรูปธรรมในการเชื่อมโยงความคิด การนำเกมตอบสนองท่าทางร่วมกับแผ่นแผนที่ตารางเดินช่องและแฟลชการ์ดคำสั่งบนโต๊ะ ช่วยแก้ปัญหาเรื่องการสับสนทิศทางซ้าย-ขวาได้อย่างชัดเจน นักเรียนได้ขยับร่างกายและจัดวางการ์ดตามมุมมองของตัวละคร ทำให้เข้าใจลำดับขั้นตอนได้อย่างถูกต้องก่อนลงมือเขียนโปรแกรมจริงบนคอมพิวเตอร์", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=20, line_spacing=240, first_line=720))

    elements.append(make_p([
        ("2) การส่งเสริมการมีส่วนร่วมด้วยเทคนิค Pair Programming: การกำหนดบทบาทผู้ขับเคลื่อน (Driver) และผู้นำทาง (Navigator) อย่างชัดเจน พร้อมทั้งสลับบทบาทกันทุกรอบภารกิจ ทำให้นักเรียนทุกคนมีส่วนร่วมอย่างเท่าเทียม นักเรียนที่คิดช้าหรือขาดความมั่นใจได้รับการสนับสนุนจากเพื่อนคู่หู เกิดการแลกเปลี่ยนเหตุผลและช่วยกันคิดวางแผน ไม่เกิดปัญหาการแย่งอุปกรณ์หรือปล่อยให้เพื่อนทำเพียงลำพัง", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=20, line_spacing=240, first_line=720))

    elements.append(make_p([
        ("3) การเปลี่ยนข้อผิดพลาดเป็นความท้าทาย: กิจกรรมการตรวจหาและแก้ไขข้อผิดพลาด (Debugging) ช่วยปรับกระบวนทัศน์ของนักเรียนจากการสุ่มลองผิดลองถูก หรือการลบคำสั่งทิ้งทั้งหมด มาเป็นการวิเคราะห์หาสาเหตุของข้อผิดพลาดทีละขั้นตอน ทำให้นักเรียนเกิดความอดทน มุ่งมั่น และมีความสุขเมื่อแก้ไขปัญหาได้สำเร็จ", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=40, line_spacing=240, first_line=720))

    elements.append(make_p([
        ("9.3 ข้อเสนอแนะ", True, False, 32, "000000")
    ], align="left", space_before=40, space_after=20, keep_next=True))

    elements.append(make_p([
        ("1) ข้อเสนอแนะในการนำผลการวิจัยไปใช้: ครูผู้สอนควรจัดเตรียมสื่อรูปธรรม เช่น บัตรคำสั่งและแผ่นตารางเดินช่อง ให้นักเรียนได้ฝึกปฏิบัติและวางแผนก่อนเข้าสู่การเขียนโปรแกรมบนเครื่องคอมพิวเตอร์เสมอ เพื่อสร้างมโนทัศน์ที่ถูกต้องและลดความสับสนในเรื่องทิศทาง", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=20, line_spacing=240, first_line=720))

    elements.append(make_p([
        ("2) ข้อเสนอแนะในการวิจัยครั้งต่อไป: ควรมีการนำกระบวนการจัดการเรียนรู้โดยใช้เกมเป็นฐานร่วมกับเทคนิค Pair Programming ไปปรับประยุกต์ใช้ในการจัดการเรียนรู้รายวิชาวิทยาการคำนวณในระดับชั้นอื่นๆ หรือขยายผลสู่เนื้อหาการเขียนโปรแกรมที่มีความซับซ้อนยิ่งขึ้นต่อไป", False, False, 32, "000000")
    ], align="both", space_before=0, space_after=40, line_spacing=240, first_line=720))

    # SECTION 10: ว.PA Alignment
    elements.append(make_p([
        ("10. การสะท้อนผลเชื่อมโยงเกณฑ์การประเมิน ว.PA (ด้านที่ 1 ด้านการจัดการเรียนรู้ ครบทั้ง 8 ตัวชี้วัด)", True, False, 32, "000000")
    ], align="left", space_before=140, space_after=40, keep_next=True))

    pa_indicators = [
        ("1.1 การสร้างและหรือพัฒนาหลักสูตร",
         "ข้าพเจ้าได้วิเคราะห์หลักสูตรแกนกลางการศึกษาขั้นพื้นฐาน พุทธศักราช 2551 (ฉบับปรับปรุง พ.ศ. 2560) กลุ่มสาระการเรียนรู้วิทยาศาสตร์และเทคโนโลยี มาตรฐาน ว 4.2 ตัวชี้วัด ป.5/1 และ ป.5/2 โดยจัดทำหน่วยการเรียนรู้เรื่อง การใช้เหตุผลเชิงตรรกะและการเขียนโปรแกรมอย่างง่าย มีโครงสร้างหน่วยการเรียนรู้ แผนการประเมิน และองค์ประกอบครบถ้วนตามหลักสูตรสถานศึกษากำหนด นำไปใช้จัดการเรียนรู้ได้จริงสอดคล้องกับบริบทของสถานศึกษา",
         "ผู้เรียนได้รับการจัดการเรียนรู้ตามหลักสูตรสถานศึกษา และมีผลการเรียนรู้ผ่านเกณฑ์ตามตัวชี้วัดและมาตรฐานที่กำหนด ไม่น้อยกว่าร้อยละ 70"),

        ("1.2 การออกแบบการจัดการเรียนรู้",
         "ข้าพเจ้าได้ออกแบบการจัดการเรียนรู้เชิงรุก (Active Learning) จำนวน 7 แผนการจัดการเรียนรู้ รวม 7 ชั่วโมง โดยเน้นผู้เรียนเป็นสำคัญ บูรณาการกระบวนการ Gamebase learning ผ่านเกมนวัตกรรม CodeBot AR Adventure ร่วมกับแผ่นแผนที่ภารกิจตารางเดินช่อง ชุดแฟลชการ์ดคำสั่งสัญลักษณ์ และการเขียนโปรแกรมด้วย Scratch ออกแบบกิจกรรมแบบจับคู่ Pair Programming เพื่อให้ผู้เรียนได้ฝึกคิดวิเคราะห์และลงมือปฏิบัติจริงตามศักยภาพ",
         "ผู้เรียนได้รับการจัดการเรียนรู้ด้วยแผนการจัดการเรียนรู้ที่เน้นผู้เรียนเป็นสำคัญ ทำให้มีความรู้ ทักษะกระบวนการ และสมรรถนะสำคัญตามหลักสูตร โดยผู้เรียนไม่น้อยกว่าร้อยละ 70 มีผลสัมฤทธิ์ทางการเรียนผ่านเกณฑ์ที่กำหนด"),

        ("1.3 การจัดกิจกรรมการเรียนรู้",
         "ข้าพเจ้าได้จัดกิจกรรมการจัดการเรียนรู้ในรายวิชาที่รับผิดชอบสอน โดยใช้กิจกรรมที่หลากหลาย มีการจัดทำแผนการจัดการเรียนรู้ที่มีองค์ประกอบครบถ้วนตามแบบที่สถานศึกษากำหนด และสามารถนำไปปฏิบัติได้จริง เน้นผู้เรียนเป็นสำคัญ มีการนำสื่อและนวัตกรรมเข้ามาช่วยในการจัดการเรียนการสอนเพื่อให้มีประสิทธิภาพมากยิ่งขึ้น จัดทำบันทึกผลหลังการจัดการเรียนรู้ และนำผลมาปรับปรุงพัฒนาการจัดการเรียนรู้อย่างเหมาะสม มีการอำนวยความสะดวกในการเรียนรู้และส่งเสริมให้ผู้เรียนได้พัฒนาเต็มตามศักยภาพ สามารถเรียนรู้และทำงานร่วมกัน โดยมีการปรับประยุกต์ให้สอดคล้องกับความแตกต่างของผู้เรียน เพื่อให้ผู้เรียนมีผลสัมฤทธิ์ทางการเรียนเป็นไปตามค่าเป้าหมายที่สถานศึกษากำหนด",
         "ผู้เรียนในรายวิชาที่รับผิดชอบสอนไม่น้อยกว่าร้อยละ 70 ได้รับการส่งเสริมการเรียนรู้อย่างมีความสุข มีความรู้และทักษะตามตัวชี้วัดและมาตรฐานการเรียนรู้ และเกิดความเข้าใจในบทเรียนอย่างมีประสิทธิภาพ"),

        ("1.4 การสร้างและหรือพัฒนาสื่อ นวัตกรรม เทคโนโลยี และแหล่งเรียนรู้",
         "ข้าพเจ้าได้สร้างและพัฒนาสื่อ นวัตกรรม และเทคโนโลยีทางการศึกษา ได้แก่ สื่อเกมจำลองภารกิจ แผ่นแผนที่ตารางเดินช่อง ชุดบัตรคำสั่งสัญลักษณ์ และสื่อการเรียนรู้ดิจิทัล โดยนำมาปรับประยุกต์ใช้จัดกิจกรรมการเรียนรู้เชิงรุกในรายวิชาที่รับผิดชอบสอน เพื่อแก้ไขปัญหาความสับสนเรื่องลำดับขั้นตอนและกระบวนการคิดของผู้เรียน ช่วยให้ผู้เรียนได้ฝึกคิด วางแผน และทดลองแก้ปัญหาอย่างเป็นรูปธรรมก่อนลงมือปฏิบัติตามสภาพจริง",
         "ผู้เรียนในรายวิชาที่รับผิดชอบสอนไม่น้อยกว่าร้อยละ 70 ได้รับการพัฒนาทักษะกระบวนการคิดและทักษะการปฏิบัติ ผ่านการใช้สื่อ นวัตกรรม และแหล่งเรียนรู้ที่หลากหลาย ส่งผลให้เข้าใจเนื้อหาและสามารถนำไปประยุกต์ใช้ในการแก้ปัญหาได้"),

        ("1.5 การวัดและประเมินผลการเรียนรู้",
         "ข้าพเจ้าได้สร้างและพัฒนาเครื่องมือวัดและประเมินผลการเรียนรู้ตามสภาพจริงที่หลากหลายและครอบคลุม ทั้งด้านความรู้ (K) ด้านทักษะกระบวนการ (P) และด้านคุณลักษณะอันพึงประสงค์ (A) ได้แก่ แบบทดสอบวัดผลสัมฤทธิ์ทางการเรียนรู้ แบบประเมินทักษะการปฏิบัติงานและการแก้ปัญหา และแบบสังเกตพฤติกรรมการทำงานร่วมกัน โดยมีการปรับประยุกต์เครื่องมือวัดและประเมินผลให้สอดคล้องกับมาตรฐานการเรียนรู้และตัวชี้วัดในรายวิชาที่รับผิดชอบสอน และสอดคล้องกับความแตกต่างของผู้เรียน เพื่อนำผลการประเมินมาใช้สะท้อนพัฒนาการ ปรับปรุง และแก้ไขปัญหาการจัดการเรียนรู้ของผู้เรียนอย่างต่อเนื่อง",
         "ผู้เรียนในรายวิชาที่รับผิดชอบสอนได้รับการวัดและประเมินผลการเรียนรู้ตามสภาพจริงที่ครอบคลุมทุกด้าน ทำให้ผู้เรียนทราบพัฒนาการและระดับความรู้ความสามารถของตนเอง ได้รับการส่งเสริมและแก้ไขข้อบกพร่องทางการเรียนรู้อย่างตรงจุด ส่งผลให้ผู้เรียนไม่น้อยกว่าร้อยละ 70 มีผลสัมฤทธิ์ทางการเรียนผ่านเกณฑ์การประเมินตามที่สถานศึกษากำหนด"),

        ("1.6 การศึกษา วิเคราะห์ และสังเคราะห์ เพื่อแก้ไขปัญหาหรือพัฒนาการเรียนรู้",
         "ข้าพเจ้ามีการศึกษา วิเคราะห์ และสังเคราะห์ปัญหาการจัดการเรียนรู้ที่ส่งผลต่อคุณภาพของผู้เรียนอย่างเป็นระบบ และนำผลการศึกษามาใช้แก้ไขปัญหาและพัฒนาคุณภาพการจัดการเรียนรู้ให้สูงขึ้น โดยได้จัดทำวิจัยปฏิบัติการในชั้นเรียน เรื่อง “การพัฒนาทักษะการเรียนรู้รายวิชาเทคโนโลยี (วิทยาการคำนวณ) กลุ่มสาระการเรียนรู้วิทยาศาสตร์และเทคโนโลยี โดยใช้กระบวนการจัดการเรียนรู้โดยใช้เกมเป็นฐานร่วมกับการจัดการเรียนรู้เชิงรุก” เพื่อนำผลการวิจัยและองค์ความรู้ที่ได้มาปรับประยุกต์พัฒนาการจัดการเรียนรู้ในรายวิชาที่รับผิดชอบสอนต่อไป",
         "ผู้เรียนได้รับการแก้ไขปัญหาการเรียนรู้และพัฒนาทักษะด้วยกระบวนการวิจัยในชั้นเรียน โดยผู้เรียนไม่น้อยกว่าร้อยละ 70 มีพัฒนาการด้านผลสัมฤทธิ์และทักษะการเรียนรู้เพิ่มขึ้นตามเกณฑ์ที่กำหนด"),

        ("1.7 การจัดบรรยากาศที่ส่งเสริมและพัฒนาผู้เรียน",
         "ข้าพเจ้าได้ปรับประยุกต์การจัดบรรยากาศในชั้นเรียนและห้องปฏิบัติการคอมพิวเตอร์ให้มีความเหมาะสม สอดคล้องกับความแตกต่างของผู้เรียนเป็นรายบุคคล เพื่อสร้างแรงบันดาลใจและส่งเสริมให้ผู้เรียนเกิดกระบวนการคิด ทักษะชีวิต ทักษะการทำงาน ทักษะด้านสารสนเทศ สื่อ และเทคโนโลยี โดยจัดห้องเรียนให้เอื้อต่อการเรียนรู้ด้วยตนเอง มีการส่งเสริมกระบวนการเรียนรู้แบบร่วมมือ (เพื่อนช่วยเพื่อน) และการจัดการเรียนรู้เชิงรุก เพื่อกระตุ้นให้ผู้เรียนทุกคนมีส่วนร่วม กล้าคิด กล้าลงมือปฏิบัติ และมีความสุขในการเรียนรู้",
         "ผู้เรียนในรายวิชาที่รับผิดชอบสอนไม่น้อยกว่าร้อยละ 80 มีความสนใจ กระตือรือร้นในการเข้าร่วมกิจกรรมการเรียนรู้ มีความสุขในการเรียน และมีเจตคติที่ดีต่อการจัดการเรียนรู้"),

        ("1.8 การอบรมและพัฒนาคุณลักษณะที่ดีของผู้เรียน",
         "ข้าพเจ้ามีการอบรมบ่มนิสัยให้ผู้เรียนมีคุณธรรม จริยธรรม คุณลักษณะอันพึงประสงค์ และค่านิยมความเป็นไทยที่ดีงาม โดยมีการปรับประยุกต์กิจกรรมการเรียนรู้และการดูแลผู้เรียนให้คำนึงถึงความแตกต่างระหว่างบุคคล ปลูกฝังระเบียบวินัย ความรับผิดชอบ ความซื่อสัตย์สุจริต ความมีน้ำใจ และการยอมรับความคิดเห็นของผู้อื่นผ่านกิจกรรมการเรียนรู้แบบร่วมมือ ตลอดจนสร้างแรงบันดาลใจและเสริมแรงเชิงบวก เพื่อให้ผู้เรียนเกิดความมั่นใจ ปลอดภัย และมีความสุขในการพัฒนาตนเองอย่างเต็มศักยภาพ",
         "ผู้เรียนได้รับการพัฒนาให้มีคุณลักษณะที่ดีทั้งต่อตนเอง ผู้อื่น และสังคม โดยผู้เรียนร้อยละ 100 มีคุณธรรม จริยธรรม ค่านิยมที่ดีงาม และมีผลการประเมินคุณลักษณะอันพึงประสงค์ตามหลักสูตรผ่านเกณฑ์ เป็นไปตามค่าเป้าหมายที่สถานศึกษากำหนด")
    ]

    for ind_title, ind_desc, ind_outcome in pa_indicators:
        elements.append(make_p([
            (ind_title, True, False, 32, "000000")
        ], align="left", space_before=40, space_after=10, keep_next=True))
        
        elements.append(make_p([
            (ind_desc, False, False, 32, "000000")
        ], align="both", space_before=0, space_after=10, line_spacing=240, first_line=720))
        
        elements.append(make_p([
            ("ผลลัพธ์:", True, False, 32, "000000", True)
        ], align="left", space_before=10, space_after=10, keep_next=True))
        
        elements.append(make_p([
            (ind_outcome, False, False, 32, "000000")
        ], align="both", space_before=0, space_after=30, line_spacing=240, first_line=720))

    # Appendices
    elements.append(make_page_break())
    elements.append(make_p([
        ("ภาคผนวก", True, False, 36, "000000")
    ], align="center", space_before=200, space_after=100, keep_next=True))

    elements.append(make_p([
        ("ร่องรอยหลักฐานการจัดกิจกรรมการเรียนรู้เชิงรุก สื่อนวัตกรรม และการประเมินผลตามสภาพจริง", False, True, 28, "000000")
    ], align="center", space_before=0, space_after=200))

    appendix_items = [
        ("ภาคผนวก ก: ", "ตัวอย่างแผนการจัดการเรียนรู้เชิงรุก (Active Learning) 7 แผน พร้อมบันทึกหลังแผน"),
        ("ภาคผนวก ข: ", "เครื่องมือวัดและประเมินผล (แบบทดสอบ 20 ข้อ, เกณฑ์รูบริกส์ ว 4.2, แบบสอบถามความพึงพอใจ)"),
        ("ภาคผนวก ค: ", "สื่อนวัตกรรมเกมตอบสนองท่าทาง CodeBot AR Adventure, แผ่นแผนที่ภารกิจ และชุดแฟลชการ์ดคำสั่งสัญลักษณ์"),
        ("ภาคผนวก ง: ", "ภาพถ่ายบรรยากาศการจัดกิจกรรมการเรียนรู้แบบจับคู่ Pair Programming (Driver & Navigator)"),
        ("ภาคผนวก จ: ", "ผลงานการเขียนโปรแกรมอย่างง่ายด้วยโปรแกรม Scratch ของนักเรียนชั้นประถมศึกษาปีที่ 5")
    ]
    for code, desc in appendix_items:
        elements.append(make_p([
            (code, True, False, 30, "000000"),
            (desc, False, False, 30, "000000")
        ], align="left", space_before=10, space_after=20, line_spacing=240, first_line=720))

    elements.append(make_p([], space_before=200, space_after=40))
    elements.append(make_p([
        ("ขอรับรองว่าข้อมูลในรายงานการวิจัยปฏิบัติการในชั้นเรียนเล่มนี้ถูกต้องตามความเป็นจริงทุกประการ\n\n"
         "ลงชื่อ.................................................................... ผู้วิจัย\n"
         "( นายเตชินท์  อินทมล )\n"
         "ตำแหน่ง ครู (ไม่มีวิทยฐานะ) โรงเรียนบ้านโนนป่าหว้านเชียงฮาย\n\n\n"
         "ลงชื่อ.................................................................... ผู้รับรองรายงาน\n"
         "( .................................................................... )\n"
         "ผู้อำนวยการโรงเรียนบ้านโนนป่าหว้านเชียงฮาย", False, False, 30, "000000")
    ], align="center", space_before=60, space_after=40, line_spacing=260))

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
      </w:pPr>
    </w:pPrDefault>
  </w:docDefaults>
</w:styles>"""

    document_xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
            xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <w:body>
    {doc_body}
    <w:sectPr>
      <w:pgSz w:w="11906" w:h="16838"/>
      <w:pgMar w:top="1418" w:right="1134" w:bottom="1418" w:left="1701" w:header="720" w:footer="720" w:gutter="0"/>
      <w:cols w:space="720"/>
      <w:docGrid w:linePitch="360"/>
    </w:sectPr>
  </w:body>
</w:document>"""

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", content_types)
        zf.writestr("_rels/.rels", rels)
        zf.writestr("word/_rels/document.xml.rels", doc_rels)
        zf.writestr("word/styles.xml", styles)
        zf.writestr("word/document.xml", document_xml)
        
    buf.seek(0)
    return buf.getvalue()

if __name__ == "__main__":
    docx_bytes = build_car_document()
    
    path1 = "รายงานวิจัยในชั้นเรียน_วิทยาการคำนวณ_ป5_ครูเตชินท์.docx"
    path2 = os.path.join("docs", "รายงานวิจัยในชั้นเรียน_วิทยาการคำนวณ_ป5_ครูเตชินท์.docx")
    
    with open(path1, "wb") as f:
        f.write(docx_bytes)
    print(f"Updated {path1} successfully.")
    
    os.makedirs("docs", exist_ok=True)
    with open(path2, "wb") as f:
        f.write(docx_bytes)
    print(f"Updated {path2} successfully.")
