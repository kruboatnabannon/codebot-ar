# -*- coding: utf-8 -*-
"""
Rebuild 'แบบข้อตกลงในการพัฒนางาน 69.docx' with:
1. Zero \u200b characters (no add_thai_breaks).
2. Clean left-aligned paragraphs for all cells (cell 0, 1, 2, 3) in all 3 tables.
3. Exact text matching user input for Table 1, Table 2, Table 3.
4. Natural, broad Section 2 (PDCA).
5. 100% ECMA-376 schema compliant.
"""
import zipfile, re, os, shutil
from test_schema_rules import validate_docx_xml

def esc(t):
    if t is None:
        return ""
    # strip any zero width spaces
    t = str(t).replace('\u200b', '')
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def make_p_xml(runs, align="left", first_line=0, left_indent=0, hanging=0,
               space_before=0, space_after=40, line_spacing=240, keep_next=False):
    pPr_parts = []
    if keep_next:
        pPr_parts.append("<w:keepNext/>")
    pPr_parts.append(f'<w:spacing w:before="{space_before}" w:after="{space_after}" w:line="{line_spacing}" w:lineRule="auto"/>')
    if hanging > 0:
        pPr_parts.append(f'<w:ind w:left="{left_indent}" w:hanging="{hanging}"/>')
    elif first_line > 0 or left_indent > 0:
        ind_attrs = []
        if left_indent > 0:
            ind_attrs.append(f'w:left="{left_indent}"')
        if first_line > 0:
            ind_attrs.append(f'w:firstLine="{first_line}"')
        attr_str = " ".join(ind_attrs)
        pPr_parts.append(f'<w:ind {attr_str}/>')
    if align:
        pPr_parts.append(f'<w:jc w:val="{align}"/>')

    runs_xml = []
    for item in runs:
        if isinstance(item, str):
            t, b, it, sz, color = item, False, False, 32, "000000"
        else:
            t = item[0]
            b = item[1] if len(item) > 1 else False
            it = item[2] if len(item) > 2 else False
            sz = item[3] if len(item) > 3 else 32
            color = item[4] if len(item) > 4 else "000000"

        rPr_parts = ['<w:rFonts w:ascii="TH SarabunPSK" w:hAnsi="TH SarabunPSK" w:cs="TH SarabunPSK"/>']
        if b:
            rPr_parts.append("<w:b/><w:bCs/>")
        if it:
            rPr_parts.append("<w:i/><w:iCs/>")
        rPr_parts.append(f'<w:color w:val="{color}"/>')
        rPr_parts.append(f'<w:sz w:val="{sz}"/><w:szCs w:val="{sz}"/>')
        rPr_parts.append('<w:lang w:val="th-TH" w:eastAsia="th-TH" w:bidi="th-TH"/>')

        runs_xml.append(f'<w:r><w:rPr>{"".join(rPr_parts)}</w:rPr><w:t xml:space="preserve">{esc(t)}</w:t></w:r>')

    return f'<w:p><w:pPr>{"".join(pPr_parts)}</w:pPr>{"".join(runs_xml)}</w:p>'

def make_tc_xml(tcPr_xml, p_xml_list):
    return f'<w:tc>{tcPr_xml}{"".join(p_xml_list)}</w:tc>'

def build_docx():
    src_file = "แบบข้อตกลงในการพัฒนางาน 69_backup.docx"
    dst_file = "แบบข้อตกลงในการพัฒนางาน 69.docx"

    with zipfile.ZipFile(src_file, "r") as zin:
        file_map = {name: zin.read(name) for name in zin.namelist()}

    xml = file_map["word/document.xml"].decode("utf-8")
    # Clean any existing zero-width spaces in the base xml
    xml = xml.replace('\u200b', '')

    # 1. Fix introductory text
    xml = xml.replace("PA 1/สPA 1/สแบบข้อตกลงในการพัฒนางาน (PA)", "PA 1/ส แบบข้อตกลงในการพัฒนางาน (PA)")
    xml = xml.replace("ตำแห่งครู", "ตำแหน่งครู")

    def repl_guidance(m):
        return m.group(0).replace("มัธยมศึกษาปีที่ 1", "มัธยมศึกษาปีที่ 2")
    xml = re.sub(r'<w:p[ >].*?รายวิชาแนะแนว.*?</w:p>', repl_guidance, xml, count=1)
    xml = re.sub(r'<w:p[ >].*?รายวิชาชุมนุม.*?</w:p>', repl_guidance, xml, count=1)

    # -------------------------------------------------------------
    # 2. Table 0 (ด้านที่ 1: ด้านการจัดการเรียนรู้ 8 ตัวชี้วัด)
    # -------------------------------------------------------------
    t0_c0_ps = [
        make_p_xml([("1. ด้านการจัดการเรียนรู้", True)], align="left", space_before=40, space_after=40),
        make_p_xml([("ลักษณะงานที่เสนอให้ครอบคลุมถึงการสร้างและหรือพัฒนาหลักสูตร การออกแบบการจัดการเรียนรู้ การจัดกิจกรรมการเรียนรู้ การสร้างและหรือพัฒนาสื่อ นวัตกรรม เทคโนโลยี และแหล่งเรียนรู้ การวัดและประเมินผลการจัดการเรียนรู้ การศึกษา วิเคราะห์ สังเคราะห์เพื่อแก้ปัญหาหรือพัฒนาการเรียนรู้ การจัดบรรยากาศที่ส่งเสริมและพัฒนาผู้เรียน และการอบรมและพัฒนาคุณลักษณะที่ดีของผู้เรียน", False)], align="left", space_before=0, space_after=40)
    ]

    t0_c1_ps = [
        make_p_xml([("1.1 การสร้างและหรือพัฒนาหลักสูตร", True)], align="left", space_before=40, space_after=20),
        make_p_xml([("- วิเคราะห์หลักสูตร มาตรฐานการเรียนรู้ และตัวชี้วัด นำไปจัดทำรายวิชาและหน่วยการเรียนรู้ ให้สอดคล้องกับหลักสูตรแกนกลางฯ และหลักสูตรสถานศึกษา โดยปรับประยุกต์ให้สอดคล้องกับบริบทของสถานศึกษาและผู้เรียน", False)], align="left", left_indent=240, hanging=240, space_before=0, space_after=60),

        make_p_xml([("1.2 ออกแบบการจัดการเรียนรู้", True)], align="left", space_before=40, space_after=20),
        make_p_xml([("- จัดทำแผนการจัดการเรียนรู้เชิงรุก (Active Learning) ในรายวิชาเทคโนโลยี (วิทยาการคำนวณ) ที่เน้นผู้เรียนเป็นสำคัญ โดยนำกระบวนการเรียนรู้โดยใช้เกมเป็นฐาน (Game-based Learning) มาปรับประยุกต์ใช้ในการจัดกิจกรรม", False)], align="left", left_indent=240, hanging=240, space_before=0, space_after=60),

        make_p_xml([("1.3 การจัดกิจกรรมการเรียนรู้", True)], align="left", space_before=40, space_after=20),
        make_p_xml([("- จัดกิจกรรมการเรียนรู้เชิงรุก (Active Learning) ในรายวิชาเทคโนโลยี (วิทยาการคำนวณ) โดยมีการปรับประยุกต์กิจกรรมการเรียนรู้ อำนวยความสะดวกในการเรียนรู้ และส่งเสริมให้ผู้เรียนได้พัฒนาเต็มตามศักยภาพ เรียนรู้และทำงานร่วมกัน มีกระบวนการคิดและค้นพบองค์ความรู้ด้วยตนเอง", False)], align="left", left_indent=240, hanging=240, space_before=0, space_after=60),

        make_p_xml([("1.4 สร้างและหรือพัฒนาสื่อ นวัตกรรม เทคโนโลยี และแหล่งเรียนรู้", True)], align="left", space_before=40, space_after=20),
        make_p_xml([("- สร้างและพัฒนาสื่อ นวัตกรรม เทคโนโลยี และแหล่งเรียนรู้ที่สอดคล้องกับกิจกรรมการเรียนรู้ ในรายวิชาเทคโนโลยี (วิทยาการคำนวณ) ทั้งสื่อดิจิทัล สื่อกิจกรรมการเรียนรู้ และสื่อเกมจำลองภารกิจ โดยมีการปรับประยุกต์ให้เหมาะสมกับความแตกต่างของผู้เรียน ทำให้ผู้เรียนมีทักษะการคิดและสามารถเรียนรู้ได้อย่างมีประสิทธิภาพ", False)], align="left", left_indent=240, hanging=240, space_before=0, space_after=60),

        make_p_xml([("1.5 การวัดและประเมินผลการเรียนรู้", True)], align="left", space_before=40, space_after=20),
        make_p_xml([("- พัฒนารูปแบบการวัดและประเมินผลการเรียนรู้ตามสภาพจริงที่หลากหลายและเหมาะสม ได้แก่ 1) แบบทดสอบ 2) แบบสังเกตพฤติกรรม 3) แบบประเมินชิ้นงาน/ภาระงาน 4) แบบประเมินความพึงพอใจ และนำผลการวัดและประเมินผลมาใช้ในการปรับประยุกต์แก้ไขปัญหาและพัฒนาการจัดการเรียนรู้", False)], align="left", left_indent=240, hanging=240, space_before=0, space_after=60),

        make_p_xml([("1.6 ศึกษา วิเคราะห์ และสังเคราะห์ เพื่อแก้ไขปัญหาหรือพัฒนาการเรียนรู้", True)], align="left", space_before=40, space_after=20),
        make_p_xml([("- ศึกษา วิเคราะห์ และสังเคราะห์ปัญหาการจัดการเรียนรู้ของผู้เรียนเป็นรายบุคคลอย่างเป็นระบบ จัดทำวิจัยปฏิบัติการในชั้นเรียน เรื่อง การจัดการเรียนรู้โดยใช้เกมเป็นฐาน (Game-based Learning) เพื่อนำผลมาปรับประยุกต์ใช้ในการแก้ปัญหาและพัฒนาการเรียนรู้ของผู้เรียน", False)], align="left", left_indent=240, hanging=240, space_before=0, space_after=60),

        make_p_xml([("1.7 จัดบรรยากาศที่ส่งเสริมและพัฒนาผู้เรียน", True)], align="left", space_before=40, space_after=20),
        make_p_xml([("- ปรับประยุกต์การจัดบรรยากาศในชั้นเรียนให้เหมาะสมกับวัยและความแตกต่างของผู้เรียน ส่งเสริมให้เกิดความสนุกสนาน กระตุ้นความสนใจ สร้างแรงบันดาลใจ และเปิดโอกาสให้ผู้เรียนทุกคนได้มีส่วนร่วมและแสดงความคิดเห็นอย่างสร้างสรรค์", False)], align="left", left_indent=240, hanging=240, space_before=0, space_after=60),

        make_p_xml([("1.8 อบรมและพัฒนาคุณลักษณะที่ดีของผู้เรียน", True)], align="left", space_before=40, space_after=20),
        make_p_xml([("- อบรมบ่มนิสัยให้ผู้เรียนมีคุณธรรม จริยธรรม คุณลักษณะอันพึงประสงค์ และค่านิยมความเป็นไทยที่ดีงาม ผ่านกิจกรรมพัฒนาผู้เรียน กิจกรรมแนะแนว และกิจกรรมโฮมรูมของนักเรียนชั้นมัธยมศึกษาปีที่ 2 ตลอดจนสอดแทรกในการจัดกิจกรรมการเรียนรู้ทุกระดับชั้นที่สอน", False)], align="left", left_indent=240, hanging=240, space_before=0, space_after=40),
    ]

    t0_c2_ps = [
        make_p_xml([("1. ผู้เรียนได้เรียนรู้ตรงตามหลักสูตร มาตรฐานการเรียนรู้ และตัวชี้วัดที่กำหนดอย่างมีประสิทธิภาพ", False)], align="left", left_indent=240, hanging=240, space_before=40, space_after=50),
        make_p_xml([("2. ผู้เรียนได้เรียนรู้ตามหน่วยการเรียนรู้และแผนการจัดการเรียนรู้ที่มีคุณภาพ และได้รับการพัฒนาสมรรถนะสำคัญตามหลักสูตร", False)], align="left", left_indent=240, hanging=240, space_before=0, space_after=50),
        make_p_xml([("3. ผู้เรียนได้รับการจัดกิจกรรมการเรียนรู้เชิงรุก (Active Learning) ได้ฝึกคิดและลงมือปฏิบัติจริง เรียนรู้อย่างมีความสุข", False)], align="left", left_indent=240, hanging=240, space_before=0, space_after=50),
        make_p_xml([("4. ผู้เรียนได้รับการพัฒนาทักษะการเรียนรู้ผ่านสื่อ นวัตกรรม และเทคโนโลยีที่หลากหลายและมีประสิทธิภาพ", False)], align="left", left_indent=240, hanging=240, space_before=0, space_after=50),
        make_p_xml([("5. ผู้เรียนได้รับการวัดและประเมินผลตามสภาพจริงด้วยเครื่องมือที่น่าเชื่อถือ สะท้อนผลสัมฤทธิ์ทางการเรียนรู้ที่แท้จริง", False)], align="left", left_indent=240, hanging=240, space_before=0, space_after=50),
        make_p_xml([("6. ผู้เรียนได้รับการแก้ไขปัญหาและพัฒนาการเรียนรู้อย่างเป็นระบบผ่านกระบวนการวิจัยปฏิบัติการในชั้นเรียน", False)], align="left", left_indent=240, hanging=240, space_before=0, space_after=50),
        make_p_xml([("7. ผู้เรียนมีส่วนร่วมในการจัดบรรยากาศในชั้นเรียน มีความสุข กระตือรือร้น และมีเจตคติที่ดีต่อการเรียนรู้", False)], align="left", left_indent=240, hanging=240, space_before=0, space_after=50),
        make_p_xml([("8. ผู้เรียนและนักเรียนชั้นมัธยมศึกษาปีที่ 2 เป็นผู้มีคุณลักษณะอันพึงประสงค์ที่ดีงามทั้งต่อตนเอง โรงเรียน และสังคม", False)], align="left", left_indent=240, hanging=240, space_before=0, space_after=40),
    ]

    t0_c3_ps = [
        make_p_xml([("1. ผู้เรียนร้อยละ 70 มีความรู้ตามตัวชี้วัดที่ต้องรู้ในรายวิชาเทคโนโลยี (วิทยาการคำนวณ) ตรงตามหลักสูตรที่กำหนด", False)], align="left", left_indent=240, hanging=240, space_before=40, space_after=50),
        make_p_xml([("2. ผู้เรียนร้อยละ 70 มีความรู้และทักษะตามตัวชี้วัด และมีคุณลักษณะอันพึงประสงค์ตามที่สถานศึกษากำหนด", False)], align="left", left_indent=240, hanging=240, space_before=0, space_after=50),
        make_p_xml([("3. ผู้เรียนร้อยละ 70 ได้เรียนรู้อย่างมีความสุข และมีความรู้ความเข้าใจตามตัวชี้วัดตรงตามหลักสูตร", False)], align="left", left_indent=240, hanging=240, space_before=0, space_after=50),
        make_p_xml([("4. ผู้เรียนร้อยละ 70 เกิดทักษะ 4 Cs (การคิดวิพากษ์ การทำงานร่วมกัน การสื่อสาร และความคิดสร้างสรรค์) ส่งผลให้มีสมรรถนะตรงตามหลักสูตร", False)], align="left", left_indent=240, hanging=240, space_before=0, space_after=50),
        make_p_xml([("5. ผู้เรียนร้อยละ 70 มีผลสัมฤทธิ์ทางการเรียนผ่านตามเกณฑ์ที่สถานศึกษากำหนดไว้ทุกตัวชี้วัด", False)], align="left", left_indent=240, hanging=240, space_before=0, space_after=50),
        make_p_xml([("6. ผู้เรียนร้อยละ 70 มีผลการพัฒนาจากการวิจัยในชั้นเรียนเพิ่มขึ้นตามเกณฑ์ที่กำหนดไว้", False)], align="left", left_indent=240, hanging=240, space_before=0, space_after=50),
        make_p_xml([("7. ผู้เรียนร้อยละ 80 มีความสนใจ กระตือรือร้นในการร่วมกิจกรรมการเรียนรู้ และมีความสุขในการเรียน", False)], align="left", left_indent=240, hanging=240, space_before=0, space_after=50),
        make_p_xml([("8. ผู้เรียนร้อยละ 100 มีคุณลักษณะอันพึงประสงค์ตามที่สถานศึกษากำหนดไว้", False)], align="left", left_indent=240, hanging=240, space_before=0, space_after=40),
    ]

    # -------------------------------------------------------------
    # 3. Table 1 (ด้านที่ 2: 4 ตัวชี้วัด)
    # -------------------------------------------------------------
    t1_c0_ps = [
        make_p_xml([("2. ด้านการส่งเสริมและสนับสนุนการจัดการเรียนรู้", True)], align="left", space_before=40, space_after=40),
        make_p_xml([("ลักษณะงานที่เสนอให้ครอบคลุมถึงการจัดทำข้อมูลสารสนเทศของผู้เรียนและรายวิชาการดำเนินการตามระบบ ดูแลช่วยเหลือผู้เรียน การปฏิบัติงานวิชาการและงานอื่น ๆ ของสถานศึกษา และการประสานความร่วมมือกับผู้ปกครอง ภาคีเครือข่าย และหรือสถานประกอบการ", False)], align="left", space_before=0, space_after=40)
    ]

    t1_c1_ps = [
        make_p_xml([("2.1 จัดทำข้อมูลสารสนเทศของผู้เรียนและรายวิชา", True)], align="left", space_before=40, space_after=20),
        make_p_xml([("- จัดทำข้อมูลในระบบสารสนเทศของนักเรียนชั้นมัธยมศึกษาปีที่ 2 และข้อมูลสารสนเทศในรายวิชาที่ทำการสอน เอกสารงานประจำชั้น และแบบ ปพ. ต่างๆ อย่างเป็นระบบ ถูกต้อง เป็นปัจจุบัน และสะดวกต่อการใช้งาน", False)], align="left", left_indent=240, hanging=240, space_before=0, space_after=60),

        make_p_xml([("2.2 ดำเนินการตามระบบดูแลช่วยเหลือผู้เรียน", True)], align="left", space_before=40, space_after=20),
        make_p_xml([("- ดำเนินการตามระบบดูแลช่วยเหลือผู้เรียนอย่างเป็นระบบ มีการคัดกรองนักเรียน ออกเยี่ยมบ้านนักเรียนชั้นมัธยมศึกษาปีที่ 2 อย่างน้อยภาคเรียนละ 1 ครั้ง และประสานความร่วมมือกับผู้เกี่ยวข้องเพื่อแก้ไขปัญหาและพัฒนาผู้เรียน", False)], align="left", left_indent=240, hanging=240, space_before=0, space_after=60),

        make_p_xml([("2.3 ปฏิบัติงานวิชาการและงานอื่นๆ ของสถานศึกษา", True)], align="left", space_before=40, space_after=20),
        make_p_xml([("- ร่วมปฏิบัติงานทางวิชาการ และงานอื่นๆ ของสถานศึกษา เพื่อยกระดับคุณภาพการจัดการศึกษาของสถานศึกษา โดยมีการปรับประยุกต์รูปแบบหรือแนวทางการดำเนินงานให้มีประสิทธิภาพ เช่น งานบริหารงานทั่วไป งานพัฒนาหลักสูตร งานวัดผลประเมินผล และโครงการพัฒนา ICT ในโรงเรียน", False)], align="left", left_indent=240, hanging=240, space_before=0, space_after=60),

        make_p_xml([("2.4 ประสานความร่วมมือกับผู้ปกครอง ภาคีเครือข่าย และหรือสถานประกอบการ", True)], align="left", space_before=40, space_after=20),
        make_p_xml([("- มีการประสานความร่วมมือกับผู้ปกครองและภาคีเครือข่าย เพื่อร่วมกันแก้ไขปัญหาและพัฒนาผู้เรียน โดยร่วมประชุมผู้ปกครองภาคเรียนละ 1 ครั้ง และประสานความร่วมมือในการดูแลช่วยเหลือนักเรียนอย่างต่อเนื่อง", False)], align="left", left_indent=240, hanging=240, space_before=0, space_after=40),
    ]

    t1_c2_ps = [
        make_p_xml([("1. ผู้เรียนมีระบบข้อมูลสารสนเทศที่สมบูรณ์ สะดวกต่อการใช้งานและมีประสิทธิภาพ สามารถนำข้อมูลมาใช้ในการส่งเสริมและพัฒนาได้อย่างทันท่วงที", False)], align="left", left_indent=240, hanging=240, space_before=40, space_after=50),
        make_p_xml([("2. นักเรียนชั้นมัธยมศึกษาปีที่ 2 มีข้อมูลพื้นฐานเป็นรายบุคคล และได้รับการดูแลช่วยเหลือในเรื่องต่างๆ จากข้อมูลการคัดกรอง การเยี่ยมบ้าน และการจัดหาทุนการศึกษาสำหรับนักเรียนยากจน", False)], align="left", left_indent=240, hanging=240, space_before=0, space_after=50),
        make_p_xml([("3. ผู้เรียนได้เรียนรู้ในกิจกรรมที่หลากหลายตามโครงการและกิจกรรมที่สถานศึกษาได้กำหนดขึ้นตลอดปีการศึกษา", False)], align="left", left_indent=240, hanging=240, space_before=0, space_after=50),
        make_p_xml([("4. ผู้เรียนได้รับการดูแลช่วยเหลือจากผู้ปกครองและภาคีเครือข่ายที่เกี่ยวข้องอย่างเป็นระบบและต่อเนื่อง", False)], align="left", left_indent=240, hanging=240, space_before=0, space_after=40),
    ]

    t1_c3_ps = [
        make_p_xml([("1. ผู้เรียนร้อยละ 100 มีข้อมูลในระบบสารสนเทศครบถ้วนในทุกด้าน เป็นระบบและเป็นรายบุคคล", False)], align="left", left_indent=240, hanging=240, space_before=40, space_after=50),
        make_p_xml([("2. นักเรียนชั้นมัธยมศึกษาปีที่ 2 ร้อยละ 100 ได้รับการดูแลเอาใจใส่ตรงตามความต้องการรายบุคคล และมีความสัมพันธ์อันดีระหว่างครูและนักเรียน", False)], align="left", left_indent=240, hanging=240, space_before=0, space_after=50),
        make_p_xml([("3. ผู้เรียนร้อยละ 70 ได้รับการพัฒนาและมีส่วนร่วมในกิจกรรมทางวิชาการและโครงการที่โรงเรียนจัดขึ้น", False)], align="left", left_indent=240, hanging=240, space_before=0, space_after=50),
        make_p_xml([("4. ผู้เรียนร้อยละ 100 ได้รับการดูแลช่วยเหลือ ประสานความร่วมมือกับผู้ปกครอง ทำให้ผู้เรียนมีคุณภาพชีวิตที่ดีขึ้น และมีผลสัมฤทธิ์ทางการเรียนสูงขึ้น", False)], align="left", left_indent=240, hanging=240, space_before=0, space_after=40),
    ]

    # -------------------------------------------------------------
    # 4. Table 2 (ด้านที่ 3: 3 ตัวชี้วัด)
    # -------------------------------------------------------------
    t2_c0_ps = [
        make_p_xml([("3. ด้านการพัฒนาตนเองและวิชาชีพ", True)], align="left", space_before=40, space_after=40),
        make_p_xml([("ลักษณะงานที่เสนอให้ครอบคลุมถึงการพัฒนาตนเองอย่างเป็นระบบและต่อเนื่อง การมีส่วนร่วมในการแลกเปลี่ยนเรียนรู้ทางวิชาชีพเพื่อพัฒนาการจัดการเรียนรู้และการนำความรู้ความสามารถทักษะที่ได้จากการพัฒนาตนเองและวิชาชีพมาใช้ในการพัฒนาการจัดการเรียนรู้ การพัฒนาคุณภาพผู้เรียน และการพัฒนานวัตกรรมการจัดการเรียนรู้", False)], align="left", space_before=0, space_after=40)
    ]

    t2_c1_ps = [
        make_p_xml([("3.1 พัฒนาตนเองอย่างเป็นระบบและต่อเนื่อง", True)], align="left", space_before=40, space_after=20),
        make_p_xml([("- พัฒนาตนเองอย่างเป็นระบบและต่อเนื่อง โดยการเข้าอบรม ประชุมเชิงปฏิบัติการ และสัมมนาตลอดปีงบประมาณ 2569 ในสาขาวิชาและสมรรถนะวิชาชีพ โดยเฉพาะการจัดการเรียนรู้วิทยาการคำนวณและเทคโนโลยีดิจิทัล ทั้งรูปแบบ Onsite และ Online เพื่อนำมาพัฒนาสื่อและกิจกรรมการเรียนรู้", False)], align="left", left_indent=240, hanging=240, space_before=0, space_after=60),

        make_p_xml([("3.2 มีส่วนร่วมในการแลกเปลี่ยนเรียนรู้ทางวิชาชีพเพื่อพัฒนาการจัดการเรียนรู้", True)], align="left", space_before=40, space_after=20),
        make_p_xml([("- เข้าร่วมกิจกรรมชุมชนการเรียนรู้ทางวิชาชีพ (PLC) เพื่อร่วมแลกเปลี่ยนเรียนรู้ สะท้อนคิด ปรึกษาหารือในการแก้ไขปัญหาการเรียนรู้ของผู้เรียน และร่วมกันสร้างหรือพัฒนานวัตกรรมการจัดการเรียนรู้", False)], align="left", left_indent=240, hanging=240, space_before=0, space_after=60),

        make_p_xml([("3.3 นำความรู้ ความสามารถ ทักษะที่ได้จากการพัฒนาตนเองและวิชาชีพมาใช้", True)], align="left", space_before=40, space_after=20),
        make_p_xml([("- นำความรู้ ความสามารถ ทักษะ และนวัตกรรมที่ได้จากการพัฒนาตนเองและการเข้าร่วม PLC มาปรับประยุกต์ใช้ในการพัฒนาการจัดการเรียนรู้ การพัฒนาคุณภาพผู้เรียน และการพัฒนานวัตกรรมการจัดการเรียนรู้ในรายวิชาวิทยาการคำนวณ", False)], align="left", left_indent=240, hanging=240, space_before=0, space_after=40),
    ]

    t2_c2_ps = [
        make_p_xml([("1. ผู้เรียนได้รับการจัดกิจกรรมการเรียนรู้ที่เน้นผู้เรียนเป็นสำคัญ มีกิจกรรมที่หลากหลายเหมาะสมตามความแตกต่างระหว่างบุคคล ทำให้ผู้เรียนมีผลสัมฤทธิ์ทางการเรียนที่ดีขึ้น", False)], align="left", left_indent=240, hanging=240, space_before=40, space_after=50),
        make_p_xml([("2. ผู้เรียนได้รับการแก้ไขปัญหาในการเรียนรู้ได้อย่างเหมาะสมตามความแตกต่างระหว่างบุคคล และได้รับการพัฒนาจากสื่อนวัตกรรมการจัดการเรียนรู้ที่ครูได้พัฒนาขึ้น", False)], align="left", left_indent=240, hanging=240, space_before=0, space_after=50),
        make_p_xml([("3. ผู้เรียนได้รับการพัฒนาทักษะกระบวนการเรียนรู้และสมรรถนะสำคัญ จากการนำความรู้และนวัตกรรมที่ได้จากกระบวนการ PLC มาปรับประยุกต์ใช้ในชั้นเรียน", False)], align="left", left_indent=240, hanging=240, space_before=0, space_after=40),
    ]

    t2_c3_ps = [
        make_p_xml([("1. ผู้เรียนร้อยละ 70 ได้รับการจัดกิจกรรมการเรียนรู้ด้วยวิธีการที่หลากหลายและเหมาะสมกับเนื้อหา ส่งผลให้มีผลสัมฤทธิ์ทางการเรียนสูงขึ้น", False)], align="left", left_indent=240, hanging=240, space_before=40, space_after=50),
        make_p_xml([("2. ผู้เรียนร้อยละ 70 ได้รับการแก้ไขปัญหาทางการเรียนรู้และปัญหาอื่นๆ อย่างต่อเนื่อง เป็นระบบ และมีผลการเรียนรู้ที่ดีขึ้น", False)], align="left", left_indent=240, hanging=240, space_before=0, space_after=50),
        make_p_xml([("3. ผู้เรียนร้อยละ 70 มีความพึงพอใจและมีเจตคติที่ดีต่อการจัดกิจกรรมการเรียนรู้ด้วยสื่อนวัตกรรมที่ครูนำมาปรับประยุกต์ใช้", False)], align="left", left_indent=240, hanging=240, space_before=0, space_after=40),
    ]

    # Find the 3 tables in XML and replace all 4 cells in Row 1
    tbl_pattern = re.compile(r'<w:tbl>.*?</w:tbl>', re.DOTALL)
    tbl_matches = list(tbl_pattern.finditer(xml))
    assert len(tbl_matches) == 3, f"Expected 3 tables, found {len(tbl_matches)}"

    # Replace backwards so string indices do not shift
    for t_idx in [2, 1, 0]:
        tbl_match = tbl_matches[t_idx]
        tbl_xml = tbl_match.group(0)

        row_pattern = re.compile(r'<w:tr[ >].*?</w:tr>', re.DOTALL)
        row_matches = list(row_pattern.finditer(tbl_xml))
        assert len(row_matches) >= 2, f"Expected at least 2 rows in table {t_idx}"
        row1_xml = row_matches[1].group(0)

        tc_pattern = re.compile(r'<w:tc[ >].*?</w:tc>', re.DOTALL)
        tc_matches = list(tc_pattern.finditer(row1_xml))
        assert len(tc_matches) == 4, f"Expected 4 cells in row 1 of table {t_idx}"

        c0_tcPr = re.search(r'<w:tcPr>.*?</w:tcPr>', tc_matches[0].group(0), re.DOTALL).group(0)
        c1_tcPr = re.search(r'<w:tcPr>.*?</w:tcPr>', tc_matches[1].group(0), re.DOTALL).group(0)
        c2_tcPr = re.search(r'<w:tcPr>.*?</w:tcPr>', tc_matches[2].group(0), re.DOTALL).group(0)
        c3_tcPr = re.search(r'<w:tcPr>.*?</w:tcPr>', tc_matches[3].group(0), re.DOTALL).group(0)

        if t_idx == 0:
            new_c0 = make_tc_xml(c0_tcPr, t0_c0_ps)
            new_c1 = make_tc_xml(c1_tcPr, t0_c1_ps)
            new_c2 = make_tc_xml(c2_tcPr, t0_c2_ps)
            new_c3 = make_tc_xml(c3_tcPr, t0_c3_ps)
        elif t_idx == 1:
            new_c0 = make_tc_xml(c0_tcPr, t1_c0_ps)
            new_c1 = make_tc_xml(c1_tcPr, t1_c1_ps)
            new_c2 = make_tc_xml(c2_tcPr, t1_c2_ps)
            new_c3 = make_tc_xml(c3_tcPr, t1_c3_ps)
        else:
            new_c0 = make_tc_xml(c0_tcPr, t2_c0_ps)
            new_c1 = make_tc_xml(c1_tcPr, t2_c1_ps)
            new_c2 = make_tc_xml(c2_tcPr, t2_c2_ps)
            new_c3 = make_tc_xml(c3_tcPr, t2_c3_ps)

        # Reconstruct row1
        row1_prefix = row1_xml[:tc_matches[0].start()]
        row1_suffix = row1_xml[tc_matches[3].end():]
        new_row1 = f"{row1_prefix}{new_c0}{new_c1}{new_c2}{new_c3}{row1_suffix}"

        # Reconstruct tbl
        new_tbl_xml = tbl_xml[:row_matches[1].start()] + new_row1 + tbl_xml[row_matches[1].end():]

        # Splice back into xml
        xml = xml[:tbl_match.start()] + new_tbl_xml + xml[tbl_match.end():]

    # -------------------------------------------------------------
    # 5. Section 2: ข้อตกลงในการพัฒนางานที่เป็นประเด็นท้าทาย
    # -------------------------------------------------------------
    sec2_ps = [
        # ส่วนที่ 2 หัวเรื่อง
        make_p_xml([("ส่วนที่ 2 ข้อตกลงในการพัฒนางานที่เป็นประเด็นท้าทายในการพัฒนาผลลัพธ์การเรียนรู้ของผู้เรียน", True)], align="center", space_before=120, space_after=60),
        make_p_xml([("ประเด็นที่ท้าทายในการพัฒนาผลลัพธ์การเรียนรู้ของผู้เรียนของผู้จัดทำข้อตกลง ซึ่งปัจจุบันดำรงตำแหน่งครู (ยังไม่มีวิทยฐานะ) ต้องแสดงให้เห็นถึงระดับการปฏิบัติที่คาดหวัง คือ การปรับประยุกต์ การจัดการเรียนรู้และการพัฒนาคุณภาพการเรียนรู้ของผู้เรียน ให้เกิดการเปลี่ยนแปลงไปในทางที่ดีขึ้นหรือมีการพัฒนามากขึ้น (ทั้งนี้ประเด็นท้าทายอาจจะแสดงให้เห็นถึงระดับการปฏิบัติที่คาดหวังที่สูงกว่าได้)", False)], align="left", first_line=720, space_before=0, space_after=80),

        # ชื่อประเด็นท้าทาย
        make_p_xml([
            ("ประเด็นท้าทาย เรื่อง ", True),
            ("การพัฒนาทักษะการเรียนรู้รายวิชาเทคโนโลยี (วิทยาการคำนวณ) กลุ่มสาระการเรียนรู้วิทยาศาสตร์และเทคโนโลยี โดยใช้กระบวนการ Game-based Learning ร่วมกับเทคนิค Active Learning ของนักเรียนชั้นประถมศึกษาปีที่ 5 โรงเรียนบ้านโนนป่าหว้านเชียงฮาย", True)
        ], align="left", first_line=720, space_before=60, space_after=120),

        # 1. สภาพปัญหา
        make_p_xml([("1. สภาพปัญหาการจัดการเรียนรู้และคุณภาพการเรียนรู้ของผู้เรียน", True)], align="left", space_before=120, space_after=60, keep_next=True),
        make_p_xml([
            ("จากการจัดการเรียนรู้ในรายวิชาวิทยาการคำนวณ และผลการประเมินคุณภาพผู้เรียนชั้นประถมศึกษาปีที่ 5 โรงเรียนบ้านโนนป่าหว้านเชียงฮาย ในปีการศึกษาที่ผ่านมา พบว่า สาระเทคโนโลยี (วิทยาการคำนวณ) หน่วยการเรียนรู้เรื่อง การใช้เหตุผลเชิงตรรกะและการเขียนโปรแกรมอย่างง่าย (ตามมาตรฐาน ว 4.2 ตัวชี้วัด ป.5/1 และ ป.5/2) มีเนื้อหาที่มีลักษณะเป็นนามธรรมและต้องใช้ทักษะการคิดเชิงตรรกะ ส่งผลให้ผู้เรียนส่วนใหญ่ยังขาดทักษะการวางแผนและการคิดอย่างเป็นขั้นตอน มักแก้ปัญหาแบบลองผิดลองถูก และยังสับสนเรื่องทิศทางและลำดับคำสั่งในการเขียนโปรแกรม ข้าพเจ้าในฐานะครูผู้สอนจึงได้กำหนดประเด็นท้าทายนี้ขึ้น โดยมีแนวคิดที่จะจัดการเรียนรู้เชิงรุก (Active Learning) นำกระบวนการเรียนรู้โดยใช้เกมเป็นฐาน (Game-based Learning) ร่วมกับสื่อเทคโนโลยี มาปรับประยุกต์ใช้เพื่อพัฒนาทักษะการคิดเชิงคำนวณและผลสัมฤทธิ์ทางการเรียนของผู้เรียนให้มีคุณภาพตามเกณฑ์มาตรฐาน", False)
        ], align="left", first_line=720, space_before=0, space_after=120),

        # 2. วิธีการดำเนินการให้บรรลุผล
        make_p_xml([("2. วิธีการดำเนินการให้บรรลุผล", True)], align="left", space_before=120, space_after=60, keep_next=True),
        make_p_xml([("เพื่อให้ประเด็นท้าทายนี้ประสบความสำเร็จ ครูผู้สอนดำเนินงานตามวงจรคุณภาพ (PDCA) ดังนี้", False)], align="left", first_line=720, space_before=0, space_after=60),

        make_p_xml([("ขั้นที่ 1: วางแผนและวิเคราะห์ข้อมูล (Plan)", True)], align="left", left_indent=720, space_before=40, space_after=20, keep_next=True),
        make_p_xml([("• ศึกษาหลักสูตรแกนกลางการศึกษาขั้นพื้นฐาน และตัวชี้วัด สาระเทคโนโลยี (วิทยาการคำนวณ) ชั้นประถมศึกษาปีที่ 5", False)], align="left", left_indent=1080, space_before=0, space_after=30),
        make_p_xml([("• วิเคราะห์เนื้อหาเรื่องการใช้เหตุผลเชิงตรรกะและการเขียนโปรแกรม ตลอดจนวิเคราะห์สภาพปัญหาและพื้นฐานการเรียนรู้ของผู้เรียน", False)], align="left", left_indent=1080, space_before=0, space_after=60),

        make_p_xml([("ขั้นที่ 2: สร้างและพัฒนาสื่อ/แผนการจัดการเรียนรู้ (Do)", True)], align="left", left_indent=720, space_before=40, space_after=20, keep_next=True),
        make_p_xml([("• ออกแบบและจัดทำแผนการจัดการเรียนรู้เชิงรุก (Active Learning) ที่เน้นให้ผู้เรียนได้ลงมือปฏิบัติจริง", False)], align="left", left_indent=1080, space_before=0, space_after=30),
        make_p_xml([("• พัฒนาสื่อนวัตกรรมการจัดการเรียนรู้โดยใช้เกมเป็นฐาน (Game-based Learning) ร่วมกับสื่อเทคโนโลยี และใบงานกิจกรรม", False)], align="left", left_indent=1080, space_before=0, space_after=30),
        make_p_xml([("• สร้างเครื่องมือวัดและประเมินผล ได้แก่ แบบทดสอบวัดผลสัมฤทธิ์ทางการเรียน และแบบประเมินทักษะการคิดเชิงคำนวณ", False)], align="left", left_indent=1080, space_before=0, space_after=60),

        make_p_xml([("ขั้นที่ 3: นำไปปฏิบัติและเก็บข้อมูล (Check)", True)], align="left", left_indent=720, space_before=40, space_after=20, keep_next=True),
        make_p_xml([("• นำแผนการจัดการเรียนรู้และสื่อนวัตกรรมไปจัดกิจกรรมการเรียนรู้กับนักเรียนชั้นประถมศึกษาปีที่ 5 ภาคเรียนที่ 1 ปีการศึกษา 2569", False)], align="left", left_indent=1080, space_before=0, space_after=30),
        make_p_xml([("• เน้นกระบวนการให้นักเรียนได้ร่วมกันคิด วางแผน แก้ไขปัญหา และฝึกปฏิบัติจริง", False)], align="left", left_indent=1080, space_before=0, space_after=30),
        make_p_xml([("• สังเกตพฤติกรรมการเรียนรู้ และประเมินพัฒนาการของผู้เรียนอย่างต่อเนื่อง", False)], align="left", left_indent=1080, space_before=0, space_after=60),

        make_p_xml([("ขั้นที่ 4: สรุปและสะท้อนผล (Act)", True)], align="left", left_indent=720, space_before=40, space_after=20, keep_next=True),
        make_p_xml([("• ดำเนินการทดสอบและประเมินผลการเรียนรู้ของผู้เรียน", False)], align="left", left_indent=1080, space_before=0, space_after=30),
        make_p_xml([("• นำผลลัพธ์มาวิเคราะห์ สรุปผลตามเป้าหมายที่ตั้งไว้ และนำข้อสะท้อนคิดมาปรับปรุงพัฒนาการจัดการเรียนรู้ หรือจัดกิจกรรมสอนซ่อมเสริมเพื่อช่วยเหลือนักเรียนต่อไป", False)], align="left", left_indent=1080, space_before=0, space_after=120),

        # 3. ผลลัพธ์การพัฒนาที่คาดหวัง
        make_p_xml([("3. ผลลัพธ์การพัฒนาที่คาดหวัง", True)], align="left", space_before=120, space_after=60, keep_next=True),

        make_p_xml([("3.1 ผลลัพธ์เชิงปริมาณ", True)], align="left", left_indent=720, space_before=20, space_after=20, keep_next=True),
        make_p_xml([("1) นักเรียนชั้นประถมศึกษาปีที่ 5 ไม่น้อยกว่าร้อยละ 70 มีผลสัมฤทธิ์ทางการเรียนรู้วิทยาการคำนวณหลังเรียนสูงกว่าก่อนเรียน", False)], align="left", left_indent=1080, space_before=0, space_after=30),
        make_p_xml([("2) นักเรียนชั้นประถมศึกษาปีที่ 5 ไม่น้อยกว่าร้อยละ 80 มีผลการประเมินทักษะการคิดเชิงคำนวณ ผ่านเกณฑ์ในระดับ “ดี” ขึ้นไป", False)], align="left", left_indent=1080, space_before=0, space_after=30),
        make_p_xml([("3) นักเรียนชั้นประถมศึกษาปีที่ 5 มีความพึงพอใจต่อการจัดกิจกรรมการเรียนรู้ อยู่ในระดับ “ดี” ขึ้นไป", False)], align="left", left_indent=1080, space_before=0, space_after=60),

        make_p_xml([("3.2 ผลลัพธ์เชิงคุณภาพ", True)], align="left", left_indent=720, space_before=20, space_after=20, keep_next=True),
        make_p_xml([("1) นักเรียนมีความรู้ความเข้าใจในหลักการแก้ปัญหาเชิงตรรกะ และสามารถเขียนโปรแกรมอย่างง่ายได้ตามลำดับขั้นตอนที่ถูกต้อง", False)], align="left", left_indent=1080, space_before=0, space_after=30),
        make_p_xml([("2) นักเรียนเกิดทักษะการคิดเชิงคำนวณ สามารถทำงานร่วมกับผู้อื่นได้อย่างมีประสิทธิภาพ และมีความสุขในการเรียนรู้", False)], align="left", left_indent=1080, space_before=0, space_after=120),
    ]
    sec2_all_xml = "".join(sec2_ps)

    # Locate start of Section 2 and start of signature in xml
    sec2_token = "ประเด็นที่ท้าทายในการพัฒนาผลลัพธ์การเรียนรู้ของผู้เรียนของผู้จัดทำข้อตกลง"
    sec2_pos = xml.find(sec2_token)
    assert sec2_pos != -1, "Could not find Section 2 start token in XML"
    sec2_p_start = max(xml.rfind("<w:p ", 0, sec2_pos), xml.rfind("<w:p>", 0, sec2_pos))

    sig_token = "ลงชื่อ........................................................................"
    sig_pos = xml.find(sig_token, sec2_pos)
    assert sig_pos != -1, "Could not find signature start in XML"
    sig_p_start = max(xml.rfind("<w:p ", 0, sig_pos), xml.rfind("<w:p>", 0, sig_pos))

    # Replace old Section 2 with new Section 2
    xml = xml[:sec2_p_start] + sec2_all_xml + xml[sig_p_start:]

    # -------------------------------------------------------------
    # 6. Fix Director Comment typo in signature block
    # -------------------------------------------------------------
    typo_str = "็็่ดหกวฟดบร"
    typo_pos = xml.find(typo_str)
    if typo_pos != -1:
        p_start = max(xml.rfind("<w:p ", 0, typo_pos), xml.rfind("<w:p>", 0, typo_pos))
        p_end = xml.find("</w:p>", typo_pos) + 6
        clean_dir_header_p = make_p_xml([("ความเห็นของผู้อำนวยการสถานศึกษา", True)], align="left", space_before=120, space_after=60)
        xml = xml[:p_start] + clean_dir_header_p + xml[p_end:]
        print("Director comment header typo successfully fixed!")

    # Validate XML against ECMA-376 schema rules before saving
    xml_bytes = xml.encode("utf-8")
    print("Validating XML against ECMA-376 rules...")
    validate_docx_xml(xml_bytes)

    file_map["word/document.xml"] = xml_bytes

    # Save to destination file
    with zipfile.ZipFile(dst_file, "w", compression=zipfile.ZIP_DEFLATED) as zout:
        for name, data in file_map.items():
            zout.writestr(name, data)
    print(f"Successfully created: {dst_file}")

    # Copy to docs/
    docs_copy = os.path.join("docs", dst_file)
    shutil.copy2(dst_file, docs_copy)
    print(f"Successfully copied to: {docs_copy}")

if __name__ == "__main__":
    build_docx()
