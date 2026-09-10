# -*- coding: utf-8 -*-
import os, zipfile, html

# ==============================================================================
# 1. HTML GENERATION (SET 2: MODERN 2-COLUMN SPLIT-CARD DESIGN)
# ==============================================================================

html_content = """<!DOCTYPE html>
<html lang="th">
<head>
  <meta charset="UTF-8">
  <title>ชุดใบงานภารกิจโค้ดดิ้ง ป.5 [ชุดที่ 2: สไตล์การ์ดแยก 2 คอลัมน์ สวยงามกระชับ พอดี A4] - ครูเตชินท์</title>
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
      background-color: #f8fafc;
      margin: 0;
      padding: 15px;
      color: #0f172a;
      font-size: 10pt;
      line-height: 1.35;
    }
    .print-bar {
      max-width: 190mm;
      margin: 0 auto 12px auto;
      background: #0284c7;
      color: white;
      padding: 12px 18px;
      border-radius: 8px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
    }
    .print-instructions {
      font-size: 9.5pt;
      color: #e0f2fe;
      line-height: 1.4;
    }
    .print-instructions strong { color: #fef08a; }
    .print-btn {
      background: #10b981;
      color: white;
      border: none;
      padding: 8px 18px;
      font-size: 12pt;
      font-weight: 700;
      border-radius: 6px;
      cursor: pointer;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .print-btn:hover { background: #059669; }

    /* Page container */
    .page {
      background: white;
      width: 190mm;
      height: 262mm;
      max-height: 262mm;
      margin: 0 auto 20px auto;
      padding: 6mm 8mm;
      box-shadow: 0 4px 6px -1px rgba(0,0,0,0.08);
      position: relative;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      border: 1px solid #e2e8f0;
      border-radius: 4px;
    }

    @media print {
      html, body {
        background: white !important;
        padding: 0 !important;
        margin: 0 !important;
        -webkit-print-color-adjust: exact !important;
        print-color-adjust: exact !important;
      }
      .no-print { display: none !important; }
      .page {
        border: none !important;
        box-shadow: none !important;
        margin: 0 !important;
        width: 100% !important;
        height: 262mm !important;
        max-height: 262mm !important;
        padding: 0 !important;
        page-break-inside: avoid !important;
        break-inside: avoid !important;
        page-break-after: always !important;
        break-after: page !important;
        overflow: hidden !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: space-between !important;
      }
      .page:last-child {
        page-break-after: auto !important;
        break-after: auto !important;
      }
    }

    .top-meta {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 2px;
    }
    .sheet-badge {
      background: #e0e7ff;
      color: #3730a3;
      padding: 2px 8px;
      border-radius: 4px;
      font-size: 8.5pt;
      font-weight: 700;
    }
    .header-box {
      text-align: center;
      border-bottom: 2px solid #0284c7;
      padding-bottom: 3px;
      margin-bottom: 5px;
    }
    .header-box h1 {
      font-size: 12.5pt;
      font-weight: 800;
      color: #0369a1;
      margin: 0 0 1px 0;
    }
    .header-box p {
      font-size: 8.5pt;
      color: #475569;
      margin: 0;
    }
    .team-table {
      width: 100%;
      border-collapse: collapse;
      margin-bottom: 5px;
    }
    .team-table th, .team-table td {
      border: 1px solid #cbd5e1;
      padding: 2px 5px;
      font-size: 9pt;
    }
    .team-table th {
      background: #f1f5f9;
      color: #0f172a;
      font-weight: 700;
      text-align: center;
    }

    /* Modern Callout Banner (Top) */
    .callout-banner {
      background: #fefce8;
      border-left: 4px solid #f59e0b;
      border-radius: 0 6px 6px 0;
      padding: 4px 8px;
      margin-bottom: 6px;
      font-size: 9pt;
      line-height: 1.35;
      color: #78350f;
    }

    /* 2-Column Split Grid */
    .split-container {
      display: grid;
      grid-template-columns: 215px 1fr;
      gap: 10px;
      align-items: stretch;
      margin-bottom: 6px;
    }

    /* Left Card: Map Board */
    .map-card {
      border: 1.5px solid #f59e0b;
      border-radius: 8px;
      padding: 6px 8px;
      background: #ffffff;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: space-between;
      box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }
    .card-title-left {
      font-size: 9.5pt;
      font-weight: 700;
      color: #92400e;
      text-align: center;
      margin-bottom: 4px;
    }
    .grid-table {
      border-collapse: collapse;
      margin: 0 auto 4px auto;
    }
    .grid-table td {
      width: 28px;
      height: 28px;
      border: 1px solid #93c5fd;
      text-align: center;
      vertical-align: middle;
      font-size: 11pt;
      padding: 0;
      background: #ffffff;
    }
    .grid-table td.robot { background: #dcfce7; border: 2px solid #22c55e; }
    .grid-table td.rocket { background: #fef08a; }
    .grid-table td.rock { background: #64748b; color: white; }
    .grid-table td.laser { background: #fee2e2; }
    .grid-table td.key { background: #fef9c3; }
    .grid-caption {
      font-size: 8pt;
      color: #475569;
      text-align: center;
      line-height: 1.25;
      margin-top: 2px;
    }

    /* Right Card: Challenges & Code */
    .quest-card {
      border: 1.5px solid #cbd5e1;
      border-radius: 8px;
      padding: 8px 10px;
      background: #ffffff;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }
    .card-title-right {
      font-size: 10pt;
      font-weight: 700;
      color: #1e3a8a;
      margin-bottom: 4px;
      display: flex;
      align-items: center;
      gap: 4px;
    }
    .quest-item {
      font-size: 9pt;
      line-height: 1.35;
      margin-bottom: 4px;
    }
    .dotted-divider {
      border-top: 1px dotted #94a3b8;
      margin: 3px 0;
    }
    .dashed-code-box {
      border: 1.5px dashed #f59e0b;
      background: #fffbeb;
      border-radius: 6px;
      padding: 5px 8px;
      font-size: 8.5pt;
      line-height: 1.35;
      color: #92400e;
      margin-top: 3px;
    }

    /* Footer & Stamps */
    .bottom-section {
      margin-top: auto;
    }
    .star-bar {
      border: 1px solid #0284c7;
      background: #f0fdf4;
      border-radius: 5px;
      padding: 3px 8px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 8.5pt;
      font-weight: 700;
      color: #0369a1;
      margin-bottom: 3px;
    }
    .footer-sig {
      font-size: 8pt;
      color: #64748b;
      display: flex;
      justify-content: space-between;
      border-top: 1px dashed #cbd5e1;
      padding-top: 2px;
    }
  </style>
</head>
<body>

  <div class="print-bar no-print">
    <div class="print-instructions">
      <strong style="font-size: 11pt; color: #ffffff;">🎨 ชุดใบงานภารกิจโค้ดดิ้ง ป.5 [ชุดที่ 2: สไตล์ Modern Split-Card 2 คอลัมน์]</strong><br>
      • <strong>ดีไซน์ใหม่:</strong> ย่อตารางแผนที่ 6x6 ไว้ฝั่งซ้าย + วางโจทย์เจาะลึกคำสั่งไว้ฝั่งขวา อ่านและเขียนตอบสะดวก ไม่กินพื้นที่แนวตั้ง<br>
      • <strong>การพิมพ์:</strong> ติ๊กเลือก <strong>"พิมพ์สองหน้า (Two-sided) -> พลิกด้านยาว (Flip on long edge)"</strong> จะได้ 2 แผ่น จบครบ 4 ภารกิจพอดีเป๊ะ!
    </div>
    <button class="print-btn" onclick="window.print()">🖨️ สั่งพิมพ์ชุดที่ 2 (Print A4)</button>
  </div>

  <!-- ===================================================================== -->
  <!-- แผ่นที่ 1 [หน้า 1 / ด้านหน้า]: ใบงานที่ 1 - แพทเทิร์นบันได 3 ขั้น (ด่าน 1-3 ป.5) -->
  <!-- ===================================================================== -->
  <div class="page">
    <div>
      <div class="top-meta">
        <span class="sheet-badge">📄 แผ่นที่ 1 [ด้านหน้า] : ชุดที่ 2 โมเดิร์นการ์ด</span>
        <span style="font-size: 8.5pt; color: #64748b;">รหัสวิชา ว15101 วิทยาการคำนวณ ชั้น ป.5</span>
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

      <div class="callout-banner">
        <strong>🎯 คำแนะนำภารกิจบันได 3 ขั้น:</strong> สังเกตเส้นทางเดินขึ้นบันได จะพบว่ามีการเดินซ้ำเป็นแพทเทิร์น ให้นักเรียนช่วยกันจับกลุ่มคำสั่งซ้ำ แล้วนำบล็อก <strong>[วนซ้ำ Loop]</strong> มาครอบเพื่อลดจำนวนโค้ดให้สั้นที่สุด!
      </div>

      <div class="split-container">
        <div class="map-card">
          <div class="card-title-left">🗺️ แผนที่ด่านบันได 3 ขั้นทะยานฟ้า</div>
          <table class="grid-table">
            <tr>
              <td></td><td></td><td></td><td class="rocket">🚀</td><td></td><td></td>
            </tr>
            <tr>
              <td></td><td></td><td class="rock">🪨</td><td>🔋</td><td></td><td></td>
            </tr>
            <tr>
              <td></td><td class="rock">🪨</td><td>🔋</td><td></td><td></td><td></td>
            </tr>
            <tr>
              <td class="rock">🪨</td><td>🔋</td><td></td><td></td><td></td><td></td>
            </tr>
            <tr>
              <td class="robot">🤖</td><td></td><td></td><td></td><td></td><td></td>
            </tr>
            <tr>
              <td></td><td></td><td></td><td></td><td></td><td></td>
            </tr>
          </table>
          <div class="grid-caption">
            <strong>เนวิเกเตอร์:</strong> ใช้สีระบายขั้นบันได 3 ขั้น เพื่อดูชุดคำสั่งที่ซ้ำกัน!
          </div>
        </div>

        <div class="quest-card">
          <div>
            <div class="card-title-right">🔍 เจาะลึกแพทเทิร์นคำสั่งซ้ำ</div>
            <div class="quest-item">
              <strong>1. ใน 1 ขั้นบันได หุ่นยนต์ต้องทำคำสั่งอะไรบ้าง?</strong><br>
              คำตอบ: ............................................................................................
            </div>
            <div class="dotted-divider"></div>
            <div class="quest-item">
              <strong>2. ต้องทำคำสั่งชุดนี้ซ้ำทั้งหมดกี่รอบ?</strong><br>
              ตอบ: ทำซ้ำจำนวน .................... รอบ
            </div>
            <div class="dotted-divider"></div>
            <div class="quest-item">
              <strong>3. เขียนบล็อกลูปคำสั่งที่คู่เราออกแบบ:</strong>
            </div>
          </div>
          <div class="dashed-code-box">
            <strong>[ วนซ้ำ (Loop) ............ รอบ ] {</strong><br>
            &nbsp;&nbsp;&nbsp;&nbsp;1) ....................................................................................<br>
            &nbsp;&nbsp;&nbsp;&nbsp;2) ....................................................................................<br>
            <strong>}</strong>
          </div>
        </div>
      </div>
    </div>

    <div class="bottom-section">
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
      <div class="top-meta">
        <span class="sheet-badge">📄 แผ่นที่ 1 [ด้านหลัง] : ชุดที่ 2 โมเดิร์นการ์ด</span>
        <span style="font-size: 8.5pt; color: #dc2626; font-weight: 700;">🔄 สลับบทบาทคู่หูแล้ว!</span>
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

      <div class="callout-banner" style="border-color: #0284c7; background: #f0f9ff; color: #0369a1;">
        <strong>🎯 คำแนะนำภารกิจรอบสถานี 4 ทิศ:</strong> หุ่นยนต์ต้องเดินลาดตระเวนรอบสถานีเพื่อชาร์จแบตเตอรี่ 4 จุด คู่หูช่วยกันนำบล็อก <strong>[วนซ้ำ Loop]</strong> แบบผสมคำสั่ง (เดินหน้า+เลี้ยว) มาใช้ย่อโค้ดจากเดิม 16 บล็อกให้เหลือเพียงบล็อกเดียว!
      </div>

      <div class="split-container">
        <div class="map-card" style="border-color: #0284c7;">
          <div class="card-title-left" style="color: #0369a1;">🗺️ แผนที่ลาดตระเวนรอบสถานี</div>
          <table class="grid-table">
            <tr>
              <td class="rocket">🚀</td><td>🔋</td><td>🔋</td><td>🔋</td><td></td><td></td>
            </tr>
            <tr>
              <td>🔋</td><td class="rock">🪨</td><td class="rock">🪨</td><td>🔋</td><td></td><td></td>
            </tr>
            <tr>
              <td>🔋</td><td class="rock">🪨</td><td class="rock">🪨</td><td>🔋</td><td></td><td></td>
            </tr>
            <tr>
              <td class="robot">🤖</td><td>🔋</td><td>🔋</td><td>🔋</td><td></td><td></td>
            </tr>
            <tr>
              <td></td><td></td><td></td><td></td><td></td><td></td>
            </tr>
            <tr>
              <td></td><td></td><td></td><td></td><td></td><td></td>
            </tr>
          </table>
          <div class="grid-caption">
            <strong>เนวิเกเตอร์:</strong> ลากเส้นเดินวนขวาตามเข็มนาฬิกา ครบ 4 ทิศทาง!
          </div>
        </div>

        <div class="quest-card">
          <div>
            <div class="card-title-right">⚡ เปรียบเทียบโค้ดลดรูป (Code Optimization)</div>
            <div class="quest-item">
              <strong>1. โค้ดเดิมแบบไม่ใช้ลูป (เรียงยาว 12 บล็อก):</strong><br>
              <span style="font-size: 8pt; color: #64748b;">(เดินหน้า 3 ก้าว &rarr; เลี้ยวขวา &rarr; เดินหน้า 3 ก้าว &rarr; เลี้ยวขวา ... ยาวมาก)</span>
            </div>
            <div class="dotted-divider"></div>
            <div class="quest-item">
              <strong>2. ใน 1 ด้าน หุ่นยนต์ต้องเดินหน้ากี่ก้าว และเลี้ยวทางไหน?</strong><br>
              ตอบ: เดินหน้า ............ ก้าว และ เลี้ยว ........................
            </div>
            <div class="dotted-divider"></div>
            <div class="quest-item">
              <strong>3. เขียนบล็อกย่อโค้ดแบบประหยัด (Multi-Action Loop):</strong>
            </div>
          </div>
          <div class="dashed-code-box" style="border-color: #0284c7; background: #f0fdf4; color: #15803d;">
            <strong>[ วนซ้ำ (Loop) ............ รอบ ] {</strong><br>
            &nbsp;&nbsp;&nbsp;&nbsp;1) เดินหน้า ............ ก้าว<br>
            &nbsp;&nbsp;&nbsp;&nbsp;2) เลี้ยว ........................................<br>
            <strong>}</strong>
          </div>
        </div>
      </div>
    </div>

    <div class="bottom-section">
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
      <div class="top-meta">
        <span class="sheet-badge" style="background: #fef3c7; color: #92400e;">📄 แผ่นที่ 2 [ด้านหน้า] : ชุดที่ 2 โมเดิร์นการ์ด</span>
        <span style="font-size: 8.5pt; color: #64748b;">รหัสวิชา ว15101 วิทยาการคำนวณ ชั้น ป.5</span>
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

      <div class="callout-banner" style="border-color: #eab308; background: #fefce8; color: #854d0e;">
        <strong>🎯 คำแนะนำภารกิจประตูปริศนาเลเซอร์:</strong> ประตูเลเซอร์ ⚡ ขวางทางเข้ายานอยู่ ห้ามเดินชนเด็ดขาด! หุ่นยนต์ต้องไปเก็บกุญแจคีย์การ์ด 🗝️ เสียก่อน ประตูเลเซอร์จึงจะดับลง ให้นักเรียนเขียนประโยคเงื่อนไขและวางแผนโค้ด 2 เฟส
      </div>

      <div class="split-container">
        <div class="map-card" style="border-color: #eab308;">
          <div class="card-title-left" style="color: #a16207;">🗺️ แผนที่ประตูปริศนาเลเซอร์</div>
          <table class="grid-table">
            <tr>
              <td></td><td></td><td></td><td class="laser">⚡</td><td class="rocket">🚀</td><td></td>
            </tr>
            <tr>
              <td class="key">🗝️</td><td></td><td></td><td class="laser">⚡</td><td></td><td></td>
            </tr>
            <tr>
              <td class="rock">🪨</td><td class="rock">🪨</td><td></td><td></td><td></td><td></td>
            </tr>
            <tr>
              <td class="robot">🤖</td><td></td><td></td><td></td><td></td><td></td>
            </tr>
            <tr>
              <td></td><td></td><td></td><td></td><td></td><td></td>
            </tr>
            <tr>
              <td></td><td></td><td></td><td></td><td></td><td></td>
            </tr>
          </table>
          <div class="grid-caption">
            <strong>เนวิเกเตอร์:</strong> ลากเส้นเฟส 1 ไปเก็บ 🗝️ แล้วเฟส 2 ผ่าน ⚡ เข้ายาน!
          </div>
        </div>

        <div class="quest-card">
          <div>
            <div class="card-title-right">🧠 ตรรกะเงื่อนไขและการวางแผน 2 เฟส</div>
            <div class="quest-item">
              <strong>1. ประโยคเงื่อนไข If-Then ของคู่เรา:</strong><br>
              • <strong>[ ถ้า (IF) ]</strong> : มีไอเทม [ ........................................................ ]<br>
              • <strong>[ แล้ว (THEN) ]</strong> : ประตูเลเซอร์จะ [ ................................. ]<br>
              • <strong>[ มิฉะนั้น ]</strong> : ถ้าชนจะเกิดผลคือ [ ..................................... ]
            </div>
            <div class="dotted-divider"></div>
            <div class="quest-item">
              <strong>2. วางแผนคำสั่ง 2 เฟสพิชิตด่าน:</strong>
            </div>
          </div>
          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 6px; margin-top: 2px;">
            <div class="dashed-code-box" style="border-color: #eab308; background: #fffdf5; color: #854d0e; padding: 4px 6px;">
              <strong>🗝️ เฟส 1: เก็บกุญแจ</strong><br>
              1. ........................................<br>
              2. ........................................<br>
              3. ........................................
            </div>
            <div class="dashed-code-box" style="border-color: #0284c7; background: #f0f9ff; color: #0369a1; padding: 4px 6px;">
              <strong>🚀 เฟส 2: เข้ายานอวกาศ</strong><br>
              1. ........................................<br>
              2. ........................................<br>
              3. ........................................
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="bottom-section">
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
      <div class="top-meta">
        <span class="sheet-badge" style="background: #fef3c7; color: #92400e;">📄 แผ่นที่ 2 [ด้านหลัง] : ชุดที่ 2 โมเดิร์นการ์ด</span>
        <span style="font-size: 8.5pt; color: #dc2626; font-weight: 700;">🔄 สลับบทบาทคู่หูแล้ว!</span>
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

      <div class="callout-banner" style="border-color: #ef4444; background: #fef2f2; color: #991b1b;">
        <strong>🎯 คำแนะนำภารกิจแก้บั๊ก & ถอดบทเรียน:</strong> ในเกมมีบั๊กหุ่นยนต์เดินตรงไปชนประตูเลเซอร์ก่อนเก็บกุญแจ! ให้ช่วยกันสืบหาจุดผิดและเขียนโค้ดที่ถูกต้อง จากนั้นบันทึกการสะท้อนคิดถอดบทเรียน (AAR) ร่วมกัน
      </div>

      <div class="split-container">
        <div class="map-card" style="border-color: #ef4444; justify-content: flex-start;">
          <div class="card-title-left" style="color: #b91c1c;">🐞 ตรวจจับและกำจัดบั๊ก</div>
          
          <div style="width: 100%; background: #fee2e2; border: 1px solid #fca5a5; border-radius: 6px; padding: 5px; font-size: 8pt; margin-bottom: 5px; line-height: 1.3;">
            <strong style="color: #991b1b;">❌ โค้ดเดิมที่มีข้อผิดพลาด:</strong><br>
            1. เดินหน้า 3 ก้าวตรงไปที่เลเซอร์<br>
            &nbsp;&nbsp;&nbsp;<strong>(บั๊ก! ชนเลเซอร์ดับ)</strong><br>
            2. เลี้ยวซ้ายไปหากุญแจ<br>
            3. เดินเข้ายาน
          </div>

          <div style="width: 100%; background: #f0fdf4; border: 1px solid #86efac; border-radius: 6px; padding: 5px; font-size: 8pt; line-height: 1.3;">
            <strong style="color: #166534;">✅ โค้ดที่ถูกต้องหลังแก้บั๊ก:</strong><br>
            1. ................................................<br>
            2. ................................................<br>
            3. ................................................<br>
            4. เดินเข้ายานสำเร็จ!
          </div>
          <div class="grid-caption" style="margin-top: 5px;">
            <strong>เนวิเกเตอร์:</strong> ลำดับเหตุการณ์ใหม่ให้เก็บกุญแจก่อนเสมอ!
          </div>
        </div>

        <div class="quest-card">
          <div>
            <div class="card-title-right">💬 ถอดบทเรียนคู่หู (After Action Review: AAR)</div>
            <div class="quest-item">
              <strong>1. สิ่งที่คู่หู (Driver & Navigator) ช่วยเหลือกันได้ดีที่สุด คืออะไร?</strong><br>
              ตอบ: ............................................................................................................................
            </div>
            <div class="dotted-divider"></div>
            <div class="quest-item">
              <strong>2. การเล่นเกม AR และใช้การ์ด ช่วยให้เข้าใจการเขียนโปรแกรมง่ายขึ้นอย่างไร?</strong><br>
              ตอบ: ............................................................................................................................
            </div>
            <div class="dotted-divider"></div>
            <div class="quest-item">
              <strong>3. ในชีวิตจริงถ้าเจอปัญหา เราจะนำวิธี "หาจุดผิดทีละก้าว (Debugging)" ไปใช้อย่างไร?</strong><br>
              ตอบ: ............................................................................................................................
            </div>
          </div>
          <div class="dashed-code-box" style="border-color: #3b82f6; background: #eff6ff; color: #1d4ed8; text-align: center; padding: 4px 6px;">
            <strong>🏆 บททดสอบมาสเตอร์ ป.5: ผ่านครบ 10 ด่าน! | ดาวสะสมรวม: ........ / 30 ⭐</strong>
          </div>
        </div>
      </div>
    </div>

    <div class="bottom-section">
      <div class="star-bar">
        <span>⭐ สรุปผลการประเมินด้านที่ 1 (ว.PA): [ &nbsp; ] ดีเยี่ยม (3 ดาวทุกด่าน) [ &nbsp; ] ดี</span>
        <span>ระดับคะแนนทักษะ CT: [ &nbsp; ] 4 (เชี่ยวชาญ) &nbsp; [ &nbsp; ] 3 (คล่องแคล่ว)</span>
      </div>

      <div class="footer-sig">
        <span>ครูผู้ตรวจ: นายเตชินท์ อินทมล</span>
        <span>ลายมือชื่อคู่หู: 1) ................................................ 2) ................................................</span>
      </div>
    </div>
  </div>

</body>
</html>
"""

html_path1 = "ใบงานภารกิจโค้ดดิ้ง_ป5_ชุดที่2_สไตล์การ์ดสองคอลัมน์.html"
html_path2 = os.path.join("docs", html_path1)

with open(html_path1, "w", encoding="utf-8") as f:
    f.write(html_content)
with open(html_path2, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Generated HTML Set 2: {html_path1} & {html_path2}")

# ==============================================================================
# 2. DOCX GENERATION (SET 2: 2-COLUMN SPLIT WITH EMBEDDED TABLES)
# ==============================================================================

def esc(text):
    if text is None: return ""
    return html.escape(str(text))

def make_p(runs, align="left", space_before=0, space_after=15, line_spacing=210):
    p_props = [f'<w:jc w:val="{align}"/>']
    p_props.append(f'<w:spacing w:before="{space_before}" w:after="{space_after}" w:line="{line_spacing}" w:lineRule="auto"/>')
    runs_xml = []
    for item in runs:
        if isinstance(item, str):
            t, b, i, sz, c = item, False, False, 22, "000000"
        else:
            t = item[0]
            b = item[1] if len(item) > 1 else False
            i = item[2] if len(item) > 2 else False
            sz = item[3] if len(item) > 3 else 22
            c = item[4] if len(item) > 4 else "000000"
        
        r_pr = ['<w:rFonts w:ascii="TH Sarabun PSK" w:hAnsi="TH Sarabun PSK" w:cs="TH Sarabun PSK"/>']
        if b: r_pr.append('<w:b/><w:bCs/>')
        if i: r_pr.append('<w:i/><w:iCs/>')
        r_pr.append(f'<w:sz w:val="{sz}"/><w:szCs w:val="{sz}"/>')
        if c and c != "000000": r_pr.append(f'<w:color w:val="{c}"/>')
        runs_xml.append(f'<w:r><w:rPr>{"".join(r_pr)}</w:rPr><w:t xml:space="preserve">{esc(t)}</w:t></w:r>')
    return f'<w:p><w:pPr>{"".join(p_props)}</w:pPr>{"".join(runs_xml)}</w:p>'

def make_callout_docx(text, title=None, bg="FEFCE8", bdr="F59E0B"):
    p_pr = f'''<w:pPr>
        <w:pBdr><w:left w:val="single" w:sz="18" w:space="8" w:color="{bdr}"/></w:pBdr>
        <w:shd w:val="clear" w:color="auto" w:fill="{bg}"/>
        <w:ind w:left="140" w:right="140"/>
        <w:spacing w:before="20" w:after="20" w:line="200" w:lineRule="auto"/>
    </w:pPr>'''
    runs_xml = []
    if title:
        runs_xml.append(f'''<w:r><w:rPr><w:rFonts w:ascii="TH Sarabun PSK" w:hAnsi="TH Sarabun PSK" w:cs="TH Sarabun PSK"/><w:b/><w:bCs/><w:sz w:val="22"/><w:szCs w:val="22"/><w:color w:val="{bdr}"/></w:rPr><w:t xml:space="preserve">{esc(title)}&#10;</w:t></w:r>''')
    runs_xml.append(f'''<w:r><w:rPr><w:rFonts w:ascii="TH Sarabun PSK" w:hAnsi="TH Sarabun PSK" w:cs="TH Sarabun PSK"/><w:sz w:val="20"/><w:szCs w:val="20"/><w:color w:val="78350F"/></w:rPr><w:t xml:space="preserve">{esc(text)}</w:t></w:r>''')
    return f'<w:p>{p_pr}{"".join(runs_xml)}</w:p>'

def make_team_table_docx(role_n, role_d):
    headers = ["ข้อมูลคู่หู Active Learning", "เลขที่", "บทบาทหน้าที่ประจำภารกิจ"]
    rows = [
        ["ชื่อทีม/กลุ่ม: ..........................................................................", "-", "กลุ่มที่: ................"],
        ["1. ......................................................................................", "......", f"[  ] Navigator ({role_n})"],
        ["2. ......................................................................................", "......", f"[  ] Driver ({role_d})"]
    ]
    col_widths = [5200, 700, 4600]
    total_w = sum(col_widths)
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
               <w:tblCellMar><w:top w:w="25" w:type="dxa"/><w:left w:w="60" w:type="dxa"/><w:bottom w:w="25" w:type="dxa"/><w:right w:w="60" w:type="dxa"/></w:tblCellMar>
           </w:tblPr>''',
           '<w:tblGrid>']
    for w in col_widths: xml.append(f'<w:gridCol w:w="{w}"/>')
    xml.append('</w:tblGrid>')
    # Header
    xml.append('<w:tr><w:trPr><w:tblHeader/><w:trHeight w:val="210" w:hRule="atLeast"/></w:trPr>')
    for i, h in enumerate(headers):
        al = "center" if i == 1 else "left"
        xml.append(f'''<w:tc><w:tcPr><w:tcW w:w="{col_widths[i]}" w:type="dxa"/><w:shd w:val="clear" w:color="auto" w:fill="0284C7"/><w:vAlign w:val="center"/></w:tcPr>
            <w:p><w:pPr><w:jc w:val="{al}"/><w:spacing w:before="10" w:after="10" w:line="180" w:lineRule="auto"/></w:pPr>
            <w:r><w:rPr><w:rFonts w:ascii="TH Sarabun PSK" w:hAnsi="TH Sarabun PSK" w:cs="TH Sarabun PSK"/><w:b/><w:bCs/><w:sz w:val="20"/><w:szCs w:val="20"/><w:color w:val="FFFFFF"/></w:rPr><w:t xml:space="preserve">{esc(h)}</w:t></w:r></w:p></w:tc>''')
    xml.append('</w:tr>')
    for row in rows:
        xml.append('<w:tr><w:trPr><w:trHeight w:val="210" w:hRule="atLeast"/></w:trPr>')
        for i, val in enumerate(row):
            al = "center" if i == 1 else "left"
            xml.append(f'''<w:tc><w:tcPr><w:tcW w:w="{col_widths[i]}" w:type="dxa"/><w:vAlign w:val="center"/></w:tcPr>
                <w:p><w:pPr><w:jc w:val="{al}"/><w:spacing w:before="10" w:after="10" w:line="180" w:lineRule="auto"/></w:pPr>
                <w:r><w:rPr><w:rFonts w:ascii="TH Sarabun PSK" w:hAnsi="TH Sarabun PSK" w:cs="TH Sarabun PSK"/><w:sz w:val="20"/><w:szCs w:val="20"/><w:color w:val="1E293B"/></w:rPr><w:t xml:space="preserve">{esc(val)}</w:t></w:r></w:p></w:tc>''')
        xml.append('</w:tr>')
    xml.append('</w:tbl>')
    return "".join(xml)

def make_mini_grid_table(grid_rows):
    xml = ['<w:tbl>',
           '''<w:tblPr>
               <w:tblW w:w="3600" w:type="dxa"/><w:jc w:val="center"/>
               <w:tblBorders>
                   <w:top w:val="single" w:sz="4" w:space="0" w:color="93C5FD"/>
                   <w:left w:val="single" w:sz="4" w:space="0" w:color="93C5FD"/>
                   <w:bottom w:val="single" w:sz="4" w:space="0" w:color="93C5FD"/>
                   <w:right w:val="single" w:sz="4" w:space="0" w:color="93C5FD"/>
                   <w:insideH w:val="single" w:sz="4" w:space="0" w:color="93C5FD"/>
                   <w:insideV w:val="single" w:sz="4" w:space="0" w:color="93C5FD"/>
               </w:tblBorders>
               <w:tblCellMar><w:top w:w="20" w:type="dxa"/><w:left w:w="20" w:type="dxa"/><w:bottom w:w="20" w:type="dxa"/><w:right w:w="20" w:type="dxa"/></w:tblCellMar>
           </w:tblPr>''',
           '<w:tblGrid>']
    for _ in range(6): xml.append('<w:gridCol w:w="600"/>')
    xml.append('</w:tblGrid>')
    for row in grid_rows:
        xml.append('<w:tr><w:trPr><w:trHeight w:val="420" w:hRule="atLeast"/></w:trPr>')
        for item in row:
            bg = "FFFFFF"
            if "🤖" in item: bg = "DCFCE7"
            elif "🚀" in item: bg = "FEF08A"
            elif "🪨" in item: bg = "64748B"
            elif "🔋" in item: bg = "FFFFFF"
            elif "⚡" in item: bg = "FEE2E2"
            elif "🗝️" in item: bg = "FEF9C3"
            xml.append(f'''<w:tc><w:tcPr><w:tcW w:w="600" w:type="dxa"/><w:shd w:val="clear" w:color="auto" w:fill="{bg}"/><w:vAlign w:val="center"/></w:tcPr>
                <w:p><w:pPr><w:jc w:val="center"/><w:spacing w:before="0" w:after="0" w:line="160" w:lineRule="auto"/></w:pPr>
                <w:r><w:rPr><w:rFonts w:ascii="TH Sarabun PSK" w:hAnsi="TH Sarabun PSK" w:cs="TH Sarabun PSK"/><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr><w:t xml:space="preserve">{esc(item)}</w:t></w:r></w:p></w:tc>''')
        xml.append('</w:tr>')
    xml.append('</w:tbl>')
    return "".join(xml)

def make_split_card_docx(left_title, left_content_xml, right_title, right_content_xml, bdr_color="F59E0B"):
    # 2 columns: Left = 4300 dxa, Right = 6200 dxa
    xml = ['<w:tbl>',
           f'''<w:tblPr>
               <w:tblW w:w="10500" w:type="dxa"/><w:tblInd w:w="0" w:type="dxa"/>
               <w:tblBorders><w:top w:val="none"/><w:left w:val="none"/><w:bottom w:val="none"/><w:right w:val="none"/><w:insideH w:val="none"/><w:insideV w:val="none"/></w:tblBorders>
               <w:tblCellMar><w:top w:w="30" w:type="dxa"/><w:left w:w="50" w:type="dxa"/><w:bottom w:w="30" w:type="dxa"/><w:right w:w="50" w:type="dxa"/></w:tblCellMar>
           </w:tblPr>''',
           '<w:tblGrid><w:gridCol w:w="4300"/><w:gridCol w:w="6200"/></w:tblGrid>',
           '<w:tr>']
    
    # Left Cell
    xml.append(f'''<w:tc><w:tcPr>
        <w:tcW w:w="4300" w:type="dxa"/>
        <w:tcBorders>
            <w:top w:val="single" w:sz="8" w:space="0" w:color="{bdr_color}"/>
            <w:left w:val="single" w:sz="8" w:space="0" w:color="{bdr_color}"/>
            <w:bottom w:val="single" w:sz="8" w:space="0" w:color="{bdr_color}"/>
            <w:right w:val="single" w:sz="8" w:space="0" w:color="{bdr_color}"/>
        </w:tcBorders>
        <w:shd w:val="clear" w:color="auto" w:fill="FFFFFF"/>
        <w:vAlign w:val="top"/>
    </w:tcPr>
    {make_p([(left_title, True, False, 22, "92400E")], align="center", space_before=15, space_after=15)}
    {left_content_xml}
    </w:tc>''')

    # Right Cell
    xml.append(f'''<w:tc><w:tcPr>
        <w:tcW w:w="6200" w:type="dxa"/>
        <w:tcBorders>
            <w:top w:val="single" w:sz="6" w:space="0" w:color="CBD5E1"/>
            <w:left w:val="single" w:sz="6" w:space="0" w:color="CBD5E1"/>
            <w:bottom w:val="single" w:sz="6" w:space="0" w:color="CBD5E1"/>
            <w:right w:val="single" w:sz="6" w:space="0" w:color="CBD5E1"/>
        </w:tcBorders>
        <w:shd w:val="clear" w:color="auto" w:fill="FFFFFF"/>
        <w:vAlign w:val="top"/>
    </w:tcPr>
    {make_p([(right_title, True, False, 22, "1E3A8A")], align="left", space_before=15, space_after=15)}
    {right_content_xml}
    </w:tc>''')

    xml.append('</w:tr></w:tbl>')
    return "".join(xml)

def make_footer_box_docx():
    p1 = make_p([("⭐ ผลทดสอบหน้ากล้อง AR:  [  ] เข้ายานสำเร็จ   [  ] ชนหิน/เลเซอร์   |   ดาวที่ได้รับ: [  ] 1 ดาว   [  ] 2 ดาว   [  ] 3 ดาว 🌟🌟🌟", True, False, 19, "0284C7")], align="left", space_before=20, space_after=10)
    p2 = make_p([("ครูผู้สอน/ผู้ตรวจ: นายเตชินท์ อินทมล      |      ลายมือชื่อคู่หู: 1) ........................................ 2) ........................................", False, True, 17, "64748B")], align="left", space_before=0, space_after=0)
    return p1 + p2

# Build all 4 worksheets for DOCX
body_docx = []

# --- WORKSHEET 1 ---
body_docx.append(make_p([("📄 แผ่นที่ 1 [ด้านหน้า] : ชุดที่ 2 โมเดิร์นการ์ด  |  วิชาวิทยาการคำนวณ ว15101 ป.5", True, False, 18, "0284C7")], space_before=0, space_after=8))
body_docx.append(make_p([("🚀 ใบงานที่ 1: การค้นหารูปแบบและลูปบันได 3 ขั้น (Pattern & Loops)", True, False, 24, "0369A1")], align="center", space_before=5, space_after=5))
body_docx.append(make_p([("สอดรับเกมนวัตกรรม CodeBot AR Adventure แทร็ก ป.5 (ด่านที่ 1 - 3) | โรงเรียนบ้านโนนป่าหว้านเชียงฮาย", False, True, 17, "475569")], align="center", space_before=0, space_after=20))
body_docx.append(make_team_table_docx("ผู้นำทาง วาดแผนที่ & สังเกตรูปแบบ", "ผู้สั่งการ ชูการ์ดคำสั่งหน้ากล้อง AR"))
body_docx.append(make_callout_docx("สังเกตเส้นทางเดินขึ้นบันได จะพบว่ามีการเดินซ้ำเป็นแพทเทิร์น ให้นักเรียนช่วยกันจับกลุ่มคำสั่งซ้ำ แล้วนำบล็อก [วนซ้ำ Loop] มาครอบเพื่อลดจำนวนโค้ดให้สั้นที่สุด!", title="🎯 คำแนะนำภารกิจบันได 3 ขั้น:"))

g1 = [
    ["", "", "", "🚀", "", ""],
    ["", "", "🪨", "🔋", "", ""],
    ["", "🪨", "🔋", "", "", ""],
    ["🪨", "🔋", "", "", "", ""],
    ["🤖", "", "", "", "", ""],
    ["", "", "", "", "", ""]
]
left_1 = make_mini_grid_table(g1) + make_p([("เนวิเกเตอร์: ใช้สีระบายขั้นบันได 3 ขั้น เพื่อดูชุดคำสั่งที่ซ้ำกัน!", False, True, 16, "475569")], align="center", space_before=15, space_after=5)

code1_text = "[ วนซ้ำ (Loop) ............ รอบ ] {\n    1) ....................................................................................\n    2) ....................................................................................\n}"
right_1 = (
    make_p([("1. ใน 1 ขั้นบันได หุ่นยนต์ต้องทำคำสั่งอะไรบ้าง?", True, False, 19, "1E293B")], space_before=5, space_after=5) +
    make_p([("คำตอบ: ........................................................................................................", False, False, 19, "475569")], space_before=0, space_after=10) +
    make_p([("2. ต้องทำคำสั่งชุดนี้ซ้ำทั้งหมดกี่รอบ?", True, False, 19, "1E293B")], space_before=5, space_after=5) +
    make_p([("ตอบ: ทำซ้ำจำนวน .................... รอบ", False, False, 19, "475569")], space_before=0, space_after=10) +
    make_p([("3. เขียนบล็อกลูปคำสั่งที่คู่เราออกแบบ:", True, False, 19, "1E293B")], space_before=5, space_after=5) +
    make_callout_docx(code1_text, title=None, bg="FFFBEB", bdr="F59E0B")
)
body_docx.append(make_split_card_docx("🗺️ แผนที่ด่านบันได 3 ขั้นทะยานฟ้า", left_1, "🔍 เจาะลึกแพทเทิร์นคำสั่งซ้ำ", right_1, "F59E0B"))
body_docx.append(make_footer_box_docx())

# --- WORKSHEET 2 ---
body_docx.append('<w:p><w:r><w:br w:type="page"/></w:r></w:p>')
body_docx.append(make_p([("📄 แผ่นที่ 1 [ด้านหลัง] : ชุดที่ 2 โมเดิร์นการ์ด  |  🔄 สลับบทบาทคู่หูแล้ว!", True, False, 18, "DC2626")], space_before=0, space_after=8))
body_docx.append(make_p([("🔄 ใบงานที่ 2: ลูปตรวจรอบสถานีและการลดรูปโค้ด (Perimeter Loop)", True, False, 24, "0369A1")], align="center", space_before=5, space_after=5))
body_docx.append(make_p([("สอดรับเกมนวัตกรรม CodeBot AR แทร็ก ป.5 (ด่านที่ 4) | โรงเรียนบ้านโนนป่าหว้านเชียงฮาย", False, True, 17, "475569")], align="center", space_before=0, space_after=20))
body_docx.append(make_team_table_docx("สลับมาเป็นผู้นำทาง วางแผนโค้ดประหยัด", "สลับมาเป็นผู้สั่งการ ควบคุมหน้ากล้อง AR"))
body_docx.append(make_callout_docx("หุ่นยนต์ต้องเดินลาดตระเวนรอบสถานีเพื่อชาร์จแบตเตอรี่ 4 จุด คู่หูช่วยกันนำบล็อก [วนซ้ำ Loop] แบบผสมคำสั่ง (เดินหน้า+เลี้ยว) มาใช้ย่อโค้ดจากเดิม 16 บล็อกให้เหลือเพียงลูปเดียว!", title="🎯 คำแนะนำภารกิจรอบสถานี 4 ทิศ:", bg="F0F9FF", bdr="0284C7"))

g2 = [
    ["🚀", "🔋", "🔋", "🔋", "", ""],
    ["🔋", "🪨", "🪨", "🔋", "", ""],
    ["🔋", "🪨", "🪨", "🔋", "", ""],
    ["🤖", "🔋", "🔋", "🔋", "", ""],
    ["", "", "", "", "", ""],
    ["", "", "", "", "", ""]
]
left_2 = make_mini_grid_table(g2) + make_p([("เนวิเกเตอร์: ลากเส้นเดินวนขวาตามเข็มนาฬิกา ครบ 4 ทิศทาง!", False, True, 16, "475569")], align="center", space_before=15, space_after=5)

code2_text = "[ วนซ้ำ (Loop) ............ รอบ ] {\n    1) เดินหน้า ............ ก้าว\n    2) เลี้ยว ........................................\n}"
right_2 = (
    make_p([("1. โค้ดเดิมแบบไม่ใช้ลูป (เรียงยาว 12 บล็อก):", True, False, 19, "1E293B")], space_before=5, space_after=5) +
    make_p([("เดินหน้า 3 ก้าว -> เลี้ยวขวา -> เดินหน้า 3 ก้าว -> เลี้ยวขวา ... (ยาวมาก)", False, True, 17, "64748B")], space_before=0, space_after=10) +
    make_p([("2. ใน 1 ด้าน หุ่นยนต์ต้องเดินหน้ากี่ก้าว และเลี้ยวทางไหน?", True, False, 19, "1E293B")], space_before=5, space_after=5) +
    make_p([("ตอบ: เดินหน้า ............ ก้าว และ เลี้ยว ........................................", False, False, 19, "475569")], space_before=0, space_after=10) +
    make_p([("3. เขียนบล็อกย่อโค้ดแบบประหยัด (Multi-Action Loop):", True, False, 19, "1E293B")], space_before=5, space_after=5) +
    make_callout_docx(code2_text, title=None, bg="F0FDF4", bdr="16A34A")
)
body_docx.append(make_split_card_docx("🗺️ แผนที่ลาดตระเวนรอบสถานี", left_2, "⚡ เปรียบเทียบโค้ดลดรูป (Optimization)", right_2, "0284C7"))
body_docx.append(make_footer_box_docx())

# --- WORKSHEET 3 ---
body_docx.append('<w:p><w:r><w:br w:type="page"/></w:r></w:p>')
body_docx.append(make_p([("📄 แผ่นที่ 2 [ด้านหน้า] : ชุดที่ 2 โมเดิร์นการ์ด  |  วิชาวิทยาการคำนวณ ว15101 ป.5", True, False, 18, "D97706")], space_before=0, space_after=8))
body_docx.append(make_p([("⚡ ใบงานที่ 3: เงื่อนไขถ้า...แล้ว กับประตูปริศนาเลเซอร์และกุญแจ (If-Then)", True, False, 24, "0369A1")], align="center", space_before=5, space_after=5))
body_docx.append(make_p([("สอดรับเกมนวัตกรรม CodeBot AR แทร็ก ป.5 (ด่านที่ 5 - 6) | โรงเรียนบ้านโนนป่าหว้านเชียงฮาย", False, True, 17, "475569")], align="center", space_before=0, space_after=20))
body_docx.append(make_team_table_docx("ผู้นำทาง คำนวณเงื่อนไขและทางแยก", "ผู้สั่งการ ส่องการ์ดกุญแจหน้ากล้อง AR"))
body_docx.append(make_callout_docx("ประตูเลเซอร์ ⚡ ขวางทางเข้ายานอยู่ ห้ามเดินชนเด็ดขาด! ต้องไปเก็บกุญแจคีย์การ์ด 🗝️ เสียก่อน ประตูจึงจะเปิดออก ให้นักเรียนเขียนประโยคเงื่อนไขและวางแผนโค้ด 2 เฟส", title="🎯 คำแนะนำภารกิจประตูปริศนาเลเซอร์:", bg="FEFCE8", bdr="EAB308"))

g3 = [
    ["", "", "", "⚡", "🚀", ""],
    ["🗝️", "", "", "⚡", "", ""],
    ["🪨", "🪨", "", "", "", ""],
    ["🤖", "", "", "", "", ""],
    ["", "", "", "", "", ""],
    ["", "", "", "", "", ""]
]
left_3 = make_mini_grid_table(g3) + make_p([("เนวิเกเตอร์: ลากเส้นเฟส 1 ไปเก็บ 🗝️ แล้วเฟส 2 ผ่าน ⚡ เข้ายาน!", False, True, 16, "475569")], align="center", space_before=15, space_after=5)

code3_text = "🗝️ เฟส 1: เก็บกุญแจ\n1) ........................................ 2) ........................................ 3) ........................................\n🚀 เฟส 2: เข้ายานอวกาศ\n1) ........................................ 2) ........................................ 3) ........................................"
right_3 = (
    make_p([("1. ประโยคเงื่อนไข If-Then ของคู่เรา:", True, False, 19, "1E293B")], space_before=5, space_after=5) +
    make_p([("• [ ถ้า (IF) ] มีไอเทม: [ .................................................................... ]", False, False, 18, "475569")], space_before=0, space_after=3) +
    make_p([("• [ แล้ว (THEN) ] เลเซอร์จะ: [ ............................................................ ]", False, False, 18, "475569")], space_before=0, space_after=3) +
    make_p([("• [ มิฉะนั้น (ELSE) ] ชนแล้วจะเกิดผล: [ ............................................ ]", False, False, 18, "475569")], space_before=0, space_after=8) +
    make_p([("2. วางแผนคำสั่ง 2 เฟสพิชิตด่าน:", True, False, 19, "1E293B")], space_before=5, space_after=5) +
    make_callout_docx(code3_text, title=None, bg="FFFDF5", bdr="EAB308")
)
body_docx.append(make_split_card_docx("🗺️ แผนที่ประตูปริศนาเลเซอร์", left_3, "🧠 ตรรกะเงื่อนไขและการวางแผน 2 เฟส", right_3, "EAB308"))
body_docx.append(make_footer_box_docx())

# --- WORKSHEET 4 ---
body_docx.append('<w:p><w:r><w:br w:type="page"/></w:r></w:p>')
body_docx.append(make_p([("📄 แผ่นที่ 2 [ด้านหลัง] : ชุดที่ 2 โมเดิร์นการ์ด  |  🔄 สลับบทบาทคู่หูแล้ว!", True, False, 18, "DC2626")], space_before=0, space_after=8))
body_docx.append(make_p([("🐞 ใบงานที่ 4: ยอดนักสืบแก้บั๊กตรรกะและบททดสอบมาสเตอร์ ป.5", True, False, 24, "0369A1")], align="center", space_before=5, space_after=5))
body_docx.append(make_p([("สอดรับเกมนวัตกรรม CodeBot AR แทร็ก ป.5 (ด่านที่ 7 - 10) | โรงเรียนบ้านโนนป่าหว้านเชียงฮาย", False, True, 17, "475569")], align="center", space_before=0, space_after=20))
body_docx.append(make_team_table_docx("สลับมาเป็นผู้นำทาง วิเคราะห์จุดผิดพลาด", "สลับมาเป็นผู้สั่งการ ทดสอบโค้ดแก้บั๊ก"))
body_docx.append(make_callout_docx("ในเกมมีบั๊กหุ่นยนต์เดินตรงไปชนประตูเลเซอร์ก่อนเก็บกุญแจ! ให้ช่วยกันสืบหาจุดผิดและเขียนโค้ดที่ถูกต้อง จากนั้นบันทึกการสะท้อนคิดถอดบทเรียน (AAR) ร่วมกัน", title="🎯 คำแนะนำภารกิจแก้บั๊ก & ถอดบทเรียน:", bg="FEF2F2", bdr="EF4444"))

bug_old = "1. เดินหน้า 3 ก้าวตรงไปที่เลเซอร์\n   (บั๊ก! ชนเลเซอร์ดับเพราะไม่มีกุญแจ)\n2. เลี้ยวซ้ายไปหากุญแจ\n3. เดินเข้ายาน"
bug_fix = "1. ................................................................\n2. ................................................................\n3. ................................................................\n4. เดินเข้ายานอวกาศสำเร็จ!"

left_4 = (
    make_callout_docx(bug_old, title="❌ โค้ดเดิมที่มีข้อผิดพลาด (Bug):", bg="FEE2E2", bdr="DC2626") +
    make_callout_docx(bug_fix, title="✅ โค้ดที่ถูกต้องหลังแก้บั๊ก:", bg="F0FDF4", bdr="16A34A") +
    make_p([("เนวิเกเตอร์: ลำดับเหตุการณ์ใหม่ให้เก็บกุญแจก่อนเสมอ!", False, True, 16, "475569")], align="center", space_before=10, space_after=5)
)

aar_badge = "🏆 ผ่านด่านมาสเตอร์ ป.5 ครบ 10 ด่าน! | ดาวสะสมรวม: ........ / 30 ดาว ⭐"
right_4 = (
    make_p([("1. สิ่งที่คู่หู (Driver & Navigator) ช่วยเหลือกันได้ดีที่สุด คืออะไร?", True, False, 18, "1E293B")], space_before=5, space_after=5) +
    make_p([("ตอบ: ........................................................................................................................", False, False, 18, "475569")], space_before=0, space_after=8) +
    make_p([("2. การเล่นเกม AR และใช้การ์ด ช่วยให้เข้าใจการเขียนโปรแกรมง่ายขึ้นอย่างไร?", True, False, 18, "1E293B")], space_before=5, space_after=5) +
    make_p([("ตอบ: ........................................................................................................................", False, False, 18, "475569")], space_before=0, space_after=8) +
    make_p([("3. ในชีวิตจริงถ้าเจอปัญหา เราจะนำวิธี 'หาจุดผิดทีละก้าว (Debugging)' ไปใช้อย่างไร?", True, False, 18, "1E293B")], space_before=5, space_after=5) +
    make_p([("ตอบ: ........................................................................................................................", False, False, 18, "475569")], space_before=0, space_after=10) +
    make_callout_docx(aar_badge, title=None, bg="EFF6FF", bdr="3B82F6")
)
body_docx.append(make_split_card_docx("🐞 ตรวจจับและกำจัดบั๊ก", left_4, "💬 ถอดบทเรียนคู่หู (AAR)", right_4, "EF4444"))
body_docx.append(make_footer_box_docx())

doc_body_set2 = "".join(body_docx)

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
        <w:sz w:val="22"/>
        <w:szCs w:val="22"/>
        <w:lang w:val="th-TH"/>
      </w:rPr>
    </w:rPrDefault>
    <w:pPrDefault>
      <w:pPr>
        <w:spacing w:before="0" w:after="15" w:line="210" w:lineRule="auto"/>
      </w:pPr>
    </w:pPrDefault>
  </w:docDefaults>
</w:styles>"""

document_xml_set2 = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:body>
    {doc_body_set2}
    <w:sectPr>
      <w:pgSz w:w="11906" w:h="16838"/>
      <w:pgMar w:top="450" w:right="600" w:bottom="450" w:left="600"/>
    </w:sectPr>
  </w:body>
</w:document>"""

docx_path1 = "ใบงานภารกิจโค้ดดิ้ง_ป5_ชุดที่2_สไตล์การ์ดสองคอลัมน์.docx"
docx_path2 = os.path.join("docs", docx_path1)

with zipfile.ZipFile(docx_path1, "w", zipfile.ZIP_DEFLATED) as docx:
    docx.writestr("[Content_Types].xml", content_types)
    docx.writestr("_rels/.rels", rels)
    docx.writestr("word/_rels/document.xml.rels", doc_rels)
    docx.writestr("word/styles.xml", styles)
    docx.writestr("word/document.xml", document_xml_set2)

print(f"Generated DOCX Set 2: {docx_path1}")
os.system(f"cp '{docx_path1}' '{docx_path2}'")
print(f"Copied to {docx_path2}")
