# -*- coding: utf-8 -*-
"""
Script: build_mission_grid_mats.py
Generates:
1. แผ่นแผนที่ภารกิจตารางเดินช่อง_Unplugged_ป5_พร้อมพิมพ์.html
2. แผ่นแผนที่ภารกิจตารางเดินช่อง_Unplugged_ป5_ครูเตชินท์.docx
Includes 4 Grade 5 Unplugged Mission Grid Mats (4x4 and 5x5) + 1 Printable Arrow Card Sheet.
"""

import os, html, zipfile

def esc(text):
    if text is None:
        return ""
    return html.escape(str(text))

# -----------------------------------------------------------------------------
# 1. HTML GENERATOR (Ready to print via Web Browser Ctrl+P / Cmd+P)
# -----------------------------------------------------------------------------
def build_html_mats():
    missions = [
        {
            "id": 1,
            "title": "ภารกิจที่ 1: พาน้องแมว Scratch เดินทางกลับบ้านแสนสุข",
            "concept": "การคิดแก้ปัญหาเชิงตรรกะและการเรียงลำดับคำสั่งแบบขั้นตอน (Sequential Algorithm)",
            "indicator": "ว 4.2 ป.5/1",
            "size": 4,
            "rows": 4,
            "cols": 4,
            "story": "น้องแมว Scratch 🐱 หลงทางอยู่ในสวนหิน ต้องการเดินทางกลับไปที่ 🏡 บ้านแสนสุข โดยในเส้นทางมี 🪨 ก้อนหินยักษ์ และ ⚠️ หลุมโคลน ขวางอยู่ ให้นักเรียนคู่หูช่วยกันวางแผน นำบัตรลูกศรมาวางเรียงลำดับหาเส้นทางที่ปลอดภัยและสั้นที่สุด!",
            "start": "🐱 น้องแมว Scratch (ช่อง A1 หันหน้าขึ้น ⬆️)",
            "goal": "🏡 บ้านแสนสุข (ช่อง D4)",
            "obstacles": "🪨 ก้อนหินยักษ์ (ช่อง A2, C3) และ ⚠️ หลุมโคลน (ช่อง C1)",
            "grid": [
                # Row 4 (Top: D)
                [{"txt": "D1", "sub": "", "type": "empty"},
                 {"txt": "D2", "sub": "", "type": "empty"},
                 {"txt": "D3", "sub": "", "type": "empty"},
                 {"txt": "🏡", "sub": "บ้านแสนสุข\n(จุดหมาย)", "type": "goal"}],
                # Row 3 (C)
                [{"txt": "⚠️", "sub": "หลุมโคลน", "type": "obstacle"},
                 {"txt": "C2", "sub": "", "type": "empty"},
                 {"txt": "🪨", "sub": "หินยักษ์", "type": "obstacle"},
                 {"txt": "C4", "sub": "", "type": "empty"}],
                # Row 2 (B)
                [{"txt": "B1", "sub": "", "type": "empty"},
                 {"txt": "B2", "sub": "", "type": "empty"},
                 {"txt": "B3", "sub": "", "type": "empty"},
                 {"txt": "B4", "sub": "", "type": "empty"}],
                # Row 1 (A: Bottom)
                [{"txt": "🐱", "sub": "จุดเริ่มต้น\n(หันหน้า ⬆️)", "type": "start"},
                 {"txt": "🪨", "sub": "หินยักษ์", "type": "obstacle"},
                 {"txt": "A3", "sub": "", "type": "empty"},
                 {"txt": "A4", "sub": "", "type": "empty"}]
            ],
            "row_labels": ["D (แถว 4)", "C (แถว 3)", "B (แถว 2)", "A (แถว 1)"],
            "col_labels": ["1 (คอลัมน์ 1)", "2 (คอลัมน์ 2)", "3 (คอลัมน์ 3)", "4 (คอลัมน์ 4)"],
            "slots": 8,
            "scratch_hint": "เมื่อคลิกธงเขียว ➔ เคลื่อนที่ ... ก้าว ➔ หันขวา 90 องศา ➔ เคลื่อนที่ ... ก้าว"
        },
        {
            "id": 2,
            "title": "ภารกิจที่ 2: หุ่นยนต์ผึ้งน้อย บินเก็บน้ำหวานดอกไม้แสนหวาน",
            "concept": "การแก้ปัญหาแบบมีเงื่อนไข (Condition) และการจัดลำดับเก็บไอเทมครบถ้วน",
            "indicator": "ว 4.2 ป.5/1",
            "size": 4,
            "rows": 4,
            "cols": 4,
            "story": "หุ่นยนต์ผึ้งน้อย 🐝 ต้องบินออกจากรังเพื่อเก็บน้ำหวานจาก 🌸 ดอกไม้สีชมพู และ 🌻 ดอกทานตะวัน ให้ครบทั้ง 2 ดอก ก่อนจะนำน้ำหวานกลับไปส่งที่ 🍯 รังผึ้งใหญ่ โดยห้ามบินชน 🐝❌ รังต่อดุร้าย และ 🌊 สระน้ำลึก เด็ดขาด!",
            "start": "🐝 หุ่นยนต์ผึ้งน้อย (ช่อง A1 หันหน้าขึ้น ⬆️)",
            "goal": "🍯 รังผึ้งใหญ่ (ช่อง D4) *ต้องเก็บดอกไม้ครบก่อนเข้า*",
            "obstacles": "🐝❌ รังต่อดุร้าย (ช่อง B3) และ 🌊 สระน้ำลึก (ช่อง C2)",
            "grid": [
                # Row 4 (D)
                [{"txt": "D1", "sub": "", "type": "empty"},
                 {"txt": "D2", "sub": "", "type": "empty"},
                 {"txt": "🌻", "sub": "ดอกทานตะวัน\n(เก็บน้ำหวาน)", "type": "item"},
                 {"txt": "🍯", "sub": "รังผึ้งใหญ่\n(จุดหมาย)", "type": "goal"}],
                # Row 3 (C)
                [{"txt": "C1", "sub": "", "type": "empty"},
                 {"txt": "🌊", "sub": "สระน้ำลึก", "type": "obstacle"},
                 {"txt": "C3", "sub": "", "type": "empty"},
                 {"txt": "C4", "sub": "", "type": "empty"}],
                # Row 2 (B)
                [{"txt": "B1", "sub": "", "type": "empty"},
                 {"txt": "🌸", "sub": "ดอกชมพู\n(เก็บน้ำหวาน)", "type": "item"},
                 {"txt": "🐝❌", "sub": "รังต่อดุร้าย", "type": "obstacle"},
                 {"txt": "B4", "sub": "", "type": "empty"}],
                # Row 1 (A)
                [{"txt": "🐝", "sub": "จุดเริ่มต้น\n(หันหน้า ⬆️)", "type": "start"},
                 {"txt": "A2", "sub": "", "type": "empty"},
                 {"txt": "A3", "sub": "", "type": "empty"},
                 {"txt": "A4", "sub": "", "type": "empty"}]
            ],
            "row_labels": ["D (แถว 4)", "C (แถว 3)", "B (แถว 2)", "A (แถว 1)"],
            "col_labels": ["1 (คอลัมน์ 1)", "2 (คอลัมน์ 2)", "3 (คอลัมน์ 3)", "4 (คอลัมน์ 4)"],
            "slots": 10,
            "scratch_hint": "ถ้า สัมผัสดอกไม้ ➔ ให้ [เก็บน้ำหวาน] ➔ ถ้า สัมผัสรังผึ้ง และ น้ำหวานครบ ➔ พูดว่า 'ภารกิจสำเร็จ!'"
        },
        {
            "id": 3,
            "title": "ภารกิจที่ 3: นักสำรวจน้อย ล่าขุมทรัพย์ในเขาวงกตปริศนา",
            "concept": "การวางแผนเส้นทางซับซ้อน (Multi-step) และการตรวจหาข้อผิดพลาด (Debugging)",
            "indicator": "ว 4.2 ป.5/1 และ ป.5/2",
            "size": 5,
            "rows": 5,
            "cols": 5,
            "story": "นักสำรวจน้อย 🧭 เดินทางเข้าไปในวิหารเขาวงกต ประตูวิหาร 🚪 ล็อกอยู่! ต้องเดินไปหยิบ 🗝️ กุญแจทองคำโบราณ เพื่อนำมาเปิดประตูวิหาร แล้วจึงจะเข้าไปเปิด 👑 หีบสมบัติ ได้ โดยต้องระวัง 🧱 กำแพงหินหนาทึบ และ ⚡ กับดักสายฟ้า!",
            "start": "🧭 นักสำรวจน้อย (ช่อง A1 หันหน้าขึ้น ⬆️)",
            "goal": "👑 หีบสมบัติ (ช่อง E5) *ต้องเก็บกุญแจ 🗝️ ผ่านประตู 🚪 ก่อน*",
            "obstacles": "🧱 กำแพงหิน (ช่อง B2, C2, C4, D4) และ ⚡ กับดักสายฟ้า (ช่อง D2)",
            "grid": [
                # Row 5 (E)
                [{"txt": "E1", "sub": "", "type": "empty"},
                 {"txt": "E2", "sub": "", "type": "empty"},
                 {"txt": "E3", "sub": "", "type": "empty"},
                 {"txt": "🚪", "sub": "ประตูกล\n(ต้องใช้กุญแจ)", "type": "item"},
                 {"txt": "👑", "sub": "หีบสมบัติ\n(จุดหมาย)", "type": "goal"}],
                # Row 4 (D)
                [{"txt": "D1", "sub": "", "type": "empty"},
                 {"txt": "⚡", "sub": "กับดักสายฟ้า", "type": "obstacle"},
                 {"txt": "D3", "sub": "", "type": "empty"},
                 {"txt": "🧱", "sub": "กำแพงหิน", "type": "obstacle"},
                 {"txt": "D5", "sub": "", "type": "empty"}],
                # Row 3 (C)
                [{"txt": "C1", "sub": "", "type": "empty"},
                 {"txt": "🧱", "sub": "กำแพงหิน", "type": "obstacle"},
                 {"txt": "🗝️", "sub": "กุญแจทองคำ\n(ต้องเก็บก่อน)", "type": "item"},
                 {"txt": "🧱", "sub": "กำแพงหิน", "type": "obstacle"},
                 {"txt": "C5", "sub": "", "type": "empty"}],
                # Row 2 (B)
                [{"txt": "B1", "sub": "", "type": "empty"},
                 {"txt": "🧱", "sub": "กำแพงหิน", "type": "obstacle"},
                 {"txt": "B3", "sub": "", "type": "empty"},
                 {"txt": "B4", "sub": "", "type": "empty"},
                 {"txt": "B5", "sub": "", "type": "empty"}],
                # Row 1 (A)
                [{"txt": "🧭", "sub": "จุดเริ่มต้น\n(หันหน้า ⬆️)", "type": "start"},
                 {"txt": "A2", "sub": "", "type": "empty"},
                 {"txt": "A3", "sub": "", "type": "empty"},
                 {"txt": "A4", "sub": "", "type": "empty"},
                 {"txt": "A5", "sub": "", "type": "empty"}]
            ],
            "row_labels": ["E (แถว 5)", "D (แถว 4)", "C (แถว 3)", "B (แถว 2)", "A (แถว 1)"],
            "col_labels": ["1 (คอลัมน์ 1)", "2 (คอลัมน์ 2)", "3 (คอลัมน์ 3)", "4 (คอลัมน์ 4)", "5 (คอลัมน์ 5)"],
            "slots": 12,
            "scratch_hint": "ถ้า ชนกำแพงหิน ➔ ให้ถอยหลัง 1 ก้าว (แก้บั๊ก) | สัมผัสกุญแจ ➔ ซ่อนกุญแจ + เปิดประตูกล"
        },
        {
            "id": 4,
            "title": "ภารกิจที่ 4: หุ่นยนต์รักษ์โลก ลาดตระเวนเก็บขยะ 4 ทิศ (พลังแห่งการวนซ้ำ)",
            "concept": "การค้นหารูปแบบ (Pattern) และการเขียนโปรแกรมวนซ้ำ (Loop Programming)",
            "indicator": "ว 4.2 ป.5/2",
            "size": 5,
            "rows": 5,
            "cols": 5,
            "story": "หุ่นยนต์ทำความสะอาด 🤖 ต้องเดินลาดตระเวนรอบนอกของสถานี 4 ทิศ เพื่อเก็บ ♻️ ขยะรีไซเคิล ให้ครบทั้ง 4 มุม แล้วกลับมายังจุดเริ่มต้น คู่หูสังเกตเห็นไหมว่าหุ่นยนต์เดินเป็น 'รูปสี่เหลี่ยม' ที่ซ้ำกัน 4 ด้าน! จงใช้บัตร [วนซ้ำ Loop 4 รอบ] เพื่อลดคำสั่งให้สั้นที่สุด!",
            "start": "🤖 หุ่นยนต์รักษ์โลก (ช่อง A1 หันหน้าขึ้น ⬆️)",
            "goal": "🏁 ครบรอบ 4 ทิศ กลับมาที่ช่อง A1 โดยเก็บขยะครบ!",
            "obstacles": "⚡ เสาไฟฟ้าแรงสูงกลางลาน (ช่อง C2, C3, C4) ห้ามเดินผ่ากลาง!",
            "grid": [
                # Row 5 (E)
                [{"txt": "♻️", "sub": "ขยะมุมบนซ้าย", "type": "item"},
                 {"txt": "E2", "sub": "", "type": "empty"},
                 {"txt": "E3", "sub": "", "type": "empty"},
                 {"txt": "E4", "sub": "", "type": "empty"},
                 {"txt": "♻️", "sub": "ขยะมุมบนขวา", "type": "item"}],
                # Row 4 (D)
                [{"txt": "D1", "sub": "", "type": "empty"},
                 {"txt": "D2", "sub": "", "type": "empty"},
                 {"txt": "D3", "sub": "", "type": "empty"},
                 {"txt": "D4", "sub": "", "type": "empty"},
                 {"txt": "D5", "sub": "", "type": "empty"}],
                # Row 3 (C)
                [{"txt": "C1", "sub": "", "type": "empty"},
                 {"txt": "⚡", "sub": "เสาไฟฟ้า", "type": "obstacle"},
                 {"txt": "⚡", "sub": "แกนกลางห้ามชน", "type": "obstacle"},
                 {"txt": "⚡", "sub": "เสาไฟฟ้า", "type": "obstacle"},
                 {"txt": "C5", "sub": "", "type": "empty"}],
                # Row 2 (B)
                [{"txt": "B1", "sub": "", "type": "empty"},
                 {"txt": "B2", "sub": "", "type": "empty"},
                 {"txt": "B3", "sub": "", "type": "empty"},
                 {"txt": "B4", "sub": "", "type": "empty"},
                 {"txt": "B5", "sub": "", "type": "empty"}],
                # Row 1 (A)
                [{"txt": "🤖", "sub": "จุดเริ่ม & จบ\n(หันหน้า ⬆️)", "type": "start"},
                 {"txt": "A2", "sub": "", "type": "empty"},
                 {"txt": "A3", "sub": "", "type": "empty"},
                 {"txt": "A4", "sub": "", "type": "empty"},
                 {"txt": "♻️", "sub": "ขยะมุมล่างขวา", "type": "item"}]
            ],
            "row_labels": ["E (แถว 5)", "D (แถว 4)", "C (แถว 3)", "B (แถว 2)", "A (แถว 1)"],
            "col_labels": ["1 (คอลัมน์ 1)", "2 (คอลัมน์ 2)", "3 (คอลัมน์ 3)", "4 (คอลัมน์ 4)", "5 (คอลัมน์ 5)"],
            "slots": 8,
            "scratch_hint": "ทำซ้ำ (4) ครั้ง { เคลื่อนที่ 4 ก้าว, หันขวา 90 องศา } -> ประหยัดโค้ดได้ถึง 16 บล็อก!"
        }
    ]

    html_parts = ["""<!DOCTYPE html>
<html lang="th">
<head>
<meta charset="UTF-8">
<title>ชุดแผ่นแผนที่ภารกิจตารางเดินช่อง (Mission Grid Mat) Unplugged ป.5 - โรงเรียนบ้านโนนป่าหว้านเชียงฮาย</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Sarabun:wght@300;400;600;700;800&family=Prompt:wght@400;600;700;800&display=swap');

  @page {
    size: A4 portrait;
    margin: 6mm 8mm 6mm 8mm;
  }

  * { box-sizing: border-box; }
  body {
    font-family: 'Sarabun', 'TH Sarabun PSK', sans-serif;
    color: #0f172a;
    background: #e2e8f0;
    margin: 0;
    padding: 15px;
    font-size: 11pt;
    line-height: 1.35;
  }

  .page {
    background: #ffffff;
    width: 210mm;
    min-height: 297mm;
    margin: 0 auto 20px auto;
    padding: 10mm 12mm;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    page-break-after: always;
    position: relative;
    border-radius: 4px;
  }

  @media print {
    body { background: #ffffff; padding: 0; }
    .page {
      margin: 0;
      box-shadow: none;
      width: 100%;
      min-height: auto;
      page-break-after: always;
      border-radius: 0;
      padding: 5mm 6mm;
    }
    .no-print { display: none !important; }
  }

  /* Headers */
  .header-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 2.5px solid #1e3a8a;
    padding-bottom: 4px;
    margin-bottom: 6px;
  }
  .header-title {
    font-family: 'Prompt', sans-serif;
    font-size: 14.5pt;
    font-weight: 800;
    color: #1e3a8a;
    margin: 0;
  }
  .header-sub {
    font-size: 9.5pt;
    color: #475569;
    font-weight: 600;
  }

  /* Team Info Box */
  .team-box {
    display: flex;
    justify-content: space-between;
    background: #f8fafc;
    border: 1.5px solid #cbd5e1;
    border-radius: 6px;
    padding: 5px 10px;
    margin-bottom: 6px;
    font-size: 10pt;
  }

  /* Mission Story Box */
  .story-box {
    background: #eff6ff;
    border-left: 4px solid #2563eb;
    padding: 6px 10px;
    border-radius: 0 6px 6px 0;
    margin-bottom: 8px;
    font-size: 10pt;
  }
  .story-box strong {
    color: #1e3a8a;
    font-family: 'Prompt', sans-serif;
  }

  /* Rules & Legend */
  .legend-bar {
    display: flex;
    justify-content: space-between;
    background: #f1f5f9;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    padding: 5px 8px;
    margin-bottom: 8px;
    font-size: 9pt;
  }
  .legend-item {
    display: flex;
    align-items: center;
    gap: 4px;
  }

  /* Main Grid */
  .grid-container {
    display: flex;
    justify-content: center;
    align-items: center;
    margin: 6px 0 10px 0;
  }
  .grid-mat {
    border-collapse: collapse;
    margin: 0 auto;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
  }
  .grid-mat th {
    background: #1e3a8a;
    color: #ffffff;
    font-family: 'Prompt', sans-serif;
    font-weight: 600;
    font-size: 10pt;
    padding: 3px 6px;
    text-align: center;
    border: 1.5px solid #1e3a8a;
  }
  .row-label {
    background: #3b82f6 !important;
    color: #ffffff;
    font-weight: 700;
    font-size: 9.5pt;
    width: 60px;
    text-align: center;
    border: 1.5px solid #2563eb;
  }
  .grid-cell {
    width: 78px;
    height: 70px;
    border: 2px solid #94a3b8;
    text-align: center;
    vertical-align: middle;
    position: relative;
    padding: 2px;
    background: #ffffff;
  }
  .grid-cell.cell-start {
    background: #ecfdf5;
    border: 2.5px solid #10b981;
  }
  .grid-cell.cell-goal {
    background: #fef2f2;
    border: 2.5px solid #ef4444;
  }
  .grid-cell.cell-obstacle {
    background: #f1f5f9;
    border: 2px dashed #64748b;
  }
  .grid-cell.cell-item {
    background: #fffbeb;
    border: 2px solid #f59e0b;
  }
  .cell-icon {
    font-size: 20pt;
    line-height: 1;
    display: block;
  }
  .cell-label {
    font-size: 7.5pt;
    font-weight: 700;
    color: #334155;
    line-height: 1.1;
    margin-top: 2px;
  }
  .cell-coord {
    position: absolute;
    top: 2px;
    left: 4px;
    font-size: 7.5pt;
    font-weight: 700;
    color: #94a3b8;
  }

  /* Coding Slot Tray */
  .tray-section {
    background: #f8fafc;
    border: 2px solid #3b82f6;
    border-radius: 8px;
    padding: 6px 10px;
    margin-bottom: 8px;
  }
  .tray-title {
    font-family: 'Prompt', sans-serif;
    font-weight: 700;
    font-size: 10.5pt;
    color: #1e3a8a;
    display: flex;
    justify-content: space-between;
    margin-bottom: 5px;
  }
  .tray-slots {
    display: flex;
    flex-wrap: wrap;
    gap: 5px;
    justify-content: center;
  }
  .slot {
    width: 52px;
    height: 48px;
    border: 2px dashed #94a3b8;
    border-radius: 6px;
    background: #ffffff;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    font-size: 8.5pt;
    color: #64748b;
    font-weight: 600;
  }
  .slot-num {
    font-size: 7.5pt;
    color: #94a3b8;
    margin-bottom: 1px;
  }

  /* Scratch Bridge Box */
  .scratch-box {
    background: #fff7ed;
    border: 1.5px solid #fdba74;
    border-radius: 6px;
    padding: 5px 8px;
    margin-bottom: 6px;
    font-size: 9.5pt;
  }
  .scratch-box strong { color: #c2410c; font-family: 'Prompt', sans-serif; }

  /* Assessment & Stamp */
  .eval-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-top: 1.5px dashed #cbd5e1;
    padding-top: 5px;
    font-size: 9pt;
  }
  .stars-box {
    font-weight: 700;
    color: #1e3a8a;
  }

  /* Card Sheet Styles */
  .card-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 8px;
    margin-top: 8px;
  }
  .coding-card {
    border: 2px solid #0f172a;
    border-radius: 8px;
    padding: 6px;
    text-align: center;
    background: #ffffff;
    position: relative;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    height: 68px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
  }
  .coding-card.blue { border-color: #2563eb; background: #eff6ff; }
  .coding-card.green { border-color: #059669; background: #ecfdf5; }
  .coding-card.amber { border-color: #d97706; background: #fffbeb; }
  .coding-card.purple { border-color: #7c3aed; background: #faf5ff; }
</style>
</head>
<body>

<div class="no-print" style="max-width:210mm; margin:10px auto 15px auto; background:#1e3a8a; color:white; padding:12px 18px; border-radius:8px; display:flex; justify-content:space-between; align-items:center;">
  <div>
    <strong style="font-size:14pt; font-family:'Prompt',sans-serif;">🖨️ ชุดแผ่นแผนที่ภารกิจตารางเดินช่อง (Mission Grid Mat) Unplugged ป.5</strong><br>
    <span style="font-size:10.5pt; color:#bfdbfe;">จัดทำสำหรับนักเรียนชั้น ป.5 โรงเรียนบ้านโนนป่าหว้านเชียงฮาย (4 ภารกิจ + 1 แผ่นบัตรคำสั่งตัดแจก)</span>
  </div>
  <button onclick="window.print()" style="background:#22c55e; color:white; font-family:'Prompt',sans-serif; font-size:12pt; font-weight:bold; padding:8px 18px; border:none; border-radius:6px; cursor:pointer;">
    🖨️ สั่งพิมพ์เอกสาร (Print A4)
  </button>
</div>
"""]

    for m in missions:
        slot_html = ""
        for s in range(1, m["slots"] + 1):
            slot_html += f"""<div class="slot"><span class="slot-num">ช่อง {s}</span><span>วางการ์ด</span></div>"""

        grid_html = f"""<table class="grid-mat"><thead><tr><th style="width:65px;">แถว / หลัก</th>"""
        for c in m["col_labels"]:
            grid_html += f"""<th>{c}</th>"""
        grid_html += "</tr></thead><tbody>"

        for r_idx, row in enumerate(m["grid"]):
            r_label = m["row_labels"][r_idx]
            grid_html += f"""<tr><td class="row-label">{r_label}</td>"""
            for cell in row:
                c_type = cell["type"]
                type_class = ""
                if c_type == "start": type_class = "cell-start"
                elif c_type == "goal": type_class = "cell-goal"
                elif c_type == "obstacle": type_class = "cell-obstacle"
                elif c_type == "item": type_class = "cell-item"

                icon = cell["txt"]
                sub = cell["sub"].replace("\n", "<br>")
                coord = "" if icon in ["🐱", "🐝", "🧭", "🤖", "🏡", "🍯", "👑", "🏁", "🪨", "⚠️", "🌊", "🧱", "⚡", "🌻", "🌸", "🗝️", "🚪", "♻️"] else icon

                grid_html += f"""<td class="grid-cell {type_class}">"""
                if coord:
                    grid_html += f"""<span class="cell-coord">{coord}</span>"""
                else:
                    grid_html += f"""<span class="cell-icon">{icon}</span><span class="cell-label">{sub}</span>"""
                grid_html += "</td>"
            grid_html += "</tr>"
        grid_html += "</tbody></table>"

        html_parts.append(f"""
<!-- PAGE {m['id']}: MISSION {m['id']} -->
<div class="page">
  <div class="header-bar">
    <div>
      <h1 class="header-title">🗺️ แผ่นแผนที่ภารกิจตารางเดินช่อง (Mission Grid Mat)</h1>
      <div class="header-sub">วิชาวิทยาการคำนวณ ว15101 ชั้น ป.5 | โรงเรียนบ้านโนนป่าหว้านเชียงฮาย สพป.หนองบัวลำภู เขต 2</div>
    </div>
    <div style="text-align:right;">
      <span style="background:#1e3a8a; color:white; font-weight:bold; padding:3px 8px; border-radius:4px; font-size:9.5pt;">
        {m['indicator']}
      </span>
      <div style="font-size:8.5pt; color:#64748b; margin-top:2px;">กิจกรรม Active Learning (Unplugged)</div>
    </div>
  </div>

  <div class="team-box">
    <div><strong>กลุ่มคู่หูที่:</strong> ......... <strong>ชื่อทีม:</strong> ................................................................</div>
    <div><strong>1. Navigator (ผู้นำทาง):</strong> ................................................ <strong>เลขที่:</strong> .....</div>
    <div><strong>2. Driver (ผู้สั่งการ):</strong> ................................................ <strong>เลขที่:</strong> .....</div>
  </div>

  <div class="story-box">
    <strong>🎯 {m['title']}</strong><br>
    {m['story']}<br>
    <span style="font-size:9pt; color:#1e40af;"><strong>ทักษะเป้าหมาย:</strong> {m['concept']}</span>
  </div>

  <div class="legend-bar">
    <div class="legend-item"><span style="font-size:12pt;">🚩</span> <strong>จุดเริ่ม:</strong> {m['start']}</div>
    <div class="legend-item"><span style="font-size:12pt;">🏆</span> <strong>เป้าหมาย:</strong> {m['goal']}</div>
    <div class="legend-item"><span style="font-size:12pt;">⛔</span> <strong>สิ่งกีดขวาง:</strong> {m['obstacles']}</div>
  </div>

  <div class="grid-container">
    {grid_html}
  </div>

  <div class="tray-section">
    <div class="tray-title">
      <span>🗂️ แถบวางบัตรคำสั่งลูกศรบนโต๊ะ (Coding Sequence Tray)</span>
      <span style="font-size:8.5pt; font-weight:normal; color:#475569;">*หยิบบัตรคำสั่งลูกศรมาวางเรียงต่อกันตามลำดับ 1, 2, 3...*</span>
    </div>
    <div class="tray-slots">
      {slot_html}
    </div>
  </div>

  <div class="scratch-box">
    <strong>💻 เชื่อมโยงสู่ Scratch ภาษาไทย (ว 4.2 ป.5/2):</strong>
    <span>เมื่อวางบัตรคำสั่งบนโต๊ะผ่านแล้ว ให้แปลงเป็นบล็อกคำสั่ง Scratch: <em>{m['scratch_hint']}</em></span>
  </div>

  <div class="eval-row">
    <div class="stars-box">
      ⭐ <strong>ผลการปฏิบัติภารกิจ:</strong> &nbsp; [ &nbsp; ] 3 ดาว (ยอดเยี่ยม ไม่ชนหิน) &nbsp;&nbsp; [ &nbsp; ] 2 ดาว (ดี มีปรับแก้ 1 ครั้ง) &nbsp;&nbsp; [ &nbsp; ] 1 ดาว (ผ่าน)
    </div>
    <div>
      <strong>ลงชื่อครูผู้ตรวจ:</strong> ............................................................ (นายเตชินท์ อินทมล)
    </div>
  </div>
</div>
""")

    # -------------------------------------------------------------------------
    # PAGE 5: CUT-OUT ARROW CARDS (FOR STUDENTS)
    # -------------------------------------------------------------------------
    cards = [
        ("⬆️ เดินหน้า 1 ช่อง", "blue", 8),
        ("⬅️ หันซ้าย 90°", "green", 4),
        ("➡️ หันขวา 90°", "green", 4),
        ("🌸 เก็บน้ำหวาน / ไอเทม", "amber", 4),
        ("🗝️ หยิบกุญแจ / ปลดล็อก", "amber", 2),
        ("🔁 วนซ้ำ (Loop) 4 รอบ", "purple", 2),
    ]
    card_items_html = ""
    for c_text, c_color, count in cards:
        for _ in range(count):
            card_items_html += f"""
            <div class="coding-card {c_color}">
              <div style="font-size:16pt; line-height:1.1;">{c_text.split()[0]}</div>
              <div style="font-size:9pt; font-weight:bold; margin-top:2px;">{' '.join(c_text.split()[1:])}</div>
            </div>"""

    tokens_html = """
    <div style="display:flex; justify-content:space-around; align-items:center; background:#f8fafc; border:2px dashed #64748b; border-radius:8px; padding:6px 10px; margin-top:8px;">
      <div style="text-align:center;">
        <div style="font-size:22pt;">🐱</div>
        <div style="font-size:8.5pt; font-weight:bold;">หมากแมว Scratch</div>
      </div>
      <div style="text-align:center;">
        <div style="font-size:22pt;">🐝</div>
        <div style="font-size:8.5pt; font-weight:bold;">หมากผึ้งน้อย</div>
      </div>
      <div style="text-align:center;">
        <div style="font-size:22pt;">🧭</div>
        <div style="font-size:8.5pt; font-weight:bold;">หมากนักสำรวจ</div>
      </div>
      <div style="text-align:center;">
        <div style="font-size:22pt;">🤖</div>
        <div style="font-size:8.5pt; font-weight:bold;">หมากหุ่นยนต์</div>
      </div>
      <div style="text-align:center;">
        <div style="font-size:22pt;">🪨 🌊 🧱 ⚡</div>
        <div style="font-size:8.5pt; font-weight:bold;">หมากสิ่งกีดขวาง</div>
      </div>
    </div>
    """

    html_parts.append(f"""
<!-- PAGE 5: PRINTABLE ARROW CARDS SHEET -->
<div class="page">
  <div class="header-bar">
    <div>
      <h1 class="header-title">✂️ ชุดบัตรคำสั่งลูกศรและตัวหมากเดินช่อง Unplugged (สำหรับตัดแจกเด็ก)</h1>
      <div class="header-sub">พิมพ์ลงกระดาษการ์ดขาวหรือเคลือบใสเพื่อใช้ซ้ำ | รายวิชาวิทยาการคำนวณ ป.5 โรงเรียนบ้านโนนป่าหว้านเชียงฮาย</div>
    </div>
    <div style="text-align:right;">
      <span style="background:#059669; color:white; font-weight:bold; padding:3px 8px; border-radius:4px; font-size:9.5pt;">
        สื่อการสอนรูปธรรม
      </span>
    </div>
  </div>

  <div style="background:#fef3c7; border-left:4px solid #f59e0b; padding:6px 10px; border-radius:0 6px 6px 0; margin-bottom:8px; font-size:9.5pt;">
    <strong>✂️ คำแนะนำสำหรับครูผู้สอน:</strong> พิมพ์แผ่นนี้ลงกระดาษหนา (120-180 แกรม) แล้วใช้กรรไกรตัดตามรอยเส้นประ แจกใส่กล่องพลาสติกหรือซองซิปล็อกให้เด็กแต่ละคู่ (คู่ละ 1 กล่อง) เพื่อใช้หยิบวางบนแผ่นตารางภารกิจ
  </div>

  <div class="card-grid">
    {card_items_html}
  </div>

  <div style="margin-top:12px; font-family:'Prompt',sans-serif; font-size:10.5pt; font-weight:700; color:#1e3a8a;">
    ♟️ ตัวหมากตัวละครและอุปสรรคจำลอง (ตัดพับตั้งโต๊ะเพื่อใช้เดินบนแผ่นแผนที่):
  </div>
  {tokens_html}

  <div style="margin-top:14px; border-top:1.5px dashed #cbd5e1; padding-top:6px; font-size:9pt; color:#64748b; display:flex; justify-content:space-between;">
    <span>จัดทำโดย นายเตชินท์ อินทมล ครูโรงเรียนบ้านโนนป่าหว้านเชียงฮาย</span>
    <span>นวัตกรรมสื่อการสอน Active Learning วิทยาการคำนวณ ว15101</span>
  </div>
</div>

</body>
</html>
""")

    out_file = "แผ่นแผนที่ภารกิจตารางเดินช่อง_Unplugged_ป5_พร้อมพิมพ์.html"
    with open(out_file, "w", encoding="utf-8") as f:
        f.write("".join(html_parts))
    print(f"Generated Printable HTML: {out_file}")


# -----------------------------------------------------------------------------
# 2. DOCX GENERATOR (Academic standard Word format for attachments)
# -----------------------------------------------------------------------------
def make_docx_p(runs, align="left", space_before=0, space_after=20, line_spacing=220):
    p_props = [f'<w:jc w:val="{align}"/>']
    p_props.append(f'<w:spacing w:before="{space_before}" w:after="{space_after}" w:line="{line_spacing}" w:lineRule="auto"/>')
    runs_xml = []
    for item in runs:
        if isinstance(item, str):
            t, b, i, sz, c = item, False, False, 24, "000000"
        else:
            t = item[0]
            b = item[1] if len(item) > 1 else False
            i = item[2] if len(item) > 2 else False
            sz = item[3] if len(item) > 3 else 24
            c = item[4] if len(item) > 4 else "000000"
        
        r_pr = ['<w:rFonts w:ascii="TH Sarabun PSK" w:hAnsi="TH Sarabun PSK" w:cs="TH Sarabun PSK"/>']
        if b: r_pr.append('<w:b/><w:bCs/>')
        if i: r_pr.append('<w:i/><w:iCs/>')
        r_pr.append(f'<w:sz w:val="{sz}"/><w:szCs w:val="{sz}"/>')
        if c and c != "000000": r_pr.append(f'<w:color w:val="{c}"/>')
        runs_xml.append(f'<w:r><w:rPr>{"".join(r_pr)}</w:rPr><w:t xml:space="preserve">{esc(t)}</w:t></w:r>')
    return f'<w:p><w:pPr>{"".join(p_props)}</w:pPr>{"".join(runs_xml)}</w:p>'

def make_docx_table(headers, rows, col_widths, alignments=None, font_size=20, header_bg="1E3A8A"):
    total_w = sum(col_widths)
    if alignments is None: alignments = ["center"] * len(headers)
    xml = ['<w:tbl>',
           f'''<w:tblPr>
               <w:tblW w:w="{total_w}" w:type="dxa"/>
               <w:tblInd w:w="0" w:type="dxa"/>
               <w:tblBorders>
                   <w:top w:val="single" w:sz="6" w:space="0" w:color="94A3B8"/>
                   <w:left w:val="single" w:sz="6" w:space="0" w:color="94A3B8"/>
                   <w:bottom w:val="single" w:sz="6" w:space="0" w:color="94A3B8"/>
                   <w:right w:val="single" w:sz="6" w:space="0" w:color="94A3B8"/>
                   <w:insideH w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>
                   <w:insideV w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>
               </w:tblBorders>
               <w:tblCellMar>
                   <w:top w:w="40" w:type="dxa"/>
                   <w:left w:w="60" w:type="dxa"/>
                   <w:bottom w:w="40" w:type="dxa"/>
                   <w:right w:w="60" w:type="dxa"/>
               </w:tblCellMar>
           </w:tblPr>''']
    xml.append('<w:tblGrid>')
    for w in col_widths: xml.append(f'<w:gridCol w:w="{w}"/>')
    xml.append('</w:tblGrid>')
    # Header
    xml.append('<w:tr><w:trPr><w:tblHeader/><w:trHeight w:val="260" w:hRule="atLeast"/></w:trPr>')
    for i, h in enumerate(headers):
        w = col_widths[i]
        al = alignments[i] if i < len(alignments) else "center"
        xml.append(f'''<w:tc><w:tcPr><w:tcW w:w="{w}" w:type="dxa"/><w:shd w:val="clear" w:color="auto" w:fill="{header_bg}"/><w:vAlign w:val="center"/></w:tcPr>
            <w:p><w:pPr><w:jc w:val="{al}"/><w:spacing w:before="20" w:after="20" w:line="200" w:lineRule="auto"/></w:pPr>
            <w:r><w:rPr><w:rFonts w:ascii="TH Sarabun PSK" w:hAnsi="TH Sarabun PSK" w:cs="TH Sarabun PSK"/><w:b/><w:bCs/><w:sz w:val="{font_size}"/><w:szCs w:val="{font_size}"/><w:color w:val="FFFFFF"/></w:rPr><w:t xml:space="preserve">{esc(h)}</w:t></w:r></w:p></w:tc>''')
    xml.append('</w:tr>')
    # Rows
    for row in rows:
        xml.append('<w:tr><w:trPr><w:trHeight w:val="340" w:hRule="atLeast"/></w:trPr>')
        for i, val in enumerate(row):
            w = col_widths[i]
            al = alignments[i] if i < len(alignments) else "left"
            bg = "FFFFFF"
            if any(k in str(val) for k in ["🐱", "🐝", "🧭", "🤖"]): bg = "ECFDF5"
            elif any(k in str(val) for k in ["🏡", "🍯", "👑", "🏁"]): bg = "FEF2F2"
            elif any(k in str(val) for k in ["🪨", "⚠️", "🌊", "🧱", "⚡", "🐝❌"]): bg = "F1F5F9"
            elif any(k in str(val) for k in ["🌸", "🌻", "🗝️", "🚪", "♻️"]): bg = "FFFBEB"
            elif "แถว" in str(val): bg = "DBEAFE"

            runs_xml = []
            for part in str(val).split("\n"):
                if part:
                    runs_xml.append(f'<w:r><w:rPr><w:rFonts w:ascii="TH Sarabun PSK" w:hAnsi="TH Sarabun PSK" w:cs="TH Sarabun PSK"/><w:sz w:val="{font_size}"/><w:szCs w:val="{font_size}"/><w:color w:val="0F172A"/></w:rPr><w:t xml:space="preserve">{esc(part)}</w:t></w:r>')
            
            p_content = "".join(runs_xml) if runs_xml else '<w:r><w:t></w:t></w:r>'
            xml.append(f'''<w:tc><w:tcPr><w:tcW w:w="{w}" w:type="dxa"/><w:shd w:val="clear" w:color="auto" w:fill="{bg}"/><w:vAlign w:val="center"/></w:tcPr>
                <w:p><w:pPr><w:jc w:val="{al}"/><w:spacing w:before="20" w:after="20" w:line="200" w:lineRule="auto"/></w:pPr>{p_content}</w:p></w:tc>''')
        xml.append('</w:tr>')
    xml.append('</w:tbl>')
    return "".join(xml)

def build_docx_mats():
    elements = []
    
    # Document Cover / Title
    elements.append(make_docx_p([
        ("ชุดแผ่นแผนที่ภารกิจตารางเดินช่อง (Mission Grid Mat) กิจกรรม Unplugged Coding", True, False, 32, "1E3A8A"),
        ("\nรายวิชาวิทยาการคำนวณ ว15101 ชั้นประถมศึกษาปีที่ 5 ภาคเรียนที่ 1 ปีการศึกษา 2569", True, False, 28, "000000"),
        ("\nโรงเรียนบ้านโนนป่าหว้านเชียงฮาย สำนักงานเขตพื้นที่การศึกษาประถมศึกษาหนองบัวลำภู เขต 2", False, False, 26, "475569")
    ], align="center", space_before=100, space_after=150, line_spacing=240))

    elements.append(make_docx_p([
        ("คำชี้แจงการใช้งานสำหรับครูผู้สอนและนักเรียน", True, False, 28, "1E3A8A"),
        ("\n1. แผ่นแผนที่ภารกิจนี้ใช้สำหรับวางบนโต๊ะของนักเรียนคู่หู (Pair Programming: Navigator & Driver) คู่ละ 1 แผ่น", False, False, 24, "000000"),
        ("\n2. ในขั้นนำและขั้นสอน เด็กยังไม่ต้องเปิดคอมพิวเตอร์ ให้ร่วมมือกันก้มดูแผนที่และนำ 'บัตรคำสั่งลูกศร' มาวางเรียงในช่อง Coding Tray", False, False, 24, "000000"),
        ("\n3. เมื่อวางแผนบัตรคำสั่งผ่านการตรวจสอบและครูตรวจแล้ว จึงอนุญาตให้นำขั้นตอนดังกล่าวไปเขียนโปรแกรมจริงใน Scratch", False, False, 24, "000000")
    ], align="left", space_before=50, space_after=150, line_spacing=220))

    missions_docx = [
        ("ภารกิจที่ 1: พาน้องแมว Scratch เดินทางกลับบ้านแสนสุข (ตาราง 4x4)", "ว 4.2 ป.5/1",
         "ให้นักเรียนช่วยพาน้องแมว 🐱 เดินทางไปที่ 🏡 บ้านแสนสุข โดยหลบ 🪨 ก้อนหินยักษ์ และ ⚠️ หลุมโคลน",
         ["แถว / คอลัมน์", "คอลัมน์ 1", "คอลัมน์ 2", "คอลัมน์ 3", "คอลัมน์ 4"],
         [
             ["แถว D (4)", "D1", "D2", "D3", "🏡 บ้านแสนสุข\n(จุดหมาย)"],
             ["แถว C (3)", "⚠️ หลุมโคลน", "C2", "🪨 หินยักษ์", "C4"],
             ["แถว B (2)", "B1", "B2", "B3", "B4"],
             ["แถว A (1)", "🐱 จุดเริ่มต้น\n(หันหน้า ⬆️)", "🪨 หินยักษ์", "A3", "A4"]
         ],
         [1800, 1900, 1900, 1900, 1900],
         "เดินหน้า ➔ เลี้ยวขวา ➔ เดินหน้า ➔ เลี้ยวซ้าย ➔ เดินหน้า (สั้นที่สุดและปลอดภัย)"),

        ("ภารกิจที่ 2: หุ่นยนต์ผึ้งน้อย บินเก็บน้ำหวานดอกไม้แสนหวาน (ตาราง 4x4)", "ว 4.2 ป.5/1",
         "หุ่นยนต์ผึ้งน้อย 🐝 ต้องเก็บน้ำหวานจาก 🌸 และ 🌻 ให้ครบทั้ง 2 ดอก ก่อนบินเข้า 🍯 รังผึ้งใหญ่ ห้ามชน 🐝❌ รังต่อ และ 🌊 สระน้ำ",
         ["แถว / คอลัมน์", "คอลัมน์ 1", "คอลัมน์ 2", "คอลัมน์ 3", "คอลัมน์ 4"],
         [
             ["แถว D (4)", "D1", "D2", "🌻 ดอกทานตะวัน\n(เก็บน้ำหวาน)", "🍯 รังผึ้งใหญ่\n(จุดหมาย)"],
             ["แถว C (3)", "C1", "🌊 สระน้ำลึก", "C3", "C4"],
             ["แถว B (2)", "B1", "🌸 ดอกชมพู\n(เก็บน้ำหวาน)", "🐝❌ รังต่อดุร้าย", "B4"],
             ["แถว A (1)", "🐝 จุดเริ่มต้น\n(หันหน้า ⬆️)", "A2", "A3", "A4"]
         ],
         [1800, 1900, 1900, 1900, 1900],
         "เดินหน้า ➔ เลี้ยวขวา ➔ เดินหน้า ➔ เก็บน้ำหวาน 🌸 ➔ เลี้ยวซ้าย ➔ เดินหน้า ➔ เลี้ยวขวา ➔ เก็บน้ำหวาน 🌻 ➔ เข้า 🍯"),

        ("ภารกิจที่ 3: นักสำรวจน้อย ล่าขุมทรัพย์ในเขาวงกตปริศนา (ตาราง 5x5)", "ว 4.2 ป.5/1 และ ป.5/2",
         "นักสำรวจน้อย 🧭 ต้องเดินไปเก็บ 🗝️ กุญแจทองคำ เพื่อนำมาเปิด 🚪 ประตูกล ก่อนเข้าไปเปิด 👑 หีบสมบัติ ห้ามชน 🧱 กำแพงหิน และ ⚡ กับดัก",
         ["แถว / คอลัมน์", "คอลัมน์ 1", "คอลัมน์ 2", "คอลัมน์ 3", "คอลัมน์ 4", "คอลัมน์ 5"],
         [
             ["แถว E (5)", "E1", "E2", "E3", "🚪 ประตูกล", "👑 หีบสมบัติ\n(จุดหมาย)"],
             ["แถว D (4)", "D1", "⚡ กับดัก", "D3", "🧱 กำแพง", "D5"],
             ["แถว C (3)", "C1", "🧱 กำแพง", "🗝️ กุญแจทอง", "🧱 กำแพง", "C5"],
             ["แถว B (2)", "B1", "🧱 กำแพง", "B3", "B4", "B5"],
             ["แถว A (1)", "🧭 จุดเริ่ม\n(หัน ⬆️)", "A2", "A3", "A4", "A5"]
         ],
         [1500, 1580, 1580, 1580, 1580, 1580],
         "เดินหน้า ➔ เลี้ยวขวา ➔ เดินหน้า ➔ เลี้ยวซ้าย ➔ เดินหน้า ➔ เก็บ 🗝️ ➔ เลี้ยวขวา ➔ เดินหน้า ➔ เลี้ยวซ้าย ➔ เปิด 🚪 ➔ รับ 👑"),

        ("ภารกิจที่ 4: หุ่นยนต์รักษ์โลก ลาดตระเวนเก็บขยะ 4 ทิศ (ตาราง 5x5 วนลูป)", "ว 4.2 ป.5/2",
         "หุ่นยนต์ 🤖 เดินวนรอบสถานีเป็นรูปสี่เหลี่ยมเพื่อเก็บ ♻️ ขยะรีไซเคิล 4 ทิศ จงออกแบบบล็อก [วนซ้ำ Loop 4 รอบ] เพื่อประหยัดโค้ด!",
         ["แถว / คอลัมน์", "คอลัมน์ 1", "คอลัมน์ 2", "คอลัมน์ 3", "คอลัมน์ 4", "คอลัมน์ 5"],
         [
             ["แถว E (5)", "♻️ ขยะมุม 2", "E2", "E3", "E4", "♻️ ขยะมุม 3"],
             ["แถว D (4)", "D1", "D2", "D3", "D4", "D5"],
             ["แถว C (3)", "C1", "⚡ เสาไฟ", "⚡ แกนห้ามชน", "⚡ เสาไฟ", "C5"],
             ["แถว B (2)", "B1", "B2", "B3", "B4", "B5"],
             ["แถว A (1)", "🤖 จุดเริ่ม & จบ\n(หัน ⬆️)", "A2", "A3", "A4", "♻️ ขยะมุม 4"]
         ],
         [1500, 1580, 1580, 1580, 1580, 1580],
         "[ ทำซ้ำ 4 รอบ ] { เดินหน้า 4 ก้าว ➔ หันขวา 90 องศา } ลดคำสั่งจาก 16 คำสั่งเหลือเพียง 1 ลูป!")
    ]

    for title, ind, desc, headers, rows, widths, ans in missions_docx:
        elements.append(make_docx_p([], space_before=0, space_after=0))
        elements.append(make_docx_p([
            (f"🗺️ {title}", True, False, 28, "1E3A8A"),
            (f"  [ ตัวชี้วัด: {ind} ]", True, False, 24, "059669")
        ], align="left", space_before=40, space_after=15))

        elements.append(make_docx_p([
            (f"🎯 ภารกิจคู่หู: {desc}", False, False, 24, "1E293B"),
            ("\nข้อมูลคู่หู: ชื่อทีม ................................................ ผู้นำทาง (Navigator) ........................................ ผู้สั่งการ (Driver) ........................................", False, True, 22, "475569")
        ], align="left", space_before=10, space_after=20))

        elements.append(make_docx_table(headers, rows, widths, alignments=["center"]*len(headers), font_size=20, header_bg="1E3A8A"))
        
        # Coding Tray & Evaluation
        elements.append(make_docx_p([
            ("🗂️ แถบเรียงบัตรคำสั่งลูกศรบนโต๊ะ (Coding Tray): [ 1 ] ➔ [ 2 ] ➔ [ 3 ] ➔ [ 4 ] ➔ [ 5 ] ➔ [ 6 ] ➔ [ 7 ] ➔ [ 8 ]", True, False, 22, "1E40AF"),
            (f"\n💡 แนวทางคำตอบ / โค้ด Scratch: {ans}", False, False, 22, "047857"),
            ("\n⭐ ผลการปฏิบัติ:  [  ] 3 ดาว (ดีเยี่ยม)    [  ] 2 ดาว (ดี)    [  ] 1 ดาว (พอใช้)       ลงชื่อครูผู้ตรวจ .....................................................", False, True, 22, "334155")
        ], align="left", space_before=25, space_after=50, line_spacing=220))
        elements.append(make_docx_p([("", False, False, 24, "000000")], space_before=0, space_after=0))
        elements.append('<w:p><w:r><w:br w:type="page"/></w:r></w:p>')

    # Wrap into full docx
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
  </w:docDefaults>
</w:styles>"""

    document_xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:body>
    {doc_body}
    <w:sectPr>
      <w:pgSz w:w="11906" w:h="16838"/>
      <w:pgMar w:top="850" w:right="1000" w:bottom="850" w:left="1000" w:header="708" w:footer="708" w:gutter="0"/>
    </w:sectPr>
  </w:body>
</w:document>"""

    out_docx = "แผ่นแผนที่ภารกิจตารางเดินช่อง_Unplugged_ป5_ครูเตชินท์.docx"
    with zipfile.ZipFile(out_docx, 'w', zipfile.ZIP_DEFLATED) as docx:
        docx.writestr('[Content_Types].xml', content_types)
        docx.writestr('_rels/.rels', rels)
        docx.writestr('word/document.xml', document_xml)
        docx.writestr('word/styles.xml', styles)
        docx.writestr('word/_rels/document.xml.rels', doc_rels)

    print(f"Generated DOCX: {out_docx}")

if __name__ == "__main__":
    build_html_mats()
    build_docx_mats()
    # Copy to docs/
    os.system("cp แผ่นแผนที่ภารกิจตารางเดินช่อง_Unplugged_ป5_พร้อมพิมพ์.html docs/ 2>/dev/null")
    os.system("cp แผ่นแผนที่ภารกิจตารางเดินช่อง_Unplugged_ป5_ครูเตชินท์.docx docs/ 2>/dev/null")
    print("Copied files to docs/ successfully.")
