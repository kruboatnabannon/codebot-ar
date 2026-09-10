# -*- coding: utf-8 -*-
import zipfile, io, os, html

def esc(text):
    if text is None:
        return ""
    return html.escape(str(text))

def make_p(runs, align="left", space_before=0, space_after=20, line_spacing=220):
    p_props = [f'<w:jc w:val="{align}"/>']
    p_props.append(f'<w:spacing w:before="{space_before}" w:after="{space_after}" w:line="{line_spacing}" w:lineRule="auto"/>')
    runs_xml = []
    for item in runs:
        if isinstance(item, str):
            t, b, i, sz, c = item, False, False, 24, "000000"
        else:
            t = item[0]
            b = item[1] if len(item) > 1 else False
            i = item[2] if len(item) > 2 else False
            sz = item[3] if len(item) > 3 else 24
            c = item[4] if len(item) > 4 else "000000"
        
        r_pr = ['<w:rFonts w:ascii="TH Sarabun PSK" w:hAnsi="TH Sarabun PSK" w:cs="TH Sarabun PSK"/>']
        if b: r_pr.append('<w:b/><w:bCs/>')
        if i: r_pr.append('<w:i/><w:iCs/>')
        r_pr.append(f'<w:sz w:val="{sz}"/><w:szCs w:val="{sz}"/>')
        if c and c != "000000": r_pr.append(f'<w:color w:val="{c}"/>')
        runs_xml.append(f'<w:r><w:rPr>{"".join(r_pr)}</w:rPr><w:t xml:space="preserve">{esc(t)}</w:t></w:r>')
    return f'<w:p><w:pPr>{"".join(p_props)}</w:pPr>{"".join(runs_xml)}</w:p>'

def make_callout(text, title=None, bg="F1F5F9", bdr="1E3A8A"):
    p_pr = f'''<w:pPr>
        <w:pBdr><w:left w:val="single" w:sz="18" w:space="8" w:color="{bdr}"/></w:pBdr>
        <w:shd w:val="clear" w:color="auto" w:fill="{bg}"/>
        <w:ind w:left="160" w:right="160"/>
        <w:spacing w:before="30" w:after="30" w:line="210" w:lineRule="auto"/>
    </w:pPr>'''
    runs_xml = []
    if title:
        runs_xml.append(f'''<w:r><w:rPr><w:rFonts w:ascii="TH Sarabun PSK" w:hAnsi="TH Sarabun PSK" w:cs="TH Sarabun PSK"/><w:b/><w:bCs/><w:sz w:val="23"/><w:szCs w:val="23"/><w:color w:val="{bdr}"/></w:rPr><w:t xml:space="preserve">{esc(title)}&#10;</w:t></w:r>''')
    runs_xml.append(f'''<w:r><w:rPr><w:rFonts w:ascii="TH Sarabun PSK" w:hAnsi="TH Sarabun PSK" w:cs="TH Sarabun PSK"/><w:sz w:val="22"/><w:szCs w:val="22"/><w:color w:val="1E293B"/></w:rPr><w:t xml:space="preserve">{esc(text)}</w:t></w:r>''')
    return f'<w:p>{p_pr}{"".join(runs_xml)}</w:p>'

def make_table(headers, rows, col_widths, alignments=None, font_size=21, header_bg="1E3A8A"):
    total_w = sum(col_widths)
    if alignments is None: alignments = ["center"] * len(headers)
    xml = ['<w:tbl>',
           f'''<w:tblPr>
               <w:tblW w:w="{total_w}" w:type="dxa"/>
               <w:tblInd w:w="0" w:type="dxa"/>
               <w:tblBorders>
                   <w:top w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>
                   <w:left w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>
                   <w:bottom w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>
                   <w:right w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>
                   <w:insideH w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/>
                   <w:insideV w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/>
               </w:tblBorders>
               <w:tblCellMar>
                   <w:top w:w="30" w:type="dxa"/>
                   <w:left w:w="60" w:type="dxa"/>
                   <w:bottom w:w="30" w:type="dxa"/>
                   <w:right w:w="60" w:type="dxa"/>
               </w:tblCellMar>
           </w:tblPr>''']
    xml.append('<w:tblGrid>')
    for w in col_widths: xml.append(f'<w:gridCol w:w="{w}"/>')
    xml.append('</w:tblGrid>')
    # Header
    xml.append('<w:tr><w:trPr><w:tblHeader/><w:trHeight w:val="230" w:hRule="atLeast"/></w:trPr>')
    for i, h in enumerate(headers):
        w = col_widths[i]
        al = alignments[i] if i < len(alignments) else "center"
        xml.append(f'''<w:tc><w:tcPr><w:tcW w:w="{w}" w:type="dxa"/><w:shd w:val="clear" w:color="auto" w:fill="{header_bg}"/><w:vAlign w:val="center"/></w:tcPr>
            <w:p><w:pPr><w:jc w:val="{al}"/><w:spacing w:before="10" w:after="10" w:line="190" w:lineRule="auto"/></w:pPr>
            <w:r><w:rPr><w:rFonts w:ascii="TH Sarabun PSK" w:hAnsi="TH Sarabun PSK" w:cs="TH Sarabun PSK"/><w:b/><w:bCs/><w:sz w:val="{font_size}"/><w:szCs w:val="{font_size}"/><w:color w:val="FFFFFF"/></w:rPr><w:t xml:space="preserve">{esc(h)}</w:t></w:r></w:p></w:tc>''')
    xml.append('</w:tr>')
    # Rows
    for row in rows:
        xml.append('<w:tr><w:trPr><w:trHeight w:val="230" w:hRule="atLeast"/></w:trPr>')
        for i, val in enumerate(row):
            w = col_widths[i]
            al = alignments[i] if i < len(alignments) else "left"
            # Highlight special cells
            bg_color = "FFFFFF"
            if "🤖" in val: bg_color = "DCFCE7"
            elif "🚀" in val: bg_color = "E0F2FE"
            elif "🔋" in val: bg_color = "FEF08A"
            elif "⚡" in val: bg_color = "FEE2E2"
            elif "🗝️" in val: bg_color = "FEF9C3"
            elif "🪨" in val: bg_color = "F1F5F9"
            
            val_escaped = esc(val).replace("\n", '</w:t></w:r></w:p><w:p><w:pPr><w:jc w:val="' + al + '"/><w:spacing w:before="10" w:after="10" w:line="190" w:lineRule="auto"/></w:pPr><w:r><w:rPr><w:rFonts w:ascii="TH Sarabun PSK" w:hAnsi="TH Sarabun PSK" w:cs="TH Sarabun PSK"/><w:sz w:val="' + str(font_size) + '"/><w:szCs w:val="' + str(font_size) + '"/><w:color w:val="1E293B"/></w:rPr><w:t xml:space="preserve">')
            
            xml.append(f'''<w:tc><w:tcPr><w:tcW w:w="{w}" w:type="dxa"/><w:shd w:val="clear" w:color="auto" w:fill="{bg_color}"/><w:vAlign w:val="center"/></w:tcPr>
                <w:p><w:pPr><w:jc w:val="{al}"/><w:spacing w:before="10" w:after="10" w:line="190" w:lineRule="auto"/></w:pPr>
                <w:r><w:rPr><w:rFonts w:ascii="TH Sarabun PSK" w:hAnsi="TH Sarabun PSK" w:cs="TH Sarabun PSK"/><w:sz w:val="{font_size}"/><w:szCs w:val="{font_size}"/><w:color w:val="1E293B"/></w:rPr><w:t xml:space="preserve">{val_escaped}</w:t></w:r></w:p></w:tc>''')
        xml.append('</w:tr>')
    xml.append('</w:tbl>')
    return "".join(xml)

def make_team_header_docx(sheet_desc, title, sub, role_n, role_d):
    el = []
    el.append(make_p([
        (f"📄 {sheet_desc}  |  วิชาวิทยาการคำนวณ ว15101 ชั้น ป.5", True, False, 20, "2563EB")
    ], align="left", space_before=0, space_after=10))
    el.append(make_p([
        (f"🚀 CodeBot AR: {title}", True, False, 26, "1E3A8A")
    ], align="center", space_before=10, space_after=10))
    el.append(make_p([
        (f"โรงเรียนบ้านโนนป่าหว้านเชียงฮาย สพป.หนองบัวลำภู เขต 2 | {sub}", False, True, 18, "475569")
    ], align="center", space_before=0, space_after=25))

    t_team = [
        ["ข้อมูลคู่หู Active Learning", "เลขที่", "บทบาทหน้าที่ประจำภารกิจ"],
        ["ชื่อทีม/กลุ่ม: ..........................................................................", "-", "กลุ่มที่: ................"],
        ["1. ......................................................................................", "......", f"[  ] Navigator ({role_n})"],
        ["2. ......................................................................................", "......", f"[  ] Driver ({role_d})"]
    ]
    el.append(make_table(t_team[0], t_team[1:], [5200, 700, 4600], ["left", "center", "left"], font_size=20, header_bg="1E40AF"))
    return el

def make_footer_box_docx(star_text, status_text="เข้ายานสำเร็จ"):
    el = []
    el.append(make_p([
        (f"⭐ ผลการทดสอบหน้ากล้อง AR:  [  ] {status_text}   [  ] ปรับแก้โค้ด  |  ดาวที่ได้: [  ] 1 ดาว   [  ] 2 ดาว   [  ] 3 ดาว 🌟🌟🌟", True, False, 20, "1E40AF")
    ], align="left", space_before=30, space_after=15))
    el.append(make_p([
        ("ครูผู้สอน/ผู้ตรวจ: นายเตชินท์ อินทมล      |      ลายมือชื่อคู่หู: 1) ........................................ 2) ........................................", False, True, 18, "64748B")
    ], align="left", space_before=0, space_after=0))
    return el

# Build all 4 worksheets
body = []

# ================= PAGE 1 =================
body.extend(make_team_header_docx(
    "แผ่นที่ 1 [ด้านหน้า] : ชุดที่ 1 พลังการวนซ้ำ (Loops)",
    "ใบงานที่ 1: ค้นหารูปแบบและลูปบันได 3 ขั้น (ด่าน 1-3 ป.5)",
    "สอดรับเกมนวัตกรรม CodeBot AR Adventure แทร็ก ป.5 (ด่านที่ 1 - 3)",
    "ผู้นำทาง วาดแผนที่ & สังเกตรูปแบบ",
    "ผู้สั่งการ ชูการ์ดคำสั่งหน้ากล้อง AR"
))
body.append(make_callout(
    "สังเกตเส้นทางเดินขึ้นบันได 3 ขั้น หุ่นยนต์ต้องก้าวเดินซ้ำๆ เป็นแพทเทิร์น ให้ใช้ดินสอลากเส้นทาง 🤖 เก็บแบตเตอรี่ 🔋 แล้วเข้าสู่ยาน 🚀 โดยไม่ชนหิน 🪨 จากนั้นช่วยกันออกแบบบล็อก [วนซ้ำ Loop] รวบคำสั่งให้สั้นที่สุดเพื่อคว้า 3 ดาว!",
    title="🎯 ภารกิจเนวิเกเตอร์ (Navigator):"
))
body.append(make_p([("🗺️ แผนที่จำลองในเกม (Grid 6x6) - เนวิเกเตอร์ใช้ดินสอลากเส้นทางเดิน:", True, False, 20, "1E3A8A")], space_before=20, space_after=15))
m1_h = ["แถว/คอลัมน์", "C1", "C2", "C3", "C4", "C5", "C6"]
m1_r = [
    ["R1", "", "", "", "🚀 (ยาน)", "", ""],
    ["R2", "", "", "🪨", "🔋 (แบต 3)", "", ""],
    ["R3", "", "🪨", "🔋 (แบต 2)", "", "", ""],
    ["R4", "🪨", "🔋 (แบต 1)", "", "", "", ""],
    ["R5", "🤖 (เริ่ม)", "", "", "", "", ""],
    ["R6", "", "", "", "", "", ""]
]
body.append(make_table(m1_h, m1_r, [1700, 1500, 1500, 1500, 1500, 1500, 1500], ["center"] * 7, font_size=19))

body.append(make_p([("📝 ถอดรหัสแพทเทิร์นและออกแบบบล็อกลูป (Loop Block Design):", True, False, 20, "1E3A8A")], space_before=25, space_after=15))
loop_text = """1. คำสั่งใน 1 ขั้นบันได ที่ทำซ้ำกัน คือ: [ ................................................................................................................................. ]
2. จำนวนรอบที่ต้องทำซ้ำติดต่อกัน คือ: .................... รอบ  (เขียนบล็อกคำสั่ง: [ วนซ้ำ Loop .................... รอบ ])
3. เปรียบเทียบความยาวโค้ด: แบบไม่ใช้ลูป = ............ บล็อก  |  แบบใช้ลูปย่อคำสั่ง = ลดเหลือเพียง ............ บล็อก!"""
body.append(make_callout(loop_text, title="วิเคราะห์แพทเทิร์นบันได"))
body.extend(make_footer_box_docx("ผลทดสอบ"))

# ================= PAGE 2 =================
body.append('<w:p><w:r><w:br w:type="page"/></w:r></w:p>')

body.extend(make_team_header_docx(
    "แผ่นที่ 1 [ด้านหลัง] : ชุดที่ 1 พลังการวนซ้ำ (Loops) [สลับบทบาท]",
    "ใบงานที่ 2: ลูปตรวจรอบสถานีและการลดรูปโค้ด (ด่าน 4 ป.5)",
    "สอดรับเกมนวัตกรรม CodeBot AR Adventure แทร็ก ป.5 (ด่านที่ 4) - พลิกด้านหลัง",
    "สลับเป็นผู้นำทาง วางแผนโค้ดประหยัด",
    "สลับเป็นผู้สั่งการ ควบคุมหน้ากล้อง AR"
))
body.append(make_callout(
    "หุ่นยนต์ต้องเดินลาดตระเวนรอบสถานีอวกาศ 4 ทิศ เพื่อชาร์จแบตเตอรี่ 🔋 ให้ครบทั้ง 4 ด้าน คู่หูช่วยกันเขียนบล็อกลูปแบบผสมคำสั่ง (Multi-Action Loop) ให้โค้ดสั้นและประหยัดบล็อกคำสั่งที่สุด!",
    title="🎯 ภารกิจสลับบทบาท (Swap Role Challenge):"
))
body.append(make_p([("🗺️ แผนที่ลาดตระเวนรอบสถานี 4 ทิศ (Grid 6x6):", True, False, 20, "1E3A8A")], space_before=20, space_after=15))
m2_h = ["แถว/คอลัมน์", "C1", "C2", "C3", "C4", "C5", "C6"]
m2_r = [
    ["R1", "🚀 (ยาน)", "🔋", "🔋", "🔋", "", ""],
    ["R2", "🔋", "🪨 (แกนกลาง)", "🪨", "🔋", "", ""],
    ["R3", "🔋", "🪨 (แกนกลาง)", "🪨", "🔋", "", ""],
    ["R4", "🤖 (เริ่ม)", "🔋", "🔋", "🔋", "", ""],
    ["R5", "", "", "", "", "", ""],
    ["R6", "", "", "", "", "", ""]
]
body.append(make_table(m2_h, m2_r, [1700, 1500, 1500, 1500, 1500, 1500, 1500], ["center"] * 7, font_size=19))

body.append(make_p([("📝 เปรียบเทียบโค้ด 2 รูปแบบ (Code Optimization):", True, False, 20, "1E3A8A")], space_before=25, space_after=15))
opt_h = ["❌ แบบเดิม (วางคำสั่งเรียงยาว)", "✅ แบบประหยัดโค้ด (Multi-Action Loop)"]
opt_r = [[
    "1. เดินหน้า 3 ก้าว    5. เดินหน้า 3 ก้าว\n2. เลี้ยวขวา           6. เลี้ยวขวา\n3. เดินหน้า 3 ก้าว    7. เดินหน้า 3 ก้าว\n4. เลี้ยวขวา           8. เลี้ยวขวา\n(รวม 12-16 บล็อก เสียเวลามาก!)",
    "[ วนซ้ำ (Loop) ............ รอบ ]\n{\n    1. เดินหน้า ............ ก้าว\n    2. เลี้ยว ................................\n}\n(ประหยัดบล็อกเหลือเพียง 1 ลูปสั้นๆ!)"
]]
body.append(make_table(opt_h, opt_r, [5250, 5250], ["left", "left"], font_size=20, header_bg="0F766E"))
body.extend(make_footer_box_docx("ผลทดสอบ", "ลาดตระเวนสำเร็จ 4 ทิศ"))

# ================= PAGE 3 =================
body.append('<w:p><w:r><w:br w:type="page"/></w:r></w:p>')

body.extend(make_team_header_docx(
    "แผ่นที่ 2 [ด้านหน้า] : ชุดที่ 2 เงื่อนไขและแก้บั๊ก (Conditionals)",
    "ใบงานที่ 3: เงื่อนไขถ้า...แล้ว กุญแจและประตูเลเซอร์ (ด่าน 5-6 ป.5)",
    "สอดรับเกมนวัตกรรม CodeBot AR Adventure แทร็ก ป.5 (ด่านที่ 5 - 6)",
    "ผู้นำทาง คำนวณเงื่อนไขและทางแยก",
    "ผู้สั่งการ ส่องการ์ดกุญแจหน้ากล้อง AR"
))
body.append(make_callout(
    "ประตูเลเซอร์ ⚡ กั้นทางเข้ายานอวกาศ ห้ามเดินชนเด็ดขาด! หุ่นยนต์ต้องวางแผนเดินไปเก็บกุญแจคีย์การ์ด 🗝️ เสียก่อน ประตูจึงจะเปิดออก ให้นักเรียนเขียนประโยคเงื่อนไขตรรกะและแบ่งภารกิจออกเป็น 2 เฟส",
    title="🎯 ภารกิจตรรกะแบบมีเงื่อนไข (If-Then Logic):"
))
body.append(make_p([("🗺️ แผนที่ประตูปริศนาเลเซอร์และกุญแจคีย์การ์ด (Grid 6x6):", True, False, 20, "1E3A8A")], space_before=20, space_after=15))
m3_h = ["แถว/คอลัมน์", "C1", "C2", "C3", "C4", "C5", "C6"]
m3_r = [
    ["R1", "", "", "", "⚡ (เลเซอร์)", "🚀 (ยานแม่)", ""],
    ["R2", "🗝️ (กุญแจ)", "", "", "⚡ (เลเซอร์)", "", ""],
    ["R3", "🪨", "🪨", "", "", "", ""],
    ["R4", "🤖 (เริ่ม)", "", "", "", "", ""],
    ["R5", "", "", "", "", "", ""],
    ["R6", "", "", "", "", "", ""]
]
body.append(make_table(m3_h, m3_r, [1700, 1500, 1500, 1500, 1500, 1500, 1500], ["center"] * 7, font_size=19))

body.append(make_p([("🧠 โครงสร้างตรรกะเงื่อนไข If-Then-Else ของคู่เรา:", True, False, 20, "1E3A8A")], space_before=20, space_after=10))
cond_t = """• [ ถ้า (IF) ] : หุ่นยนต์มีไอเทมชิ้นนี้ คือ [ ........................................................................................................................................ ]
• [ แล้ว (THEN) ] : ประตูเลเซอร์จะเกิดผลคือ [ .................................................................................................... ] และเดินผ่านเข้ายานได้
• [ มิฉะนั้น (ELSE) ] : ถ้ายังไม่มีกุญแจ ห้ามเดินชน เพราะจะเกิดผลคือ [ ...................................................................................................... ]"""
body.append(make_callout(cond_t, title="ประโยคเงื่อนไขของคู่เรา", bg="FEF9C3", bdr="B45309"))

p3_h = ["เฟส 1: เดินไปเก็บกุญแจคีย์การ์ด 🗝️", "เฟส 2: เดินทะลุประตูเลเซอร์เข้ายาน 🚀"]
p3_r = [[
    "1. ............................................................................\n2. ............................................................................\n3. ............................................................................",
    "1. ............................................................................\n2. ............................................................................\n3. ............................................................................"
]]
body.append(make_table(p3_h, p3_r, [5250, 5250], ["left", "left"], font_size=20, header_bg="B45309"))
body.extend(make_footer_box_docx("ผลทดสอบ", "ปลดล็อกเลเซอร์สำเร็จ"))

# ================= PAGE 4 =================
body.append('<w:p><w:r><w:br w:type="page"/></w:r></w:p>')

body.extend(make_team_header_docx(
    "แผ่นที่ 2 [ด้านหลัง] : ชุดที่ 2 เงื่อนไขและแก้บั๊ก [สลับบทบาท]",
    "ใบงานที่ 4: ยอดนักสืบแก้บั๊กตรรกะและบททดสอบมาสเตอร์ (ด่าน 7-10 ป.5)",
    "สอดรับเกมนวัตกรรม CodeBot AR แทร็ก ป.5 (ด่านที่ 7 - 10) - พลิกด้านหลัง",
    "สลับเป็นผู้นำทาง วิเคราะห์บั๊กและสะท้อนคิด",
    "สลับเป็นผู้สั่งการ ทดสอบโค้ดแก้บั๊กหน้ากล้อง"
))
body.append(make_callout(
    "โค้ดเดิมมีข้อผิดพลาด (Bug) ทำให้หุ่นยนต์เดินตรงไปชนประตูเลเซอร์ก่อนเก็บกุญแจ! ให้นักเรียนสืบหาจุดผิดและเขียนโค้ดที่ถูกต้อง จากนั้นร่วมกันสะท้อนคิดถอดบทเรียน (AAR) หลังจบภารกิจ 10 ด่าน",
    title="🎯 ภารกิจนักสืบแก้บั๊ก & ถอดบทเรียน (Debugging & Reflection):"
))

body.append(make_p([("🐞 ตารางตรวจจับและแก้ไขบั๊ก (Bug Detective Table):", True, False, 20, "1E3A8A")], space_before=20, space_after=15))
bug_h = ["❌ โค้ดเดิมที่มีข้อผิดพลาด (Bug)", "✅ โค้ดใหม่ที่ถูกต้อง (คู่หูแก้ไขแล้ว)"]
bug_r = [[
    "1. เดินหน้า 3 ก้าวไปที่ประตูเลเซอร์\n   ❌ (บั๊ก! ชนเลเซอร์เพราะยังไม่มีกุญแจ)\n2. เลี้ยวซ้ายไปหากุญแจ\n3. เก็บกุญแจคีย์การ์ด\n4. เดินเข้ายานอวกาศ",
    "1. แก้ไขเป็น: ................................................................\n2. ........................................................................................\n3. ........................................................................................\n4. เดินเข้ายานอวกาศสำเร็จ!"
]]
body.append(make_table(bug_h, bug_r, [5250, 5250], ["left", "left"], font_size=20, header_bg="B91C1C"))

body.append(make_p([("💬 การสะท้อนคิดถอดบทเรียนร่วมกัน (After Action Review: AAR):", True, False, 20, "1E3A8A")], space_before=20, space_after=10))
aar_t = """1. สิ่งที่คู่หู (Driver & Navigator) ช่วยเหลือกันได้ดีที่สุดในการแก้ปัญหา คืออะไร?
   ตอบ: ............................................................................................................................................................................................
2. การใช้การ์ดคำสั่งและเล่นเกม AR บนโต๊ะ ช่วยให้เข้าใจการเขียนโปรแกรมง่ายขึ้นอย่างไร?
   ตอบ: ............................................................................................................................................................................................
3. ในชีวิตจริงถ้าเจอปัญหาที่แก้ไม่ออก เราจะนำวิธี "หาจุดผิดพลาดทีละก้าว (Debugging)" ไปใช้อย่างไร?
   ตอบ: ............................................................................................................................................................................................"""
body.append(make_callout(aar_t, title="ถอดบทเรียนคู่หู ป.5", bg="F8FAFC", bdr="475569"))

body.append(make_p([
    ("🏆 บททดสอบมาสเตอร์ ป.5: ผ่านครบ 10 ด่าน!  |  คะแนนดาวสะสมรวม: ............ / 30 ดาว ⭐⭐⭐", True, False, 20, "1E40AF")
], align="left", space_before=25, space_after=15))
body.append(make_p([
    ("ครูผู้สอน/ผู้ตรวจ: นายเตชินท์ อินทมล      |      ลายมือชื่อคู่หู: 1) ........................................ 2) ........................................", False, True, 18, "64748B")
], align="left", space_before=0, space_after=0))

doc_body = "".join(body)

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
        <w:sz w:val="24"/>
        <w:szCs w:val="24"/>
        <w:lang w:val="th-TH"/>
      </w:rPr>
    </w:rPrDefault>
    <w:pPrDefault>
      <w:pPr>
        <w:spacing w:before="0" w:after="20" w:line="220" w:lineRule="auto"/>
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
      <w:pgMar w:top="500" w:right="650" w:bottom="500" w:left="650"/>
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

print(f"Successfully generated compact {out_file}")
os.system(f"cp '{out_file}' docs/")
