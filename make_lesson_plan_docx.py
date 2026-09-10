# -*- coding: utf-8 -*-
import zipfile, io, os
from generate_car_docx import esc, make_p, make_callout, make_table

def build_lesson_plan_docx():
    elements = []

    # Title & Header
    elements.append(make_p([("แผนการจัดการเรียนรู้เชิงรุก (Active Learning Lesson Plan)", True, False, 36, "1E3A8A")], align="center", space_before=100, space_after=60))
    elements.append(make_p([("กลุ่มสาระการเรียนรู้วิทยาศาสตร์และเทคโนโลยี รายวิชาเทคโนโลยี (วิทยาการคำนวณ) ว15101", True, False, 28, "1F2937")], align="center", space_before=0, space_after=40))
    elements.append(make_p([("ชั้นประถมศึกษาปีที่ 5 | ภาคเรียนที่ 2 ปีการศึกษา 2568 | เวลา 8 ชั่วโมง (หน่วยการเรียนรู้เฉพาะ)", False, True, 26, "4B5563")], align="center", space_before=0, space_after=180))

    # Meta Table
    t_meta = [
        ["ข้อมูลทั่วไปของแผนการจัดการเรียนรู้", "รายละเอียด"],
        ["หน่วยการเรียนรู้", "การใช้เหตุผลเชิงตรรกะและการเขียนโปรแกรมอย่างง่าย (ภารกิจโค้ดบอทอวกาศ)"],
        ["เรื่อง", "การบอกทิศทางและลำดับขั้นตอน, การทำซ้ำอย่างง่าย, การเลือกตามเงื่อนไข, และการตรวจหาจุดผิดพลาด"],
        ["รูปแบบการสอน", "Game-Based Learning ร่วมกับ Active Learning (Pair Programming: Driver & Navigator)"],
        ["กลุ่มเป้าหมาย", "นักเรียนชั้นประถมศึกษาปีที่ 5 โรงเรียนบ้านโนนป่าหว้านเชียงฮาย จำนวน 8 คน (4 คู่)"],
        ["ครูผู้สอน", "นายเตชินท์ อินทมล ตำแหน่ง ครู ไม่มีวิทยฐานะ"]
    ]
    elements.append(make_table(t_meta[0], t_meta[1:], [3200, 5826], ["left", "left"]))
    elements.append(make_p([], space_before=100, space_after=100))

    # 1. Standards
    elements.append(make_p([("1. มาตรฐานการเรียนรู้และตัวชี้วัด", True, False, 32, "1E3A8A")], space_before=180, space_after=80))
    elements.append(make_p([("มาตรฐาน ว 4.2: ", True, False, 30, "111827"), ("เข้าใจและใช้แนวคิดเชิงคำนวณในการแก้ปัญหาที่พบในชีวิตจริงอย่างเป็นขั้นตอนและเป็นระบบ ใช้เทคโนโลยีสารสนเทศและการสื่อสารในการเรียนรู้ การทำงาน และการแก้ปัญหาได้อย่างมีประสิทธิภาพ รู้เท่าทัน และมีจริยธรรม", False, False, 30, "374151")]))
    elements.append(make_p([("• ตัวชี้วัด ว 4.2 ป.5/1: ", True, False, 30, "1E3A8A"), ("ใช้เหตุผลเชิงตรรกะในการแก้ปัญหา การอธิบายการทำงาน การคาดการณ์ผลลัพธ์จากปัญหาอย่างง่าย", False, False, 30, "374151")]))
    elements.append(make_p([("• ตัวชี้วัด ว 4.2 ป.5/2: ", True, False, 30, "1E3A8A"), ("ออกแบบและเขียนโปรแกรมที่มีการใช้เหตุผลเชิงตรรกะอย่างง่าย ตรวจหาข้อผิดพลาดและแก้ไข", False, False, 30, "374151")]))

    # 2. Objectives
    elements.append(make_p([("2. จุดประสงค์การเรียนรู้ (Learning Objectives)", True, False, 32, "1E3A8A")], space_before=180, space_after=80))
    elements.append(make_p([("1. ด้านความรู้ (K - Knowledge):", True, False, 30, "2563EB")]))
    elements.append(make_p([("• อธิบายขั้นตอนการแก้ปัญหาอย่างง่าย การบอกทิศทาง และการทำงานแบบวนซ้ำได้อย่างถูกต้อง", False, False, 30, "374151")], bullet=True))
    elements.append(make_p([("• บอกจุดผิดพลาด (Bug) เมื่อหุ่นยนต์เดินไม่ถึงเป้าหมายหรือเดินชนสิ่งกีดขวางได้", False, False, 30, "374151")], bullet=True))
    
    elements.append(make_p([("2. ด้านทักษะกระบวนการ (P - Process/Skills):", True, False, 30, "2563EB")]))
    elements.append(make_p([("• วางแผนเส้นทางบนตารางกริดและเรียงแฟลชการ์ดคำสั่งบนโต๊ะได้ถูกต้องตามลำดับขั้นตอน", False, False, 30, "374151")], bullet=True))
    elements.append(make_p([("• ป้อนคำสั่งบล็อกผ่านท่าทางหน้ากล้อง AR และตรวจแก้ไขคำสั่งที่ผิดพลาดได้สำเร็จ", False, False, 30, "374151")], bullet=True))
    
    elements.append(make_p([("3. ด้านคุณลักษณะอันพึงประสงค์ (A - Attitude):", True, False, 30, "2563EB")]))
    elements.append(make_p([("• มีความมุ่งมั่นและสนุกกับการแก้ปัญหา ไม่ยอมแพ้เมื่อหุ่นยนต์เดินชนสิ่งกีดขวาง", False, False, 30, "374151")], bullet=True))
    elements.append(make_p([("• มีทักษะการทำงานร่วมกับคู่หู รู้จักการรับฟังและช่วยเหลือซึ่งกันและกัน ไม่แย่งกันเล่น", False, False, 30, "374151")], bullet=True))

    # 3. Roles
    elements.append(make_p([("3. โครงสร้างบทบาทคู่หู Active Learning (Pair Programming Structure)", True, False, 32, "1E3A8A")], space_before=180, space_after=80))
    t_roles = [
        ["บทบาทที่ 1: ผู้นำทาง (Navigator)", "บทบาทที่ 2: ผู้สั่งการ (Driver)"],
        [
            "- ถือใบงานตารางกริดและชุดแฟลชการ์ดสัญลักษณ์\n- ดูทิศทาง วางแผนลำดับก้าวเดินบนโต๊ะ\n- บอกคำสั่งให้ Driver ป้อนโค้ดทีละก้าว\n- ตรวจเช็คความถูกต้องและช่วยดูว่าชนหินตรงไหน\n* กฎเหล็ก: วางแผนบนการ์ด ห้ามแตะหน้าจอคอมฯ",
            "- ประจำตำแหน่งหน้ากล้องเว็บแคม\n- รับฟังทิศทางจาก Navigator อย่างตั้งใจ\n- ใช้มือแตะบล็อกคำสั่งเสมือนจริงหน้ากล้อง AR\n- กดรันเพื่อทดสอบการเดินของหุ่นยนต์\n* กฎเหล็ก: ป้อนคำสั่งตามที่ Navigator บอกเท่านั้น"
        ]
    ]
    elements.append(make_table(t_roles[0], t_roles[1:], [4513, 4513], ["left", "left"]))
    elements.append(make_p([("* มีระบบจับเวลาสลับบทบาท (Role Switch) ในเกมทุก 10-15 นาที เพื่อให้นักเรียนทั้ง 8 คน ได้ฝึกทั้งการคิดและการปฏิบัติอย่างเท่าเทียม", False, True, 24, "2563EB")], space_before=60, space_after=100))

    # 4. 5 Steps Activities
    elements.append(make_p([("4. กิจกรรมการเรียนรู้เชิงรุก (Active Learning 5 ขั้นตอน)", True, False, 32, "1E3A8A")], space_before=180, space_after=80))
    steps_content = """ขั้นที่ 1: การตั้งคำถามและกระตุ้นความสนใจ (Warm-up & Challenge) - 15 นาที
• ครูชวนเล่นเกมง่ายๆ: "ถ้าครูปิดตานักเรียน แล้วให้นักเรียนสั่งครูเดินไปหยิบแปลงลบกระดาน นักเรียนจะสั่งอย่างไรไม่ให้ครูเดินชนโต๊ะ?"
• ครูสาธิตเดินตามคำสั่งตรงๆ (ถ้าสั่งเดินหน้าโดยไม่สั่งเลี้ยวก็จะเดินชน) ให้นักเรียนเห็นว่าการสั่งงานต้องบอกทิศทางและจำนวนก้าวให้ชัดเจน
• เปิดตัวเกม CodeBot AR Adventure แสดงการขยับมือแตะบล็อกคำสั่งหน้ากล้อง สร้างความตื่นเต้น

ขั้นที่ 2: สังเกตและสืบค้นความรู้ (Guided Discovery) - 20 นาที
• นักเรียน 4 คู่ นั่งประจำเครื่องคอมฯ สังเกตแผนที่ในเกม และเปิดดูการ์ดความรู้ในเกม
• ครูแนะนำ "ชุดแฟลชการ์ดบนโต๊ะ": บัตรเดินหน้า หันซ้าย หันขวา บัตรวนซ้ำ เพื่อใช้เป็นตัวช่วยแก้การสับสนทิศทาง
• ชี้แจงกติกาบทบาท Driver & Navigator และเป้าหมายการสะสม 3 ดาว

ขั้นที่ 3: ปฏิบัติภารกิจผ่านเกม AR และแฟลชการ์ด (Hands-on Challenge) - 50 นาที
• แผนที่ 1 (ก้าวแรกและทิศทาง): Navigator ใช้ดินสอลากเส้นบนใบงานตารางกริด แล้วหยิบการ์ดลูกศรมาเรียงบนโต๊ะ Driver ป้อนโค้ดหน้ากล้อง AR
• แผนที่ 2 (การทำซ้ำง่ายๆ): สลับบทบาท! สังเกตทางเดินตรงยาวหรือบันได นำบล็อก [วนซ้ำ Loop] มาครอบเพื่อลดโค้ดให้สั้นลง
• แผนที่ 3 (เงื่อนไขกุญแจ): วางแผน 2 จังหวะ: เดินไปเก็บกุญแจก่อน แล้วจึงเดินผ่านประตูเลเซอร์
• แผนที่ 4 (ยอดนักสืบแก้บั๊ก): ดูโค้ดเดิมที่มีจุดผิด เช่น ก้าวเกิน หรือเลี้ยวผิดข้าง แล้วช่วยกันแก้ไขคำสั่งใหม่

ขั้นที่ 4: สรุปคะแนนและความสำเร็จ (Leaderboard & Debrief) - 20 นาที
• แต่ละคู่ดูคะแนนดาวที่ได้รับ และคะแนนบนกระดานเกียรติยศ (Classroom Leaderboard)
• ครูชมเชยคู่หูที่มีการปรึกษาช่วยเหลือกันดีเยี่ยม

ขั้นที่ 5: สะท้อนคิดและประเมินตนเอง (Reflection & AAR) - 15 นาที
• ร่วมกันตอบคำถามถอดบทเรียน: "ถ้าหุ่นยนต์เลี้ยวผิดข้าง เรามีวิธีดูทิศทางอย่างไร?"
• บันทึกคะแนนลงในใบงาน Mission Log และครูตรวจประเมินผล"""
    elements.append(make_callout(steps_content, title="กระบวนการจัดกิจกรรมการเรียนรู้"))

    # 5. Media & Materials
    elements.append(make_p([("5. สื่อและแหล่งการเรียนรู้", True, False, 32, "1E3A8A")], space_before=180, space_after=80))
    elements.append(make_p([("1. เว็บเกม CodeBot AR Adventure (เปิดบน Chrome/Edge ในห้องคอมฯ)", False, False, 30, "374151")], bullet=True))
    elements.append(make_p([("2. ชุดสมุดบันทึกภารกิจ 4 ใบงานเต็มแผ่น A4 พร้อมแผนที่ตารางกริด", False, False, 30, "374151")], bullet=True))
    elements.append(make_p([("3. ชุดแฟลชการ์ดบัตรคำสั่งสัญลักษณ์จริง 18 ใบ (สื่อสัมผัสช่วยแก้ความสับสนทิศทาง)", False, False, 30, "374151")], bullet=True))
    elements.append(make_p([("4. เครื่องคอมพิวเตอร์พร้อมกล้องเว็บแคม 4 เครื่อง", False, False, 30, "374151")], bullet=True))

    # 6. Evaluation Table
    elements.append(make_p([("6. การวัดและประเมินผลการเรียนรู้", True, False, 32, "1E3A8A")], space_before=180, space_after=80))
    t_eval = [
        ["สิ่งที่ต้องการวัด (K-P-A)", "วิธีการวัด", "เครื่องมือวัด", "เกณฑ์การผ่าน"],
        ["ด้านความรู้ (K)", "ตรวจใบงาน Mission Log 4 ใบงาน", "แบบตรวจใบงาน", "ร้อยละ 70 ขึ้นไป"],
        ["ด้านทักษะกระบวนการ (P)", "สังเกตการเล่นเกม / การตรวจแก้บั๊ก", "แบบประเมินรูบริกส์ CT 4 ด้านอย่างง่าย", "ระดับ 'ดี' ขึ้นไป"],
        ["ด้านคุณลักษณะอันพึงประสงค์ (A)", "สังเกตการทำงานร่วมกันแบบคู่หู", "แบบประเมินพฤติกรรมกลุ่ม", "ระดับ 'ดี' ขึ้นไป"]
    ]
    elements.append(make_table(t_eval[0], t_eval[1:], [2600, 2600, 2400, 1426], ["left", "left", "left", "center"]))
    elements.append(make_p([], space_before=100, space_after=100))

    # 7. Post-Lesson Reflection
    elements.append(make_p([("7. บันทึกผลหลังการจัดการเรียนรู้ (Post-Lesson Reflection)", True, False, 32, "1E3A8A")], space_before=180, space_after=80))
    post_text = """ผลการจัดการเรียนรู้:
นักเรียนชั้น ป.5 ทั้ง 8 คน (4 คู่) ให้ความร่วมมือในการทำกิจกรรมเป็นอย่างดี นวัตกรรมเกม CodeBot AR และชุดแฟลชการ์ดช่วยให้นักเรียนมองเห็นทิศทางและลำดับก้าวเดินได้อย่างชัดเจน สามารถแก้ปัญหาความสับสนเรื่องซ้าย-ขวาได้สำเร็จ คะแนนทดสอบหลังเรียนเฉลี่ยร้อยละ 85.63 สูงกว่าก่อนเรียนอย่างมีนัยสำคัญ

ปัญหาและอุปสรรคที่พบ:
ในชั่วโมงแรก นักเรียนบางคนยังสับสนทิศทางเมื่อหุ่นยนต์หันหน้าลงด้านล่าง ทำให้สั่งเลี้ยวผิดด้าน

แนวทางแก้ไขและการพัฒนาต่อยอด (สู่การวิจัยในชั้นเรียน):
ครูได้แนะนำให้นักเรียนหมุนแฟลชการ์ดลูกศรบนโต๊ะให้หันไปในทิศทางเดียวกับหุ่นยนต์ ซึ่งช่วยให้นักเรียนเข้าใจมุมมองของหุ่นยนต์ได้ทันที จึงเกิดการพัฒนาเป็นรายงานวิจัยในชั้นเรียน (CAR) เพื่อยืนยันประสิทธิผลของการใช้สื่อเกมและแฟลชการ์ดร่วมกับ Active Learning อย่างเป็นระบบ"""
    elements.append(make_callout(post_text, title="บันทึกผลการสอนของครูผู้สอน"))

    # Signatures
    elements.append(make_p([("การลงนามรับรองแผนการจัดการเรียนรู้", True, False, 30, "1E3A8A")], space_before=140, space_after=60))
    t_sign = [
        ["ลงชื่อครูผู้สอน", "ความเห็นของผู้อำนวยการโรงเรียน"],
        [
            "(ลงชื่อ).....................................................................\n( นายเตชินท์ อินทมล )\nตำแหน่ง ครู ไม่มีวิทยฐานะ\nวันที่ ........ เดือน ........................ พ.ศ. 2568",
            "แผนการจัดการเรียนรู้มีความเหมาะสมกับระดับพัฒนาการของเด็ก ป.5 มีการนำสื่อนวัตกรรมมาแก้ปัญหาทิศทางและลำดับขั้นตอนได้อย่างตรงจุด อนุมัติให้ใช้จัดการเรียนรู้ได้\n\n(ลงชื่อ).....................................................................\n( ..................................................................... )\nตำแหน่ง ผู้อำนวยการโรงเรียนบ้านโนนป่าหว้านเชียงฮาย"
        ]
    ]
    elements.append(make_table(t_sign[0], t_sign[1:], [4513, 4513], ["left", "left"]))

    # Wrap DOCX
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
  </w:docDefaults>
</w:styles>"""

    document_xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:body>
    {doc_body}
    <w:sectPr>
      <w:pgSz w:w="11906" w:h="16838"/>
      <w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" w:header="720" w:footer="720" w:gutter="0"/>
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
    path1 = "แผนการจัดการเรียนรู้_Active_Learning_วิทยาการคำนวณ_ป5_ครูเตชินท์.docx"
    path2 = os.path.join("docs", "แผนการจัดการเรียนรู้_Active_Learning_วิทยาการคำนวณ_ป5_ครูเตชินท์.docx")
    
    with open(path1, "wb") as f:
        f.write(data)
    with open(path2, "wb") as f:
        f.write(data)
        
    print(f"Calibrated Lesson Plan DOCX Updated Successfully: {path1}")

if __name__ == "__main__":
    build_lesson_plan_docx()
