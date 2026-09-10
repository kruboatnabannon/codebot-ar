# -*- coding: utf-8 -*-
import os, zipfile, xml.etree.ElementTree as ET

def make_run(text, bold=False, sz=32):
    b_tag = '<w:b/><w:bCs/>' if bold else ''
    text = text.replace('\u200b', '')
    return f'<w:r><w:rPr><w:rFonts w:ascii="TH SarabunPSK" w:hAnsi="TH SarabunPSK" w:cs="TH SarabunPSK"/>{b_tag}<w:sz w:val="{sz}"/><w:szCs w:val="{sz}"/><w:lang w:val="th-TH"/></w:rPr><w:t xml:space="preserve">{text}</w:t></w:r>'

def make_p(runs, align="left", left_ind=0, hanging=0, first_line=0, space_before=0, space_after=40, keep_next=False):
    pPr_parts = []
    if keep_next:
        pPr_parts.append('<w:keepNext/>')
    pPr_parts.append(f'<w:spacing w:before="{space_before}" w:after="{space_after}" w:line="240" w:lineRule="auto"/>')
    
    ind_attrs = []
    if left_ind:
        ind_attrs.append(f'w:left="{left_ind}"')
    if hanging:
        ind_attrs.append(f'w:hanging="{hanging}"')
    if first_line:
        ind_attrs.append(f'w:firstLine="{first_line}"')
    if ind_attrs:
        pPr_parts.append(f'<w:ind {" ".join(ind_attrs)}/>')
        
    pPr_parts.append(f'<w:jc w:val="{align}"/>')
    pPr_parts.append('<w:rPr><w:rFonts w:ascii="TH SarabunPSK" w:hAnsi="TH SarabunPSK" w:cs="TH SarabunPSK"/><w:sz w:val="32"/><w:szCs w:val="32"/><w:lang w:val="th-TH"/></w:rPr>')
    
    pPr_str = f'<w:pPr>{"".join(pPr_parts)}</w:pPr>'
    r_str = ''.join([make_run(txt, b, sz) for (txt, b, *rest) in runs for sz in ([rest[0]] if rest else [32])])
    return f'<w:p>{pPr_str}{r_str}</w:p>'

def make_tc(p_xml_list, width, vAlign="top", shading=None):
    shd_xml = f'<w:shd w:val="clear" w:color="auto" w:fill="{shading}"/>' if shading else ''
    tcPr = f'''<w:tcPr>
        <w:tcW w:w="{width}" w:type="dxa"/>
        {shd_xml}
        <w:tcMar>
            <w:top w:w="120" w:type="dxa"/>
            <w:left w:w="140" w:type="dxa"/>
            <w:bottom w:w="120" w:type="dxa"/>
            <w:right w:w="140" w:type="dxa"/>
        </w:tcMar>
        <w:vAlign w:val="{vAlign}"/>
    </w:tcPr>'''
    return f'<w:tc>{tcPr}{"".join(p_xml_list)}</w:tc>'

# Col widths for A4 (total 9600 dxa)
w0 = 1700  # Col 0: ลักษณะงาน
w1 = 3300  # Col 1: งาน (Tasks)
w2 = 2300  # Col 2: ผลลัพธ์ (Outcomes)
w3 = 2300  # Col 3: ตัวชี้วัด (Indicators)

def make_table_header():
    hdr_c0 = make_tc([make_p([("ลักษณะงานที่ปฏิบัติ\nตามมาตรฐานตำแหน่ง", True)], align="center", space_after=0)], w0, vAlign="center", shading="F2F2F2")
    hdr_c1 = make_tc([make_p([("งาน (Tasks)", True), ("\nที่จะดำเนินการพัฒนาตามข้อตกลง\nใน 1 รอบการประเมิน\n(โปรดระบุ)", False)], align="center", space_after=0)], w1, vAlign="center", shading="F2F2F2")
    hdr_c2 = make_tc([make_p([("ผลลัพธ์ (Outcomes)", True), ("\nของงานตามข้อตกลง\nที่คาดหวังให้เกิดขึ้น\nกับผู้เรียน\n(โปรดระบุ)", False)], align="center", space_after=0)], w2, vAlign="center", shading="F2F2F2")
    hdr_c3 = make_tc([make_p([("ตัวชี้วัด (Indicators)", True), ("\nที่จะเกิดขึ้นกับผู้เรียน\nที่แสดงให้เห็นถึงการเปลี่ยนแปลงไปในทาง\nที่ดีขึ้นหรือมีการพัฒนา\nมากขึ้นหรือผลสัมฤทธิ์\nสูงขึ้น (โปรดระบุ)", False)], align="center", space_after=0)], w3, vAlign="center", shading="F2F2F2")
    
    return f'''<w:tr>
        <w:trPr>
            <w:tblHeader/>
            <w:cantSplit/>
        </w:trPr>
        {hdr_c0}{hdr_c1}{hdr_c2}{hdr_c3}
    </w:tr>'''

def build_table_xml(row_hdr, row_data):
    return f'''<w:tbl>
        <w:tblPr>
            <w:tblW w:w="9600" w:type="dxa"/>
            <w:jc w:val="center"/>
            <w:tblBorders>
                <w:top w:val="single" w:sz="4" w:space="0" w:color="auto"/>
                <w:left w:val="single" w:sz="4" w:space="0" w:color="auto"/>
                <w:bottom w:val="single" w:sz="4" w:space="0" w:color="auto"/>
                <w:right w:val="single" w:sz="4" w:space="0" w:color="auto"/>
                <w:insideH w:val="single" w:sz="4" w:space="0" w:color="auto"/>
                <w:insideV w:val="single" w:sz="4" w:space="0" w:color="auto"/>
            </w:tblBorders>
        </w:tblPr>
        <w:tblGrid>
            <w:gridCol w:w="{w0}"/>
            <w:gridCol w:w="{w1}"/>
            <w:gridCol w:w="{w2}"/>
            <w:gridCol w:w="{w3}"/>
        </w:tblGrid>
        {row_hdr}
        {row_data}
    </w:tbl>'''

# =========================================================================
# TABLE 1 (ด้านที่ 1)
# =========================================================================
t1_p_c0 = [
    make_p([("1. ด้านการจัดการเรียนรู้", True)], align="left", space_before=40, space_after=40),
    make_p([("ลักษณะงานที่เสนอให้ครอบคลุมถึงการสร้างและหรือพัฒนาหลักสูตร การออกแบบการจัดการเรียนรู้ การจัดกิจกรรมการเรียนรู้ การสร้างและหรือพัฒนาสื่อ นวัตกรรม เทคโนโลยี และแหล่งเรียนรู้ การวัดและประเมินผลการจัดการเรียนรู้ การศึกษา วิเคราะห์ สังเคราะห์เพื่อแก้ปัญหาหรือพัฒนาการเรียนรู้ การจัดบรรยากาศที่ส่งเสริมและพัฒนาผู้เรียน และการอบรมและพัฒนาคุณลักษณะที่ดีของผู้เรียน", False)], align="left", space_before=0, space_after=40)
]

t1_p_c1 = [
    make_p([("1.1 การสร้างและหรือพัฒนาหลักสูตร", True)], align="left", space_before=40, space_after=20),
    make_p([("- วิเคราะห์หลักสูตร มาตรฐานการเรียนรู้ และตัวชี้วัด นำไปจัดทำรายวิชาและหน่วยการเรียนรู้ ให้สอดคล้องกับหลักสูตรแกนกลางฯ และหลักสูตรสถานศึกษา โดยปรับประยุกต์ให้สอดคล้องกับบริบทของสถานศึกษาและผู้เรียน", False)], align="left", left_ind=240, hanging=240, space_before=0, space_after=60),

    make_p([("1.2 ออกแบบการจัดการเรียนรู้", True)], align="left", space_before=40, space_after=20),
    make_p([("- จัดทำแผนการจัดการเรียนรู้เชิงรุก (Active Learning) ในรายวิชาเทคโนโลยี (วิทยาการคำนวณ) ที่เน้นผู้เรียนเป็นสำคัญ โดยนำกระบวนการเรียนรู้โดยใช้เกมเป็นฐาน (Game-based Learning) มาปรับประยุกต์ใช้ในการจัดกิจกรรม", False)], align="left", left_ind=240, hanging=240, space_before=0, space_after=60),

    make_p([("1.3 การจัดกิจกรรมการเรียนรู้", True)], align="left", space_before=40, space_after=20),
    make_p([("- จัดกิจกรรมการเรียนรู้เชิงรุก (Active Learning) ในรายวิชาเทคโนโลยี (วิทยาการคำนวณ) โดยมีการปรับประยุกต์กิจกรรมการเรียนรู้ อำนวยความสะดวกในการเรียนรู้ และส่งเสริมให้ผู้เรียนได้พัฒนาเต็มตามศักยภาพ เรียนรู้และทำงานร่วมกัน มีกระบวนการคิดและค้นพบองค์ความรู้ด้วยตนเอง", False)], align="left", left_ind=240, hanging=240, space_before=0, space_after=60),

    make_p([("1.4 สร้างและหรือพัฒนาสื่อ นวัตกรรม เทคโนโลยี และแหล่งเรียนรู้", True)], align="left", space_before=40, space_after=20),
    make_p([("- สร้างและพัฒนาสื่อ นวัตกรรม เทคโนโลยี และแหล่งเรียนรู้ที่สอดคล้องกับกิจกรรมการเรียนรู้ ในรายวิชาเทคโนโลยี (วิทยาการคำนวณ) ทั้งสื่อดิจิทัล สื่อกิจกรรมการเรียนรู้ และสื่อเกมจำลองภารกิจ โดยมีการปรับประยุกต์ให้เหมาะสมกับความแตกต่างของผู้เรียน ทำให้ผู้เรียนมีทักษะการคิดและสามารถเรียนรู้ได้อย่างมีประสิทธิภาพ", False)], align="left", left_ind=240, hanging=240, space_before=0, space_after=60),

    make_p([("1.5 การวัดและประเมินผลการเรียนรู้", True)], align="left", space_before=40, space_after=20),
    make_p([("- พัฒนารูปแบบการวัดและประเมินผลการเรียนรู้ตามสภาพจริงที่หลากหลายและเหมาะสม ได้แก่ 1) แบบทดสอบ 2) แบบสังเกตพฤติกรรม 3) แบบประเมินชิ้นงาน/ภาระงาน 4) แบบประเมินความพึงพอใจ และนำผลการวัดและประเมินผลมาใช้ในการปรับประยุกต์แก้ไขปัญหาและพัฒนาการจัดการเรียนรู้", False)], align="left", left_ind=240, hanging=240, space_before=0, space_after=60),

    make_p([("1.6 ศึกษา วิเคราะห์ และสังเคราะห์ เพื่อแก้ไขปัญหาหรือพัฒนาการเรียนรู้", True)], align="left", space_before=40, space_after=20),
    make_p([("- ศึกษา วิเคราะห์ และสังเคราะห์ปัญหาการจัดการเรียนรู้ของผู้เรียนเป็นรายบุคคลอย่างเป็นระบบ จัดทำวิจัยปฏิบัติการในชั้นเรียน เรื่อง การจัดการเรียนรู้โดยใช้เกมเป็นฐาน (Game-based Learning) เพื่อนำผลมาปรับประยุกต์ใช้ในการแก้ปัญหาและพัฒนาการเรียนรู้ของผู้เรียน", False)], align="left", left_ind=240, hanging=240, space_before=0, space_after=60),

    make_p([("1.7 จัดบรรยากาศที่ส่งเสริมและพัฒนาผู้เรียน", True)], align="left", space_before=40, space_after=20),
    make_p([("- ปรับประยุกต์การจัดบรรยากาศในชั้นเรียนให้เหมาะสมกับวัยและความแตกต่างของผู้เรียน ส่งเสริมให้เกิดความสนุกสนาน กระตุ้นความสนใจ สร้างแรงบันดาลใจ และเปิดโอกาสให้ผู้เรียนทุกคนได้มีส่วนร่วมและแสดงความคิดเห็นอย่างสร้างสรรค์", False)], align="left", left_ind=240, hanging=240, space_before=0, space_after=60),

    make_p([("1.8 อบรมและพัฒนาคุณลักษณะที่ดีของผู้เรียน", True)], align="left", space_before=40, space_after=20),
    make_p([("- อบรมบ่มนิสัยให้ผู้เรียนมีคุณธรรม จริยธรรม คุณลักษณะอันพึงประสงค์ และค่านิยมความเป็นไทยที่ดีงาม ผ่านกิจกรรมพัฒนาผู้เรียน กิจกรรมแนะแนว และกิจกรรมโฮมรูมของนักเรียนชั้นมัธยมศึกษาปีที่ 2 ตลอดจนสอดแทรกในการจัดกิจกรรมการเรียนรู้ทุกระดับชั้นที่สอน", False)], align="left", left_ind=240, hanging=240, space_before=0, space_after=40)
]

t1_p_c2 = [
    make_p([("1. ผู้เรียนได้เรียนรู้ตรงตามหลักสูตร มาตรฐานการเรียนรู้ และตัวชี้วัดที่กำหนดอย่างมีประสิทธิภาพ", False)], align="left", left_ind=240, hanging=240, space_before=40, space_after=50),
    make_p([("2. ผู้เรียนได้เรียนรู้ตามหน่วยการเรียนรู้และแผนการจัดการเรียนรู้ที่มีคุณภาพ และได้รับการพัฒนาสมรรถนะสำคัญตามหลักสูตร", False)], align="left", left_ind=240, hanging=240, space_before=0, space_after=50),
    make_p([("3. ผู้เรียนได้รับการจัดกิจกรรมการเรียนรู้เชิงรุก (Active Learning) ได้ฝึกคิดและลงมือปฏิบัติจริง เรียนรู้อย่างมีความสุข", False)], align="left", left_ind=240, hanging=240, space_before=0, space_after=50),
    make_p([("4. ผู้เรียนได้รับการพัฒนาทักษะการเรียนรู้ผ่านสื่อ นวัตกรรม และเทคโนโลยีที่หลากหลายและมีประสิทธิภาพ", False)], align="left", left_ind=240, hanging=240, space_before=0, space_after=50),
    make_p([("5. ผู้เรียนได้รับการวัดและประเมินผลตามสภาพจริงด้วยเครื่องมือที่น่าเชื่อถือ สะท้อนผลสัมฤทธิ์ทางการเรียนรู้ที่แท้จริง", False)], align="left", left_ind=240, hanging=240, space_before=0, space_after=50),
    make_p([("6. ผู้เรียนได้รับการแก้ไขปัญหาและพัฒนาการเรียนรู้อย่างเป็นระบบผ่านกระบวนการวิจัยปฏิบัติการในชั้นเรียน", False)], align="left", left_ind=240, hanging=240, space_before=0, space_after=50),
    make_p([("7. ผู้เรียนมีส่วนร่วมในการจัดบรรยากาศในชั้นเรียน มีความสุข กระตือรือร้น และมีเจตคติที่ดีต่อการเรียนรู้", False)], align="left", left_ind=240, hanging=240, space_before=0, space_after=50),
    make_p([("8. ผู้เรียนและนักเรียนชั้นมัธยมศึกษาปีที่ 2 เป็นผู้มีคุณลักษณะอันพึงประสงค์ที่ดีงามทั้งต่อตนเอง โรงเรียน และสังคม", False)], align="left", left_ind=240, hanging=240, space_before=0, space_after=40)
]

t1_p_c3 = [
    make_p([("1. ผู้เรียนร้อยละ 70 มีความรู้ตามตัวชี้วัดที่ต้องรู้ในรายวิชาเทคโนโลยี (วิทยาการคำนวณ) ตรงตามหลักสูตรที่กำหนด", False)], align="left", left_ind=240, hanging=240, space_before=40, space_after=50),
    make_p([("2. ผู้เรียนร้อยละ 70 มีความรู้และทักษะตามตัวชี้วัด และมีคุณลักษณะอันพึงประสงค์ตามที่สถานศึกษากำหนด", False)], align="left", left_ind=240, hanging=240, space_before=0, space_after=50),
    make_p([("3. ผู้เรียนร้อยละ 70 ได้เรียนรู้อย่างมีความสุข และมีความรู้ความเข้าใจตามตัวชี้วัดตรงตามหลักสูตร", False)], align="left", left_ind=240, hanging=240, space_before=0, space_after=50),
    make_p([("4. ผู้เรียนร้อยละ 70 เกิดทักษะ 4 Cs (การคิดวิพากษ์ การทำงานร่วมกัน การสื่อสาร และความคิดสร้างสรรค์) ส่งผลให้มีสมรรถนะตรงตามหลักสูตร", False)], align="left", left_ind=240, hanging=240, space_before=0, space_after=50),
    make_p([("5. ผู้เรียนร้อยละ 70 มีผลสัมฤทธิ์ทางการเรียนผ่านตามเกณฑ์ที่สถานศึกษากำหนดไว้ทุกตัวชี้วัด", False)], align="left", left_ind=240, hanging=240, space_before=0, space_after=50),
    make_p([("6. ผู้เรียนร้อยละ 70 มีผลการพัฒนาจากการวิจัยในชั้นเรียนเพิ่มขึ้นตามเกณฑ์ที่กำหนดไว้", False)], align="left", left_ind=240, hanging=240, space_before=0, space_after=50),
    make_p([("7. ผู้เรียนร้อยละ 80 มีความสนใจ กระตือรือร้นในการร่วมกิจกรรมการเรียนรู้ และมีความสุขในการเรียน", False)], align="left", left_ind=240, hanging=240, space_before=0, space_after=50),
    make_p([("8. ผู้เรียนร้อยละ 100 มีคุณลักษณะอันพึงประสงค์ตามที่สถานศึกษากำหนดไว้", False)], align="left", left_ind=240, hanging=240, space_before=0, space_after=40)
]

row_t1 = f'<w:tr><w:trPr><w:cantSplit/></w:trPr>{make_tc(t1_p_c0, w0)}{make_tc(t1_p_c1, w1)}{make_tc(t1_p_c2, w2)}{make_tc(t1_p_c3, w3)}</w:tr>'
tbl1_xml = build_table_xml(make_table_header(), row_t1)

# =========================================================================
# TABLE 2 (ด้านที่ 2)
# =========================================================================
t2_p_c0 = [
    make_p([("2. ด้านการส่งเสริมและสนับสนุนการจัดการเรียนรู้", True)], align="left", space_before=40, space_after=40),
    make_p([("ลักษณะงานที่เสนอให้ครอบคลุมถึงการจัดทำข้อมูลสารสนเทศของผู้เรียนและรายวิชาการดำเนินการตามระบบ ดูแลช่วยเหลือผู้เรียน การปฏิบัติงานวิชาการและงานอื่น ๆ ของสถานศึกษา และการประสานความร่วมมือกับผู้ปกครอง ภาคีเครือข่าย และหรือสถานประกอบการ", False)], align="left", space_before=0, space_after=40)
]

t2_p_c1 = [
    make_p([("2.1 จัดทำข้อมูลสารสนเทศของผู้เรียนและรายวิชา", True)], align="left", space_before=40, space_after=20),
    make_p([("- จัดทำข้อมูลในระบบสารสนเทศของนักเรียนชั้นมัธยมศึกษาปีที่ 2 และข้อมูลสารสนเทศในรายวิชาที่ทำการสอน เอกสารงานประจำชั้น และแบบ ปพ. ต่างๆ อย่างเป็นระบบ ถูกต้อง เป็นปัจจุบัน และสะดวกต่อการใช้งาน", False)], align="left", left_ind=240, hanging=240, space_before=0, space_after=60),

    make_p([("2.2 ดำเนินการตามระบบดูแลช่วยเหลือผู้เรียน", True)], align="left", space_before=40, space_after=20),
    make_p([("- ดำเนินการตามระบบดูแลช่วยเหลือผู้เรียนอย่างเป็นระบบ มีการคัดกรองนักเรียน ออกเยี่ยมบ้านนักเรียนชั้นมัธยมศึกษาปีที่ 2 อย่างน้อยภาคเรียนละ 1 ครั้ง และประสานความร่วมมือกับผู้เกี่ยวข้องเพื่อแก้ไขปัญหาและพัฒนาผู้เรียน", False)], align="left", left_ind=240, hanging=240, space_before=0, space_after=60),

    make_p([("2.3 ปฏิบัติงานวิชาการและงานอื่นๆ ของสถานศึกษา", True)], align="left", space_before=40, space_after=20),
    make_p([("- ร่วมปฏิบัติงานทางวิชาการ และงานอื่นๆ ของสถานศึกษา เพื่อยกระดับคุณภาพการจัดการศึกษาของสถานศึกษา โดยมีการปรับประยุกต์รูปแบบหรือแนวทางการดำเนินงานให้มีประสิทธิภาพ เช่น งานบริหารงานทั่วไป งานพัฒนาหลักสูตร งานวัดผลประเมินผล และโครงการพัฒนา ICT ในโรงเรียน", False)], align="left", left_ind=240, hanging=240, space_before=0, space_after=60),

    make_p([("2.4 ประสานความร่วมมือกับผู้ปกครอง ภาคีเครือข่าย และหรือสถานประกอบการ", True)], align="left", space_before=40, space_after=20),
    make_p([("- มีการประสานความร่วมมือกับผู้ปกครองและภาคีเครือข่าย เพื่อร่วมกันแก้ไขปัญหาและพัฒนาผู้เรียน โดยร่วมประชุมผู้ปกครองภาคเรียนละ 1 ครั้ง และประสานความร่วมมือในการดูแลช่วยเหลือนักเรียนอย่างต่อเนื่อง", False)], align="left", left_ind=240, hanging=240, space_before=0, space_after=40)
]

t2_p_c2 = [
    make_p([("1. ผู้เรียนมีระบบข้อมูลสารสนเทศที่สมบูรณ์ สะดวกต่อการใช้งานและมีประสิทธิภาพ สามารถนำข้อมูลมาใช้ในการส่งเสริมและพัฒนาได้อย่างทันท่วงที", False)], align="left", left_ind=240, hanging=240, space_before=40, space_after=50),
    make_p([("2. นักเรียนชั้นมัธยมศึกษาปีที่ 2 มีข้อมูลพื้นฐานเป็นรายบุคคล และได้รับการดูแลช่วยเหลือในเรื่องต่างๆ จากข้อมูลการคัดกรอง การเยี่ยมบ้าน และการจัดหาทุนการศึกษาสำหรับนักเรียนยากจน", False)], align="left", left_ind=240, hanging=240, space_before=0, space_after=50),
    make_p([("3. ผู้เรียนได้เรียนรู้ในกิจกรรมที่หลากหลายตามโครงการและกิจกรรมที่สถานศึกษาได้กำหนดขึ้นตลอดปีการศึกษา", False)], align="left", left_ind=240, hanging=240, space_before=0, space_after=50),
    make_p([("4. ผู้เรียนได้รับการดูแลช่วยเหลือจากผู้ปกครองและภาคีเครือข่ายที่เกี่ยวข้องอย่างเป็นระบบและต่อเนื่อง", False)], align="left", left_ind=240, hanging=240, space_before=0, space_after=40)
]

t2_p_c3 = [
    make_p([("1. ผู้เรียนร้อยละ 100 มีข้อมูลในระบบสารสนเทศครบถ้วนในทุกด้าน เป็นระบบและเป็นรายบุคคล", False)], align="left", left_ind=240, hanging=240, space_before=40, space_after=50),
    make_p([("2. นักเรียนชั้นมัธยมศึกษาปีที่ 2 ร้อยละ 100 ได้รับการดูแลเอาใจใส่ตรงตามความต้องการรายบุคคล และมีความสัมพันธ์อันดีระหว่างครูและนักเรียน", False)], align="left", left_ind=240, hanging=240, space_before=0, space_after=50),
    make_p([("3. ผู้เรียนร้อยละ 70 ได้รับการพัฒนาและมีส่วนร่วมในกิจกรรมทางวิชาการและโครงการที่โรงเรียนจัดขึ้น", False)], align="left", left_ind=240, hanging=240, space_before=0, space_after=50),
    make_p([("4. ผู้เรียนร้อยละ 100 ได้รับการดูแลช่วยเหลือ ประสานความร่วมมือกับผู้ปกครอง ทำให้ผู้เรียนมีคุณภาพชีวิตที่ดีขึ้น และมีผลสัมฤทธิ์ทางการเรียนสูงขึ้น", False)], align="left", left_ind=240, hanging=240, space_before=0, space_after=40)
]

row_t2 = f'<w:tr><w:trPr><w:cantSplit/></w:trPr>{make_tc(t2_p_c0, w0)}{make_tc(t2_p_c1, w1)}{make_tc(t2_p_c2, w2)}{make_tc(t2_p_c3, w3)}</w:tr>'
tbl2_xml = build_table_xml(make_table_header(), row_t2)

# =========================================================================
# TABLE 3 (ด้านที่ 3)
# =========================================================================
t3_p_c0 = [
    make_p([("3. ด้านการพัฒนาตนเองและวิชาชีพ", True)], align="left", space_before=40, space_after=40),
    make_p([("ลักษณะงานที่เสนอให้ครอบคลุมถึงการพัฒนาตนเองอย่างเป็นระบบและต่อเนื่อง การมีส่วนร่วมในการแลกเปลี่ยนเรียนรู้ทางวิชาชีพเพื่อพัฒนาการจัดการเรียนรู้และการนำความรู้ความสามารถทักษะที่ได้จากการพัฒนาตนเองและวิชาชีพมาใช้ในการพัฒนาการจัดการเรียนรู้ การพัฒนาคุณภาพผู้เรียน และการพัฒนานวัตกรรมการจัดการเรียนรู้", False)], align="left", space_before=0, space_after=40)
]

t3_p_c1 = [
    make_p([("3.1 พัฒนาตนเองอย่างเป็นระบบและต่อเนื่อง", True)], align="left", space_before=40, space_after=20),
    make_p([("- พัฒนาตนเองอย่างเป็นระบบและต่อเนื่อง โดยการเข้าอบรม ประชุมเชิงปฏิบัติการ และสัมมนาตลอดปีงบประมาณ 2569 ในสาขาวิชาและสมรรถนะวิชาชีพ โดยเฉพาะการจัดการเรียนรู้วิทยาการคำนวณและเทคโนโลยีดิจิทัล ทั้งรูปแบบ Onsite และ Online เพื่อนำมาพัฒนาสื่อและกิจกรรมการเรียนรู้", False)], align="left", left_ind=240, hanging=240, space_before=0, space_after=60),

    make_p([("3.2 มีส่วนร่วมในการแลกเปลี่ยนเรียนรู้ทางวิชาชีพเพื่อพัฒนาการจัดการเรียนรู้", True)], align="left", space_before=40, space_after=20),
    make_p([("- เข้าร่วมกิจกรรมชุมชนการเรียนรู้ทางวิชาชีพ (PLC) เพื่อร่วมแลกเปลี่ยนเรียนรู้ สะท้อนคิด ปรึกษาหารือในการแก้ไขปัญหาการเรียนรู้ของผู้เรียน และร่วมกันสร้างหรือพัฒนานวัตกรรมการจัดการเรียนรู้", False)], align="left", left_ind=240, hanging=240, space_before=0, space_after=60),

    make_p([("3.3 นำความรู้ ความสามารถ ทักษะที่ได้จากการพัฒนาตนเองและวิชาชีพมาใช้", True)], align="left", space_before=40, space_after=20),
    make_p([("- นำความรู้ ความสามารถ ทักษะ และนวัตกรรมที่ได้จากการพัฒนาตนเองและการเข้าร่วม PLC มาปรับประยุกต์ใช้ในการพัฒนาการจัดการเรียนรู้ การพัฒนาคุณภาพผู้เรียน และการพัฒนานวัตกรรมการจัดการเรียนรู้ในรายวิชาวิทยาการคำนวณ", False)], align="left", left_ind=240, hanging=240, space_before=0, space_after=40)
]

t3_p_c2 = [
    make_p([("1. ผู้เรียนได้รับการจัดกิจกรรมการเรียนรู้ที่เน้นผู้เรียนเป็นสำคัญ มีกิจกรรมที่หลากหลายเหมาะสมตามความแตกต่างระหว่างบุคคล ทำให้ผู้เรียนมีผลสัมฤทธิ์ทางการเรียนที่ดีขึ้น", False)], align="left", left_ind=240, hanging=240, space_before=40, space_after=50),
    make_p([("2. ผู้เรียนได้รับการแก้ไขปัญหาในการเรียนรู้ได้อย่างเหมาะสมตามความแตกต่างระหว่างบุคคล และได้รับการพัฒนาจากสื่อนวัตกรรมการจัดการเรียนรู้ที่ครูได้พัฒนาขึ้น", False)], align="left", left_ind=240, hanging=240, space_before=0, space_after=50),
    make_p([("3. ผู้เรียนได้รับการพัฒนาทักษะกระบวนการเรียนรู้และสมรรถนะสำคัญ จากการนำความรู้และนวัตกรรมที่ได้จากกระบวนการ PLC มาปรับประยุกต์ใช้ในชั้นเรียน", False)], align="left", left_ind=240, hanging=240, space_before=0, space_after=40)
]

t3_p_c3 = [
    make_p([("1. ผู้เรียนร้อยละ 70 ได้รับการจัดกิจกรรมการเรียนรู้ด้วยวิธีการที่หลากหลายและเหมาะสมกับเนื้อหา ส่งผลให้มีผลสัมฤทธิ์ทางการเรียนสูงขึ้น", False)], align="left", left_ind=240, hanging=240, space_before=40, space_after=50),
    make_p([("2. ผู้เรียนร้อยละ 70 ได้รับการแก้ไขปัญหาทางการเรียนรู้และปัญหาอื่นๆ อย่างต่อเนื่อง เป็นระบบ และมีผลการเรียนรู้ที่ดีขึ้น", False)], align="left", left_ind=240, hanging=240, space_before=0, space_after=50),
    make_p([("3. ผู้เรียนร้อยละ 70 มีความพึงพอใจและมีเจตคติที่ดีต่อการจัดกิจกรรมการเรียนรู้ด้วยสื่อนวัตกรรมที่ครูนำมาปรับประยุกต์ใช้", False)], align="left", left_ind=240, hanging=240, space_before=0, space_after=40)
]

row_t3 = f'<w:tr><w:trPr><w:cantSplit/></w:trPr>{make_tc(t3_p_c0, w0)}{make_tc(t3_p_c1, w1)}{make_tc(t3_p_c2, w2)}{make_tc(t3_p_c3, w3)}</w:tr>'
tbl3_xml = build_table_xml(make_table_header(), row_t3)

# =========================================================================
# Pack into DOCX
# =========================================================================
with zipfile.ZipFile('แบบข้อตกลงในการพัฒนางาน 69_backup.docx') as z:
    base_file_map = {name: z.read(name) for name in z.namelist()}

sectPr = '''<w:sectPr>
    <w:pgSz w:w="11906" w:h="16838"/>
    <w:pgMar w:top="1134" w:right="1134" w:bottom="1134" w:left="1134" w:header="720" w:footer="720" w:gutter="0"/>
    <w:cols w:space="720"/>
    <w:docGrid w:linePitch="360"/>
</w:sectPr>'''

def save_docx(body_xml, filename):
    full_xml = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
            xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
            xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"
            xmlns:v="urn:schemas-microsoft-com:vml"
            xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
            xmlns:w10="urn:schemas-microsoft-com:office:word"
            xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
            xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">
    <w:body>
        {body_xml}
        {sectPr}
    </w:body>
</w:document>'''
    fmap = dict(base_file_map)
    fmap["word/document.xml"] = full_xml.encode("utf-8")
    
    with zipfile.ZipFile(filename, "w", compression=zipfile.ZIP_DEFLATED) as zout:
        for name, data in fmap.items():
            zout.writestr(name, data)
    print(f"Created: {filename}")
    
    # copy to docs/
    docs_copy = os.path.join("docs", filename)
    with zipfile.ZipFile(docs_copy, "w", compression=zipfile.ZIP_DEFLATED) as zout:
        for name, data in fmap.items():
            zout.writestr(name, data)
    print(f"Copied to: {docs_copy}")

page_break_p = '<w:p><w:r><w:br w:type="page"/></w:r></w:p>'

# 1. Standalone Table 2 & 3
doc23_title = make_p([("ตารางที่ 2 และ 3 ด้านการส่งเสริมฯ และด้านการพัฒนาตนเองและวิชาชีพ (ว PA)", True, 36)], align="center", space_before=120, space_after=80)
doc23_sub = make_p([("(จัดฟอนต์ TH Sarabun PSK 16 pt ชิดซ้าย ไม่ยืดห่าง ก๊อปปี้ไปวางในไฟล์ PA 1 ได้ทันที)", False, 28)], align="center", space_before=0, space_after=160)

body_23 = f"{doc23_title}{doc23_sub}{tbl2_xml}{page_break_p}{tbl3_xml}"
save_docx(body_23, "ตารางที่2และ3_วPA_ฉบับก๊อปวาง.docx")

# 2. Standalone All Tables (Table 1, 2, 3)
doc_all_title = make_p([("แบบข้อตกลงในการพัฒนางาน (PA) - รวมตารางมาตรฐานตำแหน่งครบทั้ง 3 ด้าน", True, 36)], align="center", space_before=120, space_after=80)
doc_all_sub = make_p([("(รวมตารางที่ 1, 2 และ 3 จัดฟอนต์ TH Sarabun PSK 16 pt ชิดซ้าย เรียงชิดสวยงาม ไม่แตกห่าง)", False, 28)], align="center", space_before=0, space_after=160)

body_all = f"{doc_all_title}{doc_all_sub}{tbl1_xml}{page_break_p}{tbl2_xml}{page_break_p}{tbl3_xml}"
save_docx(body_all, "รวมตาราง_วPA_ด้านที่1_2_3_ครบทุกด้าน_ฉบับก๊อปวาง.docx")
