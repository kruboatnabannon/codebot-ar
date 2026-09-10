#!/usr/bin/env bash
# สคริปต์อัปเดตและดันโค้ดขึ้น Git อัตโนมัติในคำสั่งเดียว

cd "$(dirname "$0")"

COMMIT_MSG="${1:-Update project files: $(date '+%Y-%m-%d %H:%M:%S')}"

echo "📦 1. กำลังเตรียมไฟล์ (git add)..."
git add -A

echo "💾 2. กำลังบันทึกการเปลี่ยนแปลง (git commit)..."
git commit -m "$COMMIT_MSG" || echo "ℹ️ ไม่มีการเปลี่ยนแปลงใหม่ที่ต้องบันทึก"

echo "🚀 3. กำลังส่งขึ้น Git (git push)..."
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "main")
git push origin "$CURRENT_BRANCH"

echo "✅ อัปเดตขึ้น Git เรียบร้อยแล้ว!"
