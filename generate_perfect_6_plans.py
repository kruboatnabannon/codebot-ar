# -*- coding: utf-8 -*-
import zipfile, io, os
from generate_car_docx import esc, make_p, make_callout, make_table

def make_page_break():
    return '<w:p><w:r><w:br w:type="page"/></w:r></w:p>'

def heading_sec(title):
    return make_p([(title, True, False, 32, "1E3A8A")], space_before=180, space_after=80)

def heading_sub(title):
    return make_p([(title, True, False, 28, "2563EB")], space_before=140, space_after=60)

def body_p(text, bold_prefix="", bullet=False):
    runs = []
    if bold_prefix:
        runs.append((bold_prefix, True, False, 30, "111827"))
    runs.append((text, False, False, 30, "374151"))
    return make_p(runs, bullet=bullet, space_before=60, space_after=60)

def get_cover_section():
    el = []
    el.append(make_p([("เล่มแผนการจัดการเรียนรู้เชิงรุก (Active Learning Plan)", True, False, 36, "1E3A8A")], align="center", space_before=160, space_after=60))
    el.append(make_p([("กลุ่มสาระการเรียนรู้วิทยาศาสตร์และเทคโนโลยี รายวิชาเทคโนโลยี (วิทยาการคำนวณ) รหัสวิชา ว15101", True, False, 28, "1F2937")], align="center", space_before=0, space_after=40))
    el.append(make_p([("หน่วยการเรียนรู้: การใช้เหตุผลเชิงตรรกะและการเขียนโปรแกรมอย่างง่าย (CodeBot AR Adventure)", False, False, 26, "2563EB")], align="center", space_before=0, space_after=40))
    el.append(make_p([("ชั้นประถมศึกษาปีที่ 5 | ภาคเรียนที่ 2 ปีการศึกษา 2568 | แผนการจัดการเรียนรู้ 6 แผน รวม 6 ชั่วโมง", False, True, 26, "4B5563")], align="center", space_before=0, space_after=180))

    intro = """เล่มแผนการจัดการเรียนรู้ชุดนี้ ได้รับการออกแบบตามมาตรฐานการเรียนรู้และตัวชี้วัด กลุ่มสาระการเรียนรู้วิทยาศาสตร์และเทคโนโลยี (ฉบับปรับปรุง พ.ศ. 2560) ตามหลักสูตรแกนกลางการศึกษาขั้นพื้นฐาน พุทธศักราช 2551 ของ สสวท. และสอดคล้องกับเกณฑ์การประเมิน ว.PA ของ ก.ค.ศ. มุ่งเน้นการจัดการเรียนรู้เชิงรุก (Active Learning) บูรณาการกระบวนการ Game-Based Learning ผ่านเกม CodeBot AR Adventure ควบคู่กับเทคนิคการทำงานแบบคู่หู (Pair Programming: Driver & Navigator) และชุดแฟลชการ์ดสัญลักษณ์จริง เพื่อพัฒนาทักษะการคิดเชิงคำนวณและแก้ปัญหาการสับสนทิศทางของนักเรียนชั้นประถมศึกษาปีที่ 5 จำนวน 8 คน (4 คู่) โรงเรียนบ้านโนนป่าหว้านเชียงฮาย สพป.หนองบัวลำภู เขต 2"""
    el.append(make_callout(intro, title="คำนำและโครงสร้างหน่วยการเรียนรู้"))

    t_overview = [
        ["แผนที่", "ชื่อแผนการจัดการเรียนรู้", "สาระสำคัญ / ภารกิจหลัก", "เวลา"],
        ["1", "ปฐมนิเทศกติกา ปูพื้นฐานอัลกอริทึม & ทดสอบก่อนเรียน", "ทำแบบทดสอบ Pre-test 20 ข้อ + กิจกรรม Unplugged แฟลชการ์ด", "1 ชม."],
        ["2", "ก้าวแรกสู่ทิศทางและอัลกอริทึมในตารางกริด", "เล่นด่าน 1-2 ในเกม CodeBot AR + ใบงานที่ 1 (แก้สับสนทิศทาง)", "1 ชม."],
        ["3", "ค้นหารูปแบบและพลังคำสั่งวนซ้ำอย่างง่าย (Loops)", "เล่นด่าน 3-4 + ใบงานที่ 2 (วิเคราะห์ลูปบันได 3 ขั้น ลดบล็อกโค้ด)", "1 ชม."],
        ["4", "การย้ำซ้ำทวนและการตัดสินใจแบบมีเงื่อนไข (If-Then)", "ย้ำซ้ำทวนลูป + เล่นด่าน 5-6 + ใบงานที่ 3 (กุญแจ & ประตูเลเซอร์)", "1 ชม."],
        ["5", "ยอดนักสืบตามล่าและแก้ไขจุดผิดพลาด (Debugging)", "เล่นด่าน 7-10 + ใบงานที่ 4 (ตรวจจับบั๊ก + แข่งขัน Leaderboard)", "1 ชม."],
        ["6", "การสะท้อนคิดถอดบทเรียน (AAR) & ทดสอบหลังเรียน", "กิจกรรมถอดบทเรียน AAR + ทำแบบทดสอบ Post-test 20 ข้อ", "1 ชม."],
        ["รวม", "หน่วยการเรียนรู้เฉพาะ: การแก้ปัญหาอย่างง่าย", "แผนการจัดการเรียนรู้ 6 แผน (สัปดาห์ละ 1 คาบ)", "6 ชม."]
    ]
    el.append(make_table(t_overview[0], t_overview[1:], [1000, 3200, 3826, 1000], ["center", "left", "left", "center"]))
    el.append(make_p([], space_before=80, space_after=80))
    return el

def get_plan_header(num, title):
    el = []
    el.append(make_p([(f"แผนการจัดการเรียนรู้ที่ {num}", True, False, 34, "1E3A8A")], align="center", space_before=40, space_after=30))
    el.append(make_p([(f"เรื่อง: {title}", True, False, 30, "1F2937")], align="center", space_before=0, space_after=30))
    el.append(make_p([("กลุ่มสาระการเรียนรู้วิทยาศาสตร์และเทคโนโลยี รายวิชาเทคโนโลยี (วิทยาการคำนวณ) ว15101", False, False, 26, "374151")], align="center", space_before=0, space_after=20))
    el.append(make_p([("หน่วยการเรียนรู้: การใช้เหตุผลเชิงตรรกะและการเขียนโปรแกรมอย่างง่าย | ชั้น ป.5 | เวลา 1 ชั่วโมง (60 นาที)", False, True, 24, "4B5563")], align="center", space_before=0, space_after=120))
    
    t_info = [
        ["สถานศึกษา / สังกัด", "ผู้สอน / ผู้เรียน"],
        ["โรงเรียนบ้านโนนป่าหว้านเชียงฮาย สพป.หนองบัวลำภู เขต 2", "ครูผู้สอน: นายเตชินท์ อินทมล (นักเรียน 8 คน จัด 4 คู่)"]
    ]
    el.append(make_table(t_info[0], [t_info[1]], [4513, 4513], ["left", "left"]))
    el.append(make_p([], space_before=60, space_after=60))
    return el

def get_plan_eval_table(k_text, p_text, a_text):
    headers = ["สิ่งที่ต้องการวัด (K - P - A)", "วิธีการวัด", "เครื่องมือวัด", "เกณฑ์การผ่าน"]
    rows = [
        [f"ด้านความรู้ (K):\n{k_text}", "ตรวจแบบทดสอบ / ตรวจใบงาน", "แบบทดสอบ / แบบตรวจใบงาน", "ได้คะแนนร้อยละ 70 ขึ้นไป"],
        [f"ด้านทักษะกระบวนการ (P):\n{p_text}", "สังเกตการปฏิบัติหน้ากล้อง AR / การแก้ปัญหา", "แบบประเมินรูบริกส์ทักษะ CT", "ระดับคุณภาพ 'ดี' ขึ้นไป"],
        [f"ด้านคุณลักษณะ (A):\n{a_text}", "สังเกตพฤติกรรมการทำงานกลุ่มคู่หู", "แบบประเมินพฤติกรรมกลุ่ม", "ระดับคุณภาพ 'ดี' ขึ้นไป"]
    ]
    return make_table(headers, rows, [2800, 2400, 2400, 1426], ["left", "left", "left", "center"])

def get_plan_post_table(num, custom_learning, custom_prob, custom_sol):
    headers = ["ประเด็นการบันทึกหลังแผนการสอน", "รายละเอียดผลการจัดการเรียนรู้จริง"]
    rows = [
        ["1. ผลการจัดกิจกรรมการเรียนรู้\n(ด้าน K, P, A)", custom_learning],
        ["2. ปัญหาและอุปสรรคที่พบ", custom_prob],
        ["3. แนวทางแก้ไขและการพัฒนาต่อยอด", custom_sol]
    ]
    tbl = make_table(headers, rows, [2800, 6226], ["left", "left"])
    
    t_sign = [
        ["ลงชื่อครูผู้สอน", "ความเห็นของผู้บริหารสถานศึกษา"],
        [
            "(ลงชื่อ).....................................................................\n( นายเตชินท์ อินทมล )\nตำแหน่ง ครู ไม่มีวิทยฐานะ\nวันที่ ........ เดือน ........................ พ.ศ. 2568",
            "แผนการจัดการเรียนรู้มีการจัดกิจกรรมอย่างเป็นขั้นตอนชัดเจน กิจกรรม Active Learning เหมาะสมกับวัย ป.5 อนุมัติให้ใช้จัดการเรียนรู้ได้\n\n(ลงชื่อ).....................................................................\n( ..................................................................... )\nตำแหน่ง ผู้อำนวยการโรงเรียนบ้านโนนป่าหว้านเชียงฮาย"
        ]
    ]
    tbl_sign = make_table(t_sign[0], [t_sign[1]], [4513, 4513], ["left", "left"])
    return tbl + make_p([], space_before=60, space_after=60) + tbl_sign

print("Core generator template ready.")
