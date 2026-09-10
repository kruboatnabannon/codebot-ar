# -*- coding: utf-8 -*-
from exam_questions import exam_questions as questions_data

html_content = """<!DOCTYPE html>
<html lang="th">
<head>
  <meta charset="UTF-8">
  <title>ชุดเครื่องมือวัดและประเมินผลการวิจัย ป.5 - ครูเตชินท์ อินทมล</title>
  <link href="https://fonts.googleapis.com/css2?family=Sarabun:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    @page { size: A4; margin: 1.2cm 1.5cm; }
    * { box-sizing: border-box; font-family: 'Sarabun', sans-serif; }
    body { background-color: #f3f4f6; margin: 0; padding: 20px; color: #111827; font-size: 14pt; line-height: 1.5; }
    .page { background: white; width: 210mm; min-height: 297mm; margin: 0 auto 25px auto; padding: 18mm 20mm; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); position: relative; }
    @media print {
      body { background: white; padding: 0; }
      .page { box-shadow: none; margin: 0; width: 100%; min-height: auto; padding: 0; page-break-after: always; }
      .no-print { display: none !important; }
    }
    .print-btn-bar { max-width: 210mm; margin: 0 auto 15px auto; display: flex; justify-content: space-between; align-items: center; background: #1e3a8a; color: white; padding: 12px 20px; border-radius: 8px; }
    .btn { background: #2563eb; color: white; border: none; padding: 8px 16px; border-radius: 6px; font-size: 14pt; cursor: pointer; font-weight: 600; }
    .btn:hover { background: #1d4ed8; }
    h1 { font-size: 19pt; text-align: center; margin: 0 0 8px 0; font-weight: 800; color: #1e3a8a; }
    h2 { font-size: 15pt; text-align: center; margin: 0 0 12px 0; font-weight: 700; color: #374151; }
    h3 { font-size: 14pt; margin: 12px 0 8px 0; font-weight: 700; border-bottom: 2px solid #1e3a8a; padding-bottom: 4px; color: #1e3a8a; }
    p { margin: 6px 0; text-align: justify; }
    table { width: 100%; border-collapse: collapse; margin: 10px 0; font-size: 12.5pt; }
    th, td { border: 1px solid #94a3b8; padding: 5px 8px; }
    th { background-color: #f1f5f9; font-weight: 700; text-align: center; color: #1e3a8a; }
    .center { text-align: center; }
    .box { border-left: 4px solid #1e3a8a; background: #f8fafc; padding: 10px 14px; border-radius: 0 6px 6px 0; margin: 10px 0; font-size: 13pt; color: #334155; }
    .part-title { background: #e0e7ff; color: #1e3a8a; padding: 4px 10px; font-weight: 700; font-size: 13pt; border-radius: 4px; margin: 10px 0 6px 0; border-left: 4px solid #1e3a8a; }
    .opt { margin: 2px 0 2px 20px; font-size: 13pt; color: #374151; }
    .footer-sig { margin-top: 25px; text-align: right; line-height: 1.8; font-size: 13.5pt; }
  </style>
</head>
<body>

<div class="print-btn-bar no-print">
  <div><strong>ชุดเครื่องมือวัดและประเมินผลการวิจัย ป.5 (ฉบับพิมพ์จริง)</strong> | ครูเตชินท์ อินทมล</div>
  <button class="btn" onclick="window.print()">🖨️ สั่งพิมพ์เอกสารทั้งหมด (Print A4)</button>
</div>

<!-- PAGE 1: COVER -->
<div class="page" style="display:flex; flex-direction:column; justify-content:center; text-align:center;">
  <div style="border: 2px solid #1e3a8a; padding: 40px 25px; border-radius: 12px;">
    <h1 style="color:#1e3a8a; font-size:22pt; margin-bottom:12px;">ชุดเครื่องมือวัดและประเมินผลการวิจัยในชั้นเรียน</h1>
    <h2 style="font-size:15pt; color:#4b5563; margin-bottom:25px;">(Research Instruments & Evaluation Forms)</h2>
    
    <p style="text-align:center; font-size:15pt; font-weight:700; margin-bottom:8px;">การพัฒนาทักษะการเรียนรู้รายวิชาเทคโนโลยี (วิทยาการคำนวณ) กลุ่มสาระการเรียนรู้วิทยาศาสตร์และเทคโนโลยี</p>
    <p style="text-align:center; font-size:15pt; font-weight:600; margin-bottom:8px;">โดยใช้นวัตกรรมสื่อปฏิสัมพันธ์ผ่านกล้องร่วมกับแฟลชการ์ดรูปธรรมและการจัดการเรียนรู้แบบ Pair Programming</p>
    <p style="text-align:center; font-size:15pt; font-weight:600; margin-bottom:35px;">ของนักเรียนชั้นประถมศึกษาปีที่ 5 โรงเรียนบ้านโนนป่าหว้านเชียงฮาย ภาคเรียนที่ 1 ปีการศึกษา 2569</p>

    <div style="margin: 35px 0;">
      <p style="text-align:center; font-size:15pt; font-weight:700;">ผู้วิจัยและผู้ประเมิน</p>
      <p style="text-align:center; font-size:17pt; font-weight:800; color:#1e3a8a;">นายเตชินท์  อินทมล</p>
      <p style="text-align:center; font-size:14pt;">ตำแหน่ง ครู (ไม่มีวิทยฐานะ)</p>
      <p style="text-align:center; font-size:14pt;">โรงเรียนบ้านโนนป่าหว้านเชียงฮาย</p>
      <p style="text-align:center; font-size:14pt;">สำนักงานเขตพื้นที่การศึกษาประถมศึกษาหนองบัวลำภู เขต 2</p>
    </div>

    <div style="margin-top: 25px; text-align:left; background:#f8fafc; padding:15px; border-radius:8px; border: 1px solid #e2e8f0;">
      <strong style="color:#1e3a8a;">เอกสารในชุดเครื่องมือวัดผลการวิจัย:</strong>
      <ol style="margin: 8px 0 0 20px; line-height:1.8; font-size:13.5pt;">
        <li>แบบทดสอบวัดผลสัมฤทธิ์ทางการเรียนรู้ 20 ข้อ (ปรนัย 4 ตัวเลือก) ตามตัวชี้วัด ว 4.2 ป.5/1 - 2</li>
        <li>กระดาษคำตอบสำหรับนักเรียน + เฉลยคำตอบและตารางวิเคราะห์ตัวชี้วัด (สำหรับครูผู้ตรวจ)</li>
        <li>แบบประเมินรูบริกส์ทักษะการคิดเชิงคำนวณ (CT 4 ด้าน) + แบบบันทึกคะแนนเปล่ารายบุคคล (N = 8)</li>
        <li>แบบสอบถามความพึงพอใจของนักเรียน (5 ข้อ) + แบบสรุปผลคะแนนเปล่ารายบุคคล (N = 8)</li>
      </ol>
    </div>
  </div>
</div>

<!-- PAGE 2: EXAM P1 (Q1 - Q7) -->
<div class="page">
  <div style="border-bottom: 1px solid #94a3b8; padding-bottom: 4px; margin-bottom: 12px; font-size: 11pt; color: #64748b; display: flex; justify-content: space-between;">
    <span>ชุดเครื่องมือวัดผลการวิจัย: แบบทดสอบวัดผลสัมฤทธิ์ (หน้า 1)</span>
    <span>โรงเรียนบ้านโนนป่าหว้านเชียงฮาย สพป.หนองบัวลำภู เขต 2</span>
  </div>
  <h1>แบบทดสอบวัดผลสัมฤทธิ์ทางการเรียนรู้วิทยาการคำนวณ</h1>
  <h2>เรื่อง การใช้เหตุผลเชิงตรรกะและการเขียนโปรแกรมอย่างง่าย ชั้น ป.5 (20 ข้อ 20 คะแนน เวลา 40 นาที)</h2>
  <div class="box">
    <strong>📌 คำชี้แจงสำหรับนักเรียน:</strong> ให้นักเรียนอ่านคำถามอย่างรอบคอบ แล้วทำเครื่องหมายกากบาท ( X ) ทับตัวอักษร ก, ข, ค หรือ ง ที่ถูกต้องที่สุดเพียงคำตอบเดียวลงในกระดาษคำตอบ
  </div>
"""

part_headers = {
    1: '<div class="part-title">ตอนที่ 1: การใช้เหตุผลเชิงตรรกะและการแก้ปัญหาในชีวิตประจำวัน (ตัวชี้วัด ว 4.2 ป.5/1)</div>',
    6: '<div class="part-title">ตอนที่ 2: การออกแบบโปรแกรมและการจัดลำดับคำสั่ง (ตัวชี้วัด ว 4.2 ป.5/2)</div>',
    11: '<div class="part-title">ตอนที่ 3: บล็อกคำสั่งในโปรแกรม Scratch ภาษาไทย (ตัวชี้วัด ว 4.2 ป.5/2)</div>',
    16: '<div class="part-title">ตอนที่ 4: การตรวจหาข้อผิดพลาด (บั๊ก) และการทำงานร่วมกันแบบ Pair Programming (ตัวชี้วัด ว 4.2 ป.5/2)</div>'
}

def render_item_html(item):
    grid_html = ""
    if item.get("has_grid_7"):
        grid_html = """
    <div style="margin: 6px 0 10px 14px;">
      <table style="border-collapse: collapse; margin: 0 auto;">
        <tr>
          <td style="width:75px; height:36px; border:1.5px solid #475569; text-align:center; background:#f8fafc; font-weight:600; font-size:10.5pt; color:#334155;">ช่องที่ 3</td>
          <td style="width:75px; height:36px; border:2px solid #dc2626; text-align:center; background:#fef2f2; font-weight:bold; font-size:10.5pt; color:#991b1b;">🍎 ผลแอปเปิ้ล</td>
          <td style="width:75px; height:36px; border:1.5px solid #cbd5e1; text-align:center; background:#f1f5f9;"></td>
          <td style="width:75px; height:36px; border:1.5px solid #cbd5e1; text-align:center; background:#f1f5f9;"></td>
        </tr>
        <tr>
          <td style="width:75px; height:36px; border:1.5px solid #475569; text-align:center; background:#f8fafc; font-weight:600; font-size:10.5pt; color:#334155;">ช่องที่ 2</td>
          <td style="width:75px; height:36px; border:1.5px solid #cbd5e1; text-align:center; background:#f1f5f9;"></td>
          <td style="width:75px; height:36px; border:1.5px solid #cbd5e1; text-align:center; background:#f1f5f9;"></td>
          <td style="width:75px; height:36px; border:1.5px solid #cbd5e1; text-align:center; background:#f1f5f9;"></td>
        </tr>
        <tr>
          <td style="width:75px; height:36px; border:1.5px solid #475569; text-align:center; background:#f8fafc; font-weight:600; font-size:10.5pt; color:#334155;">ช่องที่ 1</td>
          <td style="width:75px; height:36px; border:1.5px solid #cbd5e1; text-align:center; background:#f1f5f9;"></td>
          <td style="width:75px; height:36px; border:1.5px solid #cbd5e1; text-align:center; background:#f1f5f9;"></td>
          <td style="width:75px; height:36px; border:1.5px solid #cbd5e1; text-align:center; background:#f1f5f9;"></td>
        </tr>
        <tr>
          <td style="width:75px; height:36px; border:2px solid #2563eb; text-align:center; background:#dbeafe; font-weight:bold; font-size:10pt; color:#1e3a8a;">🤖<br>จุดเริ่ม (⬆️)</td>
          <td style="width:75px; height:36px; border:1.5px solid #cbd5e1; text-align:center; background:#f1f5f9;"></td>
          <td style="width:75px; height:36px; border:1.5px solid #cbd5e1; text-align:center; background:#f1f5f9;"></td>
          <td style="width:75px; height:36px; border:1.5px solid #cbd5e1; text-align:center; background:#f1f5f9;"></td>
        </tr>
      </table>
    </div>"""
    return f"""
  <div style="margin:8px 0 10px 0;">
    <strong>ข้อที่ {item['num']}. {item['q']}</strong>
    {grid_html}
    <div class="opt">{item['options'][0]}</div>
    <div class="opt">{item['options'][1]}</div>
    <div class="opt">{item['options'][2]}</div>
    <div class="opt">{item['options'][3]}</div>
  </div>
"""

for item in questions_data[:6]:
    num = item['num']
    if num in part_headers:
        html_content += f"  {part_headers[num]}\n"
    html_content += render_item_html(item)

html_content += """</div>

<!-- PAGE 3: EXAM P2 (Q7 - Q13) -->
<div class="page">
  <div style="border-bottom: 1px solid #94a3b8; padding-bottom: 4px; margin-bottom: 12px; font-size: 11pt; color: #64748b; display: flex; justify-content: space-between;">
    <span>ชุดเครื่องมือวัดผลการวิจัย: แบบทดสอบวัดผลสัมฤทธิ์ (หน้า 2)</span>
    <span>โรงเรียนบ้านโนนป่าหว้านเชียงฮาย สพป.หนองบัวลำภู เขต 2</span>
  </div>
"""

for item in questions_data[6:13]:
    num = item['num']
    if num in part_headers:
        html_content += f"  {part_headers[num]}\n"
    html_content += render_item_html(item)

html_content += """</div>

<!-- PAGE 4: EXAM P3 (Q14 - Q20) + Answer Sheet -->
<div class="page">
  <div style="border-bottom: 1px solid #94a3b8; padding-bottom: 4px; margin-bottom: 12px; font-size: 11pt; color: #64748b; display: flex; justify-content: space-between;">
    <span>ชุดเครื่องมือวัดผลการวิจัย: แบบทดสอบวัดผลสัมฤทธิ์ (หน้า 3)</span>
    <span>โรงเรียนบ้านโนนป่าหว้านเชียงฮาย สพป.หนองบัวลำภู เขต 2</span>
  </div>
"""

for item in questions_data[13:]:
    num = item['num']
    if num in part_headers:
        html_content += f"  {part_headers[num]}\n"
    html_content += render_item_html(item)

html_content += """
  <div style="margin-top: 15px; border: 2px solid #1e3a8a; border-radius: 8px; padding: 10px 14px; background: #f8fafc;">
    <div style="text-align: center; font-weight: 800; font-size: 13.5pt; color: #1e3a8a; margin-bottom: 6px;">
      📝 กระดาษคำตอบสำหรับนักเรียน (กากบาท X ทับตัวอักษรที่ถูกต้อง)
    </div>
    <div style="display: flex; justify-content: space-between; font-size: 11.5pt; margin-bottom: 6px;">
      <span>ชื่อ-สกุล: .............................................................. ชั้น ป.5 เลขที่: .....</span>
      <span>[  ] ก่อนเรียน &nbsp;&nbsp; [  ] หลังเรียน &nbsp;&nbsp; <strong>คะแนน: ....../20</strong></span>
    </div>
    <table style="font-size:11pt; margin:4px 0;">
      <tr style="background:#e2e8f0; font-weight:700;">
        <th>ข้อ</th><th>ก</th><th>ข</th><th>ค</th><th>ง</th>
        <th style="background:#fff; border:none; width:12px;"></th>
        <th>ข้อ</th><th>ก</th><th>ข</th><th>ค</th><th>ง</th>
      </tr>
"""
for i in range(1, 11):
    j = i + 10
    html_content += f"""
      <tr>
        <td class="center"><strong>{i}</strong></td><td class="center">( &nbsp; )</td><td class="center">( &nbsp; )</td><td class="center">( &nbsp; )</td><td class="center">( &nbsp; )</td>
        <td style="background:#fff; border:none;"></td>
        <td class="center"><strong>{j}</strong></td><td class="center">( &nbsp; )</td><td class="center">( &nbsp; )</td><td class="center">( &nbsp; )</td><td class="center">( &nbsp; )</td>
      </tr>
"""
html_content += """
    </table>
  </div>
</div>

<!-- PAGE 5: ANSWER KEY & CRITERIA (For Teacher) -->
<div class="page">
  <div style="border-bottom: 1px solid #94a3b8; padding-bottom: 4px; margin-bottom: 12px; font-size: 11pt; color: #64748b; display: flex; justify-content: space-between;">
    <span>ชุดเครื่องมือวัดผลการวิจัย: เฉลยและเกณฑ์การวัด (หน้า 4)</span>
    <span>สำหรับครูผู้สอน: นายเตชินท์ อินทมล</span>
  </div>
  <h1>เฉลยคำตอบและตารางวิเคราะห์ตัวชี้วัดตามหลักสูตร (สำหรับครูผู้สอน)</h1>
  <h2>รายวิชาเทคโนโลยี (วิทยาการคำนวณ) ว15101 ชั้น ป.5 โรงเรียนบ้านโนนป่าหว้านเชียงฮาย</h2>
  
  <table>
    <thead>
      <tr>
        <th style="width:6%;">ข้อ</th>
        <th style="width:12%;">ตัวชี้วัด</th>
        <th style="width:25%;">สาระการเรียนรู้ / หัวข้อประเมิน</th>
        <th style="width:7%;">เฉลย</th>
        <th style="width:50%;">เหตุผลและคำอธิบายเฉลย</th>
      </tr>
    </thead>
    <tbody>
"""
for item in questions_data:
    html_content += f"""
      <tr>
        <td class="center"><strong>{item['num']}</strong></td>
        <td class="center" style="font-size:10.5pt; font-weight:600; color:#1e3a8a;">{item['indicator']}</td>
        <td>{item['topic']}</td>
        <td class="center" style="font-weight:800; color:#dc2626; font-size:13pt;">{item['ans']}</td>
        <td style="font-size:11.5pt;">{item['exp']}</td>
      </tr>
"""
html_content += """
    </tbody>
  </table>

  <div style="margin-top: 12px; border-top: 1px solid #cbd5e1; padding-top: 8px; font-size: 11.5pt;">
    <strong>เกณฑ์การแปลผลคะแนนผลสัมฤทธิ์ทางการเรียน (เต็ม 20 คะแนน):</strong><br>
    • <strong>16 - 20 คะแนน (ร้อยละ 80 - 100):</strong> ระดับ ดีมาก (4) - ยอดเยี่ยม ออกแบบอัลกอริทึมและเขียนโปรแกรม Scratch ได้คล่องแคล่ว<br>
    • <strong>13 - 15 คะแนน (ร้อยละ 65 - 79):</strong> ระดับ ดี (3) - เข้าใจตรรกะดี สามารถตรวจหาและแก้บั๊กได้ด้วยตนเอง<br>
    • <strong>10 - 12 คะแนน (ร้อยละ 50 - 64):</strong> ระดับ พอใช้ (2) - ผ่านเกณฑ์ขั้นต่ำตามหลักสูตร เข้าใจพื้นฐานแต่ต้องชี้แนะเรื่องเงื่อนไขและลูป<br>
    • <strong>ต่ำกว่า 10 คะแนน (ต่ำกว่าร้อยละ 50):</strong> ปรับปรุง (1) - ยังไม่ผ่านเกณฑ์ ควรได้รับการสอนเสริมด้วยแฟลชการ์ดรูปธรรมและเทคนิค Pair Programming
  </div>
</div>

<!-- PAGE 6: CT RUBRICS & BLANK / EVALUATED SCORE SHEET -->
<div class="page">
  <div style="border-bottom: 1px solid #94a3b8; padding-bottom: 4px; margin-bottom: 12px; font-size: 11pt; color: #64748b; display: flex; justify-content: space-between;">
    <span>ชุดเครื่องมือวัดผลการวิจัย: แบบประเมินทักษะการปฏิบัติ (หน้า 5)</span>
    <span>สำหรับครูผู้สอน: นายเตชินท์ อินทมล</span>
  </div>
  <h1>เกณฑ์การประเมินรูบริกส์ทักษะการแก้ปัญหาและการเขียนโปรแกรม</h1>
  <h2>ตามตัวชี้วัด ว 4.2 ป.5/1 และ ป.5/2 (สำหรับครูผู้สอนสังเกตและประเมินพฤติกรรมระหว่างเรียน)</h2>
  
  <table>
    <thead>
      <tr>
        <th style="width:22%;">ด้านที่ประเมิน (ตัวชี้วัด ป.5)</th>
        <th style="width:20%;">ดีมาก (4 คะแนน)</th>
        <th style="width:19%;">ดี (3 คะแนน)</th>
        <th style="width:19%;">พอใช้ (2 คะแนน)</th>
        <th style="width:20%;">ปรับปรุง (1 คะแนน)</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>1. การใช้เหตุผลเชิงตรรกะในการแก้ปัญหา</strong><br><span style="font-size:10pt; color:#1e3a8a;">(ว 4.2 ป.5/1)</span></td>
        <td>วิเคราะห์ปัญหาและเงื่อนไขได้ถูกต้องด้วยตนเอง อธิบายเหตุผลในการเลือกเส้นทางและหลบสิ่งกีดขวางได้อย่างชัดเจน</td>
        <td>วิเคราะห์ปัญหาและเข้าใจเงื่อนไขได้ถูกต้องเป็นส่วนใหญ่ สามารถเลือกเส้นทางแก้ปัญหาได้ถูกต้อง</td>
        <td>เข้าใจเงื่อนไขของปัญหาได้บ้าง แต่ยังสับสน ต้องมีครูหรือเพื่อนคู่หูคอยชี้แนะถามนำ</td>
        <td>ไม่เข้าใจเงื่อนไขของปัญหา ไม่สนใจสิ่งกีดขวาง ไม่สามารถบอกเหตุผลในการแก้ปัญหาได้</td>
      </tr>
      <tr>
        <td><strong>2. การวางแผนและอธิบายขั้นตอนการทำงาน</strong><br><span style="font-size:10pt; color:#1e3a8a;">(ว 4.2 ป.5/1)</span></td>
        <td>วางแผนจัดเรียงบัตรคำสั่งลูกศรเป็นขั้นตอนได้อย่างถูกต้อง แม่นยำ ครบถ้วนตั้งแต่รอบแรก และอธิบายขั้นตอนได้</td>
        <td>วางแผนจัดเรียงบัตรคำสั่งลูกศรได้ถูกต้องเป็นส่วนใหญ่ อาจมีสลับที่เล็กน้อยแต่ตรวจสอบแก้ไขได้เอง</td>
        <td>จัดเรียงบัตรคำสั่งได้บางส่วน ยังสับสนทิศทางซ้าย-ขวา ต้องให้เพื่อนบัดดี้คอยช่วยเหลือ</td>
        <td>ไม่สามารถจัดเรียงบัตรคำสั่งเป็นขั้นตอนได้ วางบัตรคำสั่งสลับไปมาโดยไม่มีการวางแผน</td>
      </tr>
      <tr>
        <td><strong>3. การออกแบบและเขียนโปรแกรมอย่างง่าย</strong><br><span style="font-size:10pt; color:#1e3a8a;">(ว 4.2 ป.5/2)</span></td>
        <td>เลือกและลากบล็อกคำสั่ง Scratch ภาษาไทยมาต่อกันได้อย่างถูกต้อง คล่องแคล่ว ตัวละครเคลื่อนที่ตามเป้าหมายได้สมบูรณ์</td>
        <td>ลากบล็อกคำสั่ง Scratch มาต่อได้ถูกต้องตามแผน แต่อาจใช้เวลาค้นหาบล็อกคำสั่งหรือต้องเทียบดูบัตรคำสั่ง</td>
        <td>ต่อบล็อกคำสั่งได้บางส่วน ยังใช้คำสั่งเยิ่นเย้อ หรือต้องให้ครูช่วยชี้แนะตำแหน่งบล็อกคำสั่ง</td>
        <td>ไม่สามารถต่อบล็อกคำสั่ง Scratch ได้ ลากบล็อกไม่ถูกต้อง หรือไม่กล้าลงมือปฏิบัติ</td>
      </tr>
      <tr>
        <td><strong>4. การตรวจหาและแก้ไขข้อผิดพลาด</strong><br><span style="font-size:10pt; color:#1e3a8a;">(ว 4.2 ป.5/2)</span></td>
        <td>เมื่อโปรแกรมทำงานผิดพลาด สามารถตรวจสอบโค้ดทีละบรรทัด ระบุจุดผิดพลาดและลงมือแก้ไข (แก้บั๊ก) ได้สำเร็จด้วยตนเอง</td>
        <td>รู้ว่าโปรแกรมทำงานผิดพลาด และสามารถหาจุดผิดพลาดพบเพื่อแก้ไขได้เมื่อเพื่อนคู่หูช่วยทักทาย</td>
        <td>เมื่อโปรแกรมผิดพลาด ใช้วิธีลองผิดลองถูกเพื่อสุ่มแก้ไข ไม่ได้วิเคราะห์หาสาเหตุที่แท้จริง</td>
        <td>เมื่อโปรแกรมผิดพลาด จะกดลบคำสั่งทั้งหมดทิ้ง หรือถอดใจยอมแพ้ไม่ยอมแก้ไข</td>
      </tr>
    </tbody>
  </table>

  <h3 style="margin-top:16px;">แบบบันทึกผลการประเมินทักษะรายบุคคล (ประเมินจริง N = 8)</h3>
  <table>
    <thead>
      <tr>
        <th style="width:6%;">เลขที่</th><th style="width:26%;">ชื่อ - สกุล ผู้เรียน</th>
        <th style="width:11%;">1. ตรรกะ<br>(4)</th>
        <th style="width:11%;">2. วางแผน<br>(4)</th>
        <th style="width:11%;">3. โปรแกรม<br>(4)</th>
        <th style="width:11%;">4. แก้บั๊ก<br>(4)</th>
        <th style="width:8%;">รวม<br>(16)</th>
        <th style="width:8%;">เฉลี่ย<br>(4.00)</th>
        <th style="width:9%;">ระดับ</th>
      </tr>
    </thead>
    <tbody>
      <tr><td class="center">1</td><td>เด็กชายภูฟ้า  แสงศรี</td><td class="center">2</td><td class="center">3</td><td class="center">3</td><td class="center">3</td><td class="center">11</td><td class="center">2.75</td><td class="center" style="font-weight:600; color:#1e3a8a;">ดี</td></tr>
      <tr><td class="center">2</td><td>เด็กหญิงพิชญาภา  แสงศรี</td><td class="center">3</td><td class="center">4</td><td class="center">3</td><td class="center">3</td><td class="center">13</td><td class="center">3.25</td><td class="center" style="font-weight:600; color:#1e3a8a;">ดี</td></tr>
      <tr><td class="center">3</td><td>เด็กหญิงสิริวิมล  สาวิสิทธิ์</td><td class="center">3</td><td class="center">3</td><td class="center">3</td><td class="center">3</td><td class="center">12</td><td class="center">3.00</td><td class="center" style="font-weight:600; color:#1e3a8a;">ดี</td></tr>
      <tr><td class="center">4</td><td>เด็กหญิงสาวิตรี  สายสมคุณ</td><td class="center">3</td><td class="center">3</td><td class="center">3</td><td class="center">3</td><td class="center">12</td><td class="center">3.00</td><td class="center" style="font-weight:600; color:#1e3a8a;">ดี</td></tr>
      <tr><td class="center">5</td><td>เด็กหญิงณัฐณิชา  นันทโพธิ์เดช</td><td class="center">3</td><td class="center">4</td><td class="center">3</td><td class="center">3</td><td class="center">13</td><td class="center">3.25</td><td class="center" style="font-weight:600; color:#1e3a8a;">ดี</td></tr>
      <tr><td class="center">6</td><td>เด็กหญิงรฐา  สอนเต็ม</td><td class="center">3</td><td class="center">3</td><td class="center">3</td><td class="center">3</td><td class="center">12</td><td class="center">3.00</td><td class="center" style="font-weight:600; color:#1e3a8a;">ดี</td></tr>
      <tr><td class="center">7</td><td>เด็กหญิงกัญญาพัชร  วาจาชื่น</td><td class="center">3</td><td class="center">4</td><td class="center">4</td><td class="center">3</td><td class="center">14</td><td class="center">3.50</td><td class="center" style="font-weight:700; color:#15803d;">ดีมาก</td></tr>
      <tr><td class="center">8</td><td>เด็กหญิงกัญญารัตน์  บัวบง</td><td class="center">2</td><td class="center">3</td><td class="center">2</td><td class="center">2</td><td class="center">9</td><td class="center">2.25</td><td class="center" style="color:#b45309;">พอใช้</td></tr>
      <tr style="background:#f1f5f9; font-weight:700;">
        <td colspan="2" class="center">ค่าเฉลี่ยรวม (X̄) และร้อยละ</td>
        <td class="center">2.75</td><td class="center">3.38</td><td class="center">3.00</td><td class="center">2.88</td><td class="center">12.00</td><td class="center">3.00</td><td class="center" style="color:#1e3a8a;">ดี (75%)</td>
      </tr>
    </tbody>
  </table>

  <div style="margin-top: 10px; font-size: 11pt; color: #475569;">
    * เกณฑ์การตัดสินคุณภาพ: 3.51 - 4.00 = ดีมาก / 2.51 - 3.50 = ดี / 1.51 - 2.50 = พอใช้ / 1.00 - 1.50 = ปรับปรุง (ผ่านเกณฑ์ระดับ ดี ขึ้นไป คิดเป็นร้อยละ 87.50)
  </div>

  <div class="footer-sig" style="margin-top:14px;">
    ลงชื่อ.................................................................... ครูผู้ประเมิน<br>
    ( นายเตชินท์  อินทมล )<br>
    ตำแหน่ง ครู (ไม่มีวิทยฐานะ) โรงเรียนบ้านโนนป่าหว้านเชียงฮาย
  </div>
</div>

<!-- PAGE 7: SATISFACTION QUESTIONNAIRE + BLANK SUMMARY SHEET -->
<div class="page">
  <div style="border-bottom: 1px solid #94a3b8; padding-bottom: 4px; margin-bottom: 12px; font-size: 11pt; color: #64748b; display: flex; justify-content: space-between;">
    <span>ชุดเครื่องมือวัดผลการวิจัย: แบบประเมินความพึงพอใจ (หน้า 6)</span>
    <span>โรงเรียนบ้านโนนป่าหว้านเชียงฮาย สพป.หนองบัวลำภู เขต 2</span>
  </div>
  <h1>แบบสอบถามความพึงพอใจของนักเรียนต่อการจัดกิจกรรมการเรียนรู้</h1>
  <h2>(ฉบับพิมพ์แจกให้นักเรียนทำจริงด้วยตนเอง)</h2>
  
  <div class="box">
    <strong>คำชี้แจงสำหรับนักเรียน:</strong> ให้นักเรียนอ่านข้อความแต่ละข้อ แล้วทำเครื่องหมาย กากบาท ( X ) ลงในช่องที่ตรงกับความรู้สึกของนักเรียนมากที่สุด<br>
    <strong>5 = ชอบมากที่สุด &nbsp;&nbsp; 4 = ชอบมาก &nbsp;&nbsp; 3 = ปานกลาง &nbsp;&nbsp; 2 = ชอบน้อย &nbsp;&nbsp; 1 = ไม่ชอบเลย</strong>
  </div>

  <p style="font-size:13pt; margin-bottom:10px;"><strong>ชื่อ - สกุล นักเรียน:</strong> .......................................................................................... <strong>ชั้น ป.5 &nbsp;&nbsp; เลขที่:</strong> ..........</p>

  <table>
    <thead>
      <tr>
        <th style="width:7%;">ข้อที่</th>
        <th style="width:53%;">ข้อความแสดงความรู้สึกและความคิดเห็น</th>
        <th style="width:8%;">มากที่สุด<br>(5)</th>
        <th style="width:8%;">มาก<br>(4)</th>
        <th style="width:8%;">ปานกลาง<br>(3)</th>
        <th style="width:8%;">น้อย<br>(2)</th>
        <th style="width:8%;">น้อยที่สุด<br>(1)</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td class="center">1</td>
        <td>หนูชอบการเรียนรู้โดยใช้สื่อปฏิสัมพันธ์ผ่านกล้องและการสั่งการด้วยท่าทางมือ เพราะทำให้เข้าใจลำดับคำสั่งได้ง่ายและสนุก</td>
        <td class="center">[ &nbsp; ]</td><td class="center">[ &nbsp; ]</td><td class="center">[ &nbsp; ]</td><td class="center">[ &nbsp; ]</td><td class="center">[ &nbsp; ]</td>
      </tr>
      <tr>
        <td class="center">2</td>
        <td>การจัดวางแฟลชการ์ดคำสั่งรูปธรรมบนโต๊ะ ช่วยให้หนูเข้าใจเรื่องทิศทางซ้าย-ขวา และลำดับขั้นตอนได้ชัดเจน ไม่สับสน</td>
        <td class="center">[ &nbsp; ]</td><td class="center">[ &nbsp; ]</td><td class="center">[ &nbsp; ]</td><td class="center">[ &nbsp; ]</td><td class="center">[ &nbsp; ]</td>
      </tr>
      <tr>
        <td class="center">3</td>
        <td>การจับคู่ทำงานร่วมกับเพื่อนแบบ Pair Programming (ผู้นำทาง Navigator และผู้ขับเคลื่อน Driver) ทำให้ได้ช่วยกันคิด ได้พูดคุย และช่วยเหลือกัน</td>
        <td class="center">[ &nbsp; ]</td><td class="center">[ &nbsp; ]</td><td class="center">[ &nbsp; ]</td><td class="center">[ &nbsp; ]</td><td class="center">[ &nbsp; ]</td>
      </tr>
      <tr>
        <td class="center">4</td>
        <td>หนูรู้สึกท้าทายและสนุกเวลาโปรแกรมทำงานผิดพลาด แล้วได้ร่วมมือกับเพื่อนช่วยกันตรวจหาจุดผิดและแก้ไขให้ถูกต้อง (แก้บั๊ก)</td>
        <td class="center">[ &nbsp; ]</td><td class="center">[ &nbsp; ]</td><td class="center">[ &nbsp; ]</td><td class="center">[ &nbsp; ]</td><td class="center">[ &nbsp; ]</td>
      </tr>
      <tr>
        <td class="center">5</td>
        <td>หนูมีความสุขในการเรียน และอยากเรียนวิชาวิทยาการคำนวณด้วยกิจกรรมเชิงรุกแบบนี้อีกในครั้งต่อไป</td>
        <td class="center">[ &nbsp; ]</td><td class="center">[ &nbsp; ]</td><td class="center">[ &nbsp; ]</td><td class="center">[ &nbsp; ]</td><td class="center">[ &nbsp; ]</td>
      </tr>
    </tbody>
  </table>

  <h3 style="margin-top:16px;">แบบสรุปผลการประเมินความพึงพอใจรายบุคคล (ประเมินจริง N = 8)</h3>
  <table>
    <thead>
      <tr>
        <th style="width:6%;">เลขที่</th><th style="width:28%;">ชื่อ - สกุล ผู้เรียน</th>
        <th style="width:9%;">ข้อ 1<br>(5)</th><th style="width:9%;">ข้อ 2<br>(5)</th><th style="width:9%;">ข้อ 3<br>(5)</th><th style="width:9%;">ข้อ 4<br>(5)</th><th style="width:9%;">ข้อ 5<br>(5)</th>
        <th style="width:9%;">รวม<br>(25)</th><th style="width:10%;">เฉลี่ย<br>(5.00)</th>
        <th style="width:11%;">ระดับ</th>
      </tr>
    </thead>
    <tbody>
      <tr><td class="center">1</td><td>เด็กชายภูฟ้า  แสงศรี</td><td class="center">5</td><td class="center">5</td><td class="center">5</td><td class="center">5</td><td class="center">5</td><td class="center">25</td><td class="center">5.00</td><td class="center" style="color:#15803d; font-weight:600;">มากที่สุด</td></tr>
      <tr><td class="center">2</td><td>เด็กหญิงพิชญาภา  แสงศรี</td><td class="center">4</td><td class="center">4</td><td class="center">5</td><td class="center">4</td><td class="center">4</td><td class="center">21</td><td class="center">4.20</td><td class="center" style="color:#1e3a8a;">มาก</td></tr>
      <tr><td class="center">3</td><td>เด็กหญิงสิริวิมล  สาวิสิทธิ์</td><td class="center">5</td><td class="center">4</td><td class="center">5</td><td class="center">5</td><td class="center">4</td><td class="center">23</td><td class="center">4.60</td><td class="center" style="color:#15803d; font-weight:600;">มากที่สุด</td></tr>
      <tr><td class="center">4</td><td>เด็กหญิงสาวิตรี  สายสมคุณ</td><td class="center">4</td><td class="center">4</td><td class="center">4</td><td class="center">4</td><td class="center">4</td><td class="center">20</td><td class="center">4.00</td><td class="center" style="color:#1e3a8a;">มาก</td></tr>
      <tr><td class="center">5</td><td>เด็กหญิงณัฐณิชา  นันทโพธิ์เดช</td><td class="center">4</td><td class="center">4</td><td class="center">4</td><td class="center">4</td><td class="center">4</td><td class="center">20</td><td class="center">4.00</td><td class="center" style="color:#1e3a8a;">มาก</td></tr>
      <tr><td class="center">6</td><td>เด็กหญิงรฐา  สอนเต็ม</td><td class="center">4</td><td class="center">4</td><td class="center">5</td><td class="center">4</td><td class="center">4</td><td class="center">21</td><td class="center">4.20</td><td class="center" style="color:#1e3a8a;">มาก</td></tr>
      <tr><td class="center">7</td><td>เด็กหญิงกัญญาพัชร  วาจาชื่น</td><td class="center">4</td><td class="center">4</td><td class="center">4</td><td class="center">4</td><td class="center">4</td><td class="center">20</td><td class="center">4.00</td><td class="center" style="color:#1e3a8a;">มาก</td></tr>
      <tr><td class="center">8</td><td>เด็กหญิงกัญญารัตน์  บัวบง</td><td class="center">5</td><td class="center">5</td><td class="center">5</td><td class="center">5</td><td class="center">5</td><td class="center">25</td><td class="center">5.00</td><td class="center" style="color:#15803d; font-weight:600;">มากที่สุด</td></tr>
      <tr style="background:#f1f5f9; font-weight:700;">
        <td colspan="2" class="center">ค่าเฉลี่ยรายข้อและเฉลี่ยรวม (X̄)</td>
        <td class="center">4.38</td><td class="center">4.25</td><td class="center">4.63</td><td class="center">4.38</td><td class="center">4.25</td>
        <td class="center">21.88</td><td class="center">4.38</td>
        <td class="center" style="color:#1e3a8a;">มาก</td>
      </tr>
    </tbody>
  </table>

  <div style="margin-top: 10px; font-size: 11pt; color: #475569;">
    * เกณฑ์การแปลความหมาย: 4.51 - 5.00 = มากที่สุด / 3.51 - 4.50 = มาก / 2.51 - 3.50 = ปรับปรุง / น้อยกว่า 2.50 = น้อย (บรรลุเป้าหมาย PA ระดับ "มาก" ขึ้นไป)
  </div>

  <div class="footer-sig" style="margin-top:14px;">
    ลงชื่อ.................................................................... ครูผู้รวบรวม<br>
    ( นายเตชินท์  อินทมล )<br>
    ตำแหน่ง ครู (ไม่มีวิทยฐานะ) โรงเรียนบ้านโนนป่าหว้านเชียงฮาย
  </div>
</div>

</body>
</html>
"""

with open("ชุดเครื่องมือวัดและประเมินผลการวิจัย_ป5_พร้อมพิมพ์.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("Generated Printable HTML: ชุดเครื่องมือวัดและประเมินผลการวิจัย_ป5_พร้อมพิมพ์.html")
