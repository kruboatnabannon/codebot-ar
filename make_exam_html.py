# -*- coding: utf-8 -*-
from exam_questions import exam_questions

def generate_html():
    html_content = """<!DOCTYPE html>
<html lang="th">
<head>
  <meta charset="UTF-8">
  <title>แบบทดสอบวัดผลสัมฤทธิ์ทางการเรียนรู้วิทยาการคำนวณ ป.5 - โรงเรียนบ้านโนนป่าหว้านเชียงฮาย</title>
  <link href="https://fonts.googleapis.com/css2?family=Sarabun:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    @page {
      size: A4;
      margin: 1.2cm 1.5cm;
    }
    * {
      box-sizing: border-box;
      font-family: 'Sarabun', sans-serif;
    }
    body {
      background-color: #f3f4f6;
      margin: 0;
      padding: 15px;
      color: #111827;
      font-size: 14pt;
      line-height: 1.5;
    }
    .page {
      background: white;
      width: 210mm;
      min-height: 297mm;
      margin: 0 auto 20px auto;
      padding: 18mm 20mm;
      box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
      position: relative;
    }
    @media print {
      body {
        background: white;
        padding: 0;
      }
      .page {
        box-shadow: none;
        margin: 0;
        width: 100%;
        min-height: auto;
        padding: 0;
        page-break-after: always;
      }
      .no-print {
        display: none !important;
      }
    }
    .print-btn-bar {
      max-width: 210mm;
      margin: 0 auto 12px auto;
      display: flex;
      justify-content: space-between;
      align-items: center;
      background: #1e3a8a;
      color: white;
      padding: 10px 18px;
      border-radius: 8px;
    }
    .btn {
      background: #22c55e;
      color: white;
      border: none;
      padding: 7px 16px;
      font-size: 13pt;
      font-weight: 700;
      border-radius: 6px;
      cursor: pointer;
      box-shadow: 0 2px 4px rgba(0,0,0,0.15);
    }
    .btn:hover {
      background: #16a34a;
    }
    .header-box {
      text-align: center;
      margin-bottom: 10px;
      border-bottom: 2px solid #1e3a8a;
      padding-bottom: 8px;
    }
    h1 {
      font-size: 17pt;
      margin: 0 0 4px 0;
      color: #1e3a8a;
      font-weight: 800;
    }
    h2 {
      font-size: 13.5pt;
      margin: 0 0 4px 0;
      color: #374151;
      font-weight: 700;
    }
    h3 {
      font-size: 12.5pt;
      margin: 0;
      color: #6b7280;
      font-weight: 500;
    }
    .info-table {
      width: 100%;
      border-collapse: collapse;
      margin-bottom: 10px;
      font-size: 12.5pt;
    }
    .info-table td, .info-table th {
      border: 1px solid #94a3b8;
      padding: 6px 10px;
    }
    .instructions {
      background: #f8fafc;
      border-left: 4px solid #3b82f6;
      padding: 8px 14px;
      font-size: 12.5pt;
      color: #334155;
      margin-bottom: 12px;
      border-radius: 0 6px 6px 0;
    }
    .part-title {
      background: #e0e7ff;
      color: #1e3a8a;
      padding: 5px 12px;
      font-weight: 700;
      font-size: 13pt;
      border-radius: 4px;
      margin: 10px 0 8px 0;
      border-left: 4px solid #1e3a8a;
    }
    .question-card {
      margin-bottom: 12px;
      font-size: 13pt;
    }
    .q-title {
      font-weight: 700;
      color: #111827;
      margin-bottom: 4px;
      white-space: pre-line;
      line-height: 1.45;
    }
    .options-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 3px 14px;
      padding-left: 14px;
      font-size: 12.5pt;
      color: #374151;
    }
    .opt-item {
      padding: 1px 0;
      line-height: 1.4;
    }

    /* Maze Grid Table for Question 7 */
    .maze-box {
      margin: 8px 0 12px 14px;
    }
    .maze-table {
      border-collapse: collapse;
    }
    .maze-table td {
      width: 86px;
      height: 48px;
      border: 1.5px solid #475569;
      text-align: center;
      vertical-align: middle;
      font-size: 11pt;
      background: #ffffff;
    }
    .maze-table .cell-start {
      background: #dbeafe;
      border: 2px solid #2563eb;
      color: #1e3a8a;
      font-weight: bold;
    }
    .maze-table .cell-path {
      background: #f8fafc;
      color: #475569;
      font-weight: 600;
    }
    .maze-table .cell-goal {
      background: #fef2f2;
      border: 2px solid #dc2626;
      color: #991b1b;
      font-weight: bold;
    }
    .maze-table .cell-empty {
      background: #f1f5f9;
    }

    /* Answer Sheet Page */
    .answer-sheet-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 10px;
      margin-top: 15px;
    }
    .as-col {
      border: 1px solid #cbd5e1;
      border-radius: 6px;
      padding: 8px;
      background: white;
    }
    .as-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 4px 0;
      border-bottom: 1px dashed #f1f5f9;
      font-size: 12.5pt;
    }
    .as-row:last-child {
      border-bottom: none;
    }
    .bubble-row {
      display: flex;
      gap: 6px;
    }
    .bubble-row span {
      display: inline-block;
      width: 22px;
      height: 22px;
      border: 1px solid #94a3b8;
      border-radius: 50%;
      text-align: center;
      line-height: 20px;
      font-size: 11pt;
      color: #475569;
    }
    .key-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 11.5pt;
      margin-top: 10px;
    }
    .key-table th, .key-table td {
      border: 1px solid #94a3b8;
      padding: 5px 8px;
    }
    .key-table th {
      background-color: #f1f5f9;
      font-weight: 700;
      text-align: center;
    }
  </style>
</head>
<body>

  <div class="print-btn-bar no-print">
    <div>
      <span style="font-size: 14pt; font-weight: 700;">🖨️ ระบบพิมพ์แบบทดสอบมาตรฐาน ป.5 (ฉบับภาษาไทย คุ้นชิน มีภาพตารางชัดเจน)</span>
      <span style="font-size: 11pt; opacity: 0.85; margin-left: 10px;">(ว 4.2 ป.5/1 - 2 | 20 ข้อ พร้อมกระดาษคำตอบและเฉลยละเอียด)</span>
    </div>
    <button class="btn" onclick="window.print()">กดพิมพ์หน้านี้ (Print A4)</button>
  </div>
"""

    def render_question(item):
        grid_html = ""
        if item.get('has_grid_7'):
            grid_html = """
      <div class="maze-box">
        <table class="maze-table">
          <tr>
            <td class="cell-path">ช่องที่ 3</td>
            <td class="cell-goal">🍎<br><span style="font-size:10pt;">ผลแอปเปิ้ล</span></td>
            <td class="cell-empty"></td>
            <td class="cell-empty"></td>
          </tr>
          <tr>
            <td class="cell-path">ช่องที่ 2</td>
            <td class="cell-empty"></td>
            <td class="cell-empty"></td>
            <td class="cell-empty"></td>
          </tr>
          <tr>
            <td class="cell-path">ช่องที่ 1</td>
            <td class="cell-empty"></td>
            <td class="cell-empty"></td>
            <td class="cell-empty"></td>
          </tr>
          <tr>
            <td class="cell-start">🤖<br><span style="font-size:10pt;">จุดเริ่ม (หันหน้า ⬆️)</span></td>
            <td class="cell-empty"></td>
            <td class="cell-empty"></td>
            <td class="cell-empty"></td>
          </tr>
        </table>
      </div>"""

        return f"""
    <div class="question-card">
      <div class="q-title">ข้อที่ {item['num']}. {item['q']}</div>
      {grid_html}
      <div class="options-grid">
        <div class="opt-item">{item['options'][0]}</div>
        <div class="opt-item">{item['options'][1]}</div>
        <div class="opt-item">{item['options'][2]}</div>
        <div class="opt-item">{item['options'][3]}</div>
      </div>
    </div>"""

    # -------------------------------------------------------------------------
    # PAGE 1: Header + Questions 1 to 5
    # -------------------------------------------------------------------------
    html_content += """
  <!-- PAGE 1: Header + Part 1 (Questions 1 - 5) -->
  <div class="page">
    <div class="header-box">
      <h1>แบบทดสอบวัดผลสัมฤทธิ์ทางการเรียนรู้วิทยาการคำนวณ (Pre-test / Post-test)</h1>
      <h2>กลุ่มสาระการเรียนรู้วิทยาศาสตร์และเทคโนโลยี รายวิชาเทคโนโลยี (วิทยาการคำนวณ) ว15101 ชั้นประถมศึกษาปีที่ 5</h2>
      <h3>โรงเรียนบ้านโนนป่าหว้านเชียงฮาย สำนักงานเขตพื้นที่การศึกษาประถมศึกษาหนองบัวลำภู เขต 2</h3>
    </div>

    <table class="info-table">
      <tr>
        <td style="width: 48%;">
          <strong>ชื่อ - นามสกุล:</strong> ........................................................................<br>
          <strong>ชั้น ป.5</strong> &nbsp;&nbsp;&nbsp; <strong>เลขที่:</strong> ........... &nbsp;&nbsp;&nbsp; <strong>กลุ่มคู่หูที่:</strong> ...........
        </td>
        <td style="width: 24%; text-align: center;">
          [ &nbsp; ] ก่อนเรียน (Pre-test)<br>
          [ &nbsp; ] หลังเรียน (Post-test)
        </td>
        <td style="width: 13%; text-align: center;">
          <strong>คะแนนเต็ม</strong><br>
          20 คะแนน
        </td>
        <td style="width: 15%; text-align: center;">
          <strong>คะแนนที่ได้</strong><br>
          ......... / 20
        </td>
      </tr>
    </table>

    <div class="instructions">
      <strong>📌 คำชี้แจง:</strong> แบบทดสอบปรนัย 4 ตัวเลือก 20 ข้อ คะแนนเต็ม 20 คะแนน เวลา 40 นาที ให้นักเรียนทำเครื่องหมายกากบาท ( X ) ทับตัวเลือกที่ถูกต้องที่สุดเพียงข้อเดียวลงในกระดาษคำตอบ
    </div>

    <div class="part-title">ตอนที่ 1: การใช้เหตุผลเชิงตรรกะและการแก้ปัญหาในชีวิตประจำวัน (ตัวชี้วัด ว 4.2 ป.5/1)</div>
"""
    for i in range(0, 5):
        html_content += render_question(exam_questions[i])
    html_content += "\n  </div>\n"

    # -------------------------------------------------------------------------
    # PAGE 2: Part 2 (Questions 6 - 10)
    # -------------------------------------------------------------------------
    html_content += """
  <!-- PAGE 2: Part 2 (Questions 6 - 10) -->
  <div class="page">
    <div class="part-title">ตอนที่ 2: การออกแบบโปรแกรมและการจัดลำดับคำสั่ง (ตัวชี้วัด ว 4.2 ป.5/2)</div>
"""
    for i in range(5, 10):
        html_content += render_question(exam_questions[i])
    html_content += "\n  </div>\n"

    # -------------------------------------------------------------------------
    # PAGE 3: Part 3 (Questions 11 - 15)
    # -------------------------------------------------------------------------
    html_content += """
  <!-- PAGE 3: Part 3 (Questions 11 - 15) -->
  <div class="page">
    <div class="part-title">ตอนที่ 3: บล็อกคำสั่งในโปรแกรม Scratch ภาษาไทย (ตัวชี้วัด ว 4.2 ป.5/2)</div>
"""
    for i in range(10, 15):
        html_content += render_question(exam_questions[i])
    html_content += "\n  </div>\n"

    # -------------------------------------------------------------------------
    # PAGE 4: Part 4 (Questions 16 - 20)
    # -------------------------------------------------------------------------
    html_content += """
  <!-- PAGE 4: Part 4 (Questions 16 - 20) -->
  <div class="page">
    <div class="part-title">ตอนที่ 4: การตรวจหาข้อผิดพลาด (บั๊ก) และการทำงานร่วมกันแบบ Pair Programming (ตัวชี้วัด ว 4.2 ป.5/2)</div>
"""
    for i in range(15, 20):
        html_content += render_question(exam_questions[i])
    html_content += "\n  </div>\n"

    # -------------------------------------------------------------------------
    # PAGE 5: Answer Sheet
    # -------------------------------------------------------------------------
    html_content += """
  <!-- PAGE 5: กระดาษคำตอบสำหรับนักเรียน -->
  <div class="page">
    <div class="header-box">
      <h1>กระดาษคำตอบแบบทดสอบวัดผลสัมฤทธิ์ทางการเรียนรู้วิทยาการคำนวณ ป.5</h1>
      <h2>โรงเรียนบ้านโนนป่าหว้านเชียงฮาย สพป.หนองบัวลำภู เขต 2</h2>
    </div>

    <table class="info-table">
      <tr>
        <td style="width: 50%;">
          <strong>ชื่อ - นามสกุล:</strong> ........................................................................<br>
          <strong>ชั้น ป.5</strong> &nbsp;&nbsp;&nbsp; <strong>เลขที่:</strong> ........... &nbsp;&nbsp;&nbsp; <strong>กลุ่มคู่หูที่:</strong> ...........
        </td>
        <td style="width: 25%; text-align: center;">
          [ &nbsp; ] ก่อนเรียน (Pre-test)<br>
          [ &nbsp; ] หลังเรียน (Post-test)
        </td>
        <td style="width: 25%; text-align: center;">
          <strong>คะแนนที่ได้</strong><br>
          <span style="font-size: 16pt; font-weight: bold; color: #1e3a8a;">......... / 20</span>
        </td>
      </tr>
    </table>

    <div class="instructions">
      <strong>📌 วิธีทำ:</strong> ให้นักเรียนทำเครื่องหมายกากบาท ( ✕ ) ทับอักษร ก, ข, ค หรือ ง ที่เป็นคำตอบที่ถูกต้องที่สุดเพียงข้อเดียว
    </div>

    <div class="answer-sheet-grid">
"""
    for col_idx in range(4):
        start_q = col_idx * 5 + 1
        end_q = start_q + 4
        html_content += f"""
      <div class="as-col">
        <div style="font-weight: 700; text-align: center; background: #f1f5f9; padding: 4px; border-radius: 4px; margin-bottom: 6px;">
          ข้อที่ {start_q} - {end_q}
        </div>
"""
        for q_num in range(start_q, end_q + 1):
            html_content += f"""
        <div class="as-row">
          <span style="font-weight: 700; width: 35px;">{q_num}.</span>
          <div class="bubble-row">
            <span>ก</span>
            <span>ข</span>
            <span>ค</span>
            <span>ง</span>
          </div>
        </div>
"""
        html_content += "      </div>\n"

    html_content += """
    </div>

    <div style="margin-top: 35px; display: flex; justify-content: flex-end;">
      <div style="text-align: center; width: 260px;">
        <p>ลงชื่อ ................................................................. ครูผู้ตรวจ</p>
        <p>( นายเตชินท์ อินทมล )</p>
        <p>ตำแหน่ง ครู โรงเรียนบ้านโนนป่าหว้านเชียงฮาย</p>
      </div>
    </div>
  </div>
"""

    # -------------------------------------------------------------------------
    # PAGE 6: Answer Key & Explanation Table
    # -------------------------------------------------------------------------
    html_content += """
  <!-- PAGE 6: ตารางเฉลยละเอียดและเหตุผลประกอบ (สำหรับครูผู้สอน) -->
  <div class="page">
    <div class="header-box">
      <h1>ตารางเฉลยละเอียดและคำอธิบายเหตุผลประกอบ (Teacher Answer Key)</h1>
      <h2>แบบทดสอบวัดผลสัมฤทธิ์ทางการเรียนรู้วิทยาการคำนวณ ป.5 (ฉบับประเด็นท้าทาย วPA)</h2>
    </div>

    <table class="key-table">
      <thead>
        <tr>
          <th style="width: 8%;">ข้อที่</th>
          <th style="width: 14%;">ตัวชี้วัด</th>
          <th style="width: 10%;">เฉลย</th>
          <th style="width: 26%;">สาระการเรียนรู้ / หัวข้อประเมิน</th>
          <th style="width: 42%;">คำอธิบายเหตุผลประกอบ</th>
        </tr>
      </thead>
      <tbody>
"""
    for item in exam_questions:
        html_content += f"""
        <tr>
          <td style="text-align: center; font-weight: 700;">{item['num']}</td>
          <td style="text-align: center; font-size: 10pt;">{item['indicator']}</td>
          <td style="text-align: center; font-weight: 700; color: #1e3a8a; font-size: 13pt;">{item['ans']}</td>
          <td><strong>{item['topic']}</strong></td>
          <td style="font-size: 10.5pt; color: #374151;">{item['exp']}</td>
        </tr>
"""
    html_content += """
      </tbody>
    </table>

    <div style="margin-top: 25px; display: flex; justify-content: space-between; align-items: center; font-size: 11pt; color: #4b5563; border-top: 1px solid #cbd5e1; padding-top: 10px;">
      <div>ผู้สร้างข้อสอบ: นายเตชินท์ อินทมล ตำแหน่ง ครู โรงเรียนบ้านโนนป่าหว้านเชียงฮาย</div>
      <div>สพป.หนองบัวลำภู เขต 2 • ปีการศึกษา 2569</div>
    </div>
  </div>

</body>
</html>
"""
    return html_content

if __name__ == '__main__':
    with open('แบบทดสอบวัดผลสัมฤทธิ์_วิทยาการคำนวณ_ป5_พร้อมพิมพ์.html', 'w', encoding='utf-8') as f:
        f.write(generate_html())
    print("Created 100% Familiar Child-Friendly Exam HTML!")
