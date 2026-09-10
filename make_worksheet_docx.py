# -*- coding: utf-8 -*-
import zipfile, io, os
from generate_car_docx import esc, make_p, make_callout, make_table

def build_worksheet_docx():
    elements = []

    # Title Header
    elements.append(make_p([("ใบงานกิจกรรมภารกิจนักสืบโค้ดดิ้ง (Mission Log Sheet)", True, False, 36, "1E3A8A")], align="center", space_before=100, space_after=60))
    elements.append(make_p([("รายวิชาเทคโนโลยี (วิทยาการคำนวณ) ว15101 ชั้นประถมศึกษาปีที่ 5 | นวัตกรรมเกม CodeBot AR Adventure", False, True, 26, "4B5563")], align="center", space_before=0, space_after=160))

    # Team Info Table
    team_headers = ["ข้อมูลคู่หูนักเขียนโค้ด (Pair Programming Team)", "เลขที่", "บทบาทเริ่มต้น"]
    team_rows = [
        ["ชื่อคู่หู / ทีม: .....................................................................................", "-", "กลุ่มที่ ........"],
        ["คนที่ 1: ............................................................................................", "........", "[  ] Driver (ผู้ควบคุม)   [  ] Navigator (ผู้นำทาง)"],
        ["คนที่ 2: ............................................................................................", "........", "[  ] Driver (ผู้ควบคุม)   [  ] Navigator (ผู้นำทาง)"]
    ]
    elements.append(make_table(team_headers, team_rows, [5400, 1000, 2626], ["left", "center", "center"]))
    elements.append(make_p([], space_before=100, space_after=100))

    # Instructions Box
    instr = """คำชี้แจงสำหรับนักเรียน:
1. จับคู่แบ่งหน้าที่: Navigator (ผู้วางแผน) ดูแผนที่และคิดลำดับคำสั่งบนใบงาน / Driver (ผู้ปฏิบัติการ) ยืนหน้ากล้องแตะบล็อกคำสั่ง AR
2. เมื่อเล่นผ่านไป 10 นาที หรือจบ 1 ด่าน ให้กดปุ่ม "สลับบทบาท" เพื่อผลัดกันทำหน้าที่
3. บันทึกผลการทดสอบ จำนวนดาว และคำตอบลงใน Mission Log Sheet นี้เพื่อสะสมคะแนนทีม"""
    elements.append(make_callout(instr, title="ข้อตกลงและกติกาการปฏิบัติภารกิจ"))

    # Mission 1: Sequence & Algorithm
    elements.append(make_p([("ภารกิจที่ 1: วางแผนเส้นทางพิชิตอวกาศ (Algorithm & Sequence)", True, False, 30, "1E3A8A")], space_before=180, space_after=80))
    elements.append(make_p([("ให้นักเรียนช่วยกันวางแผนพาหุ่นยนต์ CodeBot จากจุดเริ่มต้น (Start) ไปเก็บแบตเตอรี่และเข้ายานอวกาศ (Goal) โดยเขียนลำดับคำสั่ง (เช่น เดินหน้า, หันซ้าย, หันขวา, กระโดด) ทีละขั้นตอน:", False, False, 28, "1F2937")]))

    m1_headers = ["ขั้นตอน (Step)", "คำสั่งที่เลือกใช้ (Action)", "วัตถุประสงค์ / ตรวจสอบความถูกต้อง"]
    m1_rows = [
        ["ก้าวที่ 1", "........................................................", "[  ] ถูกต้อง   [  ] ชนสิ่งกีดขวาง"],
        ["ก้าวที่ 2", "........................................................", "[  ] ถูกต้อง   [  ] ชนสิ่งกีดขวาง"],
        ["ก้าวที่ 3", "........................................................", "[  ] ถูกต้อง   [  ] ชนสิ่งกีดขวาง"],
        ["ก้าวที่ 4", "........................................................", "[  ] ถูกต้อง   [  ] ชนสิ่งกีดขวาง"],
        ["ก้าวที่ 5", "........................................................", "[  ] ถูกต้อง   [  ] ชนสิ่งกีดขวาง"],
        ["ก้าวที่ 6", "........................................................", "[  ] ถูกต้อง   [  ] ชนสิ่งกีดขวาง"],
    ]
    elements.append(make_table(m1_headers, m1_rows, [1600, 4426, 3000], ["center", "left", "center"]))
    elements.append(make_p([("บันทึกผลภารกิจที่ 1:  จำนวนดาวที่ได้รับ: [  ] 1 ดาว   [  ] 2 ดาว   [  ] 3 ดาว (สมบูรณ์แบบ)", True, False, 28, "2563EB")], space_before=80, space_after=140))

    # Mission 2: Loops
    elements.append(make_p([("ภารกิจที่ 2: ถอดรหัสลับพลังวนซ้ำ (Pattern Recognition & Loops)", True, False, 30, "1E3A8A")], space_before=180, space_after=80))
    elements.append(make_p([("คำถามนักสืบ: ในด่านทางเดินยาว นักเรียนสังเกตพบคำสั่งที่ต้องทำซ้ำๆ กันหรือไม่?", False, False, 28, "1F2937")]))
    
    m2_headers = ["คำถามวิเคราะห์รูปแบบ (Pattern)", "บันทึกคำตอบของคู่เรา"]
    m2_rows = [
        ["1. คำสั่งที่ต้องทำซ้ำบ่อยที่สุด คือคำสั่งใด?", "คำสั่ง: ............................................................................"],
        ["2. คำสั่งนี้ถูกทำซ้ำติดต่อกันกี่ครั้ง?", "ทำซ้ำจำนวน: ................ ครั้ง"],
        ["3. เมื่อนำบล็อก [ ทำซ้ำ (Loop) ] มาครอบคำสั่งนี้ เกิดประโยชน์อย่างไร?", "ตอบ: ..............................................................................\n......................................................................................"],
        ["4. เปรียบเทียบความยาวโค้ด: โค้ดแบบเดิม กับ แบบวนซ้ำ", "แบบเดิมใช้: ........ บล็อก | แบบวนซ้ำใช้เพียง: ........ บล็อก"]
    ]
    elements.append(make_table(m2_headers, m2_rows, [4500, 4526], ["left", "left"]))
    elements.append(make_p([("บันทึกผลภารกิจที่ 2:  ได้รับดาวโบนัส “โค้ดสั้นกระชับ (Efficiency)” หรือไม่?  [  ] ได้รับ   [  ] ยังไม่ได้รับ", True, False, 28, "2563EB")], space_before=80, space_after=140))

    # Mission 3: Conditions
    elements.append(make_p([("ภารกิจที่ 3: เงื่อนไขกุญแจเลเซอร์ ถ้า...แล้ว (If-Then Decision)", True, False, 30, "1E3A8A")], space_before=180, space_after=80))
    elements.append(make_p([("ในด่านที่มีประตูกั้นและกุญแจเลเซอร์ ให้นักเรียนเขียนประโยคเงื่อนไขตรรกะที่หุ่นยนต์ต้องตัดสินใจ:", False, False, 28, "1F2937")]))
    
    cond_text = """เขียนตรรกะเงื่อนไขของคู่เรา:
- [ ถ้า (IF) ] : หุ่นยนต์เดินไปเก็บ .......................................................... ได้แล้ว
- [ แล้ว (THEN) ] : ประตูเลเซอร์จะ ....................................................... และหุ่นยนต์สามารถเดินผ่านได้
- [ มิฉะนั้น (ELSE) ] : ถ้ายังไม่มีกุญแจ ห้ามเดินชน เพราะจะเกิดผลคือ ........................................................"""
    elements.append(make_callout(cond_text, title="บันทึกการตัดสินใจเชิงตรรกะ"))

    # Mission 4: Debugging
    elements.append(make_p([("ภารกิจที่ 4: ยอดนักสืบตามล่าและกำจัดบั๊ก (Debugging Challenge)", True, False, 30, "1E3A8A")], space_before=180, space_after=80))
    elements.append(make_p([("ในด่านท้าทายพิเศษ มีโค้ดที่มีข้อผิดพลาด (Bug) แอบแฝงอยู่ ให้นักเรียนสืบหาและแก้ไขให้ถูกต้อง:", False, False, 28, "1F2937")]))

    m4_headers = ["จุดที่พบข้อผิดพลาด (Bug)", "คำสั่งเดิมที่ผิด", "คำสั่งใหม่ที่แก้ไขให้ถูกต้อง"]
    m4_rows = [
        ["บั๊กจุดที่ 1 (บรรทัดที่ ........)", "....................................................", "...................................................."],
        ["บั๊กจุดที่ 2 (บรรทัดที่ ........)", "....................................................", "...................................................."]
    ]
    elements.append(make_table(m4_headers, m4_rows, [3000, 3000, 3026], ["center", "left", "left"]))
    elements.append(make_p([], space_before=80, space_after=80))

    # Reflection & Self-Evaluation
    elements.append(make_p([("การประเมินตนเองและสะท้อนคิดหลังการเรียนรู้ (After Action Review: AAR)", True, False, 30, "1E3A8A")], space_before=160, space_after=80))
    
    aar_headers = ["รายการประเมินทักษะของคู่เรา", "ระดับคุณภาพ (ทำเครื่องหมาย /)", "ข้อคิดเห็นเพิ่มเติม"]
    aar_rows = [
        ["1. การวางแผนและแบ่งงาน (Driver & Navigator)", "[  ] ดีเยี่ยม   [  ] พอใช้   [  ] ต้องปรับปรุง", "...................................................."],
        ["2. การคิดแก้ปัญหาอย่างเป็นขั้นตอน (Algorithm)", "[  ] ดีเยี่ยม   [  ] พอใช้   [  ] ต้องปรับปรุง", "...................................................."],
        ["3. ความพยายามในการล่าบั๊กและไม่ยอมแพ้", "[  ] ดีเยี่ยม   [  ] พอใช้   [  ] ต้องปรับปรุง", "...................................................."],
        ["4. ความสนุกสนานและตื่นเต้นกับกล้อง AR", "[  ] ดีเยี่ยม   [  ] พอใช้   [  ] ต้องปรับปรุง", "...................................................."]
    ]
    elements.append(make_table(aar_headers, aar_rows, [4000, 2600, 2426], ["left", "center", "left"]))
    elements.append(make_p([], space_before=120, space_after=80))

    # Signoff Box
    sign_headers = ["ลงชื่อคู่หูนักเขียนโค้ด", "ความคิดเห็นและคะแนนของครูผู้สอน"]
    sign_rows = [
        [
            "Navigator: ....................................................\n\nDriver: ........................................................\n\nวันที่: ......./......./ 2568",
            "คะแนนภารกิจรวม: ............ / 20 คะแนน\nระดับคุณภาพ: [  ] ดีเยี่ยม (4)  [  ] ดี (3)  [  ] พอใช้ (2)\n\n(ลงชื่อ).................................................... ครูผู้สอน\n( นายเตชินท์ อินทมล )"
        ]
    ]
    elements.append(make_table(sign_headers, sign_rows, [4513, 4513], ["left", "left"]))

    # Package into docx
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
        <w:sz w:val="28"/>
        <w:szCs w:val="28"/>
        <w:lang w:val="th-TH"/>
      </w:rPr>
    </w:rPrDefault>
  </w:docDefaults>
</w:styles>"""

    document_xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:body>
    {doc_body}
    <w:sectPr>
      <w:pgSz w:w="11906" w:h="16838"/>
      <w:pgMar w:top="1080" w:right="1080" w:bottom="1080" w:left="1080" w:header="720" w:footer="720" w:gutter="0"/>
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
    
    path1 = "ใบงานภารกิจโค้ดดิ้ง_ป5_ครูเตชินท์.docx"
    path2 = os.path.join("docs", "ใบงานภารกิจโค้ดดิ้ง_ป5_ครูเตชินท์.docx")
    
    with open(path1, "wb") as f:
        f.write(data)
    with open(path2, "wb") as f:
        f.write(data)
        
    print(f"Generated Worksheet DOCX:")
    print(f"1. {path1} ({len(data)} bytes)")
    print(f"2. {path2} ({len(data)} bytes)")

if __name__ == "__main__":
    build_worksheet_docx()
