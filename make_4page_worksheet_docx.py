# -*- coding: utf-8 -*-
import zipfile, io, os
from generate_car_docx import esc, make_p, make_callout, make_table

def make_page_break():
    return '<w:p><w:r><w:br w:type="page"/></w:r></w:p>'

def make_big_write_table(rows_count, prefix="ก้าวที่ "):
    headers = ["ลำดับขั้นตอน", "คำสั่งที่เลือกใช้ (เขียนตัวโตๆ ได้เลย)", "ผลการทดสอบหน้ากล้อง AR"]
    rows = []
    for i in range(1, rows_count + 1):
        rows.append([f"{prefix}{i}", ".........................................................................................", "[  ] ผ่านฉลุย   [  ] ชนสิ่งกีดขวาง"])
    return make_table(headers, rows, [1400, 5226, 2400], ["center", "left", "center"])

def build_4page_docx():
    elements = []

    # =========================================================================
    # PAGE 1: ใบงานที่ 1 (ก้าวแรกและอัลกอริทึม)
    # =========================================================================
    elements.append(make_p([("🤖 ใบงานที่ 1: การค้นหารูปแบบและอัลกอริทึมก้าวแรก (Pattern Recognition & Sequence) 🚀", True, False, 32, "1E3A8A")], align="center", space_before=60, space_after=40))
    elements.append(make_p([("รายวิชาเทคโนโลยี (วิทยาการคำนวณ) ว15101 ชั้น ป.5 (สอดรับเกม CodeBot AR ด่าน 1-10 แทร็ก ป.5) | โรงเรียนบ้านโนนป่าหว้านเชียงฮาย", False, True, 24, "4B5563")], align="center", space_before=0, space_after=120))

    t_team = [
        ["ข้อมูลคู่หูนักเขียนโค้ด", "เลขที่", "บทบาทประจำด่านที่ 1"],
        ["ชื่อคู่หู/ทีม: .....................................................................", "-", "กลุ่มที่ ........."],
        ["1. ...................................................................................", "......", "[  ] Navigator (ผู้นำทาง/วาดแผนที่)"],
        ["2. ...................................................................................", "......", "[  ] Driver (ผู้สั่งการหน้ากล้อง AR)"]
    ]
    elements.append(make_table(t_team[0], t_team[1:], [4800, 800, 3426], ["left", "center", "left"]))
    elements.append(make_p([], space_before=60, space_after=60))

    elements.append(make_callout("🎯 คำแนะนำสำหรับเนวิเกเตอร์ (Navigator):\nให้ใช้ดินสอหรือปากกาสี ลากเส้นทางเดิน บนแผนที่ตารางกริดด้านล่าง เพื่อนำหุ่นยนต์ 🤖 เดินไปเก็บแบตเตอรี่ 🔋 แล้วเข้าสู่ยานอวกาศ 🚀 โดยไม่ชนหินอุกกาบาต 🪨!", title="คำชี้แจงภารกิจที่ 1"))

    elements.append(make_p([("🗺️ แผนที่ตารางกริดจำลองในเกม (Grid 5x5) - สัญลักษณ์: 🤖 เริ่มต้น, 🔋 แบตเตอรี่, 🪨 หินอุกกาบาต, 🚀 ยานอวกาศ", True, False, 26, "1E3A8A")], space_before=80, space_after=40))
    map1_headers = ["แถว / คอลัมน์", "คอลัมน์ 1", "คอลัมน์ 2", "คอลัมน์ 3", "คอลัมน์ 4", "คอลัมน์ 5"]
    map1_rows = [
        ["แถว 1", "", "", "", "", "🚀 (ยานแม่)"],
        ["แถว 2", "", "🪨 (หิน)", "", "", ""],
        ["แถว 3", "🤖 (เริ่มต้น)", "", "🔋 (แบต)", "", ""],
        ["แถว 4", "", "", "🪨 (หิน)", "", ""],
        ["แถว 5", "", "", "", "", ""]
    ]
    elements.append(make_table(map1_headers, map1_rows, [1800, 1445, 1445, 1445, 1445, 1446], ["center"] * 6))
    elements.append(make_p([], space_before=60, space_after=60))

    elements.append(make_p([("📝 ลำดับขั้นตอนคำสั่ง (Algorithm) - ช่องกว้างพิเศษสำหรับเขียนตัวโต:", True, False, 28, "1F2937")]))
    elements.append(make_big_write_table(5, prefix="ก้าวที่ "))
    elements.append(make_p([], space_before=60, space_after=60))

    elements.append(make_p([("⭐ ผลการทดสอบ:  [  ] เข้ายานสำเร็จ   [  ] ชนสิ่งกีดขวาง   |   ดาวที่ได้รับ:  [  ] 1 ดาว   [  ] 2 ดาว   [  ] 3 ดาว", True, False, 26, "2563EB")]))
    elements.append(make_p([("ครูผู้สอน: นายเตชินท์ อินทมล | ลายมือชื่อคู่หู: 1) .................................... 2) ....................................", False, True, 22, "6B7280")], space_before=80, space_after=0))

    # =========================================================================
    # PAGE 2: ใบงานที่ 2 (พลังวนซ้ำ Loops)
    # =========================================================================
    elements.append(make_page_break())

    elements.append(make_p([("🔄 ใบงานที่ 2: ลูปบันได 3 ขั้นและลูปผสมหลายคำสั่ง (Multi-Action & Staircase Loop x3) 🚀", True, False, 32, "1E3A8A")], align="center", space_before=60, space_after=40))
    elements.append(make_p([("รายวิชาเทคโนโลยี (วิทยาการคำนวณ) ว15101 ชั้น ป.5 (สอดรับเกม CodeBot AR ด่าน 1-10 แทร็ก ป.5) | โรงเรียนบ้านโนนป่าหว้านเชียงฮาย", False, True, 24, "4B5563")], align="center", space_before=0, space_after=120))

    t_team2 = [
        ["ข้อมูลคู่หูนักเขียนโค้ด", "เลขที่", "บทบาทประจำด่านที่ 2 (สลับบทบาทแล้ว)"],
        ["ชื่อคู่หู/ทีม: .....................................................................", "-", "กลุ่มที่ ........."],
        ["1. ...................................................................................", "......", "[  ] Driver (เปลี่ยนมาคุมหน้ากล้อง AR)"],
        ["2. ...................................................................................", "......", "[  ] Navigator (เปลี่ยนมาวางแผนและคิดลูป)"]
    ]
    elements.append(make_table(t_team2[0], t_team2[1:], [4800, 800, 3426], ["left", "center", "left"]))
    elements.append(make_p([], space_before=60, space_after=60))

    elements.append(make_callout("🎯 คำแนะนำภารกิจบันได 3 ขั้น:\nสังเกตเส้นทางเดินขึ้นบันได จะพบว่ามีการเดินซ้ำเป็นแพทเทิร์น ให้นักเรียนช่วยกันจับกลุ่มคำสั่งซ้ำ แล้วนำบล็อก [วนซ้ำ Loop] มาครอบเพื่อลดจำนวนโค้ดให้สั้นที่สุดและคว้า 3 ดาว!", title="คำชี้แจงภารกิจที่ 2"))

    elements.append(make_p([("🗺️ แผนที่ด่านบันได 3 ขั้นทะยานฟ้า (Grid 6x6) - เนวิเกเตอร์ใช้ดินสอระบายขั้นบันได:", True, False, 26, "1E3A8A")], space_before=80, space_after=40))
    map2_headers = ["แถว / คอลัมน์", "คอลัมน์ 1", "คอลัมน์ 2", "คอลัมน์ 3", "คอลัมน์ 4", "คอลัมน์ 5", "คอลัมน์ 6"]
    map2_rows = [
        ["แถว 1", "", "", "", "🚀 (ยานแม่)", "", ""],
        ["แถว 2", "", "", "🪨", "🔋 (แบต)", "", ""],
        ["แถว 3", "", "🪨", "🔋 (แบต)", "", "", ""],
        ["แถว 4", "🪨", "🔋 (แบต)", "", "", "", ""],
        ["แถว 5", "🤖 (เริ่ม)", "", "", "", "", ""]
    ]
    elements.append(make_table(map2_headers, map2_rows, [1500, 1254, 1254, 1254, 1254, 1254, 1256], ["center"] * 7))
    elements.append(make_p([], space_before=60, space_after=60))

    elements.append(make_p([("🔍 วิเคราะห์รูปแบบและการเขียนบล็อกลูป (Loop Block Design):", True, False, 28, "1F2937")]))
    loop_analysis = """1. ใน 1 ขั้นบันได หุ่นยนต์ต้องทำคำสั่งอะไรบ้าง?
   ตอบ: .............................................................................................................................................................

2. ต้องทำชุดคำสั่งนี้ซ้ำติดต่อกันกี่รอบ?
   ตอบ: ทำซ้ำจำนวน .................... รอบ

3. เขียนบล็อกลูปคำสั่งที่คู่เราช่วยกันออกแบบ:
   [ วนซ้ำ (Loop) .................... รอบ ]
   {
        คำสั่งที่ 1: .........................................................................................................................................
        คำสั่งที่ 2: .........................................................................................................................................
   }"""
    elements.append(make_callout(loop_analysis, title="โครงสร้างบล็อกลูปของคู่เรา"))

    elements.append(make_p([("📊 เปรียบเทียบความยาวโค้ด:  แบบเดิมไม่ใช้ลูป = ............ บล็อก  |  แบบใช้ลูป = ลดเหลือเพียง ............ บล็อก (ประหยัดโค้ด!)", True, False, 26, "2563EB")]))
    elements.append(make_p([("ครูผู้สอน: นายเตชินท์ อินทมล | ลายมือชื่อคู่หู: 1) .................................... 2) ....................................", False, True, 22, "6B7280")], space_before=80, space_after=0))

    # =========================================================================
    # PAGE 3: ใบงานที่ 3 (เงื่อนไขกุญแจและเลเซอร์)
    # =========================================================================
    elements.append(make_page_break())

    elements.append(make_p([("⚡ ใบงานที่ 3: เงื่อนไขถ้า...แล้ว กับประตูปริศนาเลเซอร์และกุญแจ (If-Then Conditionals & Key) 🚀", True, False, 32, "1E3A8A")], align="center", space_before=60, space_after=40))
    elements.append(make_p([("รายวิชาเทคโนโลยี (วิทยาการคำนวณ) ว15101 ชั้น ป.5 (สอดรับเกม CodeBot AR ด่าน 1-10 แทร็ก ป.5) | โรงเรียนบ้านโนนป่าหว้านเชียงฮาย", False, True, 24, "4B5563")], align="center", space_before=0, space_after=120))

    elements.append(make_table(t_team[0], t_team[1:], [4800, 800, 3426], ["left", "center", "left"]))
    elements.append(make_p([], space_before=60, space_after=60))

    elements.append(make_callout("🎯 คำแนะนำภารกิจตัดสินใจเชิงตรรกะ:\nประตูเลเซอร์ ⚡ กั้นทางอยู่ ถ้าหุ่นยนต์เดินชนจะระเบิดทันที! หุ่นยนต์ต้องวางแผนเดินไปเก็บกุญแจคีย์การ์ด 🗝️ เสียก่อน ประตูเลเซอร์จึงจะปลดล็อกเปิดออก", title="คำชี้แจงภารกิจที่ 3"))

    elements.append(make_p([("🗺️ แผนที่ด่านกุญแจ & ประตูเลเซอร์ (Grid 5x5) - ลากเส้นทาง 2 เฟส (เก็บกุญแจ -> เข้ายาน):", True, False, 26, "1E3A8A")], space_before=80, space_after=40))
    map3_headers = ["แถว / คอลัมน์", "คอลัมน์ 1", "คอลัมน์ 2", "คอลัมน์ 3", "คอลัมน์ 4", "คอลัมน์ 5"]
    map3_rows = [
        ["แถว 1", "", "", "🪨", "🚀 (ยานแม่)", ""],
        ["แถว 2", "🗝️ (กุญแจ)", "", "⚡⚡ (ประตูเลเซอร์)", "", ""],
        ["แถว 3", "🪨", "", "🪨", "", ""],
        ["แถว 4", "🤖 (เริ่ม)", "", "", "", ""]
    ]
    elements.append(make_table(map3_headers, map3_rows, [1800, 1445, 1445, 1445, 1445, 1446], ["center"] * 6))
    elements.append(make_p([], space_before=60, space_after=60))

    elements.append(make_p([("🧠 การตัดสินใจเชิงตรรกะแบบมีเงื่อนไข (If-Then-Else):", True, False, 28, "1F2937")]))
    cond_box = """• [ ถ้า (IF) ] : หุ่นยนต์เก็บสิ่งนี้ได้แล้ว คือ ........................................................................................................
• [ แล้ว (THEN) ] : ประตูเลเซอร์จะเกิดผลคือ ................................................................................................... และเดินผ่านได้
• [ มิฉะนั้น (ELSE) ] : ถ้ายังไม่มีกุญแจ ห้ามเดินชน เพราะจะเกิดผลคือ ................................................................................."""
    elements.append(make_callout(cond_box, title="ประโยคเงื่อนไขตรรกะของคู่เรา"))

    elements.append(make_p([("📝 สรุปแผนคำสั่ง 2 เฟส:", True, False, 28, "1F2937")]))
    phase_headers = ["เฟสที่ 1: เดินไปเก็บกุญแจคีย์การ์ด", "เฟสที่ 2: เดินทะลุประตูเข้ายานอวกาศ"]
    phase_rows = [
        ["1. ......................................................................................\n2. ......................................................................................\n3. ......................................................................................",
         "1. ......................................................................................\n2. ......................................................................................\n3. ......................................................................................"]
    ]
    elements.append(make_table(phase_headers, phase_rows, [4513, 4513], ["left", "left"]))
    elements.append(make_p([], space_before=60, space_after=60))

    elements.append(make_p([("ครูผู้สอน: นายเตชินท์ อินทมล | ลายมือชื่อคู่หู: 1) .................................... 2) ....................................", False, True, 22, "6B7280")], space_before=80, space_after=0))

    # =========================================================================
    # PAGE 4: ใบงานที่ 4 (ยอดนักสืบแก้บั๊ก & AAR)
    # =========================================================================
    elements.append(make_page_break())

    elements.append(make_p([("🐞 ใบงานที่ 4: ยอดนักสืบแก้บั๊กตรรกะและบททดสอบมาสเตอร์จักรวาล ป.5 (Logic Debugging & Grand Space Master) 🚀", True, False, 32, "1E3A8A")], align="center", space_before=60, space_after=40))
    elements.append(make_p([("รายวิชาเทคโนโลยี (วิทยาการคำนวณ) ว15101 ชั้น ป.5 (สอดรับเกม CodeBot AR ด่าน 1-10 แทร็ก ป.5) | โรงเรียนบ้านโนนป่าหว้านเชียงฮาย", False, True, 24, "4B5563")], align="center", space_before=0, space_after=120))

    elements.append(make_table(t_team2[0], t_team2[1:], [4800, 800, 3426], ["left", "center", "left"]))
    elements.append(make_p([], space_before=60, space_after=60))

    elements.append(make_callout("🎯 คำแนะนำภารกิจนักสืบแก้บั๊ก (Debugging):\nในด่านนี้มีโปรแกรมเมอร์เขียนโค้ดผิดพลาดไว้ ให้นักเรียนสังเกตโค้ดเดิม หาจุดที่ผิดพลาด (Bug) วงกลมจุดผิด แล้วช่วยกันเขียนโค้ดใหม่ที่ถูกต้อง!", title="คำชี้แจงภารกิจที่ 4"))

    elements.append(make_p([("🔎 ตารางสืบหาและกำจัดบั๊ก (Bug Detective Table):", True, False, 28, "1F2937")]))
    bug_headers = ["โค้ดเดิมที่มีข้อผิดพลาด (Bug)", "โค้ดใหม่ที่ถูกต้อง (คู่เราแก้ไขแล้ว)"]
    bug_rows = [
        [
            "1. เดินหน้า 2 ก้าว\n2. เลี้ยวซ้าย ❌ (บั๊ก! เลี้ยวผิดทำให้ชนหิน)\n3. เดินหน้า 1 ก้าว\n4. เดินหน้าเข้ายานอวกาศ",
            "1. เดินหน้า 2 ก้าว\n2. แก้ไขเป็น: ............................................................................\n3. ............................................................................................\n4. ............................................................................................"
        ]
    ]
    elements.append(make_table(bug_headers, bug_rows, [4513, 4513], ["left", "left"]))
    elements.append(make_p([], space_before=60, space_after=60))

    elements.append(make_p([("💬 การสะท้อนคิดหลังทำภารกิจสำเร็จ (After Action Review: AAR):", True, False, 28, "1F2937")]))
    aar_box = """1. ความประทับใจที่สุดในการเรียนโค้ดดิ้งด้วยเกม CodeBot AR คืออะไร?
   ตอบ: ...................................................................................................................................................................................

2. สิ่งที่คู่หู (Driver & Navigator) ของเราช่วยเหลือกันได้ดีที่สุด คืออะไร?
   ตอบ: ...................................................................................................................................................................................

3. ถ้าในชีวิตจริงเราเจอปัญหาที่แก้ไม่ออก เราจะนำวิธี "หาจุดผิดพลาดทีละก้าว" ไปใช้ทำอะไรได้บ้าง?
   ตอบ: ..................................................................................................................................................................................."""
    elements.append(make_callout(aar_box, title="ถอดบทเรียนร่วมกัน"))

    eval_headers = ["การประเมินตนเองของคู่หู", "การประเมินของครูผู้สอน (เพื่อสะท้อนผล ว.PA)"]
    eval_rows = [
        [
            "[  ] ทำงานร่วมกันได้ดีเยี่ยม ไม่แย่งกัน\n[  ] สนุกและอยากเรียนอีกในครั้งต่อไป\n\nลายมือชื่อ: 1) ............................ 2) ............................",
            "คะแนนรวม 4 ใบงาน: ............ / 20 คะแนน\nระดับคุณภาพ: [  ] ดีเยี่ยม (4)  [  ] ดี (3)  [  ] พอใช้ (2)\n\n(ลงชื่อ)..................................................... ครูผู้สอน\n( นายเตชินท์ อินทมล )"
        ]
    ]
    elements.append(make_table(eval_headers, eval_rows, [4513, 4513], ["left", "left"]))

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
    
    path1 = "ใบงานภารกิจโค้ดดิ้ง_ป5_ชุดสมบูรณ์_4ใบงาน.docx"
    path2 = os.path.join("docs", "ใบงานภารกิจโค้ดดิ้ง_ป5_ชุดสมบูรณ์_4ใบงาน.docx")
    
    with open(path1, "wb") as f:
        f.write(data)
    with open(path2, "wb") as f:
        f.write(data)
        
    print(f"Generated 4-Page Worksheet DOCX:")
    print(f"1. {path1} ({len(data)} bytes)")
    print(f"2. {path2} ({len(data)} bytes)")

if __name__ == "__main__":
    build_4page_docx()
