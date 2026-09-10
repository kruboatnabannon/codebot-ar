# -*- coding: utf-8 -*-

# 1. Update HTML generator
html_code = """<!DOCTYPE html>
<html lang="th">
<head>
  <meta charset="UTF-8">
  <title>ชุดใบงานภารกิจโค้ดดิ้ง ป.5 (ฉบับพิมพ์หน้า-หลัง 2 แผ่นจบ พอดีขอบกระดาษ A4) - ครูเตชินท์</title>
  <link href="https://fonts.googleapis.com/css2?family=Sarabun:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    @page {
      size: A4 portrait;
      margin: 8mm 10mm 8mm 10mm;
    }
    * {
      box-sizing: border-box;
      font-family: 'Sarabun', sans-serif;
    }
    body {
      background-color: #f1f5f9;
      margin: 0;
      padding: 15px;
      color: #0f172a;
      font-size: 11pt;
      line-height: 1.35;
    }
    .print-bar {
      max-width: 190mm;
      margin: 0 auto 12px auto;
      background: #1e3a8a;
      color: white;
      padding: 10px 16px;
      border-radius: 8px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .print-btn {
      background: #22c55e;
      color: white;
      border: none;
      padding: 6px 16px;
      font-size: 13pt;
      font-weight: 700;
      border-radius: 6px;
      cursor: pointer;
    }
    .print-btn:hover { background: #16a34a; }
    
    .page {
      background: white;
      width: 190mm;
      height: 278mm;
      max-height: 278mm;
      margin: 0 auto 20px auto;
      padding: 7mm 9mm;
      box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
      position: relative;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }
    
    @media print {
      body {
        background: white;
        padding: 0;
        margin: 0;
        -webkit-print-color-adjust: exact;
        print-color-adjust: exact;
      }
      .no-print { display: none !important; }
      .page {
        box-shadow: none;
        margin: 0 !important;
        width: 100% !important;
        height: 278mm !important;
        max-height: 278mm !important;
        padding: 0 !important;
        page-break-after: always !important;
        page-break-inside: avoid !important;
        overflow: hidden !important;
      }
    }
    
    .sheet-tag {
      display: inline-block;
      background: #dbeafe;
      color: #1e40af;
      padding: 2px 8px;
      border-radius: 4px;
      font-size: 10pt;
      font-weight: 700;
    }
    .header-box {
      text-align: center;
      border-bottom: 1.5px solid #1e3a8a;
      padding-bottom: 4px;
      margin-bottom: 6px;
    }
    .header-box h1 {
      font-size: 13.5pt;
      font-weight: 800;
      color: #1e3a8a;
      margin: 0 0 2px 0;
    }
    .header-box p {
      font-size: 9.5pt;
      color: #475569;
      margin: 0;
    }
    .team-table {
      width: 100%;
      border-collapse: collapse;
      margin-bottom: 6px;
    }
    .team-table th, .team-table td {
      border: 1px solid #cbd5e1;
      padding: 3px 6px;
      font-size: 10pt;
    }
    .team-table th {
      background: #f8fafc;
      color: #1e3a8a;
      font-weight: 700;
      text-align: center;
    }
    .mission-box {
      background: #eff6ff;
      border-left: 3.5px solid #2563eb;
      padding: 4px 8px;
      margin-bottom: 6px;
      font-size: 10pt;
      border-radius: 0 4px 4px 0;
      line-height: 1.35;
    }
    .grid-table {
      width: 100%;
      border-collapse: collapse;
      margin-bottom: 6px;
      text-align: center;
    }
    .grid-table th {
      background: #1e293b;
      color: white;
      padding: 2px 4px;
      font-size: 9pt;
      border: 1px solid #0f172a;
    }
    .grid-table td {
      border: 1px solid #cbd5e1;
      height: 25px;
      font-size: 9.5pt;
      font-weight: 600;
      background: #ffffff;
      padding: 1px;
    }
    .grid-table td.obstacle { background: #f1f5f9; color: #475569; }
    .grid-table td.key { background: #fef9c3; color: #854d0e; }
    .grid-table td.laser { background: #fee2e2; color: #991b1b; }
    
    .section-title {
      font-size: 10.5pt;
      font-weight: 700;
      color: #0f172a;
      margin: 4px 0 2px 0;
    }
    .write-box {
      border: 1px solid #cbd5e1;
      border-radius: 5px;
      padding: 6px 10px;
      background: #f8fafc;
      font-size: 10pt;
      line-height: 1.45;
      margin-bottom: 6px;
    }
    .star-bar {
      border: 1px solid #2563eb;
      background: #f0fdf4;
      border-radius: 4px;
      padding: 4px 10px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 10pt;
      font-weight: 700;
      color: #1e3a8a;
      margin-bottom: 4px;
    }
    .footer-sig {
      font-size: 9pt;
      color: #64748b;
      display: flex;
      justify-content: space-between;
      border-top: 1px dashed #cbd5e1;
      padding-top: 3px;
    }
  </style>
</head>
<body>

  <div class="print-bar no-print">
    <div>
      <strong>📄 ชุดใบงานภารกิจโค้ดดิ้ง ป.5 (ฉบับพิมพ์หน้า-หลัง 2 แผ่น จบครบ 4 ภารกิจ พอดีขอบ A4)</strong><br>
      <span style="font-size: 10pt; color: #cbd5e1;">คำแนะนำ: ตั้งค่าเครื่องพิมพ์เป็น "Print on both sides (Flip on long edge)" จะได้กระดาษ 2 แผ่นพอดี</span>
    </div>
    <button class="print-btn" onclick="window.print()">กดพิมพ์ใบงาน (Print A4 Duplex)</button>
  </div>

  <!-- ===================================================================== -->
  <!-- แผ่นที่ 1 [หน้า 1 / ด้านหน้า]: ใบงานที่ 1 - แพทเทิร์นบันไดซ้ำ (ด่าน 1-3 ป.5) -->
  <!-- ===================================================================== -->
  <div class="page">
    <div>
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 2px;">
        <span class="sheet-tag">📄 แผ่นที่ 1 [ด้านหน้า] : ชุดที่ 1 พลังการวนซ้ำ</span>
        <span style="font-size: 9pt; color: #64748b;">รหัสวิชา ว15101 วิทยาการคำนวณ ป.5</span>
      </div>

      <div class="header-box">
        <h1>🚀 ใบงานที่ 1: การค้นหารูปแบบและลูปบันได 3 ขั้น (Pattern & Loops)</h1>
        <p>สอดรับเกมนวัตกรรม CodeBot AR Adventure แทร็ก ป.5 (ด่านที่ 1 - 3) | โรงเรียนบ้านโนนป่าหว้านเชียงฮาย</p>
      </div>

      <table class="team-table">
        <tr>
          <th style="width: 50%;">ข้อมูลคู่หู Active Learning</th>
          <th style="width: 12%;">เลขที่</th>
          <th style="width: 38%;">บทบาทหน้าที่ประจำภารกิจที่ 1</th>
        </tr>
        <tr>
          <td>ชื่อทีม: ............................................................................</td>
          <td style="text-align: center;">-</td>
          <td>กลุ่มคู่หูที่: ....................</td>
        </tr>
        <tr>
          <td>1. .....................................................................................</td>
          <td style="text-align: center;">........</td>
          <td><strong>[ &nbsp; ] Navigator</strong> (ผู้นำทาง วาดแผนที่ & สังเกตรูปแบบ)</td>
        </tr>
        <tr>
          <td>2. .....................................................................................</td>
          <td style="text-align: center;">........</td>
          <td><strong>[ &nbsp; ] Driver</strong> (ผู้สั่งการ ชูการ์ดคำสั่งหน้ากล้อง AR)</td>
        </tr>
      </table>

      <div class="mission-box">
        <strong>🎯 ภารกิจเนวิเกเตอร์ (Navigator):</strong> สังเกตเส้นทางเดินขึ้นบันได 3 ขั้น จะพบว่าหุ่นยนต์ต้องก้าวเดินซ้ำๆ เป็นแพทเทิร์น ให้ใช้ดินสอลากเส้นทางเดินนำ 🤖 เก็บแบตเตอรี่ 🔋 แล้วเข้าสู่ยาน 🚀 โดยไม่ชนหินอวกาศ 🪨 จากนั้นช่วยกันออกแบบบล็อก [วนซ้ำ Loop] ให้โค้ดสั้นที่สุด!
      </div>

      <div class="section-title">🗺️ แผนที่จำลองในเกม (Grid 6x6) - เนวิเกเตอร์ลากเส้นทางเดิน:</div>
      <table class="grid-table">
        <tr>
          <th style="width: 16%;">แถว/คอลัมน์</th><th style="width: 14%;">C1</th><th style="width: 14%;">C2</th><th style="width: 14%;">C3</th><th style="width: 14%;">C4</th><th style="width: 14%;">C5</th><th style="width: 14%;">C6</th>
        </tr>
        <tr>
          <th>R1</th><td></td><td></td><td></td><td style="background: #e0f2fe;">🚀 (ยานแม่)</td><td></td><td></td>
        </tr>
        <tr>
          <th>R2</th><td></td><td></td><td class="obstacle">🪨 (หิน)</td><td style="background: #fef08a;">🔋 (แบต 3)</td><td></td><td></td>
        </tr>
        <tr>
          <th>R3</th><td></td><td class="obstacle">🪨 (หิน)</td><td style="background: #fef08a;">🔋 (แบต 2)</td><td></td><td></td><td></td>
        </tr>
        <tr>
          <th>R4</th><td class="obstacle">🪨 (หิน)</td><td style="background: #fef08a;">🔋 (แบต 1)</td><td></td><td></td><td></td><td></td>
        </tr>
        <tr>
          <th>R5</th><td style="background: #dcfce7;">🤖 (เริ่ม)</td><td></td><td></td><td></td><td></td><td></td>
        </tr>
        <tr>
          <th>R6</th><td></td><td></td><td></td><td></td><td></td><td></td>
        </tr>
      </table>

      <div class="section-title">📝 ถอดรหัสแพทเทิร์นและออกแบบบล็อกลูป (Loop Block Design):</div>
      <div class="write-box">
        1. รูปแบบคำสั่งใน 1 ขั้นบันได ที่ทำซ้ำกัน คือ: [ .......................................................................................................... ]<br>
        2. ต้องทำชุดคำสั่งนี้ซ้ำติดต่อกันทั้งหมด: <strong>.................... รอบ</strong> &nbsp;&nbsp;(เขียนบล็อกลูป: <strong>[ วนซ้ำ Loop ............ รอบ ]</strong>)<br>
        3. เปรียบเทียบความยาวโค้ด: แบบไม่ใช้ลูป = <strong>............ บล็อก</strong> | แบบใช้ลูปย่อคำสั่ง = ลดเหลือเพียง <strong>............ บล็อก!</strong>
      </div>
    </div>

    <div>
      <div class="star-bar">
        <span>⭐ ผลทดสอบหน้ากล้อง AR: [ &nbsp; ] เข้ายานสำเร็จ [ &nbsp; ] ชนหิน</span>
        <span>ดาวที่ได้รับ: [ &nbsp; ] 1 ดาว &nbsp; [ &nbsp; ] 2 ดาว &nbsp; [ &nbsp; ] 3 ดาว 🌟🌟🌟</span>
      </div>

      <div class="footer-sig">
        <span>ครูผู้ตรวจ: นายเตชินท์ อินทมล</span>
        <span>ลายมือชื่อคู่หู: 1) ................................................ 2) ................................................</span>
      </div>
    </div>
  </div>

  <!-- ===================================================================== -->
  <!-- แผ่นที่ 1 [หน้า 2 / ด้านหลัง]: ใบงานที่ 2 - ลูปตรวจรอบสถานี (ด่าน 4 ป.5) -->
  <!-- ===================================================================== -->
  <div class="page">
    <div>
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 2px;">
        <span class="sheet-tag">📄 แผ่นที่ 1 [ด้านหลัง] : ชุดที่ 1 พลังการวนซ้ำ</span>
        <span style="font-size: 9.5pt; color: #dc2626; font-weight: 700;">🔄 สลับบทบาทคู่หูแล้ว!</span>
      </div>

      <div class="header-box">
        <h1>🔄 ใบงานที่ 2: ลูปตรวจรอบสถานีและการลดรูปโค้ด (Perimeter Loop)</h1>
        <p>สอดรับเกมนวัตกรรม CodeBot AR Adventure แทร็ก ป.5 (ด่านที่ 4) | โรงเรียนบ้านโนนป่าหว้านเชียงฮาย</p>
      </div>

      <table class="team-table">
        <tr>
          <th style="width: 50%;">ข้อมูลคู่หู Active Learning</th>
          <th style="width: 12%;">เลขที่</th>
          <th style="width: 38%;">บทบาทหน้าที่ประจำภารกิจที่ 2 (สลับหน้าที่)</th>
        </tr>
        <tr>
          <td>ชื่อทีม: ............................................................................</td>
          <td style="text-align: center;">-</td>
          <td>กลุ่มคู่หูที่: ....................</td>
        </tr>
        <tr>
          <td>1. .....................................................................................</td>
          <td style="text-align: center;">........</td>
          <td><strong>[ &nbsp; ] Driver</strong> (เปลี่ยนมาเป็นผู้สั่งการ ควบคุมหน้ากล้อง AR)</td>
        </tr>
        <tr>
          <td>2. .....................................................................................</td>
          <td style="text-align: center;">........</td>
          <td><strong>[ &nbsp; ] Navigator</strong> (เปลี่ยนมาเป็นผู้นำทาง วางแผนโค้ดประหยัด)</td>
        </tr>
      </table>

      <div class="mission-box">
        <strong>🎯 ภารกิจสลับบทบาท (Swap Role):</strong> หุ่นยนต์ต้องเดินลาดตระเวนรอบสถานีอวกาศ 4 ทิศ เพื่อชาร์จแบตเตอรี่ 🔋 ให้ครบ 4 ด้าน คู่หูต้องช่วยกันเขียนบล็อกลูปแบบผสมหลายคำสั่ง (Multi-Action Loop) ให้โค้ดสั้นและกระชับที่สุด!
      </div>

      <div class="section-title">🗺️ แผนที่ลาดตระเวนรอบสถานี 4 ทิศ (Grid 6x6):</div>
      <table class="grid-table">
        <tr>
          <th style="width: 16%;">แถว/คอลัมน์</th><th style="width: 14%;">C1</th><th style="width: 14%;">C2</th><th style="width: 14%;">C3</th><th style="width: 14%;">C4</th><th style="width: 14%;">C5</th><th style="width: 14%;">C6</th>
        </tr>
        <tr>
          <th>R1</th><td style="background: #e0f2fe;">🚀 (ยาน)</td><td>🔋 (แบต)</td><td>🔋 (แบต)</td><td>🔋 (แบต)</td><td></td><td></td>
        </tr>
        <tr>
          <th>R2</th><td>🔋 (แบต)</td><td class="obstacle">🪨 (แกนกลาง)</td><td class="obstacle">🪨 (แกนกลาง)</td><td>🔋 (แบต)</td><td></td><td></td>
        </tr>
        <tr>
          <th>R3</th><td>🔋 (แบต)</td><td class="obstacle">🪨 (แกนกลาง)</td><td class="obstacle">🪨 (แกนกลาง)</td><td>🔋 (แบต)</td><td></td><td></td>
        </tr>
        <tr>
          <th>R4</th><td style="background: #dcfce7;">🤖 (เริ่ม)</td><td>🔋 (แบต)</td><td>🔋 (แบต)</td><td>🔋 (แบต)</td><td></td><td></td>
        </tr>
        <tr>
          <th>R5</th><td></td><td></td><td></td><td></td><td></td><td></td>
        </tr>
        <tr>
          <th>R6</th><td></td><td></td><td></td><td></td><td></td><td></td>
        </tr>
      </table>

      <div class="section-title">📝 เปรียบเทียบโค้ด 2 รูปแบบ (Code Optimization):</div>
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-bottom: 6px;">
        <div class="write-box" style="margin-bottom: 0;">
          <strong style="color: #dc2626;">❌ แบบเดิม (วางคำสั่งเรียงยาว):</strong><br>
          1. เดินหน้า 3 ก้าว &nbsp;&nbsp;&nbsp;&nbsp; 5. เดินหน้า 3 ก้าว<br>
          2. เลี้ยวขวา &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 6. เลี้ยวขวา<br>
          3. เดินหน้า 3 ก้าว &nbsp;&nbsp;&nbsp;&nbsp; 7. เดินหน้า 3 ก้าว<br>
          4. เลี้ยวขวา<br>
          <span style="font-size: 9pt; color: #64748b;">(ใช้โค้ดยาวถึง 12-16 บล็อก เสียเวลามาก!)</span>
        </div>
        <div class="write-box" style="margin-bottom: 0; background: #f0fdf4; border-color: #86efac;">
          <strong style="color: #16a34a;">✅ แบบประหยัดโค้ด (Multi-Action Loop):</strong><br>
          <strong>[ วนซ้ำ (Loop) ............ รอบ ]</strong><br>
          {<br>
          &nbsp;&nbsp;&nbsp;&nbsp;1. เดินหน้า ............ ก้าว<br>
          &nbsp;&nbsp;&nbsp;&nbsp;2. เลี้ยว ................................<br>
          }<br>
          <span style="font-size: 9pt; color: #15803d; font-weight: 700;">(ประหยัดบล็อกเหลือเพียง 1 ลูปสั้นๆ!)</span>
        </div>
      </div>
    </div>

    <div>
      <div class="star-bar">
        <span>⭐ ผลทดสอบหน้ากล้อง AR: [ &nbsp; ] ลาดตระเวนสำเร็จ 4 ทิศ</span>
        <span>ดาวที่ได้รับ: [ &nbsp; ] 1 ดาว &nbsp; [ &nbsp; ] 2 ดาว &nbsp; [ &nbsp; ] 3 ดาว 🌟🌟🌟</span>
      </div>

      <div class="footer-sig">
        <span>ครูผู้ตรวจ: นายเตชินท์ อินทมล</span>
        <span>ลายมือชื่อคู่หู: 1) ................................................ 2) ................................................</span>
      </div>
    </div>
  </div>

  <!-- ===================================================================== -->
  <!-- แผ่นที่ 2 [หน้า 3 / ด้านหน้า]: ใบงานที่ 3 - เงื่อนไขถ้า...แล้ว กุญแจเลเซอร์ (ด่าน 5-6 ป.5) -->
  <!-- ===================================================================== -->
  <div class="page">
    <div>
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 2px;">
        <span class="sheet-tag" style="background: #fef3c7; color: #92400e;">📄 แผ่นที่ 2 [ด้านหน้า] : ชุดที่ 2 เงื่อนไขและแก้บั๊ก</span>
        <span style="font-size: 9pt; color: #64748b;">รหัสวิชา ว15101 วิทยาการคำนวณ ป.5</span>
      </div>

      <div class="header-box">
        <h1>⚡ ใบงานที่ 3: เงื่อนไขถ้า...แล้ว กับประตูปริศนาเลเซอร์และกุญแจ (If-Then)</h1>
        <p>สอดรับเกมนวัตกรรม CodeBot AR Adventure แทร็ก ป.5 (ด่านที่ 5 - 6) | โรงเรียนบ้านโนนป่าหว้านเชียงฮาย</p>
      </div>

      <table class="team-table">
        <tr>
          <th style="width: 50%;">ข้อมูลคู่หู Active Learning</th>
          <th style="width: 12%;">เลขที่</th>
          <th style="width: 38%;">บทบาทหน้าที่ประจำภารกิจที่ 3</th>
        </tr>
        <tr>
          <td>ชื่อทีม: ............................................................................</td>
          <td style="text-align: center;">-</td>
          <td>กลุ่มคู่หูที่: ....................</td>
        </tr>
        <tr>
          <td>1. .....................................................................................</td>
          <td style="text-align: center;">........</td>
          <td><strong>[ &nbsp; ] Navigator</strong> (ผู้นำทาง คำนวณเงื่อนไขและทางแยก)</td>
        </tr>
        <tr>
          <td>2. .....................................................................................</td>
          <td style="text-align: center;">........</td>
          <td><strong>[ &nbsp; ] Driver</strong> (ผู้สั่งการ ส่องการ์ดกุญแจหน้ากล้อง AR)</td>
        </tr>
      </table>

      <div class="mission-box">
        <strong>🎯 ภารกิจคิดเชิงตรรกะแบบมีเงื่อนไข:</strong> ประตูเลเซอร์ ⚡ กั้นทางเข้ายานอวกาศอยู่ ห้ามเดินชนเด็ดขาด! หุ่นยนต์ต้องวางแผนเดินไปเก็บกุญแจคีย์การ์ด 🗝️ เสียก่อน ประตูเลเซอร์จึงจะดับลง ให้นักเรียนเขียนประโยคเงื่อนไขตรรกะและแบ่งคำสั่งออกเป็น 2 เฟส
      </div>

      <div class="section-title">🗺️ แผนที่ประตูปริศนาเลเซอร์และกุญแจคีย์การ์ด (Grid 6x6):</div>
      <table class="grid-table">
        <tr>
          <th style="width: 16%;">แถว/คอลัมน์</th><th style="width: 14%;">C1</th><th style="width: 14%;">C2</th><th style="width: 14%;">C3</th><th style="width: 14%;">C4</th><th style="width: 14%;">C5</th><th style="width: 14%;">C6</th>
        </tr>
        <tr>
          <th>R1</th><td></td><td></td><td></td><td class="laser">⚡ (เลเซอร์)</td><td style="background: #e0f2fe;">🚀 (ยานแม่)</td><td></td>
        </tr>
        <tr>
          <th>R2</th><td class="key">🗝️ (กุญแจ)</td><td></td><td></td><td class="laser">⚡ (เลเซอร์)</td><td></td><td></td>
        </tr>
        <tr>
          <th>R3</th><td class="obstacle">🪨 (หิน)</td><td class="obstacle">🪨 (หิน)</td><td></td><td></td><td></td><td></td>
        </tr>
        <tr>
          <th>R4</th><td style="background: #dcfce7;">🤖 (เริ่ม)</td><td></td><td></td><td></td><td></td><td></td>
        </tr>
        <tr>
          <th>R5</th><td></td><td></td><td></td><td></td><td></td><td></td>
        </tr>
        <tr>
          <th>R6</th><td></td><td></td><td></td><td></td><td></td><td></td>
        </tr>
      </table>

      <div class="section-title">🧠 โครงสร้างตรรกะเงื่อนไข If-Then-Else ของคู่เรา:</div>
      <div class="write-box">
        • <strong>[ ถ้า (IF) ]</strong> : หุ่นยนต์มีไอเทมชิ้นนี้ คือ [ ............................................................................................ ]<br>
        • <strong>[ แล้ว (THEN) ]</strong> : ประตูเลเซอร์จะเกิดผลคือ [ ........................................................................................... ] และเดินผ่านได้<br>
        • <strong>[ มิฉะนั้น (ELSE) ]</strong> : ถ้ายังไม่มีกุญแจ ห้ามเดินชน เพราะจะเกิดผลคือ [ ............................................................ ]
      </div>

      <div class="section-title">📝 วางแผนคำสั่ง 2 เฟส (เขียนตัวโตๆ ได้เลย):</div>
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-bottom: 6px;">
        <div class="write-box" style="margin-bottom: 0;">
          <strong>เฟส 1: เดินไปเก็บกุญแจ 🗝️</strong><br>
          1. .........................................................................<br>
          2. .........................................................................<br>
          3. .........................................................................
        </div>
        <div class="write-box" style="margin-bottom: 0;">
          <strong>เฟส 2: เดินทะลุประตูเลเซอร์เข้ายาน 🚀</strong><br>
          1. .........................................................................<br>
          2. .........................................................................<br>
          3. .........................................................................
        </div>
      </div>
    </div>

    <div>
      <div class="star-bar">
        <span>⭐ ผลทดสอบหน้ากล้อง AR: [ &nbsp; ] ปลดล็อกเลเซอร์สำเร็จ</span>
        <span>ดาวที่ได้รับ: [ &nbsp; ] 1 ดาว &nbsp; [ &nbsp; ] 2 ดาว &nbsp; [ &nbsp; ] 3 ดาว 🌟🌟🌟</span>
      </div>

      <div class="footer-sig">
        <span>ครูผู้ตรวจ: นายเตชินท์ อินทมล</span>
        <span>ลายมือชื่อคู่หู: 1) ................................................ 2) ................................................</span>
      </div>
    </div>
  </div>

  <!-- ===================================================================== -->
  <!-- แผ่นที่ 2 [หน้า 4 / ด้านหลัง]: ใบงานที่ 4 - ยอดนักสืบแก้บั๊ก & มาสเตอร์ (ด่าน 7-10 ป.5) -->
  <!-- ===================================================================== -->
  <div class="page">
    <div>
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 2px;">
        <span class="sheet-tag" style="background: #fef3c7; color: #92400e;">📄 แผ่นที่ 2 [ด้านหลัง] : ชุดที่ 2 เงื่อนไขและแก้บั๊ก</span>
        <span style="font-size: 9.5pt; color: #dc2626; font-weight: 700;">🔄 สลับบทบาทคู่หูแล้ว!</span>
      </div>

      <div class="header-box">
        <h1>🐞 ใบงานที่ 4: ยอดนักสืบแก้บั๊กตรรกะและบททดสอบมาสเตอร์ ป.5</h1>
        <p>สอดรับเกมนวัตกรรม CodeBot AR Adventure แทร็ก ป.5 (ด่านที่ 7 - 10) | โรงเรียนบ้านโนนป่าหว้านเชียงฮาย</p>
      </div>

      <table class="team-table">
        <tr>
          <th style="width: 50%;">ข้อมูลคู่หู Active Learning</th>
          <th style="width: 12%;">เลขที่</th>
          <th style="width: 38%;">บทบาทหน้าที่ประจำภารกิจที่ 4 (สลับหน้าที่)</th>
        </tr>
        <tr>
          <td>ชื่อทีม: ............................................................................</td>
          <td style="text-align: center;">-</td>
          <td>กลุ่มคู่หูที่: ....................</td>
        </tr>
        <tr>
          <td>1. .....................................................................................</td>
          <td style="text-align: center;">........</td>
          <td><strong>[ &nbsp; ] Driver</strong> (เปลี่ยนมาเป็นผู้สั่งการ ทดสอบโค้ดแก้บั๊ก)</td>
        </tr>
        <tr>
          <td>2. .....................................................................................</td>
          <td style="text-align: center;">........</td>
          <td><strong>[ &nbsp; ] Navigator</strong> (เปลี่ยนมาเป็นผู้นำทาง วิเคราะห์จุดผิดพลาด)</td>
        </tr>
      </table>

      <div class="mission-box">
        <strong>🎯 ภารกิจนักสืบแก้บั๊ก (Debugging):</strong> โค้ดเดิมมีข้อผิดพลาด (Bug) ทำให้หุ่นยนต์เดินตรงไปชนประตูเลเซอร์ก่อนที่จะเก็บกุญแจ! ให้นักเรียนช่วยกันสืบหาจุดผิด แก้ไขให้ถูกต้อง จากนั้นบันทึกการสะท้อนคิดถอดบทเรียนร่วมกัน
      </div>

      <div class="section-title">🐞 ตารางตรวจจับและแก้ไขบั๊ก (Bug Detective Table):</div>
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-bottom: 6px;">
        <div class="write-box" style="margin-bottom: 0; background: #fff1f2; border-color: #fca5a5;">
          <strong style="color: #b91c1c;">❌ โค้ดเดิมที่มีข้อผิดพลาด (Bug):</strong><br>
          1. เดินหน้า 3 ก้าวตรงไปที่ประตูเลเซอร์<br>
          &nbsp;&nbsp;&nbsp;&nbsp;<strong>❌ (บั๊ก! ชนเลเซอร์เพราะยังไม่มีกุญแจ)</strong><br>
          2. เลี้ยวซ้ายไปหากุญแจ<br>
          3. เก็บกุญแจคีย์การ์ด<br>
          4. เดินเข้ายานอวกาศ
        </div>
        <div class="write-box" style="margin-bottom: 0; background: #f0fdf4; border-color: #86efac;">
          <strong style="color: #15803d;">✅ โค้ดใหม่ที่ถูกต้อง (คู่หูเราแก้ไขแล้ว):</strong><br>
          1. แก้ไขเป็น: ............................................................<br>
          2. ................................................................................<br>
          3. ................................................................................<br>
          4. เดินเข้ายานอวกาศสำเร็จ!
        </div>
      </div>

      <div class="section-title">💬 การสะท้อนคิดถอดบทเรียนร่วมกัน (After Action Review: AAR):</div>
      <div class="write-box">
        1. สิ่งที่คู่หู (Driver & Navigator) ของเราช่วยเหลือกันได้ดีที่สุด คืออะไร?<br>
        &nbsp;&nbsp;&nbsp;&nbsp;ตอบ: ............................................................................................................................................................<br>
        2. การใช้การ์ดคำสั่งและเล่นเกม AR บนโต๊ะ ช่วยให้เราเข้าใจการเขียนโปรแกรมง่ายขึ้นอย่างไร?<br>
        &nbsp;&nbsp;&nbsp;&nbsp;ตอบ: ............................................................................................................................................................<br>
        3. ถ้าในชีวิตจริงเราเจอปัญหาที่แก้ไม่ออก เราจะนำวิธี "หาจุดผิดพลาดทีละก้าว (Debugging)" ไปใช้อย่างไร?<br>
        &nbsp;&nbsp;&nbsp;&nbsp;ตอบ: ............................................................................................................................................................
      </div>
    </div>

    <div>
      <div class="star-bar" style="background: #eff6ff; border-color: #3b82f6;">
        <span>🏆 บททดสอบมาสเตอร์ ป.5: ผ่านครบ 10 ด่าน!</span>
        <span>คะแนนดาวสะสมรวม: ............ / 30 ดาว ⭐⭐⭐</span>
      </div>

      <div class="footer-sig">
        <span>ครูผู้ตรวจ: นายเตชินท์ อินทมล</span>
        <span>ลายมือชื่อคู่หู: 1) ................................................ 2) ................................................</span>
      </div>
    </div>
  </div>

</body>
</html>"""

with open("ใบงานภารกิจโค้ดดิ้ง_ป5_ชุดสมบูรณ์_4ใบงาน.html", "w", encoding="utf-8") as f:
    f.write(html_code)

print("Updated HTML with perfect compact print margins!")
