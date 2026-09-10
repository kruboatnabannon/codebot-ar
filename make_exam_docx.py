# -*- coding: utf-8 -*-
import zipfile, io, os, html
from generate_car_docx import esc, make_p, make_table, make_callout
from exam_questions import exam_questions

def make_page_break():
    return '<w:p><w:r><w:br w:type="page"/></w:r></w:p>'

def make_maze_table_docx():
    col_w = 1500
    grid_cells = [
        # row 1
        [("ช่องที่ 3", "F1F5F9", "334155", True), ("🍎 ผลแอปเปิ้ล", "FEE2E2", "991B1B", True), ("", "FFFFFF", "000000", False), ("", "FFFFFF", "000000", False)],
        # row 2
        [("ช่องที่ 2", "F1F5F9", "334155", True), ("", "FFFFFF", "000000", False), ("", "FFFFFF", "000000", False), ("", "FFFFFF", "000000", False)],
        # row 3
        [("ช่องที่ 1", "F1F5F9", "334155", True), ("", "FFFFFF", "000000", False), ("", "FFFFFF", "000000", False), ("", "FFFFFF", "000000", False)],
        # row 4
        [("🤖 จุดเริ่ม\n(หันหน้า ⬆️)", "DBEAFE", "1E3A8A", True), ("", "FFFFFF", "000000", False), ("", "FFFFFF", "000000", False), ("", "FFFFFF", "000000", False)]
    ]
    xml = ['<w:tbl>']
    xml.append('''<w:tblPr>
        <w:tblW w:w="6000" w:type="dxa"/>
        <w:jc w:val="center"/>
        <w:tblBorders>
            <w:top w:val="single" w:sz="12" w:space="0" w:color="475569"/>
            <w:left w:val="single" w:sz="12" w:space="0" w:color="475569"/>
            <w:bottom w:val="single" w:sz="12" w:space="0" w:color="475569"/>
            <w:right w:val="single" w:sz="12" w:space="0" w:color="475569"/>
            <w:insideH w:val="single" w:sz="6" w:space="0" w:color="94A3B8"/>
            <w:insideV w:val="single" w:sz="6" w:space="0" w:color="94A3B8"/>
        </w:tblBorders>
    </w:tblPr>''')
    xml.append('<w:tblGrid>')
    for _ in range(4):
        xml.append(f'<w:gridCol w:w="{col_w}"/>')
    xml.append('</w:tblGrid>')

    for row in grid_cells:
        xml.append('<w:tr><w:trPr><w:trHeight w:val="460"/></w:trPr>')
        for text, bg, color, bold in row:
            b_tag = "<w:b/><w:bCs/>" if bold else ""
            lines = text.split("\n")
            p_runs = []
            for idx, line in enumerate(lines):
                br_tag = "<w:br/>" if idx > 0 else ""
                t_content = f"<w:t>{esc(line)}</w:t>" if line else "<w:t></w:t>"
                p_runs.append(f'<w:r><w:rPr><w:rFonts w:ascii="TH Sarabun PSK" w:hAnsi="TH Sarabun PSK" w:cs="TH Sarabun PSK"/>{b_tag}<w:sz w:val="26"/><w:szCs w:val="26"/><w:color w:val="{color}"/></w:rPr>{br_tag}{t_content}</w:r>')
            runs_xml = "".join(p_runs)
            xml.append(f'''<w:tc>
                <w:tcPr>
                    <w:tcW w:w="{col_w}" w:type="dxa"/>
                    <w:shd w:val="clear" w:color="auto" w:fill="{bg}"/>
                    <w:vAlign w:val="center"/>
                </w:tcPr>
                <w:p>
                    <w:pPr>
                        <w:jc w:val="center"/>
                        <w:spacing w:before="50" w:after="50"/>
                    </w:pPr>
                    {runs_xml}
                </w:p>
            </w:tc>''')
        xml.append('</w:tr>')
    xml.append('</w:tbl>')
    return "".join(xml)

def build_exam_docx():
    elements = []

    # =========================================================================
    # HEADER SECTION
    # =========================================================================
    elements.append(make_p([("แบบทดสอบวัดผลสัมฤทธิ์ทางการเรียนรู้วิทยาการคำนวณ (Pre-test / Post-test)", True, False, 34, "1E3A8A")], align="center", space_before=80, space_after=30))
    elements.append(make_p([("กลุ่มสาระการเรียนรู้วิทยาศาสตร์และเทคโนโลยี รายวิชาเทคโนโลยี (วิทยาการคำนวณ) ว15101 ชั้นประถมศึกษาปีที่ 5", True, False, 26, "1F2937")], align="center", space_before=0, space_after=30))
    elements.append(make_p([("โรงเรียนบ้านโนนป่าหว้านเชียงฮาย สำนักงานเขตพื้นที่การศึกษาประถมศึกษาหนองบัวลำภู เขต 2", False, False, 24, "4B5563")], align="center", space_before=0, space_after=60))

    # Name & Score Table
    info_headers = ["ข้อมูลประจำตัวผู้เข้าสอบ", "การทดสอบ", "คะแนนเต็ม", "คะแนนที่ได้ (ครูผู้ตรวจ)"]
    info_rows = [
        [
            "ชื่อ - นามสกุล: ........................................................................................\nชั้น ป.5    เลขที่: ..........    กลุ่มคู่หูที่: ..........",
            "[  ] ก่อนเรียน (Pre-test)\n[  ] หลังเรียน (Post-test)",
            "20 คะแนน",
            "............ / 20 คะแนน\n\n(ลงชื่อ)....................................\n( นายเตชินท์ อินทมล )"
        ]
    ]
    elements.append(make_table(info_headers, info_rows, [4500, 2000, 1200, 2326], ["left", "center", "center", "center"]))
    elements.append(make_p([], space_before=40, space_after=40))

    instructions = """1. แบบทดสอบฉบับนี้เป็นแบบปรนัย 4 ตัวเลือก (ก, ข, ค, ง) จำนวน 20 ข้อ คะแนนเต็ม 20 คะแนน เวลา 40 นาที
2. ครอบคลุมตัวชี้วัดกลุ่มสาระการเรียนรู้วิทยาศาสตร์และเทคโนโลยีตามหลักสูตรแกนกลางฯ (ฉบับปรับปรุง พ.ศ. 2560):
   • ว 4.2 ป.5/1: การใช้เหตุผลเชิงตรรกะในการแก้ปัญหา การคาดการณ์ผลลัพธ์ (ข้อ 1 - 5)
   • ว 4.2 ป.5/2: การออกแบบโปรแกรม บัตรคำสั่ง บล็อก Scratch และการตรวจหาข้อผิดพลาด (ข้อ 6 - 20)
3. ให้นักเรียนทำเครื่องหมายกากบาท ( X ) ทับตัวเลือกที่ถูกต้องที่สุดเพียงข้อเดียวลงในกระดาษคำตอบ"""
    elements.append(make_callout(instructions, title="📌 คำชี้แจงสำหรับนักเรียน"))
    elements.append(make_p([], space_before=40, space_after=40))

    # Questions loop
    part_headers = {
        1: "ตอนที่ 1: การใช้เหตุผลเชิงตรรกะและการแก้ปัญหาในชีวิตประจำวัน (ตัวชี้วัด ว 4.2 ป.5/1)",
        6: "ตอนที่ 2: การออกแบบโปรแกรมและการจัดลำดับคำสั่ง (ตัวชี้วัด ว 4.2 ป.5/2)",
        11: "ตอนที่ 3: บล็อกคำสั่งในโปรแกรม Scratch ภาษาไทย (ตัวชี้วัด ว 4.2 ป.5/2)",
        16: "ตอนที่ 4: การตรวจหาข้อผิดพลาด (บั๊ก) และการทำงานร่วมกันแบบ Pair Programming (ตัวชี้วัด ว 4.2 ป.5/2)"
    }

    for item in exam_questions:
        num = item["num"]
        if num in part_headers:
            if num > 1:
                elements.append(make_page_break())
            elements.append(make_p([(part_headers[num], True, False, 28, "1E3A8A")], space_before=100, space_after=40))

        q_text = f"ข้อที่ {num}. {item['q']}"
        elements.append(make_p([(q_text, True, False, 28, "111827")], space_before=60, space_after=20))
        
        if item.get("has_grid_7"):
            elements.append(make_maze_table_docx())
            elements.append(make_p([], space_before=20, space_after=20))

        for opt in item["options"]:
            elements.append(make_p([(f"      {opt}", False, False, 27, "374151")], space_before=12, space_after=12))

    # =========================================================================
    # STUDENT ANSWER SHEET
    # =========================================================================
    elements.append(make_page_break())
    elements.append(make_p([("กระดาษคำตอบแบบทดสอบวัดผลสัมฤทธิ์ทางการเรียนรู้", True, False, 34, "1E3A8A")], align="center", space_before=80, space_after=30))
    elements.append(make_p([("รายวิชาเทคโนโลยี (วิทยาการคำนวณ) ว15101 ชั้น ป.5 | โรงเรียนบ้านโนนป่าหว้านเชียงฮาย", True, False, 26, "1F2937")], align="center", space_before=0, space_after=50))

    ans_info_headers = ["ข้อมูลประจำตัวนักเรียน", "การทดสอบ", "คะแนนเต็ม", "คะแนนที่ได้"]
    ans_info_rows = [[
        "ชื่อ - สกุล: .................................................................................\nชั้น ป.5    เลขที่: ........    กลุ่มคู่หูที่: ........",
        "[  ] ก่อนเรียน (Pre-test)\n[  ] หลังเรียน (Post-test)",
        "20 คะแนน",
        "......... / 20 คะแนน\n\nลงชื่อผู้ตรวจ..........................."
    ]]
    elements.append(make_table(ans_info_headers, ans_info_rows, [4200, 2200, 1400, 2226], ["left", "center", "center", "center"]))
    elements.append(make_p([], space_before=50, space_after=30))

    elements.append(make_p([("คำแนะนำ: ทำเครื่องหมาย กากบาท ( X ) ทับตัวอักษร ก, ข, ค หรือ ง ที่ถูกต้องที่สุดเพียงข้อเดียว", False, True, 25, "4B5563")], align="center", space_before=0, space_after=30))

    grid_headers = ["ข้อ", "ก", "ข", "ค", "ง", " ", "ข้อ", "ก", "ข", "ค", "ง"]
    grid_rows = []
    for i in range(1, 11):
        j = i + 10
        grid_rows.append([str(i), "(  )", "(  )", "(  )", "(  )", " ", str(j), "(  )", "(  )", "(  )", "(  )"])
    elements.append(make_table(grid_headers, grid_rows, [800, 800, 800, 800, 800, 600, 800, 800, 800, 800, 800], ["center"] * 11))
    elements.append(make_p([], space_before=60, space_after=60))

    # =========================================================================
    # ANSWER KEY & CURRICULUM ALIGNMENT TABLE (For Teacher)
    # =========================================================================
    elements.append(make_page_break())
    elements.append(make_p([("เฉลยคำตอบและตารางวิเคราะห์ตัวชี้วัดตามหลักสูตร (สำหรับครูผู้สอน)", True, False, 34, "1E3A8A")], align="center", space_before=80, space_after=30))
    elements.append(make_p([("รายวิชาเทคโนโลยี (วิทยาการคำนวณ) ว15101 ชั้น ป.5 | ครูผู้สอน: นายเตชินท์ อินทมล", False, True, 25, "4B5563")], align="center", space_before=0, space_after=60))

    key_headers = ["ข้อที่", "ตัวชี้วัด", "สาระการเรียนรู้ / หัวข้อประเมิน", "เฉลย", "เหตุผลและคำอธิบายเฉลย"]
    key_rows = []

    for item in exam_questions:
        n = item["num"]
        key_rows.append([str(n), item["indicator"], item["topic"], item["ans"], item["exp"]])

    elements.append(make_table(key_headers, key_rows, [700, 1300, 2600, 600, 4826], ["center", "center", "left", "center", "left"]))
    elements.append(make_p([], space_before=60, space_after=60))

    # Scoring Criteria
    elements.append(make_p([("เกณฑ์การแปลผลคะแนนผลสัมฤทธิ์ทางการเรียน (เต็ม 20 คะแนน):", True, False, 27, "1F2937")]))
    t_criteria_headers = ["ช่วงคะแนน (เต็ม 20)", "ร้อยละ", "ระดับคุณภาพ", "ความหมายและการนำไปพัฒนา"]
    t_criteria_rows = [
        ["16 - 20 คะแนน", "80.00% - 100%", "ดีมาก (4)", "มีความรู้ความเข้าใจตรรกะและการเขียนโปรแกรมในระดับยอดเยี่ยม สามารถออกแบบอัลกอริทึมและเขียนโค้ดได้อย่างถูกต้องคล่องแคล่ว"],
        ["13 - 15 คะแนน", "65.00% - 79.99%", "ดี (3)", "มีความเข้าใจตรรกะและโครงสร้างคำสั่งเป็นอย่างดี สามารถแก้ปัญหาและตรวจหาบั๊กได้ด้วยตนเองเป็นส่วนใหญ่"],
        ["10 - 12 คะแนน", "50.00% - 64.99%", "พอใช้ (2)", "ผ่านเกณฑ์ขั้นต่ำตามหลักสูตร มีความเข้าใจพื้นฐาน แต่อาจต้องได้รับการแนะนำเพิ่มเติมเรื่องเงื่อนไขและการวนซ้ำ"],
        ["ต่ำกว่า 10 คะแนน", "ต่ำกว่า 50.00%", "ปรับปรุง (1)", "ยังไม่ผ่านเกณฑ์ ควรได้รับการสอนเสริมด้วยสื่อสัมผัสรูปธรรม (แฟลชการ์ด) และให้เพื่อนคู่หูช่วยอธิบายตามเทคนิค Pair Programming"]
    ]
    elements.append(make_table(t_criteria_headers, t_criteria_rows, [1800, 1600, 1600, 5026], ["center", "center", "center", "left"]))

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
        <w:sz w:val="30"/>
        <w:szCs w:val="30"/>
        <w:lang w:val="th-TH"/>
      </w:rPr>
    </w:rPrDefault>
    <w:pPrDefault>
      <w:pPr>
        <w:spacing w:before="50" w:after="50" w:line="260" w:lineRule="auto"/>
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
      <w:pgMar w:top="1134" w:right="1134" w:bottom="1134" w:left="1134"/>
    </w:sectPr>
  </w:body>
</w:document>"""

    out_file = "แบบทดสอบวัดผลสัมฤทธิ์_วิทยาการคำนวณ_ป5_ครูเตชินท์.docx"
    with zipfile.ZipFile(out_file, "w", zipfile.ZIP_DEFLATED) as docx:
        docx.writestr("[Content_Types].xml", content_types)
        docx.writestr("_rels/.rels", rels)
        docx.writestr("word/_rels/document.xml.rels", doc_rels)
        docx.writestr("word/styles.xml", styles)
        docx.writestr("word/document.xml", document_xml)

    print(f"Created 100% Familiar Child-Friendly Exam DOCX: {out_file}")
    os.system(f"cp '{out_file}' docs/")

if __name__ == "__main__":
    build_exam_docx()
