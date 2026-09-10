# -*- coding: utf-8 -*-
with open('make_4page_worksheet_docx.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Enhance titles to explicitly map to P.5 Levels 1-10
code = code.replace(
    '🤖 ใบงานที่ 1: แผนที่ก้าวแรกและอัลกอริทึม (First Steps & Sequence) 🚀',
    '🤖 ใบงานที่ 1: การค้นหารูปแบบและอัลกอริทึมก้าวแรก (Pattern Recognition & Sequence) 🚀'
)
code = code.replace(
    'รายวิชาเทคโนโลยี (วิทยาการคำนวณ) ว15101 ชั้น ป.5 | โรงเรียนบ้านโนนป่าหว้านเชียงฮาย',
    'รายวิชาเทคโนโลยี (วิทยาการคำนวณ) ว15101 ชั้น ป.5 (สอดรับเกม CodeBot AR ด่าน 1-10 แทร็ก ป.5) | โรงเรียนบ้านโนนป่าหว้านเชียงฮาย'
)

code = code.replace(
    '🔄 ใบงานที่ 2: ถอดรหัสลับพลังวนซ้ำ (Pattern Recognition & Loops) 🚀',
    '🔄 ใบงานที่ 2: ลูปบันได 3 ขั้นและลูปผสมหลายคำสั่ง (Multi-Action & Staircase Loop x3) 🚀'
)

code = code.replace(
    '⚡ ใบงานที่ 3: เงื่อนไขกุญแจและประตูเลเซอร์ (If-Then-Else) 🚀',
    '⚡ ใบงานที่ 3: เงื่อนไขถ้า...แล้ว กับประตูปริศนาเลเซอร์และกุญแจ (If-Then Conditionals & Key) 🚀'
)

code = code.replace(
    '🐞 ใบงานที่ 4: ยอดนักสืบตามล่าแก้บั๊ก (Debugging & AAR) 🚀',
    '🐞 ใบงานที่ 4: ยอดนักสืบแก้บั๊กตรรกะและบททดสอบมาสเตอร์จักรวาล ป.5 (Logic Debugging & Grand Space Master) 🚀'
)

with open('make_4page_worksheet_docx.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Updated make_4page_worksheet_docx.py successfully!")
