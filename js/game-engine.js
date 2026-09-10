/**
 * CodeBot AR Game Engine
 * Handles 2D grid simulation, code execution pipeline, loop unrolling, and robot physics
 */

class GameEngine {
  constructor(canvasId) {
    this.canvas = document.getElementById(canvasId);
    this.ctx = this.canvas.getContext('2d');
    this.currentLevel = null;

    // Simulation State
    this.robot = { x: 0, y: 0, dir: 1 }; // dir: 0=Up, 1=Right, 2=Down, 3=Left
    this.items = [];
    this.hasKey = false;
    this.isDoorOpen = false;

    // Execution State
    this.codeSequence = [];
    this.isExecuting = false;
    this.currentStepIdx = -1;
    this.executionSpeed = 500; // ms per step
    this.timerInterval = null;

    // Callbacks
    this.onStepChange = null; // (currentStepIndex) => {}
    this.onFinish = null;     // (result) => {}
    this.onStatusMsg = null;  // (msg, isError) => {}

    this.initCanvasResize();
  }

  initCanvasResize() {
    this.canvas.width = 440;
    this.canvas.height = 250;
  }

  loadLevel(levelData) {
    this.currentLevel = JSON.parse(JSON.stringify(levelData)); // Deep clone
    this.resetSimulation();
    this.render();
  }

  resetSimulation() {
    if (!this.currentLevel) return;

    if (this.stepTimeout) {
      clearTimeout(this.stepTimeout);
      this.stepTimeout = null;
    }
    this.isExecuting = false;
    this.isStepMode = false;
    this.currentStepIdx = -1;
    this.hasKey = false;
    this.isDoorOpen = false;

    // Reset robot position & direction
    this.robot = { ...this.currentLevel.robotStart };

    // Reset items
    this.items = this.currentLevel.items.map(item => ({ ...item, collected: false, open: false }));

    this.render();
  }

  setCode(sequence) {
    this.codeSequence = [...sequence];
  }

  render() {
    if (!this.ctx || !this.currentLevel) return;

    const width = this.canvas.width;
    const height = this.canvas.height;
    const cols = this.currentLevel.gridSize.cols;
    const rows = this.currentLevel.gridSize.rows;

    const cellSize = Math.min(Math.floor((width - 40) / cols), Math.floor((height - 30) / rows));
    const offsetX = Math.floor((width - cols * cellSize) / 2);
    const offsetY = Math.floor((height - rows * cellSize) / 2);

    this.cellSize = cellSize;
    this.offsetX = offsetX;
    this.offsetY = offsetY;

    // 1. Clean Crisp Board Background (Bright & High-Contrast for Classroom Visibility)
    this.ctx.fillStyle = '#ffffff';
    this.ctx.fillRect(0, 0, width, height);

    // 2. Draw Grid Tiles (Crisp White with Vibrant Sky-Blue Borders)
    for (let r = 0; r < rows; r++) {
      for (let c = 0; c < cols; c++) {
        const x = offsetX + c * cellSize;
        const y = offsetY + r * cellSize;

        this.ctx.fillStyle = '#ffffff';
        this.ctx.fillRect(x, y, cellSize, cellSize);

        this.ctx.strokeStyle = '#60a5fa'; // Bright Sky-Blue grid line
        this.ctx.lineWidth = 2;
        this.ctx.strokeRect(x, y, cellSize, cellSize);
      }
    }

    // 3. Draw Goal Tile (Radiant Golden Yellow with Bold Gold Border)
    const goalX = offsetX + this.currentLevel.goal.x * cellSize;
    const goalY = offsetY + this.currentLevel.goal.y * cellSize;
    this.ctx.fillStyle = '#fef08a'; // Radiant pastel yellow
    this.ctx.fillRect(goalX, goalY, cellSize, cellSize);
    this.ctx.strokeStyle = '#eab308'; // Solid Amber Gold Border
    this.ctx.lineWidth = 3.5;
    this.ctx.strokeRect(goalX + 1.5, goalY + 1.5, cellSize - 3, cellSize - 3);

    // Goal Rocket (Large & Colorful)
    this.ctx.font = `${Math.floor(cellSize * 0.65)}px "Apple Color Emoji", "Segoe UI Emoji", "Noto Color Emoji", sans-serif`;
    this.ctx.textAlign = 'center';
    this.ctx.textBaseline = 'middle';
    this.ctx.fillText('🚀', goalX + cellSize / 2, goalY + cellSize / 2);

    // 4. Draw Obstacles (Dark Slate Gray/Blue Tiles with 3D Rock)
    this.currentLevel.obstacles.forEach(obs => {
      const ox = offsetX + obs.x * cellSize;
      const oy = offsetY + obs.y * cellSize;
      
      // Dark slate blue tile background
      this.ctx.fillStyle = '#475569';
      this.ctx.fillRect(ox, oy, cellSize, cellSize);
      this.ctx.strokeStyle = '#60a5fa';
      this.ctx.lineWidth = 2;
      this.ctx.strokeRect(ox, oy, cellSize, cellSize);

      // 3D Space Rock Icon
      this.ctx.font = `${Math.floor(cellSize * 0.58)}px "Apple Color Emoji", "Segoe UI Emoji", "Noto Color Emoji", sans-serif`;
      this.ctx.textAlign = 'center';
      this.ctx.textBaseline = 'middle';
      this.ctx.fillText('🪨', ox + cellSize / 2, oy + cellSize / 2);
    });

    // 5. Draw Items (Batteries, Keys, Laser Doors)
    this.items.forEach(item => {
      const ix = offsetX + item.x * cellSize;
      const iy = offsetY + item.y * cellSize;

      if (item.type === 'battery' && !item.collected) {
        this.ctx.font = `${Math.floor(cellSize * 0.62)}px "Apple Color Emoji", "Segoe UI Emoji", "Noto Color Emoji", sans-serif`;
        this.ctx.textAlign = 'center';
        this.ctx.textBaseline = 'middle';
        this.ctx.fillText('🔋', ix + cellSize / 2, iy + cellSize / 2);
      } else if (item.type === 'key' && !item.collected) {
        this.ctx.font = `${Math.floor(cellSize * 0.62)}px "Apple Color Emoji", "Segoe UI Emoji", "Noto Color Emoji", sans-serif`;
        this.ctx.textAlign = 'center';
        this.ctx.textBaseline = 'middle';
        this.ctx.fillText('🔑', ix + cellSize / 2, iy + cellSize / 2);
      } else if (item.type === 'laser_door') {
        if (!item.open) {
          this.ctx.fillStyle = 'rgba(239, 68, 68, 0.25)';
          this.ctx.fillRect(ix, iy, cellSize, cellSize);
          this.ctx.strokeStyle = '#ef4444';
          this.ctx.lineWidth = 2.5;
          this.ctx.strokeRect(ix + 1.5, iy + 1.5, cellSize - 3, cellSize - 3);
          this.ctx.font = `${Math.floor(cellSize * 0.58)}px "Apple Color Emoji", "Segoe UI Emoji", "Noto Color Emoji", sans-serif`;
          this.ctx.textAlign = 'center';
          this.ctx.textBaseline = 'middle';
          this.ctx.fillText('🚪', ix + cellSize / 2, iy + cellSize / 2);
        } else {
          this.ctx.font = `${Math.floor(cellSize * 0.5)}px "Apple Color Emoji", "Segoe UI Emoji", "Noto Color Emoji", sans-serif`;
          this.ctx.textAlign = 'center';
          this.ctx.textBaseline = 'middle';
          this.ctx.fillText('✨', ix + cellSize / 2, iy + cellSize / 2);
        }
      }
    });

    // 6. Draw Robot Tile (Pastel Mint Green with Bright Solid Green Border)
    const rx = offsetX + this.robot.x * cellSize;
    const ry = offsetY + this.robot.y * cellSize;
    const centerX = rx + cellSize / 2;
    const centerY = ry + cellSize / 2;

    this.ctx.fillStyle = '#dcfce7'; // Pastel Green tile
    this.ctx.fillRect(rx, ry, cellSize, cellSize);
    this.ctx.strokeStyle = '#22c55e'; // Solid Green Border
    this.ctx.lineWidth = 3.5;
    this.ctx.strokeRect(rx + 1.5, ry + 1.5, cellSize - 3, cellSize - 3);

    // Direction angle: 0=Up (-90°), 1=Right (0°), 2=Down (90°), 3=Left (180°)
    const angles = [-Math.PI / 2, 0, Math.PI / 2, Math.PI];
    const angle = angles[this.robot.dir];

    // 6a. Radiant Headlight Beam (ลำแสงไฟหน้าส่องสว่างไปยังช่องด้านหน้า ชัดเจน 100%)
    this.ctx.save();
    this.ctx.translate(centerX, centerY);
    this.ctx.rotate(angle);

    const beamLen = cellSize * 0.95;
    const beamGrad = this.ctx.createRadialGradient(cellSize * 0.25, 0, 4, cellSize * 0.65, 0, beamLen);
    beamGrad.addColorStop(0, 'rgba(251, 191, 36, 0.75)'); // Radiant gold/yellow
    beamGrad.addColorStop(0.4, 'rgba(56, 189, 248, 0.35)'); // Sky blue tint
    beamGrad.addColorStop(1, 'rgba(56, 189, 248, 0.0)');

    this.ctx.fillStyle = beamGrad;
    this.ctx.beginPath();
    this.ctx.moveTo(cellSize * 0.22, -cellSize * 0.2);
    this.ctx.lineTo(cellSize * 0.22 + beamLen, -cellSize * 0.65);
    this.ctx.lineTo(cellSize * 0.22 + beamLen, cellSize * 0.65);
    this.ctx.lineTo(cellSize * 0.22, cellSize * 0.2);
    this.ctx.closePath();
    this.ctx.fill();

    // 6b. Draw Cute Hovercraft Base with Golden GPS Arrow (หุ่นยนต์ยืนบนโฮเวอร์บอร์ด ไม่ใช่รถถัง)
    this.drawCuteHoverBase(this.ctx, cellSize * 0.78);
    this.ctx.restore();

    // 6c. Draw Cute Friendly Robot Icon 🤖 (หุ่นยนต์น่ารักคมชัด ไม่ใช่รถถัง)
    this.ctx.save();
    this.ctx.font = `${Math.floor(cellSize * 0.58)}px "Apple Color Emoji", "Segoe UI Emoji", "Noto Color Emoji", sans-serif`;
    this.ctx.textAlign = 'center';
    this.ctx.textBaseline = 'middle';
    this.ctx.shadowColor = 'rgba(0, 0, 0, 0.3)';
    this.ctx.shadowBlur = 4;
    this.ctx.shadowOffsetY = 2;
    this.ctx.fillText('🤖', centerX, centerY - 2);
    this.ctx.restore();

    // 6d. Front-Edge Direction Badge (ป้ายลูกศรขนาดใหญ่ที่ขอบช่องชี้บอกทิศทาง)
    this.drawFrontDirectionBadge(this.ctx, rx, ry, cellSize, centerX, centerY);

    // 6e. Canvas Compass HUD (ป้ายเข็มทิศแสดงทิศทางที่มุมบนกระดาน ชัดเจน 100%)
    this.drawCompassHUD(this.ctx, width);
  }

  // Futuristic, friendly hovercraft base with prominent Golden GPS Arrow (NO tank treads!)
  drawCuteHoverBase(ctx, size) {
    const s = size / 2;

    // 1. Dual Rear Jet Thruster Glow (ไอพ่นสีฟ้าด้านหลัง)
    ctx.save();
    ctx.fillStyle = '#38bdf8';
    ctx.shadowColor = '#00f0ff';
    ctx.shadowBlur = 8;
    ctx.beginPath();
    ctx.ellipse(-s * 0.52, -s * 0.22, s * 0.2, s * 0.1, 0, 0, Math.PI * 2);
    ctx.ellipse(-s * 0.52, s * 0.22, s * 0.2, s * 0.1, 0, 0, Math.PI * 2);
    ctx.fill();
    ctx.restore();

    // 2. High-Tech Aerodynamic Hovercraft Disc (แผ่นรองลอยตัว สีน้ำเงินเมทัลลิกเรียบหรู)
    ctx.save();
    const podGrad = ctx.createLinearGradient(-s * 0.6, 0, s * 0.6, 0);
    podGrad.addColorStop(0, '#1e40af'); // Deep royal blue
    podGrad.addColorStop(1, '#3b82f6'); // Vibrant tech blue
    ctx.fillStyle = podGrad;
    ctx.strokeStyle = '#93c5fd';
    ctx.lineWidth = 2.5;
    ctx.beginPath();
    if (ctx.roundRect) {
      ctx.roundRect(-s * 0.52, -s * 0.45, s * 0.95, s * 0.9, s * 0.35);
    } else {
      ctx.rect(-s * 0.52, -s * 0.45, s * 0.95, s * 0.9);
    }
    ctx.fill();
    ctx.stroke();

    // 3. Bold Golden GPS Navigation Dart (หัวลูกศร GPS ชี้ไปข้างหน้าอย่างเด่นชัด)
    ctx.fillStyle = '#f59e0b';
    ctx.strokeStyle = '#ffffff';
    ctx.lineWidth = 2.5;
    ctx.beginPath();
    ctx.moveTo(s * 0.92, 0); // Pointing forward tip
    ctx.lineTo(s * 0.36, -s * 0.4);
    ctx.lineTo(s * 0.48, 0); // Inner chevron indent
    ctx.lineTo(s * 0.36, s * 0.4);
    ctx.closePath();
    ctx.fill();
    ctx.stroke();

    // 4. Dual High-Beam LED Headlights (ไฟหน้าคู่ LED สีขาวสว่างจ้า)
    ctx.fillStyle = '#ffffff';
    ctx.shadowColor = '#fef08a';
    ctx.shadowBlur = 6;
    ctx.beginPath();
    ctx.arc(s * 0.4, -s * 0.25, s * 0.09, 0, Math.PI * 2);
    ctx.arc(s * 0.4, s * 0.25, s * 0.09, 0, Math.PI * 2);
    ctx.fill();
    ctx.restore();
  }

  // Front-Edge Direction Badge (ป้ายลูกศรบอกทิศชัดเจน)
  drawFrontDirectionBadge(ctx, rx, ry, cellSize, centerX, centerY) {
    ctx.save();
    const pad = 10;
    let bx = centerX;
    let by = ry + pad;
    let arrowChar = '▲';

    if (this.robot.dir === 0) { // UP
      bx = centerX;
      by = ry + pad;
      arrowChar = '▲';
    } else if (this.robot.dir === 1) { // RIGHT
      bx = rx + cellSize - pad;
      by = centerY;
      arrowChar = '▶';
    } else if (this.robot.dir === 2) { // DOWN
      bx = centerX;
      by = ry + cellSize - pad;
      arrowChar = '▼';
    } else if (this.robot.dir === 3) { // LEFT
      bx = rx + pad;
      by = centerY;
      arrowChar = '◀';
    }

    // Badge circular backing
    const radius = Math.max(11, Math.floor(cellSize * 0.16));
    ctx.fillStyle = '#f59e0b';
    ctx.strokeStyle = '#ffffff';
    ctx.lineWidth = 2.5;
    ctx.shadowColor = 'rgba(0, 0, 0, 0.4)';
    ctx.shadowBlur = 4;
    ctx.beginPath();
    ctx.arc(bx, by, radius, 0, Math.PI * 2);
    ctx.fill();
    ctx.stroke();

    // Arrow icon inside badge
    ctx.shadowBlur = 0;
    ctx.fillStyle = '#ffffff';
    ctx.font = `900 ${Math.floor(radius * 1.35)}px system-ui, sans-serif`;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(arrowChar, bx, by + 0.5);

    ctx.restore();
  }

  // Canvas Compass HUD (ป้ายเข็มทิศบอกทิศทางบนกระดาน)
  drawCompassHUD(ctx, width) {
    ctx.save();
    const dirTexts = ['⬆️ หันขึ้น (เหนือ)', '➡️ หันขวา (ออก)', '⬇️ หันลง (ใต้)', '⬅️ หันซ้าย (ตก)'];
    const currentText = `🧭 ${dirTexts[this.robot.dir]} | 📍 (${this.robot.x}, ${this.robot.y})`;

    ctx.font = 'bold 12px system-ui, -apple-system, sans-serif';
    const textWidth = ctx.measureText ? ctx.measureText(currentText).width : 110;
    const pillW = textWidth + 18;
    const pillH = 22;
    const pillX = width - pillW - 8;
    const pillY = 6;

    // Draw pill badge background
    ctx.fillStyle = 'rgba(15, 23, 42, 0.75)';
    ctx.beginPath();
    if (ctx.roundRect) {
      ctx.roundRect(pillX, pillY, pillW, pillH, 11);
    } else {
      ctx.rect(pillX, pillY, pillW, pillH);
    }
    ctx.fill();
    ctx.strokeStyle = '#38bdf8';
    ctx.lineWidth = 1.5;
    ctx.stroke();

    // Draw text
    ctx.fillStyle = '#f8fafc';
    ctx.textAlign = 'left';
    ctx.textBaseline = 'middle';
    ctx.fillText(currentText, pillX + 9, pillY + pillH / 2);

    ctx.restore();
  }

  // Executes the next instruction step
  executeNextStep() {
    if (!this.isExecuting) return;
    if (this.currentStepIdx >= this.flattenedInstructions.length) {
      this.checkLevelOutcome();
      return;
    }

    const instr = this.flattenedInstructions[this.currentStepIdx];
    if (this.onStepChange) {
      this.onStepChange(instr.originalIndex, instr);
    }

    // Process instruction
    const action = instr.action;
    let failed = false;
    let failReason = "";

    if (action === 'FORWARD') {
      const dx = [0, 1, 0, -1][this.robot.dir];
      const dy = [-1, 0, 1, 0][this.robot.dir];
      const nextX = this.robot.x + dx;
      const nextY = this.robot.y + dy;

      // Boundary Check
      if (
        nextX < 0 || nextX >= this.currentLevel.gridSize.cols ||
        nextY < 0 || nextY >= this.currentLevel.gridSize.rows
      ) {
        failed = true;
        failReason = "หุ่นยนต์เดินออกนอกพื้นที่แผนที่!";
      }
      // Obstacle Check
      else if (this.currentLevel.obstacles.some(o => o.x === nextX && o.y === nextY)) {
        failed = true;
        failReason = "โค้ดบอทชนหินอวกาศ! ต้องหันหลบสิ่งกีดขวางนะ";
      }
      // Locked Door Check
      else if (this.items.some(it => it.type === 'laser_door' && it.x === nextX && it.y === nextY && !it.open)) {
        failed = true;
        failReason = "ประตูเลเซอร์ยังล็อคอยู่! ต้องใช้กุญแจเปิดประตูก่อน";
      } else {
        this.robot.x = nextX;
        this.robot.y = nextY;
        if (window.soundEngine) window.soundEngine.playStep();

        // Check if stepped on battery/key
        this.items.forEach(it => {
          if (it.x === this.robot.x && it.y === this.robot.y && !it.collected) {
            it.collected = true;
            if (it.type === 'key') this.hasKey = true;
            if (window.soundEngine) window.soundEngine.playItem();
          }
        });
      }
    } else if (action === 'TURN_LEFT') {
      this.robot.dir = (this.robot.dir + 3) % 4;
      if (window.soundEngine) window.soundEngine.playTurn();
    } else if (action === 'TURN_RIGHT') {
      this.robot.dir = (this.robot.dir + 1) % 4;
      if (window.soundEngine) window.soundEngine.playTurn();
    } else if (action === 'USE_KEY') {
      // Check if robot is adjacent or in front of laser door
      const door = this.items.find(it => it.type === 'laser_door');
      if (door && this.hasKey) {
        door.open = true;
        if (window.soundEngine) window.soundEngine.playItem();
      } else if (!this.hasKey) {
        failed = true;
        failReason = "ไม่มีกุญแจในกระเป๋า! ต้องไปเก็บกุญแจมาก่อนนะ";
      }
    }

    this.render();

    if (failed) {
      this.isExecuting = false;
      if (window.soundEngine) window.soundEngine.playError();
      if (this.onStatusMsg) this.onStatusMsg(`⚠️ ผิดพลาด: ${failReason}`, true);
      if (this.onFinish) {
        this.onFinish({
          success: false,
          errorReason: failReason,
          stepIndex: instr.originalIndex
        });
      }
      return;
    }

    // Progress to next step
    this.currentStepIdx++;
    if (this.currentStepIdx < this.flattenedInstructions.length) {
      this.stepTimeout = setTimeout(() => this.executeNextStep(), this.executionSpeed);
    } else {
      this.stepTimeout = setTimeout(() => this.checkLevelOutcome(), this.executionSpeed);
    }
  }

  // Unrolls loops into a flattened executable array
  prepareExecutionPlan() {
    this.flattenedInstructions = [];

    this.codeSequence.forEach((item, originalIndex) => {
      const action = item.action || item;

      // Check for customizable container loop
      if (item.type === 'loop' || action === 'LOOP_CUSTOM' || item.subActions) {
        let times = item.iterations || 5;
        if (action === 'LOOP_2') times = 2;
        else if (action === 'LOOP_3') times = 3;
        else if (action === 'LOOP_4') times = 4;
        else if (action === 'LOOP_5') times = 5;

        const subActions = (item.subActions && item.subActions.length > 0) ? item.subActions : ['FORWARD'];
        for (let t = 1; t <= times; t++) {
          subActions.forEach((subAct, subIdx) => {
            this.flattenedInstructions.push({
              action: subAct,
              originalIndex,
              isLoop: true,
              iteration: t,
              totalIterations: times,
              subIndex: subIdx,
              totalSubActions: subActions.length
            });
          });
        }
      } else if (action === 'LOOP_2') {
        this.flattenedInstructions.push({ action: 'FORWARD', originalIndex, isLoop: true, iteration: 1, totalIterations: 2 });
        this.flattenedInstructions.push({ action: 'FORWARD', originalIndex, isLoop: true, iteration: 2, totalIterations: 2 });
      } else if (action === 'LOOP_3') {
        this.flattenedInstructions.push({ action: 'FORWARD', originalIndex, isLoop: true, iteration: 1, totalIterations: 3 });
        this.flattenedInstructions.push({ action: 'FORWARD', originalIndex, isLoop: true, iteration: 2, totalIterations: 3 });
        this.flattenedInstructions.push({ action: 'FORWARD', originalIndex, isLoop: true, iteration: 3, totalIterations: 3 });
      } else if (action === 'LOOP_4') {
        this.flattenedInstructions.push({ action: 'FORWARD', originalIndex, isLoop: true, iteration: 1, totalIterations: 4 });
        this.flattenedInstructions.push({ action: 'FORWARD', originalIndex, isLoop: true, iteration: 2, totalIterations: 4 });
        this.flattenedInstructions.push({ action: 'FORWARD', originalIndex, isLoop: true, iteration: 3, totalIterations: 4 });
        this.flattenedInstructions.push({ action: 'FORWARD', originalIndex, isLoop: true, iteration: 4, totalIterations: 4 });
      } else if (action === 'LOOP_5') {
        for (let i = 1; i <= 5; i++) {
          this.flattenedInstructions.push({ action: 'FORWARD', originalIndex, isLoop: true, iteration: i, totalIterations: 5 });
        }
      } else {
        this.flattenedInstructions.push({ action, originalIndex });
      }
    });
  }

  runAll() {
    if (this.codeSequence.length === 0) {
      if (this.onStatusMsg) this.onStatusMsg("กรุณาใส่บล็อกคำสั่งก่อนกดเริ่มทำงาน!", true);
      return;
    }

    // If currently paused in step-by-step mode, smoothly resume auto execution!
    if (this.isStepMode && this.currentStepIdx >= 0 && this.currentStepIdx < this.flattenedInstructions.length) {
      this.isExecuting = true;
      this.isStepMode = false;
      if (this.onStatusMsg) this.onStatusMsg("▶️ รันโค้ดต่อเนื่องอัตโนมัติ...", false);
      this.executeNextStep();
      return;
    }

    this.resetSimulation();
    this.prepareExecutionPlan();
    this.isExecuting = true;
    this.isStepMode = false;
    this.currentStepIdx = 0;

    if (this.onStatusMsg) this.onStatusMsg("กำลังรันโปรแกรมตามอัลกอริทึม...", false);
    this.executeNextStep();
  }

  // Executes exactly one single step (Step-by-Step Debug Mode)
  executeSingleStep() {
    if (this.codeSequence.length === 0) {
      if (this.onStatusMsg) this.onStatusMsg("กรุณาใส่บล็อกคำสั่งก่อนกดเดินทีละก้าว!", true);
      return;
    }

    // Cancel any automatic execution timer
    if (this.stepTimeout) {
      clearTimeout(this.stepTimeout);
      this.stepTimeout = null;
    }

    // If starting a fresh step session
    if (!this.isExecuting && !this.isStepMode) {
      this.resetSimulation();
      this.prepareExecutionPlan();
      this.isExecuting = true;
      this.isStepMode = true;
      this.currentStepIdx = 0;
    } else {
      this.isExecuting = true;
      this.isStepMode = true;
    }

    if (this.currentStepIdx >= this.flattenedInstructions.length) {
      this.isStepMode = false;
      this.checkLevelOutcome();
      return;
    }

    const instr = this.flattenedInstructions[this.currentStepIdx];
    if (this.onStepChange) {
      this.onStepChange(instr.originalIndex, instr);
    }

    // Process single instruction
    const action = instr.action;
    let failed = false;
    let failReason = "";

    if (action === 'FORWARD') {
      const dx = [0, 1, 0, -1][this.robot.dir];
      const dy = [-1, 0, 1, 0][this.robot.dir];
      const nextX = this.robot.x + dx;
      const nextY = this.robot.y + dy;

      if (
        nextX < 0 || nextX >= this.currentLevel.gridSize.cols ||
        nextY < 0 || nextY >= this.currentLevel.gridSize.rows
      ) {
        failed = true;
        failReason = "หุ่นยนต์เดินออกนอกพื้นที่แผนที่!";
      } else if (this.currentLevel.obstacles.some(o => o.x === nextX && o.y === nextY)) {
        failed = true;
        failReason = "โค้ดบอทชนหินอวกาศ! ต้องหันหลบสิ่งกีดขวางนะ";
      } else if (this.items.some(it => it.type === 'laser_door' && it.x === nextX && it.y === nextY && !it.open)) {
        failed = true;
        failReason = "ประตูเลเซอร์ยังล็อคอยู่! ต้องใช้กุญแจเปิดประตูก่อน";
      } else {
        this.robot.x = nextX;
        this.robot.y = nextY;
        if (window.soundEngine) window.soundEngine.playStep();

        this.items.forEach(it => {
          if (it.x === this.robot.x && it.y === this.robot.y && !it.collected) {
            it.collected = true;
            if (it.type === 'key') this.hasKey = true;
            if (window.soundEngine) window.soundEngine.playItem();
          }
        });
      }
    } else if (action === 'TURN_LEFT') {
      this.robot.dir = (this.robot.dir + 3) % 4;
      if (window.soundEngine) window.soundEngine.playTurn();
    } else if (action === 'TURN_RIGHT') {
      this.robot.dir = (this.robot.dir + 1) % 4;
      if (window.soundEngine) window.soundEngine.playTurn();
    } else if (action === 'USE_KEY') {
      const door = this.items.find(it => it.type === 'laser_door');
      if (door && this.hasKey) {
        door.open = true;
        if (window.soundEngine) window.soundEngine.playItem();
      } else if (!this.hasKey) {
        failed = true;
        failReason = "ไม่มีกุญแจในกระเป๋า! ต้องไปเก็บกุญแจมาก่อนนะ";
      }
    }

    this.render();

    if (failed) {
      this.isExecuting = false;
      this.isStepMode = false;
      if (window.soundEngine) window.soundEngine.playError();
      if (this.onStatusMsg) this.onStatusMsg(`⚠️ ผิดพลาด: ${failReason}`, true);
      if (this.onFinish) {
        this.onFinish({
          success: false,
          errorReason: failReason,
          stepIndex: instr.originalIndex
        });
      }
      return;
    }

    this.currentStepIdx++;
    const totalSteps = this.flattenedInstructions.length;
    if (this.onStatusMsg) {
      const meta = window.BLOCK_CATALOG[action] || { shortLabel: action };
      this.onStatusMsg(`👣 ก้าวที่ ${this.currentStepIdx}/${totalSteps}: [${meta.shortLabel}] พิกัด (${this.robot.x}, ${this.robot.y})`, false);
    }

    if (this.currentStepIdx >= totalSteps) {
      this.isExecuting = false;
      this.isStepMode = false;
      this.checkLevelOutcome();
    } else {
      // Pause execution and wait for next click or resume
      this.isExecuting = false;
    }
  }

  checkLevelOutcome() {
    this.isExecuting = false;

    // Check if goal reached
    const reachedGoal = (this.robot.x === this.currentLevel.goal.x && this.robot.y === this.currentLevel.goal.y);

    // Check if all necessary batteries/items were collected
    const allBatteriesCollected = this.items.filter(it => it.type === 'battery').every(it => it.collected);

    if (reachedGoal && allBatteriesCollected) {
      // Calculate Stars (1-3 stars)
      // Star 1: Completed Goal
      // Star 2: Code Efficiency (<= maxBlocksForStar)
      // Star 3: Optimal / Bonus
      let stars = 1;
      const codeLength = this.codeSequence.length;

      if (codeLength <= this.currentLevel.maxBlocksForStar) {
        stars = 3;
      } else if (codeLength <= this.currentLevel.maxBlocksForStar + 2) {
        stars = 2;
      }

      if (window.soundEngine) window.soundEngine.playVictory();
      if (this.onStatusMsg) this.onStatusMsg("🎉 ภารกิจสำเร็จ! โค้ดบอทกลับถึงยานแม่แล้ว", false);

      if (this.onFinish) {
        this.onFinish({
          success: true,
          stars,
          codeBlocksUsed: codeLength,
          maxAllowedForBonus: this.currentLevel.maxBlocksForStar
        });
      }
    } else if (!reachedGoal) {
      if (window.soundEngine) window.soundEngine.playError();
      const msg = "หุ่นยนต์หยุดเดิน แต่ยังไปไม่ถึงยานอวกาศ! ลองเพิ่มหรือแก้ไขคำสั่งดูนะ";
      if (this.onStatusMsg) this.onStatusMsg(`⚠️ ${msg}`, true);
      if (this.onFinish) {
        this.onFinish({ success: false, errorReason: msg });
      }
    } else if (!allBatteriesCollected) {
      if (window.soundEngine) window.soundEngine.playError();
      const msg = "ถึงยานแล้ว แต่ยังเก็บพลังงานแบตเตอรี่ไม่ครบ!";
      if (this.onStatusMsg) this.onStatusMsg(`⚠️ ${msg}`, true);
      if (this.onFinish) {
        this.onFinish({ success: false, errorReason: msg });
      }
    }
  }
}

window.GameEngine = GameEngine;
