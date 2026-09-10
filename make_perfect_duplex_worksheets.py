# -*- coding: utf-8 -*-
import zipfile, io, os
from generate_car_docx import esc, make_p, make_table, make_callout

def make_page_break():
    return '<w:p><w:r><w:br w:type="page"/></w:r></w:p>'

def make_team_header_p5(sheet_num, page_title, page_sub, role_nav, role_drv):
    elements = []
    elements.append(make_p([(f"🚀 CodeBot AR: {page_title}", True, False, 32, "1E3A8A")], align="center", space_before=40, space_after=20))
    elements.append(make_p([(f"วิทยาการคำนวณ ว15101 ชั้น ป.5 | โรงเรียนบ้านโนนป่าหว้านเชียงฮาย | {page_sub}", False, True, 22, "4B5563")], align="center", space_before=0, space_after=80))

    t_team = [
        ["ข้อมูลคู่หู Active Learning", "เลขที่", "บทบาทหน้าที่ประจำภารกิจ"],
        ["ชื่อทีม/กลุ่ม: ..............................................................", "-", "แผ่นที่ " + str(sheet_num)],
        ["1. ..........................................................................", "......", f"[  ] Navigator ({role_nav})"],
        ["2. ..........................................................................", "......", f"[  ] Driver ({role_drv})"]
    ]
    elements.append(make_table(t_team[0], t_team[1:], [4600, 800, 3626], ["left", "center", "left"]))
    elements.append(make_p([], space_before=40, space_after=40))
    return elements

def build_perfect_worksheets():
    elements = []

    # =========================================================================
    # แผ่นที่ 1 (หน้า 1): ใบงานที่ 1 - แพทเทิร์นและลูปบันได (ด่าน 1-3 ป.5)
    # =========================================================================
    elements.extend(make_team_header_p5(
        1,
        "ใบงานที่ 1: ค้นหารูปแบบและลูปบันได 3 ขั้น (Pattern & Loops)",
        "สอดรับเกม CodeBot AR แทร็ก ป.5 (ด่านที่ 1 - 3)",
        "ผู้นำทาง วาดแผนที่ & สังเกตรูปแบบ",
        "ผู้สั่งการ ชูการ์ดคำสั่งหน้ากล้อง AR"
    ))

    elements.append(make_callout("🎯 ภารกิจเนวิเกเตอร์ (Navigator):\nสังเกตเส้นทางเดินขึ้นบันได จะพบว่าหุ่นยนต์ต้องก้าวเดินซ้ำๆ เป็นแพทเทิร์น ให้ลากเส้นทางเดิน 🤖 เก็บแบตเตอรี่ 🔋 แล้วขึ้นยาน 🚀 จากนั้นช่วยกันนำบล็อก [วนซ้ำ Loop] มารวบคำสั่งให้สั้นที่สุดเพื่อคว้า 3 ดาว!", title="📌 คำชี้แจงภารกิจที่ 1"))

    elements.append(make_p([("🗺️ แผนที่จำลองในเกม (Grid 6x6) - สัญลักษณ์: 🤖 เริ่มต้น, 🔋 แบตเตอรี่, 🪨 หินอวกาศ, 🚀 ยานอวกาศ", True, False, 24, "1E3A8A")], space_before=60, space_after=30))
    map1_headers = ["แถว/คอลัมน์", "C1", "C2", "C3", "C4", "C5", "C6"]
    map1_rows = [
        ["R1", "", "", "", "🚀 (ยาน)", "", ""],
        ["R2", "", "", "🪨", "🔋 (แบต)", "", ""],
        ["R3", "", "🪨", "🔋 (แบต)", "", "", ""],
        ["R4", "🪨", "🔋 (แบต)", "", "", "", ""],
        ["R5", "🤖 (เริ่ม)", "", "", "", "", ""],
        ["R6", "", "", "", "", "", ""]
    ]
    elements.append(make_table(map1_headers, map1_rows, [1400, 1271, 1271, 1271, 1271, 1271, 1271], ["center"] * 7))
    elements.append(make_p([], space_before=40, space_after=40))

    elements.append(make_p([("📝 การวิเคราะห์รูปแบบและออกแบบโค้ดลูป (Loop Design):", True, False, 26, "1F2937")]))
    loop_box = """1. รูปแบบคำสั่งใน 1 ขั้นบันได ที่ทำซ้ำกัน คือ: [ .......................................................................... และ .......................................................................... ]
2. จำนวนรอบที่ต้องทำซ้ำ คือ: .................... รอบ  (เขียนบล็อกลูป: [ วนซ้ำ Loop .................... รอบ ])
3. เปรียบเทียบความยาวโค้ด: แบบไม่ใช้ลูป = ............ คำสั่ง  |  แบบใช้ลูปย่อคำสั่ง = ลดเหลือเพียง ............ คำสั่ง!"""
    elements.append(make_callout(loop_box, title="ถอดรหัสแพทเทิร์นบันได"))

    elements.append(make_p([("⭐ ผลทดสอบหน้ากล้อง AR:  [  ] เข้ายานสำเร็จ   |   ดาวที่ได้:  [  ] 1 ดาว   [  ] 2 ดาว   [  ] 3 ดาว 🌟🌟🌟", True, False, 24, "2563EB")], space_before=40, space_after=20))
    elements.append(make_p([("ครูผู้ตรวจ: นายเตชินท์ อินทมล | ลายมือชื่อคู่หู: 1) ........................................ 2) ........................................", False, True, 20, "6B7280")]))

    # =========================================================================
    # แผ่นที่ 1 (หน้า 2 - ด้านหลัง): ใบงานที่ 2 - ลูปตรวจรอบสถานีและการลดรูปโค้ด (ด่าน 4 ป.5)
    # =========================================================================
    elements.append(make_page_break())

    elements.extend(make_team_header_p5(
        1,
        "ใบงานที่ 2: ลูปตรวจรอบสถานีและการลดรูปโค้ด (Perimeter Loop)",
        "สอดรับเกม CodeBot AR แทร็ก ป.5 (ด่านที่ 4) [พลิกด้านหลัง - สลับบทบาทคู่หูแล้ว]",
        "สลับมาเป็นผู้นำทาง วางแผนโค้ดประหยัด",
        "สลับมาเป็นผู้สั่งการ ควบคุมหน้ากล้อง AR"
    ))

    elements.append(make_callout("🎯 ภารกิจสลับบทบาท (Swap Role Challenge):\nหุ่นยนต์ต้องเดินลาดตระเวนรอบสถานีอวกาศเป็นรูปสี่เหลี่ยม 4 ทิศ เพื่อชาร์จแบตเตอรี่ 4 จุด คู่หูต้องช่วยกันเขียนบล็อกลูปแบบผสมคำสั่ง (Multi-Action Loop) ให้โค้ดสั้นที่สุด!", title="📌 คำชี้แจงภารกิจที่ 2"))

    elements.append(make_p([("🗺️ แผนที่ลาดตระเวนรอบสถานี (Grid 6x6) - สัญลักษณ์: 🤖 เริ่มต้น, 🔋 แบตเตอรี่ 4 ทิศ, 🚀 ยานแม่", True, False, 24, "1E3A8A")], space_before=60, space_after=30))
    map2_headers = ["แถว/คอลัมน์", "C1", "C2", "C3", "C4", "C5", "C6"]
    map2_rows = [
        ["R1", "🚀 (ยาน)", "🔋", "🔋", "🔋", "", ""],
        ["R2", "🔋", "🪨 (แกนกลาง)", "🪨", "🔋", "", ""],
        ["R3", "🔋", "🪨 (แกนกลาง)", "🪨", "🔋", "", ""],
        ["R4", "🤖 (เริ่ม)", "🔋", "🔋", "🔋", "", ""],
        ["R5", "", "", "", "", "", ""],
        ["R6", "", "", "", "", "", ""]
    ]
    elements.append(make_table(map2_headers, map2_rows, [1400, 1271, 1271, 1271, 1271, 1271, 1271], ["center"] * 7))
    elements.append(make_p([], space_before=40, space_after=40))

    elements.append(make_p([("📝 เปรียบเทียบโค้ด 2 รูปแบบ (Optimization):", True, False, 26, "1F2937")]))
    opt_headers = ["แบบเดิม (วางเรียงคำสั่งยาว)", "แบบประหยัดโค้ด (Multi-Action Loop)"]
    opt_rows = [
        [
            "• เดินหน้า 3 ก้าว\n• เลี้ยวขวา\n• เดินหน้า 3 ก้าว\n• เลี้ยวขวา\n• เดินหน้า 3 ก้าว\n• เลี้ยวขวา\n• เดินหน้า 3 ก้าว\n(รวม 12 บล็อกยาวมาก!)",
            "[ วนซ้ำ (Loop) ............ รอบ ]\n{\n    1. เดินหน้า ............ ก้าว\n    2. เลี้ยว ................................\n}\n(ประหยัดบล็อกเหลือเพียง 1 ลูป!)"
        ]
    ]
    elements.append(make_table(opt_headers, opt_rows, [4513, 4513], ["left", "left"]))
    elements.append(make_p([], space_before=40, space_after=40))

    elements.append(make_p([("⭐ ผลทดสอบหน้ากล้อง AR:  [  ] ลาดตระเวนสำเร็จ   |   ดาวที่ได้:  [  ] 1 ดาว   [  ] 2 ดาว   [  ] 3 ดาว 🌟🌟🌟", True, False, 24, "2563EB")], space_before=40, space_after=20))
    elements.append(make_p([("ครูผู้ตรวจ: นายเตชินท์ อินทมล | ลายมือชื่อคู่หู: 1) ........................................ 2) ........................................", False, True, 20, "6B7280")]))

    # =========================================================================
    # แผ่นที่ 2 (หน้า 3): ใบงานที่ 3 - เงื่อนไขถ้า...แล้ว กุญแจและเลเซอร์ (ด่าน 5-6 ป.5)
    # =========================================================================
    elements.append(make_page_break())

    elements.extend(make_team_header_p5(
        2,
        "ใบงานที่ 3: เงื่อนไขถ้า...แล้ว กุญแจและประตูเลเซอร์ (If-Then Logic)",
        "สอดรับเกม CodeBot AR แทร็ก ป.5 (ด่านที่ 5 - 6)",
        "ผู้นำทาง คำนวณเงื่อนไขและทางแยก",
        "ผู้สั่งการ ส่องการ์ดกุญแจหน้ากล้อง AR"
    ))

    elements.append(make_callout("🎯 ภารกิจคิดเชิงตรรกะแบบมีเงื่อนไข (Conditionals):\nประตูเลเซอร์ ⚡ กั้นทางเข้ายานอวกาศอยู่ ห้ามเดินชนเด็ดขาด! หุ่นยนต์ต้องวางแผนเดินไปเก็บกุญแจคีย์การ์ด 🗝️ เสียก่อน ประตูเลเซอร์จึงจะดับลง ให้นักเรียนเขียนประโยคเงื่อนไขและวางแผนคำสั่ง 2 เฟส", title="📌 คำชี้แจงภารกิจที่ 3"))

    elements.append(make_p([("🗺️ แผนที่ประตูปริศนาเลเซอร์ (Grid 6x6) - สัญลักษณ์: 🤖 เริ่มต้น, 🗝️ กุญแจ, ⚡ ประตูเลเซอร์, 🚀 ยานแม่", True, False, 24, "1E3A8A")], space_before=60, space_after=30))
    map3_headers = ["แถว/คอลัมน์", "C1", "C2", "C3", "C4", "C5", "C6"]
    map3_rows = [
        ["R1", "", "", "", "⚡ (เลเซอร์)", "🚀 (ยาน)", ""],
        ["R2", "🗝️ (กุญแจ)", "", "", "⚡ (เลเซอร์)", "", ""],
        ["R3", "🪨", "🪨", "", "", "", ""],
        ["R4", "🤖 (เริ่ม)", "", "", "", "", ""],
        ["R5", "", "", "", "", "", ""],
        ["R6", "", "", "", "", "", ""]
    ]
    elements.append(make_table(map3_headers, map3_rows, [1400, 1271, 1271, 1271, 1271, 1271, 1271], ["center"] * 7))
    elements.append(make_p([], space_before=40, space_after=40))

    elements.append(make_p([("🧠 ตรรกะเงื่อนไขและการแบ่งภารกิจ 2 เฟส (If-Then Decision):", True, False, 26, "1F2937")]))
    cond_box = """• [ ถ้า (IF) ] : หุ่นยนต์มีไอเทมนี้ คือ [ ............................................................................................................................ ]
• [ แล้ว (THEN) ] : ประตูเลเซอร์จะเกิดผลคือ [ .................................................................................................................... ]
• [ มิฉะนั้น (ELSE) ] : ถ้ายังไม่มีกุญแจ ห้ามเดินชน เพราะจะเกิดผลคือ [ ....................................................................................]"""
    elements.append(make_callout(cond_box, title="ประโยคเงื่อนไข If-Then ของคู่เรา"))

    phase_headers = ["เฟส 1: เดินไปเก็บกุญแจคีย์การ์ด 🗝️", "เฟส 2: เดินทะลุประตูเลเซอร์เข้ายาน 🚀"]
    phase_rows = [
        [
            "1. ............................................................................\n2. ............................................................................\n3. ............................................................................",
            "1. ............................................................................\n2. ............................................................................\n3. ............................................................................"
        ]
    ]
    elements.append(make_table(phase_headers, phase_rows, [4513, 4513], ["left", "left"]))
    elements.append(make_p([], space_before=40, space_after=40))

    elements.append(make_p([("⭐ ผลทดสอบหน้ากล้อง AR:  [  ] ปลดล็อกเลเซอร์สำเร็จ   |   ดาวที่ได้:  [  ] 1 ดาว   [  ] 2 ดาว   [  ] 3 ดาว 🌟🌟🌟", True, False, 24, "2563EB")], space_before=40, space_after=20))
    elements.append(make_p([("ครูผู้ตรวจ: นายเตชินท์ อินทมล | ลายมือชื่อคู่หู: 1) ........................................ 2) ........................................", False, True, 20, "6B7280")]))

    # =========================================================================
    # แผ่นที่ 2 (หน้า 4 - ด้านหลัง): ใบงานที่ 4 - ยอดนักสืบแก้บั๊ก & มาสเตอร์จักรวาล (ด่าน 7-10 ป.5)
    # =========================================================================
    elements.append(make_page_break())

    elements.extend(make_team_header_p5(
        2,
        "ใบงานที่ 4: ยอดนักสืบแก้บั๊กและบททดสอบมาสเตอร์ (Debugging & AAR)",
        "สอดรับเกม CodeBot AR แทร็ก ป.5 (ด่านที่ 7 - 10) [พลิกด้านหลัง - สลับบทบาทคู่หูแล้ว]",
        "สลับมาเป็นผู้นำทาง วิเคราะห์บั๊กและสะท้อนคิด",
        "สลับมาเป็นผู้สั่งการ ทดสอบโค้ดแก้บั๊กหน้ากล้อง"
    ))

    elements.append(make_callout("🎯 ภารกิจนักสืบแก้บั๊กและถอดบทเรียน (Debugging & Reflection):\nในด่านนี้มีโค้ดที่มีข้อผิดพลาด (Bug) ทำให้หุ่นยนต์เดินชนประตูเลเซอร์ก่อนเก็บกุญแจ! ให้นักเรียนช่วยกันสืบหาจุดผิด แก้ไขให้ถูกต้อง จากนั้นร่วมกันสะท้อนคิดถอดบทเรียนหลังพิชิตด่านมาสเตอร์จักรวาล", title="📌 คำชี้แจงภารกิจที่ 4"))

    elements.append(make_p([("🐞 ตารางตรวจจับและกำจัดบั๊ก (Bug Detective Table):", True, False, 26, "1F2937")]))
    bug_headers = ["โค้ดเดิมที่มีข้อผิดพลาด (Bug ในเกม)", "โค้ดที่ถูกต้อง (คู่หูของเราแก้ไขแล้ว)"]
    bug_rows = [
        [
            "1. เดินหน้า 3 ก้าวตรงไปที่ประตู ❌ (บั๊กชนเลเซอร์!)\n2. เลี้ยวซ้ายไปหากุญแจ\n3. เก็บกุญแจ\n4. เดินเข้ายานอวกาศ",
            "1. แก้ไขเป็น: ........................................................................\n2. ........................................................................................\n3. ........................................................................................\n4. เดินเข้ายานอวกาศสำเร็จ!"
        ]
    ]
    elements.append(make_table(bug_headers, bug_rows, [4513, 4513], ["left", "left"]))
    elements.append(make_p([], space_before=40, space_after=40))

    elements.append(make_p([("💬 การสะท้อนคิดถอดบทเรียนร่วมกัน (After Action Review: AAR):", True, False, 26, "1F2937")]))
    aar_box = """1. สิ่งที่คู่หู (Driver & Navigator) ของเราช่วยเหลือกันได้ดีที่สุดในการแก้ปัญหา คืออะไร?
   ตอบ: ...............................................................................................................................................................................
2. การใช้การ์ดคำสั่งและเล่นเกม AR บนโต๊ะ ช่วยให้เราเข้าใจการเขียนโปรแกรมง่ายขึ้นอย่างไร?
   ตอบ: ...............................................................................................................................................................................
3. ถ้าในชีวิตจริงเราเจอปัญหาที่แก้ไม่ออก เราจะนำวิธี "หาจุดผิดพลาดทีละก้าว (Debugging)" ไปใช้อย่างไร?
   ตอบ: ..............................................................................................................................................................................."""
    elements.append(make_callout(aar_box, title="ถอดบทเรียนคู่หู ป.5"))

    elements.append(make_p([("🏆 บันทึกความสำเร็จ: ผ่านด่านมาสเตอร์ ป.5 ครบ 10 ด่าน!  |  คะแนนดาวสะสมรวม: ............ / 30 ดาว ⭐⭐⭐", True, False, 24, "2563EB")], space_before=40, space_after=20))
    elements.append(make_p([("ครูผู้ตรวจ: นายเตชินท์ อินทมล | ลายมือชื่อคู่หู: 1) ........................................ 2) ........................................", False, True, 20, "6B7280")]))

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
        <w:spacing w:before="40" w:after="40" w:line="260" w:lineRule="auto"/>
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
      <w:pgMar w:top="850" w:right="850" w:bottom="850" w:left="850"/>
    </w:sectPr>
  </w:body>
</w:document>"""

    out_file = "ใบงานภารกิจโค้ดดิ้ง_ป5_ชุดสมบูรณ์_4ใบงาน.docx"
    with zipfile.ZipFile(out_file, "w", zipfile.ZIP_DEFLATED) as docx:
        docx.writestr("[Content_Types].xml", content_types)
        docx.writestr("_rels/.rels", rels)
        docx.writestr("word/_rels/document.xml.rels", doc_rels)
        docx.writestr("word/styles.xml", styles)
        docx.writestr("word/document.xml", document_xml)

    print(f"Created Perfect Duplex Worksheets DOCX: {out_file}")
    os.system(f"cp '{out_file}' docs/")

build_perfect_worksheets()
