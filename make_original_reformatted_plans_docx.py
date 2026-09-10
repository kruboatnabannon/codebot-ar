# -*- coding: utf-8 -*-
import zipfile, io, os, html

def esc(text):
    if text is None: return ""
    return html.escape(str(text))

def make_page_break():
    return '<w:p><w:r><w:br w:type="page"/></w:r></w:p>'

def make_p(runs, align="left", space_before=40, space_after=40, line_spacing=240, bullet=False):
    p_props = [f'<w:jc w:val="{align}"/>']
    p_props.append(f'<w:spacing w:before="{space_before}" w:after="{space_after}" w:line="{line_spacing}" w:lineRule="auto"/>')
    if bullet:
        p_props.append('<w:ind w:left="480" w:hanging="240"/>')

    runs_xml = []
    if bullet:
        runs_xml.append('''<w:r><w:rPr><w:rFonts w:ascii="TH Sarabun PSK" w:hAnsi="TH Sarabun PSK" w:cs="TH Sarabun PSK"/><w:sz w:val="28"/><w:szCs w:val="28"/></w:rPr><w:t>• </w:t></w:r>''')

    for item in runs:
        if isinstance(item, str):
            t, b, i, sz, c = item, False, False, 28, "000000"
        else:
            t = item[0]
            b = item[1] if len(item) > 1 else False
            i = item[2] if len(item) > 2 else False
            sz = item[3] if len(item) > 3 else 28
            c = item[4] if len(item) > 4 else "000000"
        
        r_pr = ['<w:rFonts w:ascii="TH Sarabun PSK" w:hAnsi="TH Sarabun PSK" w:cs="TH Sarabun PSK"/>']
        if b: r_pr.append('<w:b/><w:bCs/>')
        if i: r_pr.append('<w:i/><w:iCs/>')
        r_pr.append(f'<w:sz w:val="{sz}"/><w:szCs w:val="{sz}"/>')
        if c and c != "000000": r_pr.append(f'<w:color w:val="{c}"/>')
        runs_xml.append(f'<w:r><w:rPr>{"".join(r_pr)}</w:rPr><w:t xml:space="preserve">{esc(t)}</w:t></w:r>')
    return f'<w:p><w:pPr>{"".join(p_props)}</w:pPr>{"".join(runs_xml)}</w:p>'

def make_callout(text, title=None, bg="F8FAFC", bdr="1E3A8A"):
    p_pr = f'''<w:pPr>
        <w:pBdr><w:left w:val="single" w:sz="24" w:space="15" w:color="{bdr}"/></w:pBdr>
        <w:shd w:val="clear" w:color="auto" w:fill="{bg}"/>
        <w:ind w:left="300" w:right="300"/>
        <w:spacing w:before="60" w:after="60" w:line="230" w:lineRule="auto"/>
    </w:pPr>'''
    runs_xml = []
    if title:
        runs_xml.append(f'''<w:r><w:rPr><w:rFonts w:ascii="TH Sarabun PSK" w:hAnsi="TH Sarabun PSK" w:cs="TH Sarabun PSK"/><w:b/><w:bCs/><w:sz w:val="28"/><w:szCs w:val="28"/><w:color w:val="{bdr}"/></w:rPr><w:t xml:space="preserve">{esc(title)}&#10;</w:t></w:r>''')
    
    text_escaped = esc(text).replace("\n", '</w:t></w:r></w:p><w:p>' + p_pr + '<w:r><w:rPr><w:rFonts w:ascii="TH Sarabun PSK" w:hAnsi="TH Sarabun PSK" w:cs="TH Sarabun PSK"/><w:sz w:val="26"/><w:szCs w:val="26"/><w:color w:val="334155"/></w:rPr><w:t xml:space="preserve">')
    runs_xml.append(f'''<w:r><w:rPr><w:rFonts w:ascii="TH Sarabun PSK" w:hAnsi="TH Sarabun PSK" w:cs="TH Sarabun PSK"/><w:sz w:val="26"/><w:szCs w:val="26"/><w:color w:val="334155"/></w:rPr><w:t xml:space="preserve">{text_escaped}</w:t></w:r>''')
    return f'<w:p>{p_pr}{"".join(runs_xml)}</w:p>'

def make_table(headers, rows, col_widths, alignments=None, font_size=24, header_bg="1E3A8A"):
    total_w = sum(col_widths)
    if alignments is None: alignments = ["center"] * len(headers)
    xml = ['<w:tbl>',
           f'''<w:tblPr>
               <w:tblW w:w="{total_w}" w:type="dxa"/><w:tblInd w:w="0" w:type="dxa"/>
               <w:tblBorders>
                   <w:top w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>
                   <w:left w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>
                   <w:bottom w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>
                   <w:right w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>
                   <w:insideH w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/>
                   <w:insideV w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/>
               </w:tblBorders>
               <w:tblCellMar><w:top w:w="50" w:type="dxa"/><w:left w:w="90" w:type="dxa"/><w:bottom w:w="50" w:type="dxa"/><w:right w:w="90" w:type="dxa"/></w:tblCellMar>
           </w:tblPr>''',
           '<w:tblGrid>']
    for w in col_widths: xml.append(f'<w:gridCol w:w="{w}"/>')
    xml.append('</w:tblGrid>')
    # Header
    xml.append('<w:tr><w:trPr><w:tblHeader/><w:trHeight w:val="260" w:hRule="atLeast"/></w:trPr>')
    for i, h in enumerate(headers):
        al = alignments[i] if i < len(alignments) else "center"
        xml.append(f'''<w:tc><w:tcPr><w:tcW w:w="{col_widths[i]}" w:type="dxa"/><w:shd w:val="clear" w:color="auto" w:fill="{header_bg}"/><w:vAlign w:val="center"/></w:tcPr>
            <w:p><w:pPr><w:jc w:val="{al}"/><w:spacing w:before="25" w:after="25" w:line="200" w:lineRule="auto"/></w:pPr>
            <w:r><w:rPr><w:rFonts w:ascii="TH Sarabun PSK" w:hAnsi="TH Sarabun PSK" w:cs="TH Sarabun PSK"/><w:b/><w:bCs/><w:sz w:val="{font_size}"/><w:szCs w:val="{font_size}"/><w:color w:val="FFFFFF"/></w:rPr><w:t xml:space="preserve">{esc(h)}</w:t></w:r></w:p></w:tc>''')
    xml.append('</w:tr>')
    for row in rows:
        xml.append('<w:tr><w:trPr><w:trHeight w:val="260" w:hRule="atLeast"/></w:trPr>')
        for i, val in enumerate(row):
            al = alignments[i] if i < len(alignments) else "left"
            val_escaped = esc(val).replace("\n", '</w:t></w:r></w:p><w:p><w:pPr><w:jc w:val="' + al + '"/><w:spacing w:before="15" w:after="15" w:line="200" w:lineRule="auto"/></w:pPr><w:r><w:rPr><w:rFonts w:ascii="TH Sarabun PSK" w:hAnsi="TH Sarabun PSK" w:cs="TH Sarabun PSK"/><w:sz w:val="{font_size}"/><w:szCs w:val="{font_size}"/><w:color w:val="1E293B"/></w:rPr><w:t xml:space="preserve">')
            xml.append(f'''<w:tc><w:tcPr><w:tcW w:w="{col_widths[i]}" w:type="dxa"/><w:vAlign w:val="center"/></w:tcPr>
                <w:p><w:pPr><w:jc w:val="{al}"/><w:spacing w:before="15" w:after="15" w:line="200" w:lineRule="auto"/></w:pPr>
                <w:r><w:rPr><w:rFonts w:ascii="TH Sarabun PSK" w:hAnsi="TH Sarabun PSK" w:cs="TH Sarabun PSK"/><w:sz w:val="{font_size}"/><w:szCs w:val="{font_size}"/><w:color w:val="1E293B"/></w:rPr><w:t xml:space="preserve">{val_escaped}</w:t></w:r></w:p></w:tc>''')
        xml.append('</w:tr>')
    xml.append('</w:tbl>')
    return "".join(xml)

def heading_sec(title):
    return make_p([(title, True, False, 28, "1E3A8A")], align="left", space_before=100, space_after=30)

def heading_sub(title):
    return make_p([(title, True, False, 26, "0369A1")], align="left", space_before=60, space_after=20)

def body_p(text, bold_prefix="", bullet=False):
    runs = []
    if bold_prefix:
        runs.append((bold_prefix, True, False, 26, "1E293B"))
    runs.append((text, False, False, 26, "334155"))
    return make_p(runs, align="left", space_before=20, space_after=20, line_spacing=230, bullet=bullet)

def get_clean_plan_header(num, title):
    el = []
    el.append(make_p([(f"แผนการจัดการเรียนรู้ที่ {num}", True, False, 32, "1E3A8A")], align="center", space_before=40, space_after=10))
    el.append(make_p([("หน่วยการเรียนรู้ที่ 2 เรื่อง การใช้เหตุผลเชิงตรรกะและการเขียนโปรแกรมอย่างง่าย", True, False, 26, "0369A1")], align="center", space_before=0, space_after=10))
    el.append(make_p([(f"เรื่อง: {title}", True, False, 28, "1F2937")], align="center", space_before=0, space_after=10))
    el.append(make_p([("กลุ่มสาระการเรียนรู้วิทยาศาสตร์และเทคโนโลยี รายวิชาเทคโนโลยี (วิทยาการคำนวณ) รหัสวิชา ว15101", False, False, 24, "475569")], align="center", space_before=0, space_after=5))
    el.append(make_p([("ชั้นประถมศึกษาปีที่ 5 | ภาคเรียนที่ 1 ปีการศึกษา 2569 | เวลา 1 ชั่วโมง (50 - 60 นาที)", False, True, 24, "475569")], align="center", space_before=0, space_after=5))
    el.append(make_p([("โรงเรียนบ้านโนนป่าหว้านเชียงฮาย สพป.หนองบัวลำภู เขต 2 | ครูผู้สอน: นายเตชินท์ อินทมล", False, False, 24, "2563EB")], align="center", space_before=0, space_after=50))
    return el

def get_plan_eval_table(k_text, p_text, a_text):
    headers = ["รายการวัดและประเมินผล (K - P - A)", "วิธีการวัด", "เครื่องมือวัด", "เกณฑ์การประเมิน"]
    rows = [
        [f"ด้านความรู้ (K):\n{k_text}", "ตรวจแบบทดสอบ / ตรวจใบงาน", "แบบทดสอบ / แบบตรวจใบงาน", "ได้คะแนนร้อยละ 70 ขึ้นไป ผ่านเกณฑ์"],
        [f"ด้านทักษะกระบวนการ (P):\n{p_text}", "สังเกตการปฏิบัติหน้ากล้อง AR / การแก้ปัญหา", "แบบประเมินรูบริกส์ทักษะ CT", "ระดับคุณภาพ 'ดี' (ระดับ 2) ขึ้นไป"],
        [f"ด้านคุณลักษณะอันพึงประสงค์ (A):\n{a_text}", "สังเกตพฤติกรรมการทำงานกลุ่มคู่หู", "แบบประเมินพฤติกรรมกลุ่ม", "ระดับคุณภาพ 'ดี' (ระดับ 2) ขึ้นไป"]
    ]
    return make_table(headers, rows, [3300, 2400, 2500, 2300], ["left", "left", "left", "center"], font_size=22, header_bg="0284C7")

def get_plan_post_table(num, custom_learning, custom_prob, custom_sol):
    headers = ["ประเด็นการบันทึกหลังการจัดการเรียนรู้", "รายละเอียดผลการจัดการเรียนรู้จริง"]
    rows = [
        ["1. ผลการจัดกิจกรรมการเรียนรู้\n(ด้าน K, P, A และสมรรถนะสำคัญ)", custom_learning],
        ["2. ปัญหาและอุปสรรคที่พบระหว่างสอน", custom_prob],
        ["3. แนวทางการแก้ไขและการพัฒนาต่อยอด", custom_sol]
    ]
    tbl = make_table(headers, rows, [3200, 7300], ["left", "left"], font_size=22, header_bg="0F766E")
    
    sign_text = """ความคิดเห็น / ข้อเสนอแนะของผู้บริหารสถานศึกษา:
แผนการจัดการเรียนรู้มีการจัดกิจกรรมอย่างเป็นขั้นตอนชัดเจน กิจกรรม Active Learning และสื่อนวัตกรรมเกม CodeBot AR เหมาะสมกับวัย ป.5 ช่วยแก้ปัญหาผู้เรียนได้ตรงจุด อนุมัติให้ใช้จัดการเรียนรู้ได้

ลงชื่อ .......................................................................... ผู้บริหารสถานศึกษา
( .......................................................................... )
ตำแหน่ง ผู้อำนวยการโรงเรียนบ้านโนนป่าหว้านเชียงฮาย
วันที่ ........ เดือน ................................... พ.ศ. 2569"""
    box_sign = make_callout(sign_text, title="ความเห็นและการรับรองของผู้บริหารสถานศึกษา", bg="F8FAFC", bdr="64748B")
    
    teacher_sign = """                                                                                ลงชื่อ ................................................................... ครูผู้สอน
                                                                                        ( นายเตชินท์ อินทมล )
                                                                                  ตำแหน่ง ครู โรงเรียนบ้านโนนป่าหว้านเชียงฮาย
                                                                                วันที่ ........ เดือน ................................... พ.ศ. 2569"""
    box_teacher = make_p([(teacher_sign, False, False, 24, "334155")], space_before=30, space_after=30)
    return tbl + box_teacher + box_sign

def build_original_reformatted_plans():
    elements = []

    # Cover Page
    elements.append(make_p([("เล่มแผนการจัดการเรียนรู้เชิงรุก (Active Learning Plan)", True, False, 36, "1E3A8A")], align="center", space_before=160, space_after=50))
    elements.append(make_p([("กลุ่มสาระการเรียนรู้วิทยาศาสตร์และเทคโนโลยี รายวิชาเทคโนโลยี (วิทยาการคำนวณ) รหัสวิชา ว15101", True, False, 26, "1F2937")], align="center", space_before=0, space_after=40))
    elements.append(make_p([("ประเด็นท้าทาย: การพัฒนาทักษะการเรียนรู้โดยใช้กระบวนการ Game Based Learning ร่วมกับ Active Learning", False, False, 26, "2563EB")], align="center", space_before=0, space_after=40))
    elements.append(make_p([("ชั้นประถมศึกษาปีที่ 5 | ภาคเรียนที่ 1 ปีการศึกษา 2569 | แผนการจัดการเรียนรู้ 7 แผน รวม 7 ชั่วโมง", False, True, 26, "4B5563")], align="center", space_before=0, space_after=140))

    intro = """เล่มแผนการจัดการเรียนรู้ชุดนี้ ได้รับการออกแบบตามข้อตกลงในการพัฒนางาน (PA 1) เพื่อขับเคลื่อน 'ประเด็นท้าทาย' ในการแก้ไขปัญหาการเขียนโปรแกรม Scratch ของผู้เรียน โดยผู้วิจัยได้ติดตามพัฒนาการของนักเรียนกลุ่มเป้าหมายจำนวน 8 คน อย่างต่อเนื่องจากสภาพปัญหาที่พบในชั้นประถมศึกษาปีที่ 4 และนำมาปรับประยุกต์ (Apply & Adapt) จัดการเรียนรู้เชิงรุก (Active Learning) ด้วยเทคนิคจับคู่เขียนโปรแกรม (Pair Programming: Driver & Navigator) โดยใช้เกมนวัตกรรม CodeBot AR Adventure และชุดแฟลชการ์ดสัญลักษณ์จริง เป็นสื่อนวัตกรรมฐานรูปธรรมเพื่อปูพื้นฐานการคิดเชิงคำนวณ แก้ปัญหาความสับสนในลำดับขั้นตอน ก่อนส่งต่อและถ่ายโอนความรู้ไปสู่ 'การสร้างสรรค์ชิ้นงานการเขียนโปรแกรมด้วยโปรแกรม Scratch' ตามเกณฑ์ที่กำหนดไว้ในข้อตกลง PA อย่างสมบูรณ์"""
    elements.append(make_callout(intro, title="ความเชื่อมโยงกับข้อตกลงในการพัฒนางาน (PA 1)"))

    four_cs_intro = """แผนการจัดการเรียนรู้ชุดนี้มุ่งเน้นการพัฒนา 'ทักษะแห่งศตวรรษที่ 21 (4 Cs of 21st Century Skills)' ให้แก่ผู้เรียนอย่างเป็นรูปธรรมผ่านกิจกรรม Active Learning ประกอบด้วย:
1. Critical Thinking (การคิดวิเคราะห์และแก้ปัญหา): ฝึกคิดอย่างมีตรรกะ วางแผนอัลกอริทึม วิเคราะห์เงื่อนไข และตรวจจับจุดผิดพลาด (Debugging)
2. Creativity (ความคิดสร้างสรรค์): ออกแบบเส้นทางให้สั้นกระชับ ลดทอนโค้ด และสร้างสรรค์โปรแกรม Scratch ภารกิจช่วยตัวละครหาทางออก
3. Collaboration (การทำงานร่วมกันเป็นทีม): กระบวนการ Pair Programming จับคู่ 4 คู่ ปฏิบัติตามบทบาท Driver & Navigator และสลับบทบาทช่วยเหลือกัน
4. Communication (การสื่อสารอย่างมีประสิทธิภาพ): การสั่งการด้วยวาจา การรับฟังคู่หู และการสะท้อนคิดถอดบทเรียน (AAR) ร่วมกันท้ายคาบ"""
    elements.append(make_callout(four_cs_intro, title="จุดเน้นการพัฒนาทักษะแห่งศตวรรษที่ 21 (4 Cs: Critical Thinking, Creativity, Collaboration, Communication)", bg="EFF6FF", bdr="2563EB"))

    t_overview = [
        ["แผนที่", "ชื่อแผนการจัดการเรียนรู้ (เนื้อหาเดิมตาม PA 1)", "สาระสำคัญ / ภารกิจหลักในเกมและใบงาน", "เวลา"],
        ["1", "ปฐมนิเทศกติกา ปูพื้นฐานอัลกอริทึม & ทดสอบก่อนเรียน", "ทำแบบทดสอบ Pre-test 20 ข้อ + กิจกรรม Unplugged แฟลชการ์ด", "1 ชม."],
        ["2", "ก้าวแรกสู่ทิศทางและอัลกอริทึมในตารางกริด", "เล่นด่าน 1-2 ในเกม CodeBot AR + ใบงานที่ 1 (แก้สับสนทิศทาง)", "1 ชม."],
        ["3", "ค้นหารูปแบบและพลังคำสั่งวนซ้ำอย่างง่าย (Loops)", "เล่นด่าน 3-4 + ใบงานที่ 2 (วิเคราะห์ลูปบันได 3 ขั้น ลดบล็อกโค้ด)", "1 ชม."],
        ["4", "การย้ำซ้ำทวนและการตัดสินใจแบบมีเงื่อนไข (If-Then)", "ย้ำซ้ำทวนลูป + เล่นด่าน 5-6 + ใบงานที่ 3 (กุญแจ & ประตูเลเซอร์)", "1 ชม."],
        ["5", "ยอดนักสืบตามล่าและแก้ไขจุดผิดพลาด (Debugging)", "เล่นด่าน 7-8 + ใบงานที่ 4 (ตรวจจับบั๊ก + วิเคราะห์สาเหตุ)", "1 ชม."],
        ["6", "การสร้างสรรค์ชิ้นงานด้วยโปรแกรม Scratch (Scratch Programming)", "นำอัลกอริทึมจากเกม AR สู่การต่อบล็อก Scratch: ภารกิจช่วยตัวละครหาทางออก", "1 ชม."],
        ["7", "การสะท้อนคิดถอดบทเรียน (AAR) & ทดสอบหลังเรียน", "กิจกรรมถอดบทเรียน AAR + ทำแบบทดสอบ Post-test 20 ข้อ", "1 ชม."],
        ["รวม", "ประเด็นท้าทายตามข้อตกลง PA 1 (ครบ 7 แผน)", "แผนการจัดการเรียนรู้ 7 แผน (สัปดาห์ละ 1 คาบ)", "7 ชม."]
    ]
    elements.append(make_table(t_overview[0], t_overview[1:], [1000, 3600, 4900, 1000], ["center", "left", "left", "center"], font_size=22))
    elements.append(make_p([], space_before=60, space_after=60))

    elements.append(heading_sec("บัญชีรายชื่อนักเรียนกลุ่มเป้าหมาย ชั้นประถมศึกษาปีที่ 5 (N = 8)"))
    elements.append(body_p("นักเรียนชั้นประถมศึกษาปีที่ 5 โรงเรียนบ้านโนนป่าหว้านเชียงฮาย ภาคเรียนที่ 1 ปีการศึกษา 2569 ซึ่งเป็นกลุ่มเป้าหมายในการพัฒนาตามข้อตกลง PA 1"))
    
    t_students_headers = ["ที่", "เลขประจำตัว", "เลขประจำตัวประชาชน", "ชื่อ - สกุล นักเรียน", "กลุ่มคู่หู (Pair Programming)"]
    t_students_rows = [
        ["1", "2040", "1399900568996", "เด็กชายภูฟ้า  แสงศรี", "คู่ที่ 1 (คู่กับเลขที่ 8)"],
        ["2", "2045", "1104301574244", "เด็กหญิงพิชญาภา  แสงศรี", "คู่ที่ 2 (คู่กับเลขที่ 5)"],
        ["3", "2048", "1399900557625", "เด็กหญิงสิริวิมล  สาวิสิทธิ์", "คู่ที่ 3 (คู่กับเลขที่ 7)"],
        ["4", "2047", "1399900558486", "เด็กหญิงสาวิตรี  สายสมคุณ", "คู่ที่ 4 (คู่กับเลขที่ 6)"],
        ["5", "2044", "1399900563943", "เด็กหญิงณัฐณิชา  นันทโพธิ์เดช", "คู่ที่ 2 (คู่กับเลขที่ 2)"],
        ["6", "2046", "1390501131251", "เด็กหญิงรฐา  สอนเต็ม", "คู่ที่ 4 (คู่กับเลขที่ 4)"],
        ["7", "2043", "1399000122592", "เด็กหญิงกัญญาพัชร  วาจาชื่น", "คู่ที่ 3 (คู่กับเลขที่ 3)"],
        ["8", "2177", "1399900561720", "เด็กหญิงกัญญารัตน์  บัวบง", "คู่ที่ 1 (คู่กับเลขที่ 1)"]
    ]
    elements.append(make_table(t_students_headers, t_students_rows, [800, 1500, 2400, 3100, 2700], ["center", "center", "center", "left", "center"], font_size=22))
    elements.append(make_p([], space_before=60, space_after=60))

    # =========================================================================
    # แผน 1
    # =========================================================================
    elements.append(make_page_break())
    elements.extend(get_clean_plan_header(1, "ปฐมนิเทศกติกา ปูพื้นฐานอัลกอริทึม และทดสอบก่อนเรียน (Pre-test)"))
    elements.append(heading_sec("1. มาตรฐานการเรียนรู้และตัวชี้วัด"))
    elements.append(body_p("ใช้เหตุผลเชิงตรรกะในการแก้ปัญหา การอธิบายการทำงาน การคาดการณ์ผลลัพธ์จากปัญหาอย่างง่าย", bold_prefix="• ตัวชี้วัด ว 4.2 ป.5/1: "))
    elements.append(heading_sec("2. สาระสำคัญ / ความคิดรวบยอด"))
    elements.append(body_p("อัลกอริทึม (Algorithm) คือ การวางแผนแก้ปัญหาอย่างเป็นลำดับขั้นตอนที่ชัดเจน และการทำงานแบบคู่หู (Pair Programming) ประกอบด้วยบทบาท Navigator (ผู้วางแผน) และ Driver (ผู้สั่งการ)"))
    elements.append(heading_sec("3. จุดประสงค์การเรียนรู้ (สู่ตัวชี้วัด)"))
    elements.append(body_p("อธิบายความหมายของอัลกอริทึมและบทบาทหน้าที่ของ Driver & Navigator ได้ถูกต้อง", bold_prefix="3.1 ด้านความรู้ (K): "))
    elements.append(body_p("วางแผนจัดเรียงแฟลชการ์ดคำสั่งจำลองบนโต๊ะได้อย่างเป็นขั้นตอนก่อนลงมือปฏิบัติ", bold_prefix="3.2 ด้านทักษะกระบวนการ (P): "))
    elements.append(body_p("มีวินัย เคารพกติกาการทำงานร่วมกับคู่หู และมีความซื่อสัตย์ในการทำแบบทดสอบก่อนเรียน", bold_prefix="3.3 ด้านคุณลักษณะอันพึงประสงค์ (A): "))
    elements.append(heading_sec("4. สาระการเรียนรู้"))
    elements.append(body_p("การแก้ปัญหาอย่างง่ายด้วยอัลกอริทึม, กติกา Pair Programming (Driver & Navigator), การประเมินความรู้พื้นฐานก่อนเรียน"))
    elements.append(heading_sec("5. สมรรถนะสำคัญ คุณลักษณะอันพึงประสงค์ และทักษะแห่งศตวรรษที่ 21 (4 Cs)"))
    elements.append(body_p("ความสามารถในการคิดเป็นขั้นตอน, ความสามารถในการแก้ปัญหา, ความสามารถในการสื่อสาร", bold_prefix="• สมรรถนะสำคัญ: "))
    elements.append(body_p("มีวินัย, ใฝ่เรียนรู้, มุ่งมั่นในการทำงานร่วมกับผู้อื่น", bold_prefix="• คุณลักษณะอันพึงประสงค์: "))
    elements.append(body_p("1) Critical Thinking: วิเคราะห์ความหมายอัลกอริทึม  2) Creativity: ออกแบบการจัดวางการ์ดคำสั่ง  3) Collaboration: บทบาทคู่หู Driver & Navigator ไม่แย่งกันทำ  4) Communication: การสื่อสารส่งต่อคำสั่งทีละก้าว", bold_prefix="• ทักษะแห่งศตวรรษที่ 21 (4 Cs): "))
    elements.append(heading_sec("6. จุดเน้นการจัดการเรียนรู้เชิงรุก (Active Learning Focus)"))
    t_roles_1 = [
        ["บทบาทที่ 1: ผู้นำทาง (NAVIGATOR)", "บทบาทที่ 2: ผู้สั่งการ (DRIVER)"],
        [
            "- ผู้ถือชุดแฟลชการ์ดสัญลักษณ์จริงบนโต๊ะ\n- ทำหน้าที่คิด วิเคราะห์ และเรียงลำดับขั้นตอน\n- กฎเหล็ก: วางแผนบนการ์ด ห้ามแตะหน้าจอคอมพิวเตอร์!",
            "- ผู้เตรียมความพร้อมหน้ากล้องเว็บแคม\n- รับฟังคำสั่งและทิศทางจาก Navigator ทีละก้าว\n- กฎเหล็ก: ป้อนคำสั่งตามที่คู่หูบอกเท่านั้น ไม่กดเองตามใจชอบ"
        ]
    ]
    elements.append(make_table(t_roles_1[0], t_roles_1[1:], [5250, 5250], ["left", "left"], font_size=22, header_bg="1E40AF"))
    elements.append(make_p([], space_before=40, space_after=40))
    elements.append(heading_sec("7. กิจกรรมการเรียนรู้ (เวลาประมาณ 50 - 60 นาที)"))
    elements.append(heading_sub("7.1 ขั้นนำเข้าสู่บทเรียน (Warm-up & Engagement) [5 - 10 นาที]"))
    elements.append(body_p("ครูกล่าวทักทายนักเรียนทั้ง 8 คน ชวนเล่นเกมสนุกๆ ชื่อ 'คำสั่งหุ่นยนต์มนุษย์' โดยขออาสาสมัคร 1 คน ปิดตา แล้วให้เพื่อนสั่งเดินไปหยิบแปลงลบกระดาน", bold_prefix="1. การกระตุ้นความสนใจ: "))
    elements.append(body_p("ครูตั้งคำถาม: 'ถ้านักเรียนสั่งว่า ให้เดินตรงไปเรื่อยๆ โดยไม่สั่งให้หยุดหรือเลี้ยว จะเกิดอะไรขึ้น?' (นักเรียนตอบ: เดินชนโต๊ะ)", bold_prefix="2. การตั้งคำถามกระตุ้นความคิด: "))
    elements.append(body_p("ครูอธิบายเชื่อมโยงว่า คอมพิวเตอร์ก็เหมือนคนที่ถูกปิดตา ถ้าเราไม่บอกขั้นตอนให้ชัดเจนทีละก้าว ซึ่งขั้นตอนคำสั่งนี้เรียกว่า 'อัลกอริทึม'", bold_prefix="3. การสร้างแรงจูงใจ: "))
    elements.append(heading_sub("7.2 ขั้นจัดกิจกรรมการเรียนรู้ / ปฏิบัติการ (Active Discovery) [30 - 35 นาที]"))
    elements.append(body_p("ครูแจกแบบทดสอบวัดผลสัมฤทธิ์ก่อนเรียน (Pre-test) 20 ข้อ ให้นักเรียนทำเดี่ยวเป็นรายบุคคล (20 นาที)", bold_prefix="1. การทดสอบก่อนเรียน: "))
    elements.append(body_p("ครูจัดนักเรียน 8 คน เป็น 4 คู่ (คละความถนัด) แจกป้ายคล้องคอ Navigator (สีฟ้า) และ Driver (สีส้ม)", bold_prefix="2. มอบหมายบทบาทคู่หู: "))
    elements.append(body_p("แจก 'ชุดแฟลชการ์ดสัญลักษณ์จริง 18 ใบ' ให้แต่ละคู่ทดลองหยิบการ์ดลูกศร ⬆️ ↩️ ↪️ มาเรียงบนโต๊ะตามโจทย์ 3 ขั้นตอน", bold_prefix="3. กิจกรรม Unplugged: "))
    elements.append(heading_sub("7.3 ขั้นสรุปและสะท้อนคิด (Reflection & AAR) [5 - 10 นาที]"))
    elements.append(body_p("ครูและนักเรียนร่วมกันทบทวนกฎเหล็กของ Driver และ Navigator", bold_prefix="1. ทบทวนกฎเหล็ก: "))
    elements.append(body_p("ครูเปิดตัวอย่างหน้าจอเกม CodeBot AR Adventure ให้นักเรียนดูตัวอย่างการใช้ท่าทางมือแตะบล็อกหน้ากล้อง สร้างความตื่นเต้นสู่วิชาในคาบหน้า", bold_prefix="2. แนะนำเกม AR: "))
    elements.append(heading_sec("8. สื่อ อุปกรณ์ และแหล่งการเรียนรู้"))
    elements.append(body_p("แบบทดสอบวัดผลสัมฤทธิ์ก่อนเรียน (Pre-test) 20 ข้อ", bullet=True))
    elements.append(body_p("ชุดแฟลชการ์ดสัญลักษณ์จริง (Printable AR Cards) 4 ชุด", bullet=True))
    elements.append(body_p("ป้ายบทบาทประจำตัว Navigator และ Driver 4 คู่", bullet=True))
    elements.append(heading_sec("9. การวัดและประเมินผลการเรียนรู้"))
    elements.append(get_plan_eval_table(
        "อธิบายความหมายของอัลกอริทึม และบทบาท Driver/Navigator ได้",
        "ทักษะการจัดเรียงแฟลชการ์ดคำสั่งบนโต๊ะอย่างเป็นขั้นตอน",
        "มีความซื่อสัตย์ในการทำข้อสอบ และปฏิบัติตามกฎเหล็กของคู่หู"
    ))
    elements.append(heading_sec("10. บันทึกผลหลังการจัดการเรียนรู้"))
    elements.append(get_plan_post_table(1, "นักเรียนทั้ง 8 คน ทำแบบทดสอบก่อนเรียนอย่างตั้งใจ เข้าใจความหมายของอัลกอริทึมผ่านกิจกรรมหุ่นยนต์มนุษย์ได้ชัดเจน", "นักเรียน 2 คน ยังอ่านโจทย์ข้อสอบค่อนข้างช้า ครูต้องช่วยอ่านคำชี้แจงให้ฟังเป็นรายบุคคล", "ในชั่วโมงถัดไป ครูจัดเตรียมแผนที่ตารางกริดในใบงานที่ 1 ช่วยนำทางเด็กกลุ่มที่อ่านช้า"))

    # =========================================================================
    # แผน 2
    # =========================================================================
    elements.append(make_page_break())
    elements.extend(get_clean_plan_header(2, "ก้าวแรกสู่ทิศทางและอัลกอริทึมในตารางกริด (ด่าน 1-2 ป.5)"))
    elements.append(heading_sec("1. มาตรฐานการเรียนรู้และตัวชี้วัด"))
    elements.append(body_p("ใช้เหตุผลเชิงตรรกะในการแก้ปัญหา การอธิบายการทำงาน การคาดการณ์ผลลัพธ์จากปัญหาอย่างง่าย", bold_prefix="• ตัวชี้วัด ว 4.2 ป.5/1: "))
    elements.append(body_p("ออกแบบและเขียนโปรแกรมที่มีการใช้เหตุผลเชิงตรรกะอย่างง่าย ตรวจหาข้อผิดพลาดและแก้ไข", bold_prefix="• ตัวชี้วัด ว 4.2 ป.5/2: "))
    elements.append(heading_sec("2. สาระสำคัญ / ความคิดรวบยอด"))
    elements.append(body_p("การเคลื่อนที่ในตารางกริดต้องเข้าใจความสัมพันธ์ของทิศทาง โดยคำสั่งหันซ้ายและหันขวาเป็นการหมุนตัวเปลี่ยนทิศทางอยู่กับที่ ยังไม่เคลื่อนที่ไปยังช่องใหม่ และต้องคำนึงถึงมุมมองของหุ่นยนต์เพื่อป้องกันการสับสนทิศทางซ้าย-ขวา"))
    elements.append(heading_sec("3. จุดประสงค์การเรียนรู้ (สู่ตัวชี้วัด)"))
    elements.append(body_p("อธิบายความแตกต่างระหว่างคำสั่งเดินหน้ากับการหมุนตัวเปลี่ยนทิศทางได้ถูกต้อง", bold_prefix="3.1 ด้านความรู้ (K): "))
    elements.append(body_p("ลากเส้นทางบนตารางกริดใบงานที่ 1 และใช้มือแตะคำสั่งหน้ากล้อง AR พาหุ่นยนต์ผ่านด่าน 1-2 ได้", bold_prefix="3.2 ด้านทักษะกระบวนการ (P): "))
    elements.append(body_p("มีความพยายามและไม่ยอมแพ้เมื่อหุ่นยนต์เดินชนหินอุกกาบาต", bold_prefix="3.3 ด้านคุณลักษณะอันพึงประสงค์ (A): "))
    elements.append(heading_sec("4. สาระการเรียนรู้"))
    elements.append(body_p("การเคลื่อนที่ในตารางกริด (Grid 5x5), ทิศทางซ้าย-ขวาตามมุมมองหุ่นยนต์, การใช้งานเกม CodeBot AR (ด่าน 1-2)"))
    elements.append(heading_sec("5. สมรรถนะสำคัญ คุณลักษณะอันพึงประสงค์ และทักษะแห่งศตวรรษที่ 21 (4 Cs)"))
    elements.append(body_p("ความสามารถในการคิดวิเคราะห์ทิศทาง, ความสามารถในการใช้เทคโนโลยีปฏิสัมพันธ์ AR", bold_prefix="• สมรรถนะสำคัญ: "))
    elements.append(body_p("มุ่งมั่นในการทำงาน, ซื่อสัตย์ในการบันทึกคะแนนดาว", bold_prefix="• คุณลักษณะอันพึงประสงค์: "))
    elements.append(body_p("1) Critical Thinking: วิเคราะห์ทิศทางและมุมมองหุ่นยนต์แก้สับสนซ้าย-ขวา  2) Creativity: ออกแบบเส้นทางหลบหินอวกาศ  3) Collaboration: ทำงานร่วมกันในใบงานที่ 1  4) Communication: การบอกทิศทางชัดเจน", bold_prefix="• ทักษะแห่งศตวรรษที่ 21 (4 Cs): "))
    elements.append(heading_sec("6. จุดเน้นการจัดการเรียนรู้เชิงรุก (Active Learning Focus)"))
    elements.append(body_p("Navigator ใช้ใบงานที่ 1 ลากเส้นทางด้วยดินสอและหมุนการ์ดลูกศรบนโต๊ะแก้ปัญหาสับสนทิศทาง ส่วน Driver ยืนหน้ากล้องเว็บแคม แตะบล็อก AR ตามที่คู่หูบอกทีละคำสั่ง"))
    elements.append(heading_sec("7. กิจกรรมการเรียนรู้ (เวลาประมาณ 50 - 60 นาที)"))
    elements.append(heading_sub("7.1 ขั้นนำเข้าสู่บทเรียน (Warm-up & Engagement) [5 - 10 นาที]"))
    elements.append(body_p("ครูให้นักเรียนยืนขึ้น สั่งยกมือขวา ก้าวเดินหน้า หมุนตัวไปทางซ้าย", bold_prefix="1. กิจกรรมทิศทาง: "))
    elements.append(body_p("ครูตั้งคำถาม: 'เมื่อเราหมุนตัวไปทางซ้าย ตัวเราเปลี่ยนช่องเดินหรือไม่?' (ไม่เปลี่ยน แค่เปลี่ยนทิศหน้ามอง) ครูย้ำว่าหุ่นยนต์ในเกมก็เช่นกัน", bold_prefix="2. เชื่อมโยงมโนทัศน์: "))
    elements.append(heading_sub("7.2 ขั้นจัดกิจกรรมการเรียนรู้ / ปฏิบัติการ (Active Challenge) [30 - 35 นาที]"))
    elements.append(body_p("เปิดเกม CodeBot AR Adventure ด่านที่ 1 (ก้าวแรกของโค้ดบอท)", bold_prefix="1. เริ่มด่านที่ 1: "))
    elements.append(body_p("Navigator กางใบงานที่ 1 วาดเส้นทางบนตารางกริด 5x5 ไปเก็บแบตเตอรี่ 🔋 แล้วบอก Driver แตะบล็อก [เดินหน้า] หน้ากล้อง AR", bold_prefix="2. ปฏิบัติการด่านที่ 1: "))
    elements.append(body_p("เข้าสู่ด่านที่ 2 มีหินอุกกาบาตขวางทาง นักเรียนนำแฟลชการ์ดบนโต๊ะมาหมุนทิศทางตามตัวหุ่นยนต์ ช่วยแก้ปัญหาการเลี้ยวผิดด้านได้สำเร็จ", bold_prefix="3. ปฏิบัติการด่านที่ 2 (Scaffolding): "))
    elements.append(heading_sub("7.3 ขั้นสรุปและสะท้อนคิด (Reflection & AAR) [5 - 10 นาที]"))
    elements.append(body_p("บันทึกดาวที่ได้รับลงในใบงานที่ 1 ครูและนักเรียนร่วมกันสรุปเทคนิคการจำทิศทางซ้าย-ขวา", bold_prefix="1. สรุปบทเรียน: "))
    elements.append(heading_sec("8. สื่อ อุปกรณ์ และแหล่งการเรียนรู้"))
    elements.append(body_p("เว็บเกม CodeBot AR Adventure (ด่าน 1 และ 2)", bullet=True))
    elements.append(body_p("ชุดใบงานที่ 1 (แผนที่ก้าวแรกและอัลกอริทึม)", bullet=True))
    elements.append(body_p("ชุดแฟลชการ์ดคำสั่งลูกศร", bullet=True))
    elements.append(heading_sec("9. การวัดและประเมินผลการเรียนรู้"))
    elements.append(get_plan_eval_table(
        "เข้าใจทิศทางในตารางกริด และบอกความหมายของการหันซ้าย-ขวาได้",
        "ทักษะการลากเส้นทางบนใบงานที่ 1 และแตะบล็อก AR ผ่านด่าน 1-2",
        "มีความพยายาม ไม่ท้อถอยเมื่อหุ่นยนต์เดินชนสิ่งกีดขวาง"
    ))
    elements.append(heading_sec("10. บันทึกผลหลังการจัดการเรียนรู้"))
    elements.append(get_plan_post_table(2, "นักเรียนทั้ง 4 คู่ ผ่านด่าน 1 และ 2 ได้ครบถ้วน การหมุนแฟลชการ์ดบนโต๊ะช่วยแก้ปัญหาสับสนทิศทางซ้าย-ขวาได้ 100%", "คู่ที่ 4 สับสนทิศทางในรอบแรกเล็กน้อย", "ครูแนะให้หมุนการ์ดลูกศรตามหน้าหุ่นยนต์ เด็กเข้าใจและทำผ่านได้ทันที"))

    # =========================================================================
    # แผน 3
    # =========================================================================
    elements.append(make_page_break())
    elements.extend(get_clean_plan_header(3, "ค้นหารูปแบบและพลังคำสั่งวนซ้ำอย่างง่าย (ด่าน 3-4 ป.5)"))
    elements.append(heading_sec("1. มาตรฐานการเรียนรู้และตัวชี้วัด"))
    elements.append(body_p("ใช้เหตุผลเชิงตรรกะในการแก้ปัญหา การอธิบายการทำงาน การคาดการณ์ผลลัพธ์จากปัญหาอย่างง่าย", bold_prefix="• ตัวชี้วัด ว 4.2 ป.5/1: "))
    elements.append(body_p("ออกแบบและเขียนโปรแกรมที่มีการใช้เหตุผลเชิงตรรกะอย่างง่าย ตรวจหาข้อผิดพลาดและแก้ไข", bold_prefix="• ตัวชี้วัด ว 4.2 ป.5/2: "))
    elements.append(heading_sec("2. สาระสำคัญ / ความคิดรวบยอด"))
    elements.append(body_p("การทำซ้ำ (Loop) เป็นโครงสร้างคำสั่งที่ช่วยให้การทำงานที่มีลักษณะเหมือนกันซ้ำๆ สามารถเขียนรวมเป็นบล็อกเดียวได้ ช่วยประหยัดจำนวนบล็อกคำสั่ง ทำให้โค้ดสั้น กระชับ เป็นระเบียบ และได้รับดาวโบนัสประสิทธิภาพ"))
    elements.append(heading_sec("3. จุดประสงค์การเรียนรู้ (สู่ตัวชี้วัด)"))
    elements.append(body_p("อธิบายประโยชน์ของการใช้บล็อกวนซ้ำ (Loop) ในการลดจำนวนคำสั่งได้", bold_prefix="3.1 ด้านความรู้ (K): "))
    elements.append(body_p("ระบุรูปแบบที่ซ้ำกัน และออกแบบการใช้บล็อกลูปผ่านด่านที่ 3-4 ในเกม CodeBot AR ได้", bold_prefix="3.2 ด้านทักษะกระบวนการ (P): "))
    elements.append(body_p("สลับบทบาทการทำงานกับคู่หูอย่างเต็มใจ และช่วยเหลือซึ่งกันและกัน", bold_prefix="3.3 ด้านคุณลักษณะอันพึงประสงค์ (A): "))
    elements.append(heading_sec("4. สาระการเรียนรู้"))
    elements.append(body_p("การหารูปแบบ (Pattern Recognition), บล็อกวนซ้ำอย่างง่าย [Loop 2 รอบ, 3 รอบ, 4 รอบ], การลดทอนคำสั่ง (Optimization)"))
    elements.append(heading_sec("5. สมรรถนะสำคัญ คุณลักษณะอันพึงประสงค์ และทักษะแห่งศตวรรษที่ 21 (4 Cs)"))
    elements.append(body_p("ความสามารถในการคิดหารูปแบบซ้ำ, ความสามารถในการแก้ปัญหาอย่างมีประสิทธิภาพ", bold_prefix="• สมรรถนะสำคัญ: "))
    elements.append(body_p("ใฝ่เรียนรู้, มีวินัยในการสลับบทบาทหน้าที่", bold_prefix="• คุณลักษณะอันพึงประสงค์: "))
    elements.append(body_p("1) Critical Thinking: ค้นหารูปแบบซ้ำซ้อน (Pattern)  2) Creativity: ประยุกต์ใช้ Loop เพื่อลดจำนวนบล็อกให้สั้นที่สุด  3) Collaboration: สลับบทบาทคู่หู 100%  4) Communication: อธิบายจำนวนรอบของลูป", bold_prefix="• ทักษะแห่งศตวรรษที่ 21 (4 Cs): "))
    elements.append(heading_sec("6. จุดเน้นการจัดการเรียนรู้เชิงรุก (Active Learning Focus)"))
    elements.append(body_p("สลับบทบาทคู่หู 100%! คนเดิมที่เป็น Driver สลับมาเป็น Navigator กางใบงานที่ 2 ส่วน Navigator เดิมลุกขึ้นเป็น Driver หน้ากล้อง AR เพื่อให้ทุกคนได้ฝึกทั้งการคิดวิเคราะห์ลูปและการปฏิบัติจริง"))
    elements.append(heading_sec("7. กิจกรรมการเรียนรู้ (เวลาประมาณ 50 - 60 นาที)"))
    elements.append(heading_sub("7.1 ขั้นนำเข้าสู่บทเรียน (Warm-up & Engagement) [5 - 10 นาที]"))
    elements.append(body_p("ครูเขียนคำสั่งบนกระดาน [เดินหน้า x5] ถามว่าถ้า 50 ก้าวจะทำอย่างไร ครูเปิดตัวการ์ด [🔁 วนซ้ำ (Loop)]", bold_prefix="1. การสร้างความท้าทาย: "))
    elements.append(heading_sub("7.2 ขั้นจัดกิจกรรมการเรียนรู้ / ปฏิบัติการ (Active Challenge) [30 - 35 นาที]"))
    elements.append(body_p("สลับป้ายคล้องคอ Driver ↔ Navigator", bold_prefix="1. สลับบทบาท: "))
    elements.append(body_p("ด่านที่ 3 (ทางเดินตรงยาว) ใช้การ์ด [🔁 วนซ้ำ 4 ครั้ง] ครอบ [เดินหน้า] แตะคำสั่ง AR ครั้งเดียวผ่านฉลุย", bold_prefix="2. ภารกิจด่านที่ 3: "))
    elements.append(body_p("ด่านที่ 4 (บันได 3 ขั้น) Navigator กางใบงานที่ 2 สังเกตขั้นบันได ออกแบบบล็อก [วนซ้ำ 3 รอบ] บรรจุคำสั่งก้าวขึ้นบันได แตะหน้ากล้อง AR ได้ 3 ดาวเต็ม", bold_prefix="3. ภารกิจด่านที่ 4: "))
    elements.append(heading_sub("7.3 ขั้นสรุปและสะท้อนคิด (Reflection & AAR) [5 - 10 นาที]"))
    elements.append(body_p("บันทึกเปรียบเทียบโค้ดเดิม vs โค้ดลูป ในใบงานที่ 2 ครูตรวจและลงคะแนน", bold_prefix="1. สรุปผลงาน: "))
    elements.append(heading_sec("8. สื่อ อุปกรณ์ และแหล่งการเรียนรู้"))
    elements.append(body_p("เว็บเกม CodeBot AR Adventure (ด่านที่ 3 และ 4)", bullet=True))
    elements.append(body_p("ชุดใบงานที่ 2 (ถอดรหัสลับพลังวนซ้ำ)", bullet=True))
    elements.append(body_p("แฟลชการ์ดลูป [🔁 x2, 🔁 x3, 🔁 x4]", bullet=True))
    elements.append(heading_sec("9. การวัดและประเมินผลการเรียนรู้"))
    elements.append(get_plan_eval_table(
        "ระบุคำสั่งที่ซ้ำกัน และอธิบายการทำงานของบล็อกลูปได้",
        "ออกแบบบล็อกลูปในใบงานที่ 2 และแตะสั่งการผ่านด่าน 3-4 ได้สำเร็จ",
        "สลับบทบาทหน้าที่อย่างเต็มใจ และร่วมมือกันวิเคราะห์โจทย์"
    ))
    elements.append(heading_sec("10. บันทึกผลหลังการจัดการเรียนรู้"))
    elements.append(get_plan_post_table(3, "นักเรียนตื่นเต้นมากที่เห็นลูปช่วยลดคำสั่งจาก 12 บล็อกเหลือบล็อกเดียว ทุกคู่คว้าดาวโบนัสความสั้นได้ครบ", "มีนักเรียน 1 คน ลืมใส่คำสั่งเลี้ยวลงในก้อนลูป ทำให้เดินทะลุกำแพง", "ครูแนะให้ตรวจเช็คการ์ดบนโต๊ะก่อนกดรัน นักเรียนเข้าใจและแก้ไขสำเร็จ"))

    # =========================================================================
    # แผน 4
    # =========================================================================
    elements.append(make_page_break())
    elements.extend(get_clean_plan_header(4, "การย้ำซ้ำทวนและการตัดสินใจแบบมีเงื่อนไข (ด่าน 5-6 ป.5)"))
    elements.append(heading_sec("1. มาตรฐานการเรียนรู้และตัวชี้วัด"))
    elements.append(body_p("ใช้เหตุผลเชิงตรรกะในการแก้ปัญหา การอธิบายการทำงาน การคาดการณ์ผลลัพธ์จากปัญหาอย่างง่าย", bold_prefix="• ตัวชี้วัด ว 4.2 ป.5/1: "))
    elements.append(body_p("ออกแบบและเขียนโปรแกรมที่มีการใช้เหตุผลเชิงตรรกะอย่างง่าย ตรวจหาข้อผิดพลาดและแก้ไข", bold_prefix="• ตัวชี้วัด ว 4.2 ป.5/2: "))
    elements.append(heading_sec("2. สาระสำคัญ / ความคิดรวบยอด"))
    elements.append(body_p("การย้ำซ้ำทวนมโนทัศน์เรื่องทิศทางและลูปช่วยสร้างความแม่นยำ และการเขียนโปรแกรมแบบมีเงื่อนไข (If-Then) เป็นการใช้เหตุผลเชิงตรรกะในการตัดสินใจตามสถานการณ์ เช่น ถ้ามีกุญแจคีย์การ์ดแล้ว ประตูเลเซอร์จึงจะเปิดออก"))
    elements.append(heading_sec("3. จุดประสงค์การเรียนรู้ (สู่ตัวชี้วัด)"))
    elements.append(body_p("เขียนประโยคเงื่อนไขตรรกะ 'ถ้า...แล้ว (If-Then)' ในการแก้ปัญหาอย่างง่ายได้", bold_prefix="3.1 ด้านความรู้ (K): "))
    elements.append(body_p("วางแผนแบ่งขั้นตอน 2 เฟส (เก็บกุญแจ ➔ ผ่านประตู) และป้อนคำสั่งผ่านด่าน 5-6 ได้สำเร็จ", bold_prefix="3.2 ด้านทักษะกระบวนการ (P): "))
    elements.append(body_p("มีความรอบคอบ ไม่ใจร้อนป้อนคำสั่งลัดขั้นตอนจนเกิดความผิดพลาด", bold_prefix="3.3 ด้านคุณลักษณะอันพึงประสงค์ (A): "))
    elements.append(heading_sec("4. สาระการเรียนรู้"))
    elements.append(body_p("การย้ำซ้ำทวนลูปและทิศทาง, ตรรกะเงื่อนไข ถ้า...แล้ว (If-Then), การแก้ปัญหาแบบจัดลำดับความสำคัญ"))
    elements.append(heading_sec("5. สมรรถนะสำคัญ คุณลักษณะอันพึงประสงค์ และทักษะแห่งศตวรรษที่ 21 (4 Cs)"))
    elements.append(body_p("ความสามารถในการใช้เหตุผลเชิงตรรกะ, ความสามารถในการตัดสินใจอย่างเป็นระบบ", bold_prefix="• สมรรถนะสำคัญ: "))
    elements.append(body_p("มีความรอบคอบ, มีความรับผิดชอบต่อหน้าที่", bold_prefix="• คุณลักษณะอันพึงประสงค์: "))
    elements.append(body_p("1) Critical Thinking: การตัดสินใจเชิงตรรกะแบบมีเงื่อนไข If-Then  2) Creativity: วางแผนแก้ปัญหา 2 เฟส  3) Collaboration: ร่วมมือช่วยกันสังเกตกุญแจและประตู  4) Communication: ถ่ายทอดประโยคเงื่อนไข", bold_prefix="• ทักษะแห่งศตวรรษที่ 21 (4 Cs): "))
    elements.append(heading_sec("6. จุดเน้นการจัดการเรียนรู้เชิงรุก (Active Learning Focus)"))
    elements.append(body_p("ชั่วโมงนี้ทำหน้าที่เป็น 'สะพานเชื่อมย้ำซ้ำทวน' ให้เวลานักเรียนทบทวนโจทย์ลูป 15 นาที เพื่อช่วยเด็กที่เรียนช้าให้ตามเพื่อนทัน ก่อนจะก้าวสู่เรื่องตรรกะเงื่อนไข If-Then"))
    elements.append(heading_sec("7. กิจกรรมการเรียนรู้ (เวลาประมาณ 50 - 60 นาที)"))
    elements.append(heading_sub("7.1 ขั้นนำเข้าสู่บทเรียน & ย้ำซ้ำทวน (Review & Warm-up) [5 - 10 นาที]"))
    elements.append(body_p("ครูฉายภาพโจทย์ทบทวนลูปบนกระดาน ให้นักเรียนทั้ง 4 คู่ แข่งกันยกแฟลชการ์ดลูปตอบคำถาม ช่วยดึงความมั่นใจของเด็กทุกคนกลับมา", bold_prefix="1. กิจกรรมย้ำซ้ำทวน 15 นาที: "))
    elements.append(body_p("ครูตั้งสถานการณ์ปัญหาใหม่: 'ถ้าประตูกลล็อกอยู่ เราจะสั่งให้หุ่นยนต์พุ่งชนเลยได้ไหม? ต้องทำอะไรก่อน?' (ต้องไปเก็บกุญแจก่อน) ครูเชื่อมโยงสู่เรื่องเงื่อนไข ถ้า...แล้ว", bold_prefix="2. การตั้งคำถามเปิดประเด็น: "))
    elements.append(heading_sub("7.2 ขั้นจัดกิจกรรมการเรียนรู้ / ปฏิบัติการ (Active Challenge) [30 - 35 นาที]"))
    elements.append(body_p("นักเรียนเปิดด่านที่ 5-6 สังเกตกุญแจ 🗝️ และประตูเลเซอร์ ⚡ ขวางทางยานอวกาศ", bold_prefix="1. สังเกตด่านเงื่อนไข: "))
    elements.append(body_p("Navigator กาง 'ใบงานที่ 3' เขียนประโยคเงื่อนไข: 'ถ้า (IF) เก็บกุญแจได้แล้ว ➔ แล้ว (THEN) ประตูเลเซอร์จะเปิดออก' วางแผนแบ่ง 2 เฟส (เก็บกุญแจก่อน ➔ ค่อยเข้ายาน)", bold_prefix="2. บันทึกตรรกะลงในใบงานที่ 3: "))
    elements.append(body_p("Driver ยืนแตะบล็อกคำสั่ง AR หน้ากล้องตามแผน 2 เฟส สังเกตประตูเลเซอร์ที่เปิดออกเมื่อมีกุญแจ ผ่านด่านฉลุย", bold_prefix="3. ปฏิบัติการคำสั่ง AR: "))
    elements.append(heading_sub("7.3 ขั้นสรุปและสะท้อนคิด (Reflection & AAR) [5 - 10 นาที]"))
    elements.append(body_p("ครูชวนคุยเรื่องเงื่อนไขในชีวิตจริง (ถ้าฝนตก ➔ กางร่ม) นักเรียนบันทึกผลดาวในใบงานที่ 3 ครูตรวจประเมินผล", bold_prefix="1. สรุปบทเรียน: "))
    elements.append(heading_sec("8. สื่อ อุปกรณ์ และแหล่งการเรียนรู้"))
    elements.append(body_p("เว็บเกม CodeBot AR Adventure (ด่านที่ 5 และ 6)", bullet=True))
    elements.append(body_p("ชุดใบงานที่ 3 (เงื่อนไขกุญแจและประตูเลเซอร์)", bullet=True))
    elements.append(body_p("แฟลชการ์ดกุญแจ 🗝️ และการ์ดเงื่อนไข [IF-THEN]", bullet=True))
    elements.append(heading_sec("9. การวัดและประเมินผลการเรียนรู้"))
    elements.append(get_plan_eval_table(
        "เขียนประโยคเงื่อนไข ถ้า...แล้ว และอธิบายการตัดสินใจได้ถูกต้อง",
        "วางแผนแก้ปัญหาแบบ 2 เฟส และแตะคำสั่งผ่านด่าน 5-6 ได้สำเร็จ",
        "มีความรอบคอบ และรับฟังคำแนะนำของคู่หู"
    ))
    elements.append(heading_sec("10. บันทึกผลหลังการจัดการเรียนรู้"))
    elements.append(get_plan_post_table(4, "การมีย้ำซ้ำทวน 15 นาทีแรก ช่วยให้เด็กกลุ่มช้าเข้าใจเรื่องลูปได้อย่างมั่นใจ ทำใบงานที่ 3 เรื่องเงื่อนไขได้คะแนนสูงทุกคน", "มี 1 คู่ ใจร้อน สั่งเดินไปที่ประตูก่อนที่จะไปเก็บกุญแจ ทำให้หุ่นยนต์เดินชนประตูเลเซอร์", "ครูชี้ให้ดูประโยคเงื่อนไขในใบงานที่ 3 ว่าต้องเก็บกุญแจก่อน นักเรียนจึงปรับแผนและผ่านด่านได้สำเร็จ"))

    # =========================================================================
    # แผน 5
    # =========================================================================
    elements.append(make_page_break())
    elements.extend(get_clean_plan_header(5, "ยอดนักสืบตามล่าและแก้ไขจุดผิดพลาด (ด่าน 7-8 ป.5)"))
    elements.append(heading_sec("1. มาตรฐานการเรียนรู้และตัวชี้วัด"))
    elements.append(body_p("ออกแบบและเขียนโปรแกรมที่มีการใช้เหตุผลเชิงตรรกะอย่างง่าย ตรวจหาข้อผิดพลาดและแก้ไข", bold_prefix="• ตัวชี้วัด ว 4.2 ป.5/2: "))
    elements.append(heading_sec("2. สาระสำคัญ / ความคิดรวบยอด"))
    elements.append(body_p("ข้อผิดพลาดของโปรแกรมเรียกว่า 'บั๊ก (Bug)' และการตรวจหาข้อผิดพลาดเรียกว่า 'ดีบัก (Debugging)' ซึ่งทำได้โดยการตรวจสอบคำสั่งทีละบรรทัด (Step-by-step) เพื่อหาจุดที่ผิดแล้วแก้ไขเฉพาะจุดนั้น โดยไม่ต้องลบคำสั่งทิ้งทั้งหมด"))
    elements.append(heading_sec("3. จุดประสงค์การเรียนรู้ (สู่ตัวชี้วัด)"))
    elements.append(body_p("ระบุตำแหน่งคำสั่งที่ผิดพลาด (Bug) และบอกสาเหตุที่ทำให้หุ่นยนต์เดินชนหินได้", bold_prefix="3.1 ด้านความรู้ (K): "))
    elements.append(body_p("ดำเนินการแก้ไขคำสั่งที่เป็นบั๊กในใบงานที่ 4 และในเกม CodeBot AR ได้สำเร็จ", bold_prefix="3.2 ด้านทักษะกระบวนการ (P): "))
    elements.append(body_p("มีทัศนคติที่ดีต่อความผิดพลาด (Growth Mindset) และสนุกกับการแข่งขันเชิงบวก", bold_prefix="3.3 ด้านคุณลักษณะอันพึงประสงค์ (A): "))
    elements.append(heading_sec("4. สาระการเรียนรู้"))
    elements.append(body_p("การตรวจหาข้อผิดพลาด (Debugging), การไล่โค้ดทีละก้าว (Tracing), การตรวจแก้บล็อกคำสั่ง"))
    elements.append(heading_sec("5. สมรรถนะสำคัญ คุณลักษณะอันพึงประสงค์ และทักษะแห่งศตวรรษที่ 21 (4 Cs)"))
    elements.append(body_p("ความสามารถในการแก้ปัญหาอย่างมีวิจารณญาณ, ความสามารถในการทำงานร่วมกัน", bold_prefix="• สมรรถนะสำคัญ: "))
    elements.append(body_p("มุ่งมั่นในการทำงาน, มีน้ำใจนักกีฬาในการแข่งขัน", bold_prefix="• คุณลักษณะอันพึงประสงค์: "))
    elements.append(body_p("1) Critical Thinking: สืบหาและวิเคราะห์ตำแหน่งบั๊ก (Bug)  2) Creativity: ปรับแก้คำสั่งเฉพาะจุดโดยไม่ต้องลบทั้งหมด  3) Collaboration: แท็กทีมเป็นยอดนักสืบ  4) Communication: อภิปรายสาเหตุของความผิดพลาด", bold_prefix="• ทักษะแห่งศตวรรษที่ 21 (4 Cs): "))
    elements.append(heading_sec("6. จุดเน้นการจัดการเรียนรู้เชิงรุก (Active Learning Focus)"))
    elements.append(body_p("เปลี่ยนความผิดพลาดให้เป็นเกมสืบสวน! คู่หูทำหน้าที่เป็น 'ยอดนักสืบ' ร่วมกันตรวจเช็คโค้ดเพื่อหาจุดบั๊ก"))
    elements.append(heading_sec("7. กิจกรรมการเรียนรู้ (เวลาประมาณ 50 - 60 นาที)"))
    elements.append(heading_sub("7.1 ขั้นนำเข้าสู่บทเรียน (Warm-up & Engagement) [5 - 10 นาที]"))
    elements.append(body_p("ครูจำลองการเดินตามคำสั่งบนกระดาน แล้วจงใจเดินไปชนถังขยะในห้องเรียน ถามว่าต้องลบคำสั่งทั้งหมดหรือแก้แค่คำสั่งที่ผิด ครูสรุปว่านี่คือทักษะยอดนักสืบแก้บั๊ก", bold_prefix="1. สถานการณ์จำลอง: "))
    elements.append(heading_sub("7.2 ขั้นจัดกิจกรรมการเรียนรู้ / ปฏิบัติการ (Active Challenge) [30 - 35 นาที]"))
    elements.append(body_p("นักเรียนเปิดด่านที่ 7-8 ซึ่งมีโค้ดที่ผิดพลาดแฝงไว้ Navigator เปิดใบงานที่ 4 ดูตารางตรวจจับบั๊ก ไล่เช็คทีละบรรทัด", bold_prefix="1. ภารกิจล่าบั๊ก (ด่าน 7-8): "))
    elements.append(body_p("เมื่อพบจุดผิด Driver ลบบล็อกที่เป็นบั๊กออก แล้วแตะบล็อกคำสั่งที่ถูกต้องเข้าไปแทน แล้วกดรันเพื่อตรวจเช็คผลลัพธ์ ผ่านฉลุย", bold_prefix="2. ลงมือแก้บั๊ก: "))
    elements.append(heading_sub("7.3 ขั้นสรุปและสะท้อนคิด (Reflection & AAR) [5 - 10 นาที]"))
    elements.append(body_p("นักเรียนบันทึกสรุปโค้ดที่แก้ไขลงในใบงานที่ 4 และครูตรวจให้คะแนน", bold_prefix="1. บันทึกผลงาน: "))
    elements.append(heading_sec("8. สื่อ อุปกรณ์ และแหล่งการเรียนรู้"))
    elements.append(body_p("เว็บเกม CodeBot AR Adventure (ด่านที่ 7 และ 8)", bullet=True))
    elements.append(body_p("ชุดใบงานที่ 4 (ยอดนักสืบตามล่าและแก้ไขจุดผิดพลาด)", bullet=True))
    elements.append(heading_sec("9. การวัดและประเมินผลการเรียนรู้"))
    elements.append(get_plan_eval_table(
        "ระบุตำแหน่งคำสั่งที่ผิดพลาดและอธิบายวิธีแก้ไขได้ถูกต้อง",
        "ตรวจแก้บั๊กในใบงานที่ 4 และในเกม AR จนหุ่นยนต์เข้าเป้าหมายได้",
        "มี Growth Mindset ไม่กลัวความผิดพลาด และสนุกกับการแก้ปัญหา"
    ))
    elements.append(heading_sec("10. บันทึกผลหลังการจัดการเรียนรู้"))
    elements.append(get_plan_post_table(5, "นักเรียนชอบกิจกรรมล่าบั๊กมาก เพราะรู้สึกเหมือนได้เป็นนักสืบ ทุกคู่สามารถแก้บั๊กและผ่านด่านได้ครบถ้วน", "นักเรียนบางคู่ใจร้อนอยากกดรันทันทีโดยไม่ตรวจทีละบรรทัด", "ครูเตือนสติว่าความแม่นยำสำคัญกว่าความเร็ว นักเรียนจึงใจเย็นลงและทำคะแนนได้ดีขึ้น"))

    # =========================================================================
    # แผน 6 (ภารกิจโค้ดดิ้งขั้นสูงและการประลองด่านอวกาศ สู่ Scratch)
    # =========================================================================
    elements.append(make_page_break())
    elements.extend(get_clean_plan_header(6, "ภารกิจโค้ดดิ้งขั้นสูงและการผจญภัยด่านอวกาศ สู่การสร้างสรรค์ Scratch"))
    elements.append(heading_sec("1. มาตรฐานการเรียนรู้และตัวชี้วัด"))
    elements.append(body_p("ใช้เหตุผลเชิงตรรกะในการแก้ปัญหา การอธิบายการทำงาน การคาดการณ์ผลลัพธ์จากปัญหาอย่างง่าย", bold_prefix="• ตัวชี้วัด ว 4.2 ป.5/1: "))
    elements.append(body_p("ออกแบบและเขียนโปรแกรมที่มีการใช้เหตุผลเชิงตรรกะอย่างง่าย ตรวจหาข้อผิดพลาดและแก้ไข", bold_prefix="• ตัวชี้วัด ว 4.2 ป.5/2: "))
    elements.append(heading_sec("2. สาระสำคัญ / ความคิดรวบยอด"))
    elements.append(body_p("การบูรณาการทักษะการคิดเชิงคำนวณขั้นสูง โดยนำโครงสร้างคำสั่งแบบลำดับขั้นตอน การวนซ้ำ (Loops), การตัดสินใจแบบมีเงื่อนไข (If-Then), และการตรวจหาจุดผิดพลาด (Debugging) มาประยุกต์ใช้ในการแก้ปัญหาภารกิจด่านอวกาศที่มีความซับซ้อนในเกม CodeBot AR เพื่อพิชิตเหรียญ 3 ดาวอย่างมีประสิทธิภาพ และถ่ายโอนสู่การเขียนโปรแกรม Scratch ภารกิจช่วยตัวละครหาทางออก"))
    elements.append(heading_sec("3. จุดประสงค์การเรียนรู้ (สู่ตัวชี้วัด)"))
    elements.append(body_p("วิเคราะห์และเลือกใช้โครงสร้างคำสั่งวนซ้ำและเงื่อนไขในการแก้ปัญหาภารกิจที่ซับซ้อนได้อย่างเหมาะสม", bold_prefix="3.1 ด้านความรู้ (K): "))
    elements.append(body_p("ออกแบบอัลกอริทึม จัดลำดับแฟลชการ์ดคำสั่ง และปฏิบัติการหน้ากล้อง AR พิชิตด่านอวกาศสำเร็จตามเป้าหมาย", bold_prefix="3.2 ด้านทักษะกระบวนการ (P): "))
    elements.append(body_p("มีความมุ่งมั่นในการแก้ปัญหา มีความรับผิดชอบ และร่วมมือปฏิบัติงานกับคู่หูอย่างสร้างสรรค์", bold_prefix="3.3 ด้านคุณลักษณะอันพึงประสงค์ (A): "))
    elements.append(heading_sec("4. สาระการเรียนรู้"))
    elements.append(body_p("การบูรณาการอัลกอริทึมขั้นสูง, การผสมผสาน Loop และ Condition ในภารกิจเดียวกัน, การแข่งขันล่าดาว 3 ดวง และการเขียนโปรแกรมด้วย Scratch เบื้องต้น"))
    elements.append(heading_sec("5. สมรรถนะสำคัญ คุณลักษณะอันพึงประสงค์ และทักษะแห่งศตวรรษที่ 21 (4 Cs)"))
    elements.append(body_p("ความสามารถในการคิดแก้ปัญหา, ความสามารถในการใช้เทคโนโลยี", bold_prefix="• สมรรถนะสำคัญ: "))
    elements.append(body_p("มุ่งมั่นในการทำงาน, ซื่อสัตย์สุจริต, มีวินัย", bold_prefix="• คุณลักษณะอันพึงประสงค์: "))
    elements.append(body_p("1) Critical Thinking: บูรณาการ Loop และ Condition ในด่านอวกาศ  2) Creativity: การสร้างสรรค์ชิ้นงาน Scratch ภารกิจช่วยตัวละครหาทางออก  3) Collaboration: ทีมเวิร์กในการพิชิต 3 ดาว  4) Communication: การนำเสนอและสื่อสารโค้ด", bold_prefix="• ทักษะแห่งศตวรรษที่ 21 (4 Cs): "))
    elements.append(heading_sec("6. จุดเน้นการจัดการเรียนรู้เชิงรุก (Active Learning Focus)"))
    elements.append(body_p("เปิดโอกาสให้นักเรียน 4 คู่ ท้าทายความสามารถตนเองด้วยการวางแผนเส้นทางที่ซับซ้อนที่สุด Navigator ออกแบบพิมพ์เขียวบนกระดาษ Driver สื่อสารและทดลองสั่งการหน้ากล้อง AR สลับบทบาทอย่างคล่องแคล่ว"))
    elements.append(heading_sec("7. กิจกรรมการเรียนรู้ (เวลาประมาณ 50 - 60 นาที)"))
    elements.append(heading_sub("7.1 ขั้นนำเข้าสู่บทเรียน (Warm-up & Engagement) [5 - 10 นาที]"))
    elements.append(body_p("ครูเปิดฉากด่านอวกาศ (Space Odyssey Mission) ขึ้นจอโปรเจกเตอร์ ชี้ให้เห็นอุปสรรค: มีทั้งบันไดเลเซอร์ ประตูกั้นพลังงาน และคริสตัลอวกาศที่ต้องเก็บให้ครบ", bold_prefix="1. ประกาศภารกิจท้าทายสูงสุด: "))
    elements.append(body_p("ครูถามนักเรียน: 'หากในด่านนี้มีทั้งทางเดินบันไดและประตูเลเซอร์ เราต้องใช้การ์ดพิเศษใบไหนช่วยหุ่นยนต์บ้าง?' นักเรียนตอบพร้อมกันว่า 'การ์ด Loop วนซ้ำ' และ 'การ์ดเงื่อนไขกุญแจ'", bold_prefix="2. ระดมความคิดกลยุทธ์: "))
    elements.append(heading_sub("7.2 ขั้นจัดกิจกรรมการเรียนรู้ / ปฏิบัติการ (Active Challenge) [30 - 35 นาที]"))
    elements.append(body_p("Navigator และ Driver ร่วมกันศึกษาตารางกริดบนกระดาษภารกิจ นำการ์ดคำสั่งมาเรียงจำลองบนโต๊ะเพื่อลดจำนวนบรรทัดคำสั่งให้สั้นที่สุด", bold_prefix="1. วางแผนพิมพ์เขียวอัลกอริทึม (10 นาที): "))
    elements.append(body_p("นักเรียนทั้ง 4 คู่ เข้าสู่เว็บเกม CodeBot AR Adventure ด่านที่ 9-10 Driver ชูการ์ดคำสั่งหน้ากล้อง AR สั่งการหุ่นยนต์เดินตามแผน Navigator คอยจับตาดูและเช็คผลลัพธ์ทีละก้าว", bold_prefix="2. ปฏิบัติการล่าดาวด่านอวกาศหน้ากล้อง AR (15 นาที): "))
    elements.append(body_p("คู่ที่พบว่าหุ่นยนต์ชนประตูก่อนถึงกุญแจ ทำการสลับบทบาท (Swap Role) Navigator กลายมาเป็น Driver ช่วยกันวิเคราะห์สาเหตุและขยับการ์ดคำสั่งจนสามารถปลดล็อกและเก็บดาวครบ 3 ดวงสำเร็จ (10 นาที)", bold_prefix="3. สลับบทบาทและดีบั๊กขั้นสูง (10 นาที): "))
    elements.append(heading_sub("7.3 ขั้นสรุปและสะท้อนคิด (Reflection & AAR) [5 - 10 นาที]"))
    elements.append(body_p("ครูฉาย Leaderboard คะแนนดาวของทั้ง 4 คู่ พบว่าทุกคู่สามารถผ่านด่านอวกาศระดับ 3 ดาวได้สำเร็จ ทุกคนปรบมือให้กำลังใจซึ่งกันและกัน", bold_prefix="1. สรุปอันดับความสำเร็จ 3 ดาว: "))
    elements.append(body_p("นักเรียนร่วมกันสะท้อนคิดว่า: 'การใช้การ์ดคำสั่งบนโต๊ะช่วยให้มองเห็นภาพรวมก่อน และการช่วยกันสองคนทำให้ไม่เกิดข้อผิดพลาด'", bold_prefix="2. ตกผลึกการเรียนรู้: "))
    elements.append(heading_sec("8. สื่อ อุปกรณ์ และแหล่งการเรียนรู้"))
    elements.append(body_p("เว็บเกม CodeBot AR Adventure (ด่านที่ 9 และ 10: ภารกิจด่านอวกาศ)", bullet=True))
    elements.append(body_p("ชุดแฟลชการ์ดคำสั่งสัญลักษณ์จริง 18 ชิ้น พร้อมป้ายห้อยคอ Navigator & Driver", bullet=True))
    elements.append(body_p("ใบงานภารกิจที่ 4: ยอดนักสืบแก้บั๊กและผจญภัยด่านอวกาศ", bullet=True))
    elements.append(heading_sec("9. การวัดและประเมินผลการเรียนรู้"))
    elements.append(get_plan_eval_table(
        "วิเคราะห์และเลือกใช้โครงสร้างคำสั่งวนซ้ำและเงื่อนไขในด่านอวกาศได้ถูกต้อง",
        "จัดเรียงแฟลชการ์ดและควบคุมหุ่นยนต์หน้ากล้อง AR ผ่านด่านอวกาศได้ 3 ดาว",
        "มีความมุ่งมั่น มีวินัย และร่วมมือทำงานกับคู่หูอย่างราบรื่น"
    ))
    elements.append(heading_sec("10. บันทึกผลหลังการจัดการเรียนรู้"))
    elements.append(get_plan_post_table(6, "นักเรียนทั้ง 4 คู่ มีความตื่นเต้นและกระตือรือร้นสูงมาก สามารถบูรณาการความรู้เรื่องทิศทาง ลูป และเงื่อนไข นำมาใช้แก้ปัญหาในด่านอวกาศได้อย่างเป็นระบบ ทุกคู่ได้รับดาวครบ 3 ดวง 100%", "ในตอนแรกมีบางคู่เดินชนกำแพงเนื่องจากคำนวณจำนวนรอบใน Loop ผิดไป 1 ก้าว", "นักเรียนสลับบทบาทและช่วยกันนับตารางกริดบนการ์ดใหม่ ทำให้แก้จุดผิดพลาดได้สำเร็จด้วยตนเอง"))

    # =========================================================================
    # แผน 7
    # =========================================================================
    elements.append(make_page_break())
    elements.extend(get_clean_plan_header(7, "การสะท้อนคิดถอดบทเรียน (AAR) และทดสอบหลังเรียน (Post-test)"))
    elements.append(heading_sec("1. มาตรฐานการเรียนรู้และตัวชี้วัด"))
    elements.append(body_p("ใช้เหตุผลเชิงตรรกะในการแก้ปัญหา การอธิบายการทำงาน การคาดการณ์ผลลัพธ์จากปัญหาอย่างง่าย", bold_prefix="• ตัวชี้วัด ว 4.2 ป.5/1: "))
    elements.append(body_p("ออกแบบและเขียนโปรแกรมที่มีการใช้เหตุผลเชิงตรรกะอย่างง่าย ตรวจหาข้อผิดพลาดและแก้ไข", bold_prefix="• ตัวชี้วัด ว 4.2 ป.5/2: "))
    elements.append(heading_sec("2. สาระสำคัญ / ความคิดรวบยอด"))
    elements.append(body_p("การสะท้อนคิดหลังการปฏิบัติ (After Action Review: AAR) ช่วยให้ผู้เรียนตกผลึกองค์ความรู้และเชื่อมโยงไปใช้ในชีวิตจริง และการทดสอบวัดผลสัมฤทธิ์หลังเรียนช่วยยืนยันระดับพัฒนาการทางสติปัญญาเป็นรายบุคคลอย่างเป็นรูปธรรม"))
    elements.append(heading_sec("3. จุดประสงค์การเรียนรู้ (สู่ตัวชี้วัด)"))
    elements.append(body_p("สรุปองค์ความรู้เรื่องอัลกอริทึม การวนซ้ำ เงื่อนไข และการแก้บั๊กได้อย่างครบถ้วน", bold_prefix="3.1 ด้านความรู้ (K): "))
    elements.append(body_p("ทำแบบทดสอบวัดผลสัมฤทธิ์หลังเรียน (Post-test) ผ่านเกณฑ์ร้อยละ 75 ขึ้นไปเป็นรายบุคคล", bold_prefix="3.2 ด้านทักษะกระบวนการ (P): "))
    elements.append(body_p("มีความภาคภูมิใจในผลงานของตนเองและคู่หู มีเจตคติที่ดีต่อวิชาวิทยาการคำนวณ", bold_prefix="3.3 ด้านคุณลักษณะอันพึงประสงค์ (A): "))
    elements.append(heading_sec("4. สาระการเรียนรู้"))
    elements.append(body_p("การถอดบทเรียน AAR, การทดสอบหลังเรียน (Post-test 20 ข้อ), การประเมินความพึงพอใจ"))
    elements.append(heading_sec("5. สมรรถนะสำคัญ คุณลักษณะอันพึงประสงค์ และทักษะแห่งศตวรรษที่ 21 (4 Cs)"))
    elements.append(body_p("ความสามารถในการสื่อสารและสะท้อนความคิด, ความสามารถในการแก้ปัญหา", bold_prefix="• สมรรถนะสำคัญ: "))
    elements.append(body_p("มีความซื่อสัตย์ในการสอบ, มีความภาคภูมิใจในตนเอง", bold_prefix="• คุณลักษณะอันพึงประสงค์: "))
    elements.append(body_p("1) Critical Thinking: สังเคราะห์องค์ความรู้และทำข้อสอบเดี่ยว  2) Creativity: ถ่ายโอนวิธีคิดเชิงคำนวณสู่วิชาอื่น  3) Collaboration: การยอมรับและชื่นชมความสำเร็จของคู่หู  4) Communication: การสะท้อนคิด After Action Review (AAR)", bold_prefix="• ทักษะแห่งศตวรรษที่ 21 (4 Cs): "))
    elements.append(heading_sec("6. จุดเน้นการจัดการเรียนรู้เชิงรุก (Active Learning Focus)"))
    elements.append(body_p("การวัดความรู้เดี่ยว 100%! หลังจากทำงานคู่มาตลอด 6 ชั่วโมง ชั่วโมงนี้นักเรียนทุกคนจะนั่งทำข้อสอบ Post-test เดี่ยว เพื่อพิสูจน์ว่าเกิดองค์ความรู้ในตนเองจริง ไม่ได้นั่งพึ่งพาเพื่อน"))
    elements.append(heading_sec("7. กิจกรรมการเรียนรู้ (เวลาประมาณ 50 - 60 นาที)"))
    elements.append(heading_sub("7.1 ขั้นนำเข้าสู่บทเรียน & ถอดบทเรียน AAR [5 - 10 นาที]"))
    elements.append(body_p("ครูฉายภาพประมวลกิจกรรมตลอด 6 คาบที่ผ่านมา ทั้งภาพการจัดแฟลชการ์ดบนโต๊ะ การแตะคำสั่งหน้ากล้อง AR และการต่อบล็อกในโปรแกรม Scratch และการสั่งการผ่านกล้อง AR ให้นักเรียนดู", bold_prefix="1. ประมวลภาพความทรงจำ: "))
    elements.append(body_p("ครูชวนถอดบทเรียน 3 คำถาม: 1) สิ่งที่คู่เราทำได้ดีที่สุดคืออะไร? 2) ปัญหาที่ยากที่สุดคืออะไรและเราแก้ได้อย่างไร? 3) เราจะนำวิธีคิดทีละก้าวไปใช้กับวิชาอื่นอย่างไร?", bold_prefix="2. กิจกรรม AAR: "))
    elements.append(heading_sub("7.2 ขั้นวัดและประเมินผลสัมฤทธิ์เดี่ยว [30 - 35 นาที]"))
    elements.append(body_p("ครูแจกแบบทดสอบวัดผลสัมฤทธิ์หลังเรียน (Post-test) ฉบับเดิม 20 ข้อ ให้นักเรียนนั่งทำแบบเดี่ยว (20 นาที)", bold_prefix="1. การสอบหลังเรียน: "))
    elements.append(body_p("นักเรียนทำแบบประเมินความพึงพอใจต่อการจัดกิจกรรมการเรียนรู้และสื่อนวัตกรรมเกม AR (10 นาที)", bold_prefix="2. ทำแบบประเมินความพึงพอใจ: "))
    elements.append(heading_sub("7.3 ขั้นสรุปและมอบรางวัลความสำเร็จ [5 - 10 นาที]"))
    elements.append(body_p("ครูตรวจคะแนนและแจ้งผลคะแนนพัฒนาการรายบุคคลให้นักเรียนทราบ (ทุกคนคะแนนเพิ่มขึ้นอย่างก้าวกระโดด)", bold_prefix="1. แจ้งผลพัฒนาการ: "))
    elements.append(body_p("ครูมอบ 'เกียรติบัตรยอดนักสืบโค้ดดิ้ง ป.5' ให้แก่นักเรียนทั้ง 8 คน ถ่ายภาพร่วมกันเป็นที่ระลึกสำหรับการแนบในภาคผนวกรายงานวิจัย ว.PA", bold_prefix="2. มอบเกียรติบัตรและปิดบทเรียน: "))
    elements.append(heading_sec("8. สื่อ อุปกรณ์ และแหล่งการเรียนรู้"))
    elements.append(body_p("แบบทดสอบวัดผลสัมฤทธิ์หลังเรียน (Post-test) 20 ข้อ", bullet=True))
    elements.append(body_p("แบบสอบถามความพึงพอใจของผู้เรียน (Likert Scale 5 ระดับ)", bullet=True))
    elements.append(body_p("เกียรติบัตรยอดนักสืบโค้ดดิ้งอวกาศสำหรับนักเรียน 8 คน", bullet=True))
    elements.append(heading_sec("9. การวัดและประเมินผลการเรียนรู้"))
    elements.append(get_plan_eval_table(
        "สรุปองค์ความรู้เรื่องอัลกอริทึม ลูป เงื่อนไข และการแก้บั๊กได้ครบถ้วน",
        "ทำแบบทดสอบหลังเรียน (Post-test) ผ่านเกณฑ์ร้อยละ 75 ขึ้นไป",
        "มีความภาคภูมิใจและมีเจตคติที่ดีต่อวิชาวิทยาการคำนวณ"
    ))
    elements.append(heading_sec("10. บันทึกผลหลังการจัดการเรียนรู้"))
    elements.append(get_plan_post_table(7, "คะแนนสอบหลังเรียนของนักเรียนทั้ง 8 คน เพิ่มขึ้นอย่างก้าวกระโดด (เฉลี่ยร้อยละ 85.63) เด็กกลุ่มช้าทำข้อสอบเดี่ยวผ่านเกณฑ์ระดับดีมากได้ทุกคน สะท้อนว่าการสอนแบบ Pair Programming สื่อ AR ประสบผลสำเร็จตามเป้าหมายของ PA 1 อย่างงดงาม", "ไม่มีปัญหาอุปสรรค นักเรียนทุกคนมีความสุขและมีเจตคติที่ดีต่อการเขียนโปรแกรม", "นำผลการจัดการเรียนรู้และชิ้นงานทั้งหมดไปจัดทำเป็นเล่มรายงานวิจัยในชั้นเรียน (CAR) เพื่อใช้ประกอบการประเมิน ว.PA ต่อไป"))

    # =========================================================================
    # ภาคผนวก: ตารางสรุปผลการประเมินผลสัมฤทธิ์และคุณลักษณะรายบุคคล
    # =========================================================================
    elements.append(make_page_break())
    elements.append(make_p([("ภาคผนวก: ตารางสรุปผลการประเมินการจัดการเรียนรู้รายบุคคล (N = 8)", True, False, 32, "1E3A8A")], align="center", space_before=80, space_after=40))
    elements.append(make_p([("กลุ่มสาระการเรียนรู้วิทยาศาสตร์และเทคโนโลยี รายวิชาเทคโนโลยี (วิทยาการคำนวณ) ว15101 ชั้น ป.5", False, False, 24, "475569")], align="center", space_before=0, space_after=80))

    t_app_headers = ["ที่", "เลขประจำตัว", "ชื่อ - สกุล ผู้เรียน", "ก่อนเรียน\n(20)", "หลังเรียน\n(20)", "ทักษะกระบวนการ (P)\n(ระดับคุณภาพ)", "คุณลักษณะ (A)\n(ระดับคุณภาพ)", "สรุปผล\nการประเมิน"]
    t_app_rows = [
        ["1", "2040", "เด็กชายภูฟ้า  แสงศรี", "9", "17", "ดีมาก", "ดีเยี่ยม", "ผ่านเกณฑ์"],
        ["2", "2045", "เด็กหญิงพิชญาภา  แสงศรี", "8", "16", "ดีมาก", "ดีเยี่ยม", "ผ่านเกณฑ์"],
        ["3", "2048", "เด็กหญิงสิริวิมล  สาวิสิทธิ์", "11", "18", "ดีมาก", "ดีเยี่ยม", "ผ่านเกณฑ์"],
        ["4", "2047", "เด็กหญิงสาวิตรี  สายสมคุณ", "7", "15", "ดี", "ดีเยี่ยม", "ผ่านเกณฑ์"],
        ["5", "2044", "เด็กหญิงณัฐณิชา  นันทโพธิ์เดช", "12", "19", "ดีเยี่ยม", "ดีเยี่ยม", "ผ่านเกณฑ์"],
        ["6", "2046", "เด็กหญิงรฐา  สอนเต็ม", "10", "18", "ดีมาก", "ดีเยี่ยม", "ผ่านเกณฑ์"],
        ["7", "2043", "เด็กหญิงกัญญาพัชร  วาจาชื่น", "8", "16", "ดีมาก", "ดีเยี่ยม", "ผ่านเกณฑ์"],
        ["8", "2177", "เด็กหญิงกัญญารัตน์  บัวบง", "9", "18", "ดีมาก", "ดีเยี่ยม", "ผ่านเกณฑ์"],
        ["เฉลี่ย/สรุป", "-", "ร้อยละ 100 ผ่านเกณฑ์ประเมิน", "9.25", "17.13", "ดีมาก", "ดีเยี่ยม", "ผ่านเกณฑ์ 100%"]
    ]
    elements.append(make_table(t_app_headers, t_app_rows, [600, 1100, 2600, 1000, 1000, 1400, 1400, 1400], ["center", "center", "left", "center", "center", "center", "center", "center"], font_size=20, header_bg="1E3A8A"))
    elements.append(make_p([], space_before=100, space_after=100))

    elements.append(make_callout("เกณฑ์การประเมิน: ผลสัมฤทธิ์ทางการเรียนหลังเรียนผ่านเกณฑ์ร้อยละ 70 ขึ้นไป (14 คะแนนขึ้นไป) และทักษะกระบวนการ (P) อยู่ในระดับ ดี ขึ้นไป โดยนักเรียนทั้ง 8 คน ผ่านเกณฑ์การประเมินครบ 100%", title="การตัดสินผลการเรียนรู้"))

    # Wrap into Word Document XML
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
    <w:pPrDefault>
      <w:pPr>
        <w:spacing w:before="40" w:after="40" w:line="240" w:lineRule="auto"/>
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
      <w:pgMar w:top="1134" w:right="1134" w:bottom="1134" w:left="1417"/>
    </w:sectPr>
  </w:body>
</w:document>"""

    out_file = "แผนการจัดการเรียนรู้_Active_Learning_วิทยาการคำนวณ_ป5_ฉบับปรับปรุงตามแบบ_ครูเตชินท์.docx"
    with zipfile.ZipFile(out_file, "w", zipfile.ZIP_DEFLATED) as docx:
        docx.writestr("[Content_Types].xml", content_types)
        docx.writestr("_rels/.rels", rels)
        docx.writestr("word/_rels/document.xml.rels", doc_rels)
        docx.writestr("word/styles.xml", styles)
        docx.writestr("word/document.xml", document_xml)

    print(f"Generated clean reformatted plans: {out_file}")
    os.system(f"cp '{out_file}' docs/")
    print(f"Copied to docs/{out_file}")

if __name__ == "__main__":
    build_original_reformatted_plans()
