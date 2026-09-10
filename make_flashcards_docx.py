# -*- coding: utf-8 -*-
import zipfile, io, os
from generate_car_docx import esc, make_p, make_callout, make_table

def make_page_break():
    return '<w:p><w:r><w:br w:type="page"/></w:r></w:p>'

def build_flashcards_docx():
    elements = []

    # =========================================================================
    # แผ่นที่ 1: บัตรบทบาท & คำสั่งเคลื่อนที่พื้นฐาน
    # =========================================================================
    elements.append(make_p([("ชุดแฟลชการ์ดบัตรคำสั่งโค้ดดิ้ง (CodeBot AR Tangible Cards) - แผ่นที่ 1", True, False, 30, "1E3A8A")], align="center", space_before=40, space_after=20))
    elements.append(make_p([("พิมพ์ลงบนกระดาษการ์ดหนา แล้วตัดตามเส้นประเพื่อแจกให้นักเรียน 4 คู่ (คู่ละ 1 ชุด)", False, True, 22, "64748B")], align="center", space_before=0, space_after=100))

    t1_headers = ["การ์ดฝั่งซ้าย (ตัดตามเส้นประ)", "การ์ดฝั่งขวา (ตัดตามเส้นประ)"]
    t1_rows = [
        [
            "🧭 ป้ายบทบาท: ผู้นำทาง (NAVIGATOR)\n\n[ หน้าที่หลัก ]\n- วางแผนเส้นทางและคิดอัลกอริทึม\n- เรียงการ์ดคำสั่งบนโต๊ะ\n- ตรวจสอบจุดผิดพลาด (Bug)\n\n* กฎเหล็ก: ถือการ์ดวางแผน ห้ามแตะหน้าจอคอมฯ",
            "🎮 ป้ายบทบาท: ผู้สั่งการ (DRIVER)\n\n[ หน้าที่หลัก ]\n- รับคำสั่งจาก Navigator\n- ป้อนคำสั่งด้วยท่าทางหน้ากล้อง AR\n- กดทดสอบการทำงานของหุ่นยนต์\n\n* กฎเหล็ก: ป้อนโค้ดตามที่คู่หูบอกเท่านั้น"
        ],
        [
            "⬆️ คำสั่ง: เดินหน้า 1 ก้าว (MOVE FORWARD)\n\n[ การทำงาน ]\nหุ่นยนต์ก้าวไปข้างหน้า 1 ช่อง\nตามทิศทางที่หันอยู่\n\n[ บล็อกคำสั่ง AR #1 ]",
            "↩️ คำสั่ง: หันซ้าย 90° (TURN LEFT)\n\n[ การทำงาน ]\nหุ่นยนต์หมุนตัวไปทางซ้าย 90 องศา\n(ยังอยู่ที่เดิม ไม่เปลี่ยนช่องเดิน)\n\n[ บล็อกคำสั่ง AR #2 ]"
        ],
        [
            "↪️ คำสั่ง: หันขวา 90° (TURN RIGHT)\n\n[ การทำงาน ]\nหุ่นยนต์หมุนตัวไปทางขวา 90 องศา\n(ยังอยู่ที่เดิม ไม่เปลี่ยนช่องเดิน)\n\n[ บล็อกคำสั่ง AR #3 ]",
            "🦘 คำสั่ง: กระโดดข้ามหลุม (JUMP)\n\n[ การทำงาน ]\nหุ่นยนต์กระโดดข้ามสิ่งกีดขวาง\nไปข้างหน้า 1 ช่อง\n\n[ บล็อกคำสั่ง AR #4 ]"
        ]
    ]
    elements.append(make_table(t1_headers, t1_rows, [4513, 4513], ["left", "left"]))
    elements.append(make_p([("✂️ ตัดตามขอบตาราง แจกให้นักเรียนเรียงบนโต๊ะก่อนเริ่มเล่นหน้ากล้อง AR", False, True, 20, "94A3B8")], align="center", space_before=60, space_after=60))

    # =========================================================================
    # แผ่นที่ 2: บัตรพลังวนซ้ำ & เงื่อนไขตรรกะ
    # =========================================================================
    elements.append(make_page_break())
    elements.append(make_p([("ชุดแฟลชการ์ดบัตรคำสั่งโค้ดดิ้ง (CodeBot AR Tangible Cards) - แผ่นที่ 2", True, False, 30, "1E3A8A")], align="center", space_before=40, space_after=20))
    elements.append(make_p([("บัตรพลังวนซ้ำ (Loops) และ เงื่อนไขการตัดสินใจ (Conditions)", False, True, 22, "64748B")], align="center", space_before=0, space_after=100))

    t2_headers = ["การ์ดฝั่งซ้าย (ตัดตามเส้นประ)", "การ์ดฝั่งขวา (ตัดตามเส้นประ)"]
    t2_rows = [
        [
            "🔁 วนซ้ำ 2 ครั้ง (REPEAT 2 TIMES)\n\n[ การทำงาน ]\nใช้ครอบคำสั่งที่ทำซ้ำกัน 2 รอบ\nช่วยลดจำนวนบล็อกคำสั่งให้สั้นลง\n\n[ LOOP CARD x2 ]",
            "🔁 วนซ้ำ 3 ครั้ง (REPEAT 3 TIMES)\n\n[ การทำงาน ]\nใช้ครอบแพทเทิร์นด่านบันได 3 ขั้น\nช่วยคว้าดาวโบนัสโค้ดสั้นกระชับ\n\n[ LOOP CARD x3 ]"
        ],
        [
            "🔁 วนซ้ำ 4 ครั้ง (REPEAT 4 TIMES)\n\n[ การทำงาน ]\nใช้ครอบทางเดินตรงยาว 4 ช่อง\nประหยัดบล็อกได้ถึง 3 บล็อก!\n\n[ LOOP CARD x4 ]",
            "🗝️ การ์ดไอเทม: กุญแจคีย์การ์ด (COLLECT KEY)\n\n[ เงื่อนไข ]\nหุ่นยนต์ต้องเดินไปเก็บกุญแจก่อน\nจึงจะสามารถปลดล็อกประตูเลเซอร์ได้\n\n[ KEY ITEM ]"
        ],
        [
            "⚡ ประตูเลเซอร์ & เงื่อนไข (IF-THEN)\n\n[ ตรรกะเงื่อนไข ]\nถ้ามีกุญแจ ➔ ประตูเลเซอร์เปิดออก\nถ้าไม่มีกุญแจ ➔ ห้ามชนประตูเด็ดขาด!\n\n[ DECISION CARD ]",
            "🔋 แบตเตอรี่พลังงาน (ENERGY BATTERY)\n\n[ เป้าหมาย ]\nสะสมพลังงานตามทางเดิน\nเพื่อชาร์จพลังให้ยานอวกาศ\n\n[ +100 XP ]"
        ]
    ]
    elements.append(make_table(t2_headers, t2_rows, [4513, 4513], ["left", "left"]))
    elements.append(make_p([("✂️ ตัดตามขอบตาราง แจกให้นักเรียนเรียงบนโต๊ะก่อนเริ่มเล่นหน้ากล้อง AR", False, True, 20, "94A3B8")], align="center", space_before=60, space_after=60))

    # =========================================================================
    # แผ่นที่ 3: บัตรนักสืบแก้บั๊ก & รางวัล 3 ดาว
    # =========================================================================
    elements.append(make_page_break())
    elements.append(make_p([("ชุดแฟลชการ์ดบัตรคำสั่งโค้ดดิ้ง (CodeBot AR Tangible Cards) - แผ่นที่ 3", True, False, 30, "1E3A8A")], align="center", space_before=40, space_after=20))
    elements.append(make_p([("บัตรนักสืบแก้บั๊ก (Debugging), การสลับบทบาท และ รางวัล 3 ดาว", False, True, 22, "64748B")], align="center", space_before=0, space_after=100))

    t3_headers = ["การ์ดฝั่งซ้าย (ตัดตามเส้นประ)", "การ์ดฝั่งขวา (ตัดตามเส้นประ)"]
    t3_rows = [
        [
            "🐞 ตรวจพบบั๊ก! (BUG DETECTED!)\n\n[ สัญญาณเตือน ]\nหุ่นยนต์เดินชนหิน หรือเดินไม่ถึงเป้าหมาย\nให้นักเรียนกดหยุด เพื่อตรวจเช็คโค้ดทีละบรรทัด\n\n[ DEBUG ALERT ]",
            "🛠️ แก้ไขโค้ดสำเร็จ! (BUG FIXED!)\n\n[ ภารกิจสำเร็จ ]\nปรับปรุงอัลกอริทึมให้ถูกต้อง\nหุ่นยนต์เดินเข้าสู่เป้าหมายได้อย่างแม่นยำ\n\n[ SYSTEM OK ]"
        ],
        [
            "🔄 สลับบทบาทคู่หู! (ROLE SWITCH)\n\n[ กติกา Active Learning ]\nNavigator สลับไปเป็น Driver\nDriver สลับมาเป็น Navigator\nได้คิดและทำทุกคน 100%\n\n[ CO-OP ACTIVE ]",
            "⭐⭐⭐ ภารกิจ 3 ดาวสมบูรณ์แบบ!\n\n[ เงื่อนไข 3 ดาว ]\nดาว 1: พิชิตด่านสำเร็จ\nดาว 2: โค้ดสั้นประหยัดบล็อก\nดาว 3: ทำเวลาได้รวดเร็ว\n\n[ MASTER ACHIEVEMENT ]"
        ],
        [
            "🚀 ยานอวกาศ (GOAL TARGET)\n\n[ ปลายทาง ]\nจุดหมายปลายทางที่หุ่นยนต์ต้องเข้า\nเพื่อจบภารกิจอย่างสมบูรณ์\n\n[ MISSION CLEAR ]",
            "🪨 หินอุกกาบาต (OBSTACLE)\n\n[ สิ่งกีดขวาง ]\nห้ามเดินชนเด็ดขาด!\nต้องใช้คำสั่งเลี้ยวซ้ายหรือเลี้ยวขวาเพื่อหลบ\n\n[ WARNING HAZARD ]"
        ]
    ]
    elements.append(make_table(t3_headers, t3_rows, [4513, 4513], ["left", "left"]))
    elements.append(make_p([("✂️ ตัดตามขอบตาราง แจกให้นักเรียนเรียงบนโต๊ะก่อนเริ่มเล่นหน้ากล้อง AR", False, True, 20, "94A3B8")], align="center", space_before=60, space_after=60))

    # Package DOCX
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
    path1 = "ชุดแฟลชการ์ดคำสั่งโค้ดดิ้ง_ป5_ครูเตชินท์.docx"
    path2 = os.path.join("docs", "ชุดแฟลชการ์ดคำสั่งโค้ดดิ้ง_ป5_ครูเตชินท์.docx")
    
    with open(path1, "wb") as f:
        f.write(data)
    with open(path2, "wb") as f:
        f.write(data)
        
    print(f"Generated Flashcards DOCX:")
    print(f"1. {path1} ({len(data)} bytes)")
    print(f"2. {path2} ({len(data)} bytes)")

if __name__ == "__main__":
    build_flashcards_docx()
