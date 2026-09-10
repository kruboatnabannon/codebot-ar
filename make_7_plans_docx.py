# -*- coding: utf-8 -*-
import zipfile, io, os
from generate_car_docx import esc, make_p, make_callout, make_table
from generate_perfect_6_plans import make_page_break, heading_sec, heading_sub, body_p, get_plan_header, get_plan_eval_table, get_plan_post_table

def build_7_plans_compilation():
    elements = []

    # Cover Page
    elements.append(make_p([("เล่มแผนการจัดการเรียนรู้เชิงรุก (Active Learning Plan)", True, False, 36, "1E3A8A")], align="center", space_before=160, space_after=60))
    elements.append(make_p([("กลุ่มสาระการเรียนรู้วิทยาศาสตร์และเทคโนโลยี รายวิชาเทคโนโลยี (วิทยาการคำนวณ) ว15101", True, False, 28, "1F2937")], align="center", space_before=0, space_after=40))
    elements.append(make_p([("ประเด็นท้าทาย: การพัฒนาทักษะการเรียนรู้โดยใช้กระบวนการ Game Based Learning ร่วมกับ Active Learning", False, False, 26, "2563EB")], align="center", space_before=0, space_after=40))
    elements.append(make_p([("ชั้นประถมศึกษาปีที่ 5 | ภาคเรียนที่ 2 ปีการศึกษา 2568 | แผนการจัดการเรียนรู้ 7 แผน รวม 7 ชั่วโมง", False, True, 26, "4B5563")], align="center", space_before=0, space_after=180))

    intro = """เล่มแผนการจัดการเรียนรู้ชุดนี้ ได้รับการออกแบบตามข้อตกลงในการพัฒนางาน (PA 1) เพื่อขับเคลื่อน 'ประเด็นท้าทาย' ในการแก้ไขปัญหาและพัฒนาคุณภาพการเรียนรู้ของผู้เรียน โดยผู้วิจัยได้ติดตามพัฒนาการของนักเรียนกลุ่มเป้าหมายจำนวน 8 คน อย่างต่อเนื่องจากสภาพปัญหาที่พบในชั้นประถมศึกษาปีที่ 4 และนำมาปรับประยุกต์ (Apply & Adapt) จัดการเรียนรู้เชิงรุก (Active Learning) ด้วยเทคนิคจับคู่เขียนโปรแกรม (Pair Programming: Driver & Navigator) บูรณาการเกม CodeBot AR Adventure และชุดแฟลชการ์ดสัญลักษณ์จริง เพื่อปูพื้นฐานมโนทัศน์ตรรกะแบบรูปธรรม ก่อนเชื่อมโยงสู่การเขียนโปรแกรมด้วย Scratch ตามเกณฑ์ที่กำหนดไว้ในข้อตกลง PA"""
    elements.append(make_callout(intro, title="ความเชื่อมโยงกับข้อตกลงในการพัฒนางาน (PA 1)"))

    t_overview = [
        ["แผนที่", "ชื่อแผนการจัดการเรียนรู้", "สาระสำคัญ / กิจกรรมหลัก", "เวลา"],
        ["1", "ปฐมนิเทศกติกา ปูพื้นฐานอัลกอริทึม & ทดสอบก่อนเรียน", "ทำแบบทดสอบ Pre-test 20 ข้อ + กิจกรรม Unplugged แฟลชการ์ด", "1 ชม."],
        ["2", "ก้าวแรกสู่ทิศทางและอัลกอริทึมในตารางกริด", "เล่นด่าน 1-2 ในเกม CodeBot AR + ใบงานที่ 1 (แก้สับสนทิศทาง)", "1 ชม."],
        ["3", "ค้นหารูปแบบและพลังคำสั่งวนซ้ำอย่างง่าย (Loops)", "เล่นด่าน 3-4 + ใบงานที่ 2 (วิเคราะห์ลูปบันได 3 ขั้น ลดบล็อกโค้ด)", "1 ชม."],
        ["4", "การย้ำซ้ำทวนและการตัดสินใจแบบมีเงื่อนไข (If-Then)", "ย้ำซ้ำทวนลูป + เล่นด่าน 5-6 + ใบงานที่ 3 (กุญแจ & ประตูเลเซอร์)", "1 ชม."],
        ["5", "ยอดนักสืบตามล่าและแก้ไขจุดผิดพลาด (Debugging)", "เล่นด่าน 7-8 + ใบงานที่ 4 (ตรวจจับบั๊ก + วิเคราะห์สาเหตุ)", "1 ชม."],
        ["6", "การบูรณาการโค้ดดิ้งสู่โปรแกรม Scratch (Scratch Bridging)", "ด่านมาสเตอร์จักรวาล + นำอัลกอริทึมที่ได้ไปต่อบล็อกคำสั่งใน Scratch", "1 ชม."],
        ["7", "การสะท้อนคิดถอดบทเรียน (AAR) & ทดสอบหลังเรียน", "กิจกรรมถอดบทเรียน AAR + ทำแบบทดสอบ Post-test 20 ข้อ", "1 ชม."],
        ["รวม", "ประเด็นท้าทายตามข้อตกลง PA 1 (ครบ 7 แผน)", "แผนการจัดการเรียนรู้ 7 แผน (สัปดาห์ละ 1 คาบ)", "7 ชม."]
    ]
    elements.append(make_table(t_overview[0], t_overview[1:], [1000, 3200, 3826, 1000], ["center", "left", "left", "center"]))
    elements.append(make_p([], space_before=80, space_after=80))

    # Import plans 1 to 5 from make_complete_6_plans logic (we can write plans 1-7 cleanly)
    return elements

print("Helper for 7 plans ready.")
