import os, zipfile, xml.etree.ElementTree as ET

def make_run(text, bold=False, sz=32):
    b_tag = '<w:b/><w:bCs/>' if bold else ''
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

# Read base template
with zipfile.ZipFile('แบบข้อตกลงในการพัฒนางาน 69_backup.docx') as z:
    file_map = {name: z.read(name) for name in z.namelist()}

# Col widths for A4 (total 9600 dxa)
w0 = 1700  # Col 0: ลักษณะงาน
w1 = 3300  # Col 1: งาน (Tasks)
w2 = 2300  # Col 2: ผลลัพธ์ (Outcomes)
w3 = 2300  # Col 3: ตัวชี้วัด (Indicators)

# Header Row
hdr_c0 = make_tc([make_p([("ลักษณะงานที่ปฏิบัติตามมาตรฐานตำแหน่ง", True)], align="center", space_after=0)], w0, vAlign="center", shading="F2F2F2")
hdr_c1 = make_tc([make_p([("งาน (Tasks)", True), ("\nที่จะดำเนินการพัฒนาตามข้อตกลงใน 1 รอบการประเมิน\n(โปรดระบุ)", False)], align="center", space_after=0)], w1, vAlign="center", shading="F2F2F2")
hdr_c2 = make_tc([make_p([("ผลลัพธ์ (Outcomes)", True), ("\nของงานตามข้อตกลงที่คาดหวังให้เกิดขึ้นกับผู้เรียน\n(โปรดระบุ)", False)], align="center", space_after=0)], w2, vAlign="center", shading="F2F2F2")
hdr_c3 = make_tc([make_p([("ตัวชี้วัด (Indicators)", True), ("\nที่จะเกิดขึ้นกับผู้เรียน ที่แสดงให้เห็นถึงการเปลี่ยนแปลงไปในทางที่ดีขึ้นหรือมีการพัฒนามากขึ้นหรือผลสัมฤทธิ์สูงขึ้น (โปรดระบุ)", False)], align="center", space_after=0)], w3, vAlign="center", shading="F2F2F2")

row_hdr = f'''<w:tr>
    <w:trPr>
        <w:tblHeader/>
        <w:cantSplit/>
    </w:trPr>
    {hdr_c0}{hdr_c1}{hdr_c2}{hdr_c3}
</w:tr>'''

# Data Row
# Col 0: ด้านการจัดการเรียนรู้
p_c0 = [
    make_p([("1. ด้านการจัดการเรียนรู้", True)], align="left", space_before=40, space_after=40),
    make_p([("ลักษณะงานที่เสนอให้ครอบคลุมถึงการสร้างและหรือพัฒนาหลักสูตร การออกแบบการจัดการเรียนรู้ การจัดกิจกรรมการเรียนรู้ การสร้างและหรือพัฒนาสื่อ นวัตกรรม เทคโนโลยี และแหล่งเรียนรู้ การวัดและประเมินผลการจัดการเรียนรู้ การศึกษา วิเคราะห์ สังเคราะห์เพื่อแก้ปัญหาหรือพัฒนาการเรียนรู้ การจัดบรรยากาศที่ส่งเสริมและพัฒนาผู้เรียน และการอบรมและพัฒนาคุณลักษณะที่ดีของผู้เรียน", False)], align="left", space_before=0, space_after=40)
]

# Col 1: Tasks 1.1 - 1.8
p_c1 = [
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

# Col 2: Outcomes 1 - 8
p_c2 = [
    make_p([("1. ผู้เรียนได้เรียนรู้ตรงตามหลักสูตร มาตรฐานการเรียนรู้ และตัวชี้วัดที่กำหนดอย่างมีประสิทธิภาพ", False)], align="left", left_ind=240, hanging=240, space_before=40, space_after=50),
    make_p([("2. ผู้เรียนได้เรียนรู้ตามหน่วยการเรียนรู้และแผนการจัดการเรียนรู้ที่มีคุณภาพ และได้รับการพัฒนาสมรรถนะสำคัญตามหลักสูตร", False)], align="left", left_ind=240, hanging=240, space_before=0, space_after=50),
    make_p([("3. ผู้เรียนได้รับการจัดกิจกรรมการเรียนรู้เชิงรุก (Active Learning) ได้ฝึกคิดและลงมือปฏิบัติจริง เรียนรู้อย่างมีความสุข", False)], align="left", left_ind=240, hanging=240, space_before=0, space_after=50),
    make_p([("4. ผู้เรียนได้รับการพัฒนาทักษะการเรียนรู้ผ่านสื่อ นวัตกรรม และเทคโนโลยีที่หลากหลายและมีประสิทธิภาพ", False)], align="left", left_ind=240, hanging=240, space_before=0, space_after=50),
    make_p([("5. ผู้เรียนได้รับการวัดและประเมินผลตามสภาพจริงด้วยเครื่องมือที่น่าเชื่อถือ สะท้อนผลสัมฤทธิ์ทางการเรียนรู้ที่แท้จริง", False)], align="left", left_ind=240, hanging=240, space_before=0, space_after=50),
    make_p([("6. ผู้เรียนได้รับการแก้ไขปัญหาและพัฒนาการเรียนรู้อย่างเป็นระบบผ่านกระบวนการวิจัยปฏิบัติการในชั้นเรียน", False)], align="left", left_ind=240, hanging=240, space_before=0, space_after=50),
    make_p([("7. ผู้เรียนมีส่วนร่วมในการจัดบรรยากาศในชั้นเรียน มีความสุข กระตือรือร้น และมีเจตคติที่ดีต่อการเรียนรู้", False)], align="left", left_ind=240, hanging=240, space_before=0, space_after=50),
    make_p([("8. ผู้เรียนและนักเรียนชั้นมัธยมศึกษาปีที่ 2 เป็นผู้มีคุณลักษณะอันพึงประสงค์ที่ดีงามทั้งต่อตนเอง โรงเรียน และสังคม", False)], align="left", left_ind=240, hanging=240, space_before=0, space_after=40)
]

# Col 3: Indicators 1 - 8
p_c3 = [
    make_p([("1. ผู้เรียนร้อยละ 70 มีความรู้ตามตัวชี้วัดที่ต้องรู้ในรายวิชาเทคโนโลยี (วิทยาการคำนวณ) ตรงตามหลักสูตรที่กำหนด", False)], align="left", left_ind=240, hanging=240, space_before=40, space_after=50),
    make_p([("2. ผู้เรียนร้อยละ 70 มีความรู้และทักษะตามตัวชี้วัด และมีคุณลักษณะอันพึงประสงค์ตามที่สถานศึกษากำหนด", False)], align="left", left_ind=240, hanging=240, space_before=0, space_after=50),
    make_p([("3. ผู้เรียนร้อยละ 70 ได้เรียนรู้อย่างมีความสุข และมีความรู้ความเข้าใจตามตัวชี้วัดตรงตามหลักสูตร", False)], align="left", left_ind=240, hanging=240, space_before=0, space_after=50),
    make_p([("4. ผู้เรียนร้อยละ 70 เกิดทักษะ 4 Cs (การคิดวิพากษ์ การทำงานร่วมกัน การสื่อสาร และความคิดสร้างสรรค์) ส่งผลให้มีสมรรถนะตรงตามหลักสูตร", False)], align="left", left_ind=240, hanging=240, space_before=0, space_after=50),
    make_p([("5. ผู้เรียนร้อยละ 70 มีผลสัมฤทธิ์ทางการเรียนผ่านตามเกณฑ์ที่สถานศึกษากำหนดไว้ทุกตัวชี้วัด", False)], align="left", left_ind=240, hanging=240, space_before=0, space_after=50),
    make_p([("6. ผู้เรียนร้อยละ 70 มีผลการพัฒนาจากการวิจัยในชั้นเรียนเพิ่มขึ้นตามเกณฑ์ที่กำหนดไว้", False)], align="left", left_ind=240, hanging=240, space_before=0, space_after=50),
    make_p([("7. ผู้เรียนร้อยละ 80 มีความสนใจ กระตือรือร้นในการร่วมกิจกรรมการเรียนรู้ และมีความสุขในการเรียน", False)], align="left", left_ind=240, hanging=240, space_before=0, space_after=50),
    make_p([("8. ผู้เรียนร้อยละ 100 มีคุณลักษณะอันพึงประสงค์ตามที่สถานศึกษากำหนดไว้", False)], align="left", left_ind=240, hanging=240, space_before=0, space_after=40)
]

data_c0 = make_tc(p_c0, w0)
data_c1 = make_tc(p_c1, w1)
data_c2 = make_tc(p_c2, w2)
data_c3 = make_tc(p_c3, w3)

row_data = f'<w:tr><w:trPr><w:cantSplit/></w:trPr>{data_c0}{data_c1}{data_c2}{data_c3}</w:tr>'

tbl_xml = f'''<w:tbl>
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

# Full document XML for standalone file
doc_title_p = make_p([("ตารางที่ 1 ด้านการจัดการเรียนรู้ (งานที่จะปฏิบัติตามมาตรฐานตำแหน่งครู)", True, 36)], align="center", space_before=120, space_after=180)
instruction_p = make_p([("(คุณครูสามารถคัดลอกตารางนี้ไปวางแทนตารางที่ 1 ในเล่มแบบข้อตกลง PA 1 ได้ทันที จัดฟอนต์และระยะขอบเรียบร้อยแล้ว)", False, 28)], align="center", space_before=0, space_after=180)

sectPr = '''<w:sectPr>
    <w:pgSz w:w="11906" w:h="16838"/>
    <w:pgMar w:top="1134" w:right="1134" w:bottom="1134" w:left="1134" w:header="720" w:footer="720" w:gutter="0"/>
    <w:cols w:space="720"/>
    <w:docGrid w:linePitch="360"/>
</w:sectPr>'''

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
        {doc_title_p}
        {instruction_p}
        {tbl_xml}
        {sectPr}
    </w:body>
</w:document>'''

out_filename = "ตารางที่1_ด้านการจัดการเรียนรู้_วPA_ฉบับก๊อปวาง.docx"
file_map["word/document.xml"] = full_xml.encode("utf-8")

with zipfile.ZipFile(out_filename, "w", compression=zipfile.ZIP_DEFLATED) as zout:
    for name, data in file_map.items():
        zout.writestr(name, data)

print(f"Created standalone file: {out_filename}")

# Also copy to docs/
docs_copy = os.path.join("docs", out_filename)
with open(docs_copy, "wb") as f:
    f.write(file_map["word/document.xml"])
with zipfile.ZipFile(docs_copy, "w", compression=zipfile.ZIP_DEFLATED) as zout:
    for name, data in file_map.items():
        zout.writestr(name, data)
print(f"Copied to: {docs_copy}")
