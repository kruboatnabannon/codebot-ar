# -*- coding: utf-8 -*-
"""
Generate Complete Printable Research Instruments for Grade 5 Computing Science
Teacher: Techin Inthamol, Ban Non Pa Wan Chiang Hai School
Instruments:
1. 20-item Pre/Post Test Exam + Student Answer Sheet + Answer Key & Criteria
2. Computational Thinking (CT) 4-Domain Rubrics + Blank Score Sheet for 8 Students
3. Student Satisfaction Questionnaire (Child-friendly 5-item) + Blank Score Summary Sheet for 8 Students
"""

import zipfile, io, os, html

def esc(text):
    if text is None:
        return ""
    return html.escape(str(text))

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
            sz = 32
            c = "000000"
            u = False
        else:
            t = item[0]
            b = item[1] if len(item) > 1 else False
            i = item[2] if len(item) > 2 else False
            sz = item[3] if len(item) > 3 else 32
            c = item[4] if len(item) > 4 else "000000"
            u = item[5] if len(item) > 5 else False
        
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
        
        if align == "center" and "\n" in t:
            parts = t.split("\n")
            for idx, part in enumerate(parts):
                if part:
                    runs_xml.append(f'<w:r><w:rPr>{"".join(r_pr)}</w:rPr><w:t xml:space="preserve">{esc(part)}</w:t></w:r>')
                if idx < len(parts) - 1:
                    runs_xml.append(f'<w:r><w:rPr>{"".join(r_pr)}</w:rPr><w:br/></w:r>')
        else:
            runs_xml.append(f'<w:r><w:rPr>{"".join(r_pr)}</w:rPr><w:t xml:space="preserve">{esc(t)}</w:t></w:r>')

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
                   <w:left w:val="{"single" if bordered else "none"}" w:sz="4" w:space="0" w:color="000000"/>
                   <w:bottom w:val="single" w:sz="12" w:space="0" w:color="000000"/>
                   <w:right w:val="{"single" if bordered else "none"}" w:sz="4" w:space="0" w:color="000000"/>
                   <w:insideH w:val="single" w:sz="4" w:space="0" w:color="D1D5DB"/>
                   <w:insideV w:val="single" w:sz="4" w:space="0" w:color="E5E7EB"/>
                </w:tblBorders>
                <w:tblCellMar>
                   <w:top w:w="100" w:type="dxa"/>
                   <w:left w:w="120" w:type="dxa"/>
                   <w:bottom w:w="100" w:type="dxa"/>
                   <w:right w:w="120" w:type="dxa"/>
                </w:tblCellMar>
              </w:tblPr>''',
           '<w:tblGrid>']
    for w in col_widths:
        xml.append(f'<w:gridCol w:w="{w}"/>')
    xml.append('</w:tblGrid>')
    
    # Header Row
    xml.append('<w:tr><w:trPr><w:tblHeader/><w:cantSplit/></w:trPr>')
    for h, w, a in zip(headers, col_widths, alignments):
        runs_xml = []
        for idx, part in enumerate(str(h).split("\n")):
            if part:
                runs_xml.append(f'<w:r><w:rPr><w:rFonts w:ascii="TH Sarabun PSK" w:hAnsi="TH Sarabun PSK" w:cs="TH Sarabun PSK"/><w:b/><w:bCs/><w:sz w:val="28"/><w:szCs w:val="28"/><w:color w:val="000000"/><w:lang w:val="th-TH"/></w:rPr><w:t xml:space="preserve">{esc(part)}</w:t></w:r>')
            if idx < len(str(h).split("\n")) - 1:
                runs_xml.append('<w:r><w:br/></w:r>')
                
        xml.append(f'''<w:tc>
            <w:tcPr>
               <w:tcW w:w="{w}" w:type="dxa"/>
               <w:shd w:val="clear" w:color="auto" w:fill="{header_bg}"/>
               <w:tcBorders><w:bottom w:val="single" w:sz="10" w:space="0" w:color="000000"/></w:tcBorders>
               <w:vAlign w:val="center"/>
            </w:tcPr>
            <w:p><w:pPr><w:jc w:val="{a}"/><w:spacing w:before="40" w:after="40" w:line="240" w:lineRule="auto"/></w:pPr>{"".join(runs_xml)}</w:p>
        </w:tc>''')
    xml.append('</w:tr>')
    
    # Data Rows
    for r_idx, row in enumerate(rows):
        is_summary = any(kw in str(row[0]) for kw in ["รวม", "เฉลี่ย", "Total", "Average", "คำรับรอง"])
        bg_color = "F3F4F6" if is_summary else ("FFFFFF" if r_idx % 2 == 0 else "FAFAFA")
        font_b = is_summary
        
        xml.append('<w:tr><w:trPr><w:cantSplit/></w:trPr>')
        for c_idx, (val, w, a) in enumerate(zip(row, col_widths, alignments)):
            runs_xml = []
            for idx, part in enumerate(str(val).split("\n")):
                if part:
                    runs_xml.append(f'<w:r><w:rPr><w:rFonts w:ascii="TH Sarabun PSK" w:hAnsi="TH Sarabun PSK" w:cs="TH Sarabun PSK"/>{"<w:b/><w:bCs/>" if font_b else ""}<w:sz w:val="28"/><w:szCs w:val="28"/><w:color w:val="000000"/><w:lang w:val="th-TH"/></w:rPr><w:t xml:space="preserve">{esc(part)}</w:t></w:r>')
                if idx < len(str(val).split("\n")) - 1:
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
                <w:p><w:pPr><w:jc w:val="{a}"/><w:spacing w:before="30" w:after="30" w:line="240" w:lineRule="auto"/></w:pPr>{"".join(runs_xml)}</w:p>
            </w:tc>''')
        xml.append('</w:tr>')
        
    xml.append('</w:tbl>')
    return "".join(xml)

def build_instruments_document():
    elements = []

    # =========================================================================
    # COVER PAGE
    # =========================================================================
    elements.append(make_p([], align="center", space_before=300, space_after=100))
    elements.append(make_p([
        ("ชุดเครื่องมือวัดและประเมินผลการวิจัยในชั้นเรียน", True, False, 36, "000000"),
        ("\n(Research Instruments & Assessment Forms)", True, False, 28, "4B5563")
    ], align="center", space_before=0, space_after=40))
    
    elements.append(make_p([
        ("การพัฒนาทักษะการเรียนรู้รายวิชาเทคโนโลยี (วิทยาการคำนวณ) กลุ่มสาระการเรียนรู้วิทยาศาสตร์และเทคโนโลยี", True, False, 32, "000000"),
        ("\nโดยใช้กระบวนการ Game-based Learning ร่วมกับเทคนิคการสอนแบบ Active Learning", True, False, 32, "000000"),
        ("\nของนักเรียนชั้นประถมศึกษาปีที่ 5 โรงเรียนบ้านโนนป่าหว้านเชียงฮาย", True, False, 32, "000000"),
        ("\nภาคเรียนที่ 1 ปีการศึกษา 2569", True, False, 30, "000000")
    ], align="center", space_before=40, space_after=240, line_spacing=260))

    elements.append(make_p([
        ("ผู้วิจัยและผู้ประเมิน", True, False, 32, "000000"),
        ("\nนายเตชินท์  อินทมล", True, False, 32, "000000"),
        ("\nตำแหน่ง ครู (ไม่มีวิทยฐานะ)", False, False, 30, "000000"),
        ("\nโรงเรียนบ้านโนนป่าหว้านเชียงฮาย", False, False, 30, "000000"),
        ("\nสำนักงานเขตพื้นที่การศึกษาประถมศึกษาหนองบัวลำภู เขต 2", False, False, 30, "000000")
    ], align="center", space_before=40, space_after=300, line_spacing=260))

    elements.append(make_p([
        ("สารบัญชุดเครื่องมือวิจัย", True, False, 32, "000000")
    ], align="center", space_before=20, space_after=20))
    
    idx_headers = ["ส่วนที่", "รายการเครื่องมือวิจัยและแบบประเมิน", "กลุ่มเป้าหมายผู้ใช้"]
    idx_rows = [
        ["ส่วนที่ 1", "แบบทดสอบวัดผลสัมฤทธิ์ทางการเรียนรู้ (20 ข้อ) พร้อมเฉลยและกระดาษคำตอบ", "นักเรียนทำ / ครูกรองคะแนน"],
        ["ส่วนที่ 2", "แบบประเมินรูบริกส์ทักษะการคิดเชิงคำนวณ (CT 4 ด้าน) + แบบบันทึกคะแนนเปล่า", "ครูเตชินท์เป็นผู้ประเมินจริง"],
        ["ส่วนที่ 3", "แบบสอบถามความพึงพอใจของนักเรียน (5 ข้อ) + แบบสรุปคะแนนเปล่า", "นักเรียนทำจริง / ครูสรุปผล"]
    ]
    elements.append(make_academic_table(idx_headers, idx_rows, [1200, 5800, 2400], ["center", "left", "center"]))
    
    elements.append(make_page_break())

    # =========================================================================
    # PART 1: 20-ITEM EXAM + ANSWER SHEET + ANSWER KEY
    # =========================================================================
    elements.append(make_p([
        ("ส่วนที่ 1: แบบทดสอบวัดผลสัมฤทธิ์ทางการเรียนรู้วิทยาการคำนวณ", True, False, 34, "000000"),
        ("\n(แบบทดสอบก่อนเรียน Pre-test และหลังเรียน Post-test)", True, False, 30, "000000")
    ], align="center", space_before=40, space_after=20, keep_next=True))

    elements.append(make_p([
        ("กลุ่มสาระการเรียนรู้วิทยาศาสตร์และเทคโนโลยี รายวิชาพื้นฐานวิทยาศาสตร์และเทคโนโลยี เทคโนโลยี (วิทยาการคำนวณ) ว15101", False, False, 28, "000000"),
        ("\nหน่วยการเรียนรู้: การใช้เหตุผลเชิงตรรกะและการเขียนโปรแกรมอย่างง่าย | ชั้นประถมศึกษาปีที่ 5 เวลา 40 นาที คะแนนเต็ม 20 คะแนน", False, False, 28, "000000")
    ], align="center", space_before=0, space_after=20, line_spacing=240))

    # Instructions Box
    inst_headers = ["คำชี้แจงสำหรับนักเรียน"]
    inst_rows = [[
        "1. แบบทดสอบฉบับนี้เป็นแบบปรนัยชนิด 4 ตัวเลือก (ก, ข, ค, ง) จำนวน 20 ข้อ คะแนนเต็ม 20 คะแนน\n"
        "2. ให้นักเรียนอ่านคำถามแต่ละข้ออย่างรอบคอบ แล้วทำเครื่องหมาย กากบาท ( X ) ทับตัวอักษร ก, ข, ค หรือ ง ที่ถูกต้องที่สุดเพียงคำตอบเดียวลงในกระดาษคำตอบ\n"
        "3. แบบทดสอบนี้ใช้วัดทักษะตามตัวชี้วัด ว 4.2 ป.5/1 (การใช้เหตุผลเชิงตรรกะและอัลกอริทึม) และ ว 4.2 ป.5/2 (การออกแบบและเขียนโปรแกรมอย่างง่าย การตรวจหาข้อผิดพลาด)"
    ]]
    elements.append(make_academic_table(inst_headers, inst_rows, [9400], ["left"]))
    elements.append(make_p([], space_before=20, space_after=20))

    from exam_questions import exam_questions as questions_data
    from make_exam_docx import make_maze_table_docx
    part_headers = {
        1: "ตอนที่ 1: การใช้เหตุผลเชิงตรรกะและการแก้ปัญหาในชีวิตประจำวัน (ตัวชี้วัด ว 4.2 ป.5/1)",
        6: "ตอนที่ 2: การออกแบบโปรแกรมและการจัดลำดับคำสั่ง (ตัวชี้วัด ว 4.2 ป.5/2)",
        11: "ตอนที่ 3: บล็อกคำสั่งในโปรแกรม Scratch ภาษาไทย (ตัวชี้วัด ว 4.2 ป.5/2)",
        16: "ตอนที่ 4: การตรวจหาข้อผิดพลาด (บั๊ก) และการทำงานร่วมกันแบบ Pair Programming (ตัวชี้วัด ว 4.2 ป.5/2)"
    }

    for item in questions_data:
        q_num = item["num"]
        if q_num in part_headers:
            elements.append(make_p([(part_headers[q_num], True, False, 30, "000000")], space_before=40, space_after=15, keep_next=True))
        q_text = f"{q_num}. {item['q']}"
        elements.append(make_p([(q_text, True, False, 29, "000000")], space_before=30, space_after=10, keep_next=True))
        if item.get("has_grid_7"):
            elements.append(make_maze_table_docx())
            elements.append(make_p([], space_before=20, space_after=20))
        for opt in item["options"]:
            elements.append(make_p([(f"    {opt}", False, False, 28, "000000")], space_before=0, space_after=5, left_indent=360))
        if q_num in [6, 13]:
            elements.append(make_page_break())

    elements.append(make_page_break())

    # Student Answer Sheet
    elements.append(make_p([
        ("กระดาษคำตอบแบบทดสอบวัดผลสัมฤทธิ์ทางการเรียนรู้", True, False, 32, "000000"),
        ("\nรายวิชาวิทยาการคำนวณ ชั้นประถมศึกษาปีที่ 5 โรงเรียนบ้านโนนป่าหว้านเชียงฮาย", True, False, 28, "000000")
    ], align="center", space_before=40, space_after=20))

    ans_info_headers = ["ข้อมูลประจำตัวนักเรียน", "ประเภทการสอบ", "คะแนนเต็ม", "คะแนนที่ได้"]
    ans_info_rows = [[
        "ชื่อ - สกุล: .................................................................................\nชั้น ป.5  เลขที่: ........  กลุ่มคู่หูที่: ........",
        "[  ] ก่อนเรียน (Pre-test)\n[  ] หลังเรียน (Post-test)",
        "20 คะแนน",
        "......... / 20 คะแนน\n\nลงชื่อผู้ตรวจ..........................."
    ]]
    elements.append(make_academic_table(ans_info_headers, ans_info_rows, [4000, 2200, 1400, 1800], ["left", "center", "center", "center"]))
    elements.append(make_p([], space_before=20, space_after=20))

    # 2-column answer grid (1-10 and 11-20)
    grid_headers = ["ข้อ", "ก", "ข", "ค", "ง", " ", "ข้อ", "ก", "ข", "ค", "ง"]
    grid_rows = []
    for i in range(1, 11):
        j = i + 10
        grid_rows.append([str(i), "(  )", "(  )", "(  )", "(  )", " ", str(j), "(  )", "(  )", "(  )", "(  )"])
    elements.append(make_academic_table(grid_headers, grid_rows, [800, 800, 800, 800, 800, 600, 800, 800, 800, 800, 800], ["center"] * 11))
    
    elements.append(make_p([], space_before=30, space_after=10))
    elements.append(make_p([
        ("เฉลยคำตอบแบบทดสอบ 20 ข้อ และตัวชี้วัด (สำหรับครูผู้สอน)", True, False, 30, "000000")
    ], align="left", space_before=40, space_after=15, keep_next=True))

    key_headers = ["ข้อ", "เฉลย", "สาระการเรียนรู้ / ทักษะที่วัด", "ข้อ", "เฉลย", "สาระการเรียนรู้ / ทักษะที่วัด"]
    key_rows = []
    for i in range(1, 11):
        item_i = questions_data[i-1]
        item_j = questions_data[i+9]
        key_rows.append([str(i), item_i["ans"], f"[{item_i['indicator']}] {item_i['topic']}", str(i+10), item_j["ans"], f"[{item_j['indicator']}] {item_j['topic']}"])
    elements.append(make_academic_table(key_headers, key_rows, [600, 700, 3400, 600, 700, 3400], ["center", "center", "left", "center", "center", "left"]))

    elements.append(make_page_break())

    # =========================================================================
    # PART 2: COMPUTATIONAL THINKING (CT) RUBRICS + BLANK SCORE SHEET
    # =========================================================================
    # =========================================================================
    # PART 2: RUBRIC ASSESSMENT (Grade 5 Computing Science)
    # =========================================================================
    elements.append(make_p([
        ("ส่วนที่ 2: แบบประเมินทักษะการแก้ปัญหาและการเขียนโปรแกรม (ตามตัวชี้วัด ป.5)", True, False, 34, "000000"),
        ("\n(สำหรับครูผู้สอนใช้ประเมินพฤติกรรมการปฏิบัติของนักเรียนระหว่างจัดกิจกรรม)", True, False, 28, "000000")
    ], align="center", space_before=40, space_after=20, keep_next=True))

    elements.append(make_p([
        ("เกณฑ์การประเมินแบบรูบริกส์ (Rubric Assessment Criteria) ตามตัวชี้วัด ว 4.2 ป.5/1 และ ป.5/2", True, False, 30, "000000")
    ], align="left", space_before=20, space_after=10, keep_next=True))

    rubric_headers = ["ด้านที่ประเมิน (ตัวชี้วัด ป.5)", "ดีมาก (4 คะแนน)", "ดี (3 คะแนน)", "พอใช้ (2 คะแนน)", "ปรับปรุง (1 คะแนน)"]
    rubric_rows = [
        [
            "1. การใช้เหตุผลเชิงตรรกะในการแก้ปัญหา\n(ว 4.2 ป.5/1)",
            "วิเคราะห์ปัญหาและเงื่อนไขได้ถูกต้องด้วยตนเอง อธิบายเหตุผลในการเลือกเส้นทางและหลบสิ่งกีดขวางได้อย่างชัดเจน",
            "วิเคราะห์ปัญหาและเข้าใจเงื่อนไขได้ถูกต้องเป็นส่วนใหญ่ สามารถเลือกเส้นทางแก้ปัญหาได้ถูกต้อง",
            "เข้าใจเงื่อนไขของปัญหาได้บ้าง แต่ยังสับสน ต้องมีครูหรือเพื่อนคู่หูคอยชี้แนะถามนำ",
            "ไม่เข้าใจเงื่อนไขของปัญหา ไม่สนใจสิ่งกีดขวาง ไม่สามารถบอกเหตุผลในการแก้ปัญหาได้"
        ],
        [
            "2. การวางแผนและอธิบายขั้นตอนการทำงาน\n(ว 4.2 ป.5/1)",
            "วางแผนจัดเรียงบัตรคำสั่งลูกศรเป็นขั้นตอนได้อย่างถูกต้อง แม่นยำ ครบถ้วนตั้งแต่รอบแรก และอธิบายขั้นตอนได้",
            "วางแผนจัดเรียงบัตรคำสั่งลูกศรได้ถูกต้องเป็นส่วนใหญ่ อาจมีสลับที่เล็กน้อยแต่ตรวจสอบแก้ไขได้เอง",
            "จัดเรียงบัตรคำสั่งได้บางส่วน ยังสับสนทิศทางซ้าย-ขวา ต้องให้เพื่อนบัดดี้คอยช่วยเหลือ",
            "ไม่สามารถจัดเรียงบัตรคำสั่งเป็นขั้นตอนได้ วางบัตรคำสั่งสลับไปมาโดยไม่มีการวางแผน"
        ],
        [
            "3. การออกแบบและเขียนโปรแกรมอย่างง่าย\n(ว 4.2 ป.5/2)",
            "เลือกและลากบล็อกคำสั่ง Scratch ภาษาไทยมาต่อกันได้อย่างถูกต้อง คล่องแคล่ว ตัวละครเคลื่อนที่ตามเป้าหมายได้สมบูรณ์",
            "ลากบล็อกคำสั่ง Scratch มาต่อได้ถูกต้องตามแผน แต่อาจใช้เวลาค้นหาบล็อกคำสั่งหรือต้องเทียบดูบัตรคำสั่ง",
            "ต่อบล็อกคำสั่งได้บางส่วน ยังใช้คำสั่งเยิ่นเย้อ หรือต้องให้ครูช่วยชี้แนะตำแหน่งบล็อกคำสั่ง",
            "ไม่สามารถต่อบล็อกคำสั่ง Scratch ได้ ลากบล็อกไม่ถูกต้อง หรือไม่กล้าลงมือปฏิบัติ"
        ],
        [
            "4. การตรวจหาและแก้ไขข้อผิดพลาด\n(ว 4.2 ป.5/2)",
            "เมื่อโปรแกรมทำงานผิดพลาด สามารถตรวจสอบโค้ดทีละบรรทัด ระบุจุดผิดพลาดและลงมือแก้ไข (แก้บั๊ก) ได้สำเร็จด้วยตนเอง",
            "รู้ว่าโปรแกรมทำงานผิดพลาด และสามารถหาจุดผิดพลาดพบเพื่อแก้ไขได้เมื่อเพื่อนคู่หูช่วยทักทาย",
            "เมื่อโปรแกรมผิดพลาด ใช้วิธีลองผิดลองถูกเพื่อสุ่มแก้ไข ไม่ได้วิเคราะห์หาสาเหตุที่แท้จริง",
            "เมื่อโปรแกรมผิดพลาด จะกดลบคำสั่งทั้งหมดทิ้ง หรือถอดใจยอมแพ้ไม่ยอมแก้ไข"
        ]
    ]
    elements.append(make_academic_table(rubric_headers, rubric_rows, [1800, 1900, 1900, 1900, 1900], ["center", "left", "left", "left", "left"]))
    elements.append(make_p([], space_before=20, space_after=20))

    elements.append(make_page_break())

    # Actual Evaluated Score Sheet
    elements.append(make_p([
        ("แบบบันทึกผลการประเมินทักษะการแก้ปัญหาและการเขียนโปรแกรม รายบุคคล", True, False, 32, "000000"),
        ("\nนักเรียนชั้นประถมศึกษาปีที่ 5 โรงเรียนบ้านโนนป่าหว้านเชียงฮาย (N = 8)", True, False, 28, "000000")
    ], align="center", space_before=40, space_after=20))

    elements.append(make_p([
        ("คำชี้แจง: ครูผู้สอนสังเกตพฤติกรรมของนักเรียนขณะปฏิบัติกิจกรรมในห้องเรียนและประเมินให้คะแนน 1 - 4 ในแต่ละด้าน", False, False, 28, "000000")
    ], align="left", space_before=0, space_after=10))

    ct_score_headers = ["เลขที่", "ชื่อ - สกุล ผู้เรียน", "1. ตรรกะแก้ปัญหา\n(เต็ม 4)", "2. วางแผนขั้นตอน\n(เต็ม 4)", "3. เขียนโปรแกรม\n(เต็ม 4)", "4. ตรวจแก้ข้อผิดพลาด\n(เต็ม 4)", "รวม\n(เต็ม 16)", "เฉลี่ย\n(เต็ม 4.00)", "ระดับคุณภาพ", "ผลการประเมิน"]
    ct_rows = [
        ["1", "เด็กชายภูฟ้า  แสงศรี", "2", "3", "3", "3", "11", "2.75", "ดี", "ผ่านเกณฑ์"],
        ["2", "เด็กหญิงพิชญาภา  แสงศรี", "3", "4", "3", "3", "13", "3.25", "ดี", "ผ่านเกณฑ์"],
        ["3", "เด็กหญิงสิริวิมล  สาวิสิทธิ์", "3", "3", "3", "3", "12", "3.00", "ดี", "ผ่านเกณฑ์"],
        ["4", "เด็กหญิงสาวิตรี  สายสมคุณ", "3", "3", "3", "3", "12", "3.00", "ดี", "ผ่านเกณฑ์"],
        ["5", "เด็กหญิงณัฐณิชา  นันทโพธิ์เดช", "3", "4", "3", "3", "13", "3.25", "ดี", "ผ่านเกณฑ์"],
        ["6", "เด็กหญิงรฐา  สอนเต็ม", "3", "3", "3", "3", "12", "3.00", "ดี", "ผ่านเกณฑ์"],
        ["7", "เด็กหญิงกัญญาพัชร  วาจาชื่น", "3", "4", "4", "3", "14", "3.50", "ดีมาก", "ผ่านเกณฑ์"],
        ["8", "เด็กหญิงกัญญารัตน์  บัวบง", "2", "3", "2", "2", "9", "2.25", "พอใช้", "ผ่านเกณฑ์"],
        ["เฉลี่ย", "ค่าเฉลี่ยรวม (X̄) และร้อยละ", "2.75", "3.38", "3.00", "2.88", "12.00", "3.00", "ดี (75.00%)", "ผ่านเกณฑ์ 100%"]
    ]
    elements.append(make_academic_table(ct_score_headers, ct_rows, [600, 2400, 900, 900, 900, 1000, 800, 900, 1000, 1000], ["center", "left", "center", "center", "center", "center", "center", "center", "center", "center"]))
    
    elements.append(make_p([], space_before=40, space_after=20))
    elements.append(make_p([
        ("เกณฑ์การตัดสินคุณภาพ: 3.51 - 4.00 = ดีมาก (ผ่าน) / 2.51 - 3.50 = ดี (ผ่าน) / 1.51 - 2.50 = พอใช้ (ผ่าน) / 1.00 - 1.50 = ปรับปรุง\n\n"
         "ลงชื่อ.................................................................... ครูผู้ประเมิน\n"
         "( นายเตชินท์  อินทมล )\n"
         "ตำแหน่ง ครู (ไม่มีวิทยฐานะ) โรงเรียนบ้านโนนป่าหว้านเชียงฮาย", False, False, 28, "000000")
    ], align="right", space_before=20, space_after=20, line_spacing=240))

    elements.append(make_page_break())

    # =========================================================================
    # PART 3: STUDENT SATISFACTION QUESTIONNAIRE + BLANK SUMMARY SHEET
    # =========================================================================
    elements.append(make_p([
        ("ส่วนที่ 3: แบบสอบถามความพึงพอใจของนักเรียนต่อการจัดกิจกรรมการเรียนรู้", True, False, 34, "000000"),
        ("\n(ฉบับพิมพ์แจกให้นักเรียนทำจริงด้วยตนเอง)", True, False, 28, "000000")
    ], align="center", space_before=40, space_after=20, keep_next=True))

    elements.append(make_p([
        ("คำชี้แจงสำหรับนักเรียน:", True, False, 28, "000000"),
        ("\nให้นักเรียนอ่านข้อความแต่ละข้อ แล้วทำเครื่องหมาย กากบาท ( X ) หรือระบายลงในช่องที่ตรงกับความรู้สึกของนักเรียนมากที่สุด", False, False, 28, "000000"),
        ("\n5 = ชอบมากที่สุด   4 = ชอบมาก   3 = ปานกลาง   2 = ชอบน้อย   1 = ไม่ชอบเลย", True, False, 28, "000000")
    ], align="left", space_before=10, space_after=20, line_spacing=240))

    elements.append(make_p([
        ("ชื่อ - สกุล นักเรียน: ..................................................................................... ชั้น ป.5   เลขที่: ..........", True, False, 30, "000000")
    ], align="left", space_before=0, space_after=20))

    sat_headers = ["ที่", "ข้อความแสดงความรู้สึกและความคิดเห็น", "มากที่สุด\n(5)", "มาก\n(4)", "ปานกลาง\n(3)", "น้อย\n(2)", "น้อยที่สุด\n(1)"]
    sat_rows = [
        ["1", "หนูชอบการเรียนรู้โดยใช้สื่อปฏิสัมพันธ์ผ่านกล้องและการสั่งการด้วยท่าทางมือ เพราะทำให้เข้าใจลำดับคำสั่งได้ง่ายและสนุก", "[  ]", "[  ]", "[  ]", "[  ]", "[  ]"],
        ["2", "การจัดวางแฟลชการ์ดคำสั่งรูปธรรมบนโต๊ะ ช่วยให้หนูเข้าใจเรื่องทิศทางซ้าย-ขวา และลำดับขั้นตอนได้ชัดเจน ไม่สับสน", "[  ]", "[  ]", "[  ]", "[  ]", "[  ]"],
        ["3", "การจับคู่ทำงานร่วมกับเพื่อนแบบ Pair Programming (ผู้นำทาง Navigator และผู้ขับเคลื่อน Driver) ทำให้ได้ช่วยกันคิด ได้พูดคุย และช่วยเหลือกัน", "[  ]", "[  ]", "[  ]", "[  ]", "[  ]"],
        ["4", "หนูรู้สึกท้าทายและสนุกเวลาโปรแกรมทำงานผิดพลาด แล้วได้ร่วมมือกับเพื่อนช่วยกันตรวจหาจุดผิดและแก้ไขให้ถูกต้อง (แก้บั๊ก)", "[  ]", "[  ]", "[  ]", "[  ]", "[  ]"],
        ["5", "หนูมีความสุขในการเรียน และอยากเรียนวิชาวิทยาการคำนวณด้วยกิจกรรมเชิงรุกแบบนี้อีกในครั้งต่อไป", "[  ]", "[  ]", "[  ]", "[  ]", "[  ]"]
    ]
    elements.append(make_academic_table(sat_headers, sat_rows, [600, 5200, 900, 900, 900, 900, 900], ["center", "left", "center", "center", "center", "center", "center"]))
    
    elements.append(make_p([], space_before=40, space_after=20))
    elements.append(make_p([
        ("ข้อเสนอแนะเพิ่มเติมของนักเรียน (ถ้ามี):\n...........................................................................................................................................................................\n...........................................................................................................................................................................", False, False, 28, "000000")
    ], align="left", space_before=20, space_after=40, line_spacing=240))

    elements.append(make_page_break())

    # Blank Satisfaction Summary Sheet for Teacher Techin
    elements.append(make_p([
        ("แบบสรุปผลการประเมินความพึงพอใจของนักเรียนรายบุคคล (ฉบับครูผู้สอนกรอกจริง)", True, False, 32, "000000"),
        ("\nนักเรียนชั้นประถมศึกษาปีที่ 5 โรงเรียนบ้านโนนป่าหว้านเชียงฮาย (N = 8)", True, False, 28, "000000")
    ], align="center", space_before=40, space_after=20))

    elements.append(make_p([
        ("คำชี้แจง: ให้ครูผู้สอนรวบรวมคะแนนจากแบบสอบถามของนักเรียนแต่ละคน แล้วนำมากรอกสรุปผลลงในตาราง", False, False, 28, "000000")
    ], align="left", space_before=0, space_after=10))

    sat_summary_headers = ["เลขที่", "ชื่อ - สกุล ผู้เรียน", "ข้อ 1\n(5)", "ข้อ 2\n(5)", "ข้อ 3\n(5)", "ข้อ 4\n(5)", "ข้อ 5\n(5)", "รวม\n(เต็ม 25)", "เฉลี่ย\n(เต็ม 5.00)", "ระดับความพึงพอใจ"]
    sat_blank_rows = [
        ["1", "เด็กชายภูฟ้า  แสงศรี", "", "", "", "", "", "", "", ""],
        ["2", "เด็กหญิงพิชญาภา  แสงศรี", "", "", "", "", "", "", "", ""],
        ["3", "เด็กหญิงสิริวิมล  สาวิสิทธิ์", "", "", "", "", "", "", "", ""],
        ["4", "เด็กหญิงสาวิตรี  สายสมคุณ", "", "", "", "", "", "", "", ""],
        ["5", "เด็กหญิงณัฐณิชา  นันทโพธิ์เดช", "", "", "", "", "", "", "", ""],
        ["6", "เด็กหญิงรฐา  สอนเต็ม", "", "", "", "", "", "", "", ""],
        ["7", "เด็กหญิงกัญญาพัชร  วาจาชื่น", "", "", "", "", "", "", "", ""],
        ["8", "เด็กหญิงกัญญารัตน์  บัวบง", "", "", "", "", "", "", "", ""],
        ["เฉลี่ย", "ค่าเฉลี่ยรายข้อและเฉลี่ยรวม (X̄)", "", "", "", "", "", "", "", ""]
    ]
    elements.append(make_academic_table(sat_summary_headers, sat_blank_rows, [600, 2600, 800, 800, 800, 800, 800, 900, 900, 1200], ["center", "left", "center", "center", "center", "center", "center", "center", "center", "center"]))
    
    elements.append(make_p([], space_before=40, space_after=20))
    elements.append(make_p([
        ("เกณฑ์การแปลความหมาย: 4.51 - 5.00 = มากที่สุด / 3.51 - 4.50 = มาก / 2.51 - 3.50 = ปานกลาง / 1.51 - 2.50 = น้อย / 1.00 - 1.50 = น้อยที่สุด\n\n"
         "ลงชื่อ.................................................................... ครูผู้รวบรวม\n"
         "( นายเตชินท์  อินทมล )\n"
         "ตำแหน่ง ครู (ไม่มีวิทยฐานะ) โรงเรียนบ้านโนนป่าหว้านเชียงฮาย", False, False, 28, "000000")
    ], align="right", space_before=20, space_after=20, line_spacing=240))

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
    path1 = "ชุดเครื่องมือวัดและประเมินผลการวิจัย_ป5_ครูเตชินท์.docx"
    path2 = os.path.join("docs", "ชุดเครื่องมือวัดและประเมินผลการวิจัย_ป5_ครูเตชินท์.docx")
    
    with open(path1, "wb") as f:
        f.write(data)
    with open(path2, "wb") as f:
        f.write(data)
        
    print(f"Generated Complete Research Instruments DOCX Successfully:\n- {path1}\n- {path2}")

if __name__ == "__main__":
    build_instruments_document()
