/**
 * CodeBot AR Camera Engine - Powered by Google MediaPipe Hands (100% Offline)
 * Developed for CodeBot AR Adventure - วิชาวิทยาการคำนวณ ป.4-ป.5
 * ผู้พัฒนา: นายเตชินท์ อินทมล ตำแหน่ง ครู โรงเรียนบ้านโนนป่าหว้านเชียงฮาย
 *
 * 🤖 ขับเคลื่อนด้วยโมเดล Deep Learning จาก Google MediaPipe Hands:
 * - ทำงานแบบ Offline 100% จากไดเรกทอรี vendor/mediapipe/ ไม่ต้องต่อเน็ต
 * - ตรวจจับข้อต่อนิ้วมือ 21 จุด แยก "มือซ้าย" และ "มือขวา" ของนักเรียนจริง 100%
 *
 * 🌟 กฎการควบคุมแบบใหม่ (จำง่ายและเป็นธรรมชาติที่สุดสำหรับเด็ก ป.4-ป.5):
 * - ☝️ 1 นิ้ว (มือใดก็ได้) = เดินหน้า (FORWARD)
 * - ✋ / ✌️ ยกมือซ้าย (แบมือ หรือ ชู 2 นิ้วมือซ้าย) = หันซ้าย (TURN_LEFT)
 * - ✋ / ✌️ ยกมือขวา (แบมือ หรือ ชู 2 นิ้วมือขวา) = หันขวา (TURN_RIGHT)
 * - 🤟 3 นิ้ว (มือใดก็ได้) = วนลูป (LOOP) หรือ ไขกุญแจ (USE_KEY)
 * - 🫰 มินิฮาร์ท = รันโค้ดโปรแกรม (RUN_CODE)
 * - 🙅 กากบาท (สองแขนไขว้) = รีเซ็ตและล้างคำสั่งทั้งหมด (RESET_CODE)
 * - 👎 คว่ำมือ/นิ้วโป้งลง = ลบคำสั่งล่าสุด (UNDO)
 * - ✊ กำมือ / วางมือ = สถานะพัก (IDLE) ปลอดภัย 100%
 */

class CameraEngine {
  constructor(canvasId, videoId) {
    this.canvas = document.getElementById(canvasId);
    this.ctx = this.canvas ? this.canvas.getContext('2d') : null;
    this.video = document.getElementById(videoId);
    this.stream = null;
    this.isRunning = false;
    this.isDetectionEnabled = true;

    // MediaPipe Hands & AI state
    this.hands = null;
    this.isHandsReady = false;
    this.isSendingFrame = false;
    this.aiStatusText = 'กำลังเตรียมระบบ AI...';
    this.aiError = null;
    this.allHandsLandmarks = [];
    this.allHandedness = [];
    this.lastLandmarks = null;
    this.primaryHandSide = null; // 'LEFT' or 'RIGHT'
    this.handCenter = { x: 320, y: 240 };
    this.fingersCount = 0;

    // Gesture State Machine
    this.currentGesture = null;
    this.gestureHoldTime = 0;
    this.gestureTriggerThreshold = 1000; // 1.0s hold time
    this.cooldownUntil = 0;
    this.lastTriggeredGesture = null;
    this.lastTriggerAnimUntil = 0;

    // Mini Heart (🫰 RUN_CODE)
    this.runHoldTime = 0;
    this.runTriggerThreshold = 1500; // 1.5s hold time
    this.runCooldownUntil = 0;
    this.runAnimUntil = 0;
    this.isMiniHeartActive = false;
    this.lastMiniHeartDetectedTime = 0;
    this.onRunTrigger = null;

    // Cross Gesture (🙅 RESET_CODE)
    this.resetHoldTime = 0;
    this.resetTriggerThreshold = 1500; // 1.5s deliberate hold time to prevent accidental reset
    this.resetCooldownUntil = 0;
    this.resetAnimUntil = 0;
    this.crossPoint = null;
    this.isCrossActive = false;
    this.lastCrossDetectedTime = 0;
    this.onResetTrigger = null;

    // Undo State (👎 UNDO)
    this.undoHoldTime = 0;
    this.undoTriggerThreshold = 1000; // 1.0s hold time
    this.undoCooldownUntil = 0;
    this.undoPoint = null;
    this.onUndoTrigger = null;

    // Hands-Free Loop Recording Mode State
    this.isLoopRecordingMode = false;
    this.awaitingLoopIteration = false;
    this.loopIterHoldTime = 0;
    this.loopIterTarget = null;
    this.onStartLoopRecording = null;
    this.onFinishLoopRecording = null;
    this.onSelectLoopIteration = null;

    // Smoothing history
    this.fingerHistory = [];
    this.lastFrameTime = performance.now();

    // Available blocks & callbacks
    this.availableBlockIds = ['FORWARD', 'TURN_LEFT', 'TURN_RIGHT'];
    this.onZoneTrigger = null;

    // DOM indicators
    this.liveTextEl = document.getElementById('live-gesture-text');
    this.liveDotEl = document.getElementById('live-pulse-dot');
  }

  setAvailableBlocks(blockIds) {
    this.availableBlockIds = blockIds || ['FORWARD', 'TURN_LEFT', 'TURN_RIGHT'];
  }

  async startCamera() {
    if (this.isRunning) return true;

    // 1. Check protocol
    if (window.location.protocol === 'file:') {
      this.aiError = 'กรุณาเปิดผ่าน http://localhost:8000 (ห้ามเปิดผ่าน file://)';
      console.warn('MediaPipe Hands requires HTTP/HTTPS server due to browser WebAssembly restrictions.');
    }

    // 2. Start Video Stream First (Instant video feed with mobile camera support)
    try {
      this.stream = await navigator.mediaDevices.getUserMedia({
        video: { width: { ideal: 640 }, height: { ideal: 480 }, facingMode: 'user' },
        audio: false
      });

      // Mobile Safari / Chrome explicit inline attributes
      this.video.setAttribute('playsinline', '');
      this.video.setAttribute('webkit-playsinline', '');
      this.video.playsInline = true;
      this.video.muted = true;
      this.video.autoplay = true;
      this.video.srcObject = this.stream;

      // Ensure video dimensions are available before playing (especially on mobile)
      if (this.video.readyState < 1 || !this.video.videoWidth) {
        await new Promise((resolve) => {
          const onMeta = () => {
            this.video.removeEventListener('loadedmetadata', onMeta);
            resolve();
          };
          this.video.addEventListener('loadedmetadata', onMeta);
          setTimeout(resolve, 600);
        });
      }

      try {
        await this.video.play();
      } catch (playErr) {
        console.warn('Webcam play() notice:', playErr);
      }

      this.canvas.width = this.video.videoWidth || 640;
      this.canvas.height = this.video.videoHeight || 480;
      this.isRunning = true;
      this.lastFrameTime = performance.now();

      const ind = document.getElementById('camera-status');
      if (ind) { ind.classList.remove('off'); ind.title = 'กล้องพร้อมทำงาน'; }

      // 3. Start Animation Loop Immediately
      this.processLoop();
    } catch (err) {
      console.warn('Webcam error:', err);
      const ind = document.getElementById('camera-status');
      if (ind) ind.classList.add('off');
      this.renderFallbackMode('ไม่พบกล้อง หรือยังไม่ได้อนุญาตการใช้กล้อง');
      return false;
    }

    // 4. Initialize MediaPipe Hands in Background
    this.initMediaPipeHands();

    return true;
  }

  async initMediaPipeHands() {
    if (!window.Hands) {
      this.aiError = 'ไม่พบโมเดล AI MediaPipe (Hands.js)';
      this.aiStatusText = 'ไม่พบไลบรารี AI';
      return;
    }

    try {
      this.aiStatusText = 'กำลังโหลดโมเดล AI...';
      this.hands = new window.Hands({
        locateFile: (file) => `vendor/mediapipe/${file}`
      });

      this.hands.setOptions({
        maxNumHands: 2, // Support up to 2 hands simultaneously
        modelComplexity: 0, // Lite model (2MB) for ultra-fast load and smooth 60 FPS
        minDetectionConfidence: 0.5,
        minTrackingConfidence: 0.5
      });

      this.hands.onResults((results) => {
        this.onHandResults(results);
      });

      // Await actual WebAssembly & model asset compilation
      await this.hands.initialize();
      this.isHandsReady = true;
      this.aiStatusText = 'AI พร้อมตรวจจับ ✅';
      console.log('MediaPipe Hands Initialized Successfully!');
    } catch (e) {
      console.warn('Failed to init MediaPipe Hands:', e);
      this.aiError = 'โหลด AI ไม่สำเร็จ: ' + (e.message || e);
      this.aiStatusText = 'เกิดข้อผิดพลาดในการโหลด AI';
    }
  }

  stopCamera() {
    if (this.stream) {
      this.stream.getTracks().forEach(t => t.stop());
      this.stream = null;
    }
    this.isRunning = false;
    this.isHandsReady = false;
  }

  // =========================================================================
  // Determine Physical Hand Side (Left or Right of the Student)
  // =========================================================================
  getStudentHandSide(lm, handedness) {
    if (handedness && handedness.label) {
      if (handedness.score > 0.7) {
        // MediaPipe raw perspective: 'Right' label corresponds to student's physical Left hand
        return handedness.label === 'Right' ? 'LEFT' : 'RIGHT';
      }
    }
    // Fallback: 2D cross product of hand orientation
    // Vector V1 = MCP_index(5) - Wrist(0), Vector V2 = MCP_pinky(17) - Wrist(0)
    const vIndex = { x: lm[5].x - lm[0].x, y: lm[5].y - lm[0].y };
    const vPinky = { x: lm[17].x - lm[0].x, y: lm[17].y - lm[0].y };
    const crossZ = vIndex.x * vPinky.y - vIndex.y * vPinky.x;
    const isPalmFacing = crossZ > 0;

    // Physical Left hand facing camera: thumb (4) x is smaller than pinky (17) x in raw image
    return (isPalmFacing ? (lm[4].x < lm[17].x) : (lm[4].x > lm[17].x)) ? 'LEFT' : 'RIGHT';
  }

  // Count extended fingers for a single hand landmarks array
  countHandExtendedFingers(lm) {
    if (!lm || lm.length < 21) return 0;
    const p0 = lm[0];
    const dist0 = (idx) => Math.hypot(lm[idx].x - p0.x, lm[idx].y - p0.y);
    const isIndexExt  = dist0(8)  > dist0(6)  * 1.05;
    const isMiddleExt = dist0(12) > dist0(10) * 1.05;
    const isRingExt   = dist0(16) > dist0(14) * 1.05;
    const isPinkyExt  = dist0(20) > dist0(18) * 1.05;

    const palmScale = Math.hypot(lm[9].x - p0.x, lm[9].y - p0.y);
    const pScale = Math.max(0.06, palmScale);
    const palmCenter = { x: (p0.x + lm[9].x) / 2, y: (p0.y + lm[9].y) / 2 };
    const dThumbPalmCenter = Math.hypot(lm[4].x - palmCenter.x, lm[4].y - palmCenter.y);
    const dThumbMiddleMcp = Math.hypot(lm[4].x - lm[9].x, lm[4].y - lm[9].y);
    const dThumbIndexMcp = Math.hypot(lm[4].x - lm[5].x, lm[4].y - lm[5].y);
    const isThumbFolded = (dThumbPalmCenter < pScale * 0.40) || (dThumbMiddleMcp < pScale * 0.46 && dThumbIndexMcp < pScale * 0.38);
    const isThumbExt = !isThumbFolded && dThumbPalmCenter > pScale * 0.45;

    return (isIndexExt ? 1 : 0) + (isMiddleExt ? 1 : 0) + (isRingExt ? 1 : 0) + (isPinkyExt ? 1 : 0) + (isThumbExt ? 1 : 0);
  }

  // =========================================================================
  // Main Animation Loop (Runs decoupled at 60 FPS)
  // =========================================================================
  processLoop() {
    if (!this.isRunning) return;

    // Dynamically sync canvas size with camera stream (handles mobile orientation change)
    if (this.video && this.video.videoWidth > 0) {
      if (this.canvas.width !== this.video.videoWidth || this.canvas.height !== this.video.videoHeight) {
        this.canvas.width = this.video.videoWidth;
        this.canvas.height = this.video.videoHeight;
      }
    }

    const width = this.canvas.width;
    const height = this.canvas.height;
    const now = performance.now();
    const deltaTime = Math.min(80, now - this.lastFrameTime);
    this.lastFrameTime = now;

    // 1. ALWAYS Draw Mirrored Video Frame (Zero freezing, zero black screen)
    if (this.ctx && this.video && this.video.readyState >= 2) {
      this.ctx.save();
      this.ctx.scale(-1, 1);
      this.ctx.drawImage(this.video, -width, 0, width, height);
      this.ctx.restore();
    }

    // 2. Draw Hand Skeletons & Joints for all detected hands
    if (this.allHandsLandmarks && this.allHandsLandmarks.length > 0) {
      for (let i = 0; i < this.allHandsLandmarks.length; i++) {
        const lm = this.allHandsLandmarks[i];
        const handedness = this.allHandedness ? this.allHandedness[i] : null;
        const side = this.getStudentHandSide(lm, handedness);
        this.drawHandSkeleton(lm, width, height, side);
      }
      this.analyzeAllHandsGestures(this.allHandsLandmarks, this.allHandedness, width, height, deltaTime);
    } else {
      this.lastLandmarks = null;
      this.primaryHandSide = null;
      this.fingersCount = 0;
      this.decayAllHoldTimes(deltaTime);
      if (this.isHandsReady) {
        this.updateLiveFeedback(null, 0);
      }
    }

    // 3. Render AR Visual Overlay (Charging Rings, Confirmation Banners, Status HUD)
    this.renderAROverlay(width, height);

    // 4. Send Frame to MediaPipe AI (Asynchronous, non-blocking)
    if (this.isDetectionEnabled && this.isHandsReady && this.hands && this.video && this.video.readyState >= 2 && !this.isSendingFrame) {
      this.isSendingFrame = true;
      this.hands.send({ image: this.video })
        .then(() => { this.isSendingFrame = false; })
        .catch(() => {
          this.isSendingFrame = false;
        });
    }

    requestAnimationFrame(() => this.processLoop());
  }

  // =========================================================================
  // MediaPipe Results Callback
  // =========================================================================
  onHandResults(results) {
    if (results.multiHandLandmarks && results.multiHandLandmarks.length > 0) {
      this.allHandsLandmarks = results.multiHandLandmarks;
      this.allHandedness = results.multiHandedness || [];
      this.lastLandmarks = results.multiHandLandmarks[0];
      const h0 = this.allHandedness.length > 0 ? this.allHandedness[0] : null;
      this.primaryHandSide = this.getStudentHandSide(this.lastLandmarks, h0);
    } else {
      this.allHandsLandmarks = [];
      this.allHandedness = [];
      this.lastLandmarks = null;
      this.primaryHandSide = null;
      this.fingersCount = 0;
    }
  }

  // =========================================================================
  // Comprehensive Gesture Analysis with Left / Right Hand Separation
  // =========================================================================
  analyzeAllHandsGestures(allHands, allHandedness, width, height, deltaTime) {
    const now = Date.now();

    // -----------------------------------------------------------------------
    // PRIORITY 1: Cross Gesture (🙅 สองแขนไขว้กากบาทชัดเจน) = รีเซ็ตโค้ดใหม่
    // -----------------------------------------------------------------------
    let isCross = false;
    let crossPt = null;

    // A single hand MUST NEVER trigger Reset/Clear!
    if (allHands.length >= 2) {
      const lm0 = allHands[0], lm1 = allHands[1];
      const p0 = lm0[9], p1 = lm1[9]; // Palm centers
      const w0 = lm0[0], w1 = lm1[0]; // Wrists

      // 1. True physical arm crossing: wrists cross over the opposite palm axis
      const isArmCross = (w0.x - w1.x) * (p0.x - p1.x) < -0.04;
      const dPalms = Math.hypot(p0.x - p1.x, p0.y - p1.y);

      // 2. Both hands showing 10 fingers (5 + 5 fingers)
      const count0 = this.countHandExtendedFingers(lm0);
      const count1 = this.countHandExtendedFingers(lm1);
      const isTenFingers = (count0 + count1 >= 9); // Tolerant 9-10 fingers

      // Trigger if either arms cross OR 10 fingers are shown with 2 hands
      if ((isArmCross && dPalms < 0.35) || isTenFingers) {
        isCross = true;
        this.fingersCount = 10;
        crossPt = { x: (1 - (p0.x + p1.x) / 2) * width, y: ((p0.y + p1.y) / 2) * height };
      }
    }

    if (isCross) {
      this.lastCrossDetectedTime = now;
      this.fingersCount = 10;
    }
    // Tolerate tracking flicker up to 250ms
    const isRecentlyCross = isCross || (now - (this.lastCrossDetectedTime || 0) < 250 && this.resetHoldTime > 100);

    if (isRecentlyCross && now >= this.resetCooldownUntil) {
      this.isCrossActive = true;
      this.fingersCount = 10;
      if (crossPt) this.crossPoint = crossPt;
      this.resetHoldTime += deltaTime;
      const ratio = Math.min(1.0, this.resetHoldTime / this.resetTriggerThreshold);
      this.updateLiveFeedback('RESET', ratio);
      this.decayOtherHoldTimes('RESET', deltaTime);

      if (this.resetHoldTime >= this.resetTriggerThreshold) {
        this.triggerResetCode();
      }
      return;
    } else {
      this.isCrossActive = false;
      this.resetHoldTime = Math.max(0, this.resetHoldTime - deltaTime * 1.5);
      if (this.resetHoldTime === 0) this.crossPoint = null;
    }

    // -----------------------------------------------------------------------
    // PRIORITY 2: Mini Heart (🫰 มินิฮาร์ท) = รันโค้ดโปรแกรม
    // -----------------------------------------------------------------------
    const primaryHand = allHands[0];
    const h0 = allHandedness && allHandedness.length > 0 ? allHandedness[0] : null;
    const side = this.getStudentHandSide(primaryHand, h0);
    this.primaryHandSide = side;

    const palmX = (1 - primaryHand[9].x) * width;
    const palmY = primaryHand[9].y * height;
    this.handCenter = { x: palmX, y: palmY };

    // Thumb tip (4) touches Index near tip (8) or joint (7)
    const dThumbIndex = Math.hypot(primaryHand[4].x - primaryHand[8].x, primaryHand[4].y - primaryHand[8].y);
    const dThumbJoint = Math.hypot(primaryHand[4].x - primaryHand[7].x, primaryHand[4].y - primaryHand[7].y);
    const isThumbCrossingIndex = (dThumbIndex < 0.10 || dThumbJoint < 0.10);

    const mhMiddleFolded = primaryHand[12].y > primaryHand[10].y - 0.02;
    const mhRingFolded   = primaryHand[16].y > primaryHand[14].y - 0.02;
    const mhPinkyFolded  = primaryHand[20].y > primaryHand[18].y - 0.02;
    const isThumbUp      = primaryHand[4].y < primaryHand[2].y;

    const isMiniHeart = isThumbCrossingIndex && mhMiddleFolded && mhRingFolded && mhPinkyFolded && isThumbUp;

    if (isMiniHeart) {
      this.lastMiniHeartDetectedTime = now;
    }
    const isRecentlyMiniHeart = isMiniHeart || (now - (this.lastMiniHeartDetectedTime || 0) < 200 && this.runHoldTime > 100);

    if (isRecentlyMiniHeart && now >= this.runCooldownUntil) {
      this.isMiniHeartActive = true;
      this.runHoldTime += deltaTime;
      const ratio = Math.min(1.0, this.runHoldTime / this.runTriggerThreshold);
      this.updateLiveFeedback('RUN', ratio);
      this.decayOtherHoldTimes('RUN', deltaTime);

      if (this.runHoldTime >= this.runTriggerThreshold) {
        this.triggerRunCode();
      }
      return;
    } else {
      this.isMiniHeartActive = false;
      this.runHoldTime = Math.max(0, this.runHoldTime - deltaTime * 1.5);
    }

    // -----------------------------------------------------------------------
    // PRIORITY 3: Undo Gesture (👎 คว่ำมือ / นิ้วโป้งลงอย่างจงใจ) = ลบคำสั่งล่าสุด
    // -----------------------------------------------------------------------
    const palmScale = Math.hypot(primaryHand[9].x - primaryHand[0].x, primaryHand[9].y - primaryHand[0].y);
    const pScale = Math.max(0.06, palmScale);

    // Distance from wrist (0)
    const p0 = primaryHand[0];
    const dist0 = (idx) => Math.hypot(primaryHand[idx].x - p0.x, primaryHand[idx].y - p0.y);

    // Finger is extended if tip is distinctly farther from wrist than PIP
    // Highly reliable across small children and adults
    const isIndexExt  = dist0(8)  > dist0(6)  * 1.05;
    const isMiddleExt = dist0(12) > dist0(10) * 1.05;
    const isRingExt   = dist0(16) > dist0(14) * 1.05;
    const isPinkyExt  = dist0(20) > dist0(18) * 1.05;

    // Geometric palm center (midpoint of wrist 0 and middle knuckle 9)
    const palmCenter = {
      x: (p0.x + primaryHand[9].x) / 2,
      y: (p0.y + primaryHand[9].y) / 2
    };
    const dThumbPalmCenter = Math.hypot(primaryHand[4].x - palmCenter.x, primaryHand[4].y - palmCenter.y);
    const dThumbMcp = Math.hypot(primaryHand[4].x - primaryHand[2].x, primaryHand[4].y - primaryHand[2].y);
    const dThumbIndexMcp = Math.hypot(primaryHand[4].x - primaryHand[5].x, primaryHand[4].y - primaryHand[5].y);
    const dThumbMiddleMcp = Math.hypot(primaryHand[4].x - primaryHand[9].x, primaryHand[4].y - primaryHand[9].y);

    // Thumb is folded across palm (e.g. 4-finger gesture: tip 4 is nestled against palm center/base)
    const isThumbFoldedAcrossPalm = (dThumbPalmCenter < pScale * 0.40) ||
                                   (dThumbMiddleMcp < pScale * 0.46 && dThumbIndexMcp < pScale * 0.38);

    // Thumb extension: tip (4) is clearly extended outward away from the palm and fingers
    const isThumbExt = !isThumbFoldedAcrossPalm &&
      ((dThumbMcp > pScale * 0.38 && dThumbIndexMcp > pScale * 0.32 && dThumbPalmCenter > pScale * 0.45) ||
       (dThumbMiddleMcp > pScale * 0.55 && dThumbPalmCenter > pScale * 0.48));

    // Folded finger checks
    const isIndexFolded  = dist0(8)  <= dist0(6)  * 1.02 || primaryHand[8].y  > primaryHand[6].y;
    const isMiddleFolded = dist0(12) <= dist0(10) * 1.02 || primaryHand[12].y > primaryHand[10].y;
    const isRingFolded   = dist0(16) <= dist0(14) * 1.02 || primaryHand[16].y > primaryHand[14].y;
    const isPinkyFolded  = dist0(20) <= dist0(18) * 1.02 || primaryHand[20].y > primaryHand[18].y;

    const isThumbDown = primaryHand[4].y > primaryHand[3].y + (pScale * 0.15)
      && primaryHand[4].y > primaryHand[0].y;
    const isAllOtherFolded = !isIndexExt && isMiddleFolded && isRingFolded && isPinkyFolded;

    if (isThumbDown && isAllOtherFolded && now >= this.undoCooldownUntil) {
      this.undoPoint = { x: (1 - primaryHand[4].x) * width, y: primaryHand[4].y * height };
      this.undoHoldTime += deltaTime;
      const ratio = Math.min(1.0, this.undoHoldTime / this.undoTriggerThreshold);
      this.updateLiveFeedback('UNDO', ratio);
      this.decayOtherHoldTimes('UNDO', deltaTime);

      if (this.undoHoldTime >= this.undoTriggerThreshold) {
        this.triggerUndo();
      }
      return;
    } else {
      this.undoHoldTime = Math.max(0, this.undoHoldTime - deltaTime * 2.0);
      this.undoPoint = null;
    }

    // -----------------------------------------------------------------------
    // PRIORITY 4: Left/Right Hand + Finger Counting Commands
    // -----------------------------------------------------------------------
    const rawExtCount = (isIndexExt ? 1 : 0) + (isMiddleExt ? 1 : 0) + (isRingExt ? 1 : 0) + (isPinkyExt ? 1 : 0) + (isThumbExt ? 1 : 0);

    // Explicit 3-finger patterns (Child & Adult friendly)
    // 1. Scout 3: ชี้, กลาง, นาง (นิ้วก้อยพับ)
    const isScout3 = isIndexExt && isMiddleExt && isRingExt && isPinkyFolded;
    // 2. Scout 3 touching: นิ้วโป้งแตะ/จับนิ้วก้อยไว้ในฝ่ามือ
    const dThumbPinky = Math.hypot(primaryHand[4].x - primaryHand[20].x, primaryHand[4].y - primaryHand[20].y);
    const isScoutTouch = isIndexExt && isMiddleExt && isRingExt && (dThumbPinky < pScale * 0.40);
    // 3. Asian 3 / นับเลขไทย 3: นิ้วโป้ง, ชี้, กลาง
    const isAsian3 = isThumbExt && isIndexExt && isMiddleExt && isRingFolded && isPinkyFolded;
    // 4. I Love You / Rock 3: นิ้วโป้ง, ชี้, ก้อย (🤟)
    const isLove3  = isThumbExt && isIndexExt && isPinkyExt && isMiddleFolded && isRingFolded;
    // 5. นับนิ้วเหยียดรวมได้ 3 นิ้วพอดี
    const isAny3   = (rawExtCount === 3);

    // Explicit 4-finger pattern: ชี้, กลาง, นาง, ก้อย (นิ้วโป้งพับเก็บในฝ่ามือ)
    const is4Fingers = isIndexExt && isMiddleExt && isRingExt && isPinkyExt && (!isThumbExt || isThumbFoldedAcrossPalm);

    let count = 0;
    if (is4Fingers) {
      count = 4; // ชู 4 นิ้วชัดเจน 100% (ชี้ กลาง นาง ก้อย + พับนิ้วโป้งในฝ่ามือ)
    } else if (isIndexExt && isMiddleExt && isRingExt && isPinkyExt && isThumbExt) {
      count = 5; // แบมือครบ 5 นิ้ว (กางนิ้วโป้งออกด้วย)
    } else if (isScout3 || isScoutTouch || isAsian3 || isLove3 || isAny3) {
      count = 3; // รูปแบบ 3 นิ้วทุกประเภท
    } else if (isIndexExt && isMiddleFolded && isRingFolded && isPinkyFolded && !isThumbExt) {
      count = 1; // 1 นิ้ว (เดินหน้า)
    } else if (isIndexExt && isMiddleExt && isRingFolded && isPinkyFolded && !isThumbExt) {
      count = 2; // 2 นิ้ว
    } else if (!isIndexExt && !isMiddleExt && !isRingExt && !isPinkyExt) {
      count = 0; // กำมือ (Fist)
    } else {
      count = rawExtCount;
    }

    this.processCommandRules(count, side, deltaTime);
  }

  processCommandRules(fingers, side, deltaTime) {
    // 3-frame majority smoothing
    this.fingerHistory.push(fingers);
    if (this.fingerHistory.length > 3) this.fingerHistory.shift();

    const counts = {};
    let stableFingers = fingers, maxFreq = 0;
    for (const f of this.fingerHistory) {
      counts[f] = (counts[f] || 0) + 1;
      if (counts[f] > maxFreq) { maxFreq = counts[f]; stableFingers = f; }
    }
    this.fingersCount = stableFingers;

    // -----------------------------------------------------------------------
    // HANDS-FREE LOOP RECORDING MODE & ITERATION SELECTION
    // -----------------------------------------------------------------------
    if (this.awaitingLoopIteration) {
      if (stableFingers >= 2 && stableFingers <= 5) {
        if (this.loopIterTarget === stableFingers) {
          this.loopIterHoldTime += deltaTime;
          if (this.loopIterHoldTime >= 1000) { // 1.0s hold
            const chosen = this.loopIterTarget;
            this.awaitingLoopIteration = false;
            this.loopIterHoldTime = 0;
            this.loopIterTarget = null;
            this.cooldownUntil = Date.now() + 1200;
            if (this.onSelectLoopIteration) this.onSelectLoopIteration(chosen);
          }
        } else {
          this.loopIterTarget = stableFingers;
          this.loopIterHoldTime = 0;
        }
      } else {
        this.loopIterHoldTime = Math.max(0, this.loopIterHoldTime - deltaTime * 1.5);
      }
      return;
    }

    let targetGesture = null;

    // RULE 1: 1 Finger (any hand) = เดินหน้า (FORWARD)
    if (stableFingers === 1) {
      targetGesture = 'FORWARD';
    }
    // RULE 2: 3 Fingers (any hand) = เปิด/ปิดโหมดบันทึกลูป หรือ ไขกุญแจ (ทำงานได้ทุกด่าน 100%)
    else if (stableFingers === 3) {
      if (this.isLoopRecordingMode) {
        targetGesture = 'FINISH_LOOP';
      } else if (this.availableBlockIds.includes('USE_KEY') && !this.availableBlockIds.some(id => id.startsWith('LOOP') || id === 'LOOP_CUSTOM')) {
        targetGesture = 'USE_KEY';
      } else {
        targetGesture = 'START_LOOP';
      }
    }
    // RULE 3: ยกมือซ้าย (แบมือ 5 นิ้ว) = หันซ้าย (TURN_LEFT)
    else if (side === 'LEFT' && stableFingers === 5) {
      targetGesture = 'TURN_LEFT';
    }
    // RULE 4: ยกมือขวา (แบมือ 5 นิ้ว) = หันขวา (TURN_RIGHT)
    else if (side === 'RIGHT' && stableFingers === 5) {
      targetGesture = 'TURN_RIGHT';
    }

    const now = Date.now();
    const inCooldown = now < this.cooldownUntil;

    if (!targetGesture || inCooldown) {
      this.gestureHoldTime = Math.max(0, this.gestureHoldTime - deltaTime * 2.0);
      if (this.gestureHoldTime === 0) this.currentGesture = null;
      this.updateLiveFeedback(null, 0);
      return;
    }

    if (this.currentGesture === targetGesture) {
      this.gestureHoldTime += deltaTime;
      const effectiveThreshold = this.gestureTriggerThreshold; // 2.0s hold
      const ratio = Math.min(1.0, this.gestureHoldTime / effectiveThreshold);
      this.updateLiveFeedback(targetGesture, ratio);

      if (this.gestureHoldTime >= effectiveThreshold) {
        if (targetGesture === 'START_LOOP') {
          this.isLoopRecordingMode = true;
          this.lastTriggeredGesture = 'START_LOOP';
          this.lastTriggerAnimUntil = now + 900;
          this.cooldownUntil = now + 1200;
          this.gestureHoldTime = 0;
          this.currentGesture = null;
          if (this.onStartLoopRecording) this.onStartLoopRecording();
        } else if (targetGesture === 'FINISH_LOOP') {
          this.isLoopRecordingMode = false;
          this.awaitingLoopIteration = true;
          this.loopIterTarget = null;
          this.loopIterHoldTime = 0;
          this.lastTriggeredGesture = 'FINISH_LOOP';
          this.lastTriggerAnimUntil = now + 900;
          this.cooldownUntil = now + 800;
          this.gestureHoldTime = 0;
          this.currentGesture = null;
          if (this.onFinishLoopRecording) this.onFinishLoopRecording();
        } else {
          this.triggerGestureAction(targetGesture);
        }
      }
    } else {
      this.currentGesture = targetGesture;
      this.gestureHoldTime = 0;
      this.updateLiveFeedback(targetGesture, 0);
    }
  }

  decayAllHoldTimes(deltaTime) {
    this.gestureHoldTime = Math.max(0, this.gestureHoldTime - deltaTime * 2.0);
    this.runHoldTime = Math.max(0, this.runHoldTime - deltaTime * 2.0);
    this.resetHoldTime = Math.max(0, this.resetHoldTime - deltaTime * 2.0);
    this.undoHoldTime = Math.max(0, this.undoHoldTime - deltaTime * 2.0);
    if (this.gestureHoldTime === 0) this.currentGesture = null;
    this.isMiniHeartActive = false;
    this.isCrossActive = false;
  }

  decayOtherHoldTimes(activeMode, deltaTime) {
    if (activeMode !== 'GESTURE') this.gestureHoldTime = Math.max(0, this.gestureHoldTime - deltaTime * 2.0);
    if (activeMode !== 'RUN')     this.runHoldTime = Math.max(0, this.runHoldTime - deltaTime * 2.0);
    if (activeMode !== 'RESET')   this.resetHoldTime = Math.max(0, this.resetHoldTime - deltaTime * 2.0);
    if (activeMode !== 'UNDO')    this.undoHoldTime = Math.max(0, this.undoHoldTime - deltaTime * 2.0);
  }

  // =========================================================================
  // Draw Hand Skeleton with Hand Side Colors (Left = Cyan, Right = Gold)
  // =========================================================================
  drawHandSkeleton(lm, width, height, side) {
    const ctx = this.ctx;
    if (!ctx) return;

    const connections = [
      // Thumb
      [0, 1], [1, 2], [2, 3], [3, 4],
      // Index
      [0, 5], [5, 6], [6, 7], [7, 8],
      // Middle
      [5, 9], [9, 10], [10, 11], [11, 12],
      // Ring
      [0, 13], [13, 14], [14, 15], [15, 16],
      // Pinky
      [0, 17], [17, 18], [18, 19], [19, 20],
      // Palm base
      [5, 9], [9, 13], [13, 17]
    ];

    ctx.save();

    // Color theme: Cyan for Left Hand, Warm Gold for Right Hand
    const boneColor = side === 'LEFT' ? '#38bdf8' : '#fbbf24';

    // 1. Draw glowing neon bones
    ctx.lineWidth = 4;
    ctx.strokeStyle = boneColor;
    ctx.shadowColor = boneColor;
    ctx.shadowBlur = 10;
    ctx.beginPath();
    connections.forEach(([i, j]) => {
      const xi = (1 - lm[i].x) * width;
      const yi = lm[i].y * height;
      const xj = (1 - lm[j].x) * width;
      const yj = lm[j].y * height;
      ctx.moveTo(xi, yi);
      ctx.lineTo(xj, yj);
    });
    ctx.stroke();

    // 2. Draw 21 joint landmark dots
    for (let i = 0; i < lm.length; i++) {
      const x = (1 - lm[i].x) * width;
      const y = lm[i].y * height;
      const isTip = (i === 4 || i === 8 || i === 12 || i === 16 || i === 20);

      ctx.beginPath();
      ctx.arc(x, y, isTip ? 7 : 4, 0, Math.PI * 2);
      ctx.fillStyle = isTip ? '#10b981' : boneColor;
      ctx.shadowColor = isTip ? '#10b981' : boneColor;
      ctx.shadowBlur = 8;
      ctx.fill();

      ctx.strokeStyle = '#ffffff';
      ctx.lineWidth = 1.5;
      ctx.stroke();
    }

    // 3. Wrist Hand-Side Tag
    const wx = (1 - lm[0].x) * width;
    const wy = Math.min(height - 18, lm[0].y * height + 26);
    ctx.fillStyle = 'rgba(15, 23, 42, 0.88)';
    ctx.beginPath();
    ctx.roundRect(wx - 55, wy - 12, 110, 24, 12);
    ctx.fill();
    ctx.strokeStyle = boneColor;
    ctx.lineWidth = 1.5;
    ctx.stroke();

    ctx.font = 'bold 11px system-ui, sans-serif';
    ctx.fillStyle = '#ffffff';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';

    // Show recognized hand gesture dynamically right on the wrist tag
    let tagText = (side === 'LEFT' ? '🖐️ มือซ้าย' : '🖐️ มือขวา');
    if (this.isCrossActive || this.fingersCount === 10) {
      tagText = '🙅 10 นิ้ว (กากบาทรีเซ็ต)';
    } else if (this.awaitingLoopIteration) {
      if (this.fingersCount >= 2 && this.fingersCount <= 5) {
        tagText = `✌️ ${this.fingersCount} นิ้ว (วน ${this.fingersCount} รอบ)`;
      } else {
        tagText = 'ชู 2, 3, 4 หรือ 5 นิ้ว';
      }
    } else if (this.currentGesture === 'START_LOOP' || this.currentGesture === 'FINISH_LOOP' || this.fingersCount === 3) {
      tagText = '🤟 3 นิ้ว (วนลูป)';
    } else if (this.currentGesture === 'FORWARD' || this.fingersCount === 1) {
      tagText = '☝️ 1 นิ้ว (เดินหน้า)';
    } else if (this.currentGesture === 'TURN_LEFT') {
      tagText = '↩️ หันซ้าย (มือซ้าย)';
    } else if (this.currentGesture === 'TURN_RIGHT') {
      tagText = '↪️ หันขวา (มือขวา)';
    } else if (this.isMiniHeartActive) {
      tagText = '🫰 มินิฮาร์ท (รัน)';
    } else if (this.fingersCount === 5) {
      tagText = side === 'LEFT' ? '🖐️ ยกมือซ้าย (หันซ้าย)' : '🖐️ ยกมือขวา (หันขวา)';
    } else if (this.fingersCount === 4) {
      tagText = '✌️✌️ 4 นิ้ว';
    } else if (this.fingersCount === 2) {
      tagText = '✌️ 2 นิ้ว';
    } else if (this.fingersCount === 0) {
      tagText = '✊ กำมือ (พัก)';
    }
    ctx.fillText(tagText, wx, wy);

    ctx.restore();
  }

  // =========================================================================
  // Live Feedback Status Text & Indicator
  // =========================================================================
  updateLiveFeedback(actionType, ratio) {
    if (!this.liveTextEl || !this.liveDotEl) return;

    if (actionType === 'RESET') {
      const pct = Math.floor(ratio * 100);
      this.liveTextEl.textContent = `🙅 ตรวจพบ: 10 นิ้ว / กากบาทรีเซ็ตคำสั่ง... ${pct}%`;
      this.liveDotEl.className = 'live-pulse-dot charging';
      return;
    }

    if (actionType === 'RUN') {
      const pct = Math.floor(ratio * 100);
      this.liveTextEl.textContent = `🫰 ตรวจพบ: มินิฮาร์ทรันโค้ด... ${pct}%`;
      this.liveDotEl.className = 'live-pulse-dot charging';
      return;
    }

    if (actionType === 'UNDO') {
      const pct = Math.floor(ratio * 100);
      this.liveTextEl.textContent = `👎 ตรวจพบ: คว่ำมือลบคำสั่งล่าสุด... ${pct}%`;
      this.liveDotEl.className = 'live-pulse-dot charging';
      return;
    }

    if (actionType) {
      const meta = this.getGestureMeta(actionType);
      const pct = Math.floor(ratio * 100);
      if (actionType === 'START_LOOP' || actionType === 'FINISH_LOOP' || actionType === 'USE_KEY') {
        this.liveTextEl.textContent = `${meta.icon} ตรวจพบ: ${meta.label} — ค้างไว้... ${pct}%`;
      } else {
        const sideText = this.primaryHandSide === 'LEFT' ? 'มือซ้าย' : 'มือขวา';
        this.liveTextEl.textContent = `${meta.icon} ตรวจพบ: ${meta.label} (${sideText}) — ค้างไว้... ${pct}%`;
      }
      this.liveDotEl.className = 'live-pulse-dot charging';
    } else {
      if (this.lastLandmarks) {
        const sideText = this.primaryHandSide === 'LEFT' ? 'มือซ้าย' : 'มือขวา';
        this.liveTextEl.textContent = `ตรวจพบ: ${sideText} (☝️ 1 นิ้ว: เดินหน้า / 🖐️ แบมือ: เลี้ยวตามข้างมือ / 🤟 3 นิ้ว: วนลูป)`;
      } else {
        this.liveTextEl.textContent = 'กล้องพร้อม: ยกมือขึ้นหน้ากล้อง';
      }
      this.liveDotEl.className = 'live-pulse-dot';
    }
  }

  // =========================================================================
  // Trigger Action Callbacks
  // =========================================================================
  triggerGestureAction(gesture) {
    const now = Date.now();
    this.cooldownUntil = now + 1400; // 1.4s cooldown
    this.lastTriggeredGesture = gesture;
    this.lastTriggerAnimUntil = now + 700;
    this.gestureHoldTime = 0;
    this.currentGesture = null;

    if (this.liveDotEl) this.liveDotEl.className = 'live-pulse-dot active';
    if (window.soundEngine) window.soundEngine.playGrab();
    if (this.onZoneTrigger) this.onZoneTrigger(gesture);
  }

  triggerRunCode() {
    const now = Date.now();
    this.runCooldownUntil = now + 1800;
    this.runHoldTime = 0;
    this.runAnimUntil = now + 900;
    this.isMiniHeartActive = false;

    if (this.liveDotEl) this.liveDotEl.className = 'live-pulse-dot active';
    if (window.soundEngine) window.soundEngine.playTouch();
    if (this.onRunTrigger) this.onRunTrigger();
  }

  triggerResetCode() {
    const now = Date.now();
    this.resetCooldownUntil = now + 1800;
    this.resetHoldTime = 0;
    this.resetAnimUntil = now + 900;
    this.isCrossActive = false;
    this.crossPoint = null;

    if (this.liveDotEl) this.liveDotEl.className = 'live-pulse-dot active';
    if (window.soundEngine) window.soundEngine.playError();
    if (this.onResetTrigger) this.onResetTrigger();
  }

  triggerUndo() {
    const now = Date.now();
    this.undoCooldownUntil = now + 1600;
    this.undoHoldTime = 0;
    this.undoAnimUntil = now + 800;
    this.undoPoint = null;

    if (this.liveDotEl) this.liveDotEl.className = 'live-pulse-dot active';
    if (window.soundEngine) window.soundEngine.playError();
    if (this.onUndoTrigger) this.onUndoTrigger();
  }

  // =========================================================================
  // AR Overlay Renderer (Progress Rings & Banners)
  // =========================================================================
  renderAROverlay(width, height) {
    const ctx = this.ctx;
    if (!ctx) return;
    const now = Date.now();
    const isTriggerAnim = now < this.lastTriggerAnimUntil;
    const isRunAnim     = now < this.runAnimUntil;
    const isResetAnim   = now < this.resetAnimUntil;
    const isUndoAnim    = now < this.undoAnimUntil;
    const inCooldown    = now < this.cooldownUntil;

    // 0a. Loop Recording Active Overlay (Cosmic Purple Neon Border)
    if (this.isLoopRecordingMode) {
      ctx.save();
      ctx.strokeStyle = '#c084fc';
      ctx.lineWidth = 4;
      ctx.shadowColor = '#a855f7';
      ctx.shadowBlur = 14;
      ctx.strokeRect(6, 6, width - 12, height - 12);

      // Top recording banner
      ctx.fillStyle = 'rgba(59, 7, 100, 0.88)';
      ctx.beginPath();
      ctx.roundRect(width / 2 - 165, 10, 330, 36, 18);
      ctx.fill();
      ctx.strokeStyle = '#d8b4fe';
      ctx.lineWidth = 1.5;
      ctx.stroke();

      ctx.fillStyle = '#ffffff';
      ctx.font = 'bold 13px system-ui, sans-serif';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText('🔁 บันทึกลูป: ทำท่าคำสั่ง (3 นิ้ว = ปิดกล่อง)', width / 2, 28);
      ctx.restore();
    }

    // 0b. Awaiting Loop Iterations Overlay (Prompt card: 2, 3, 4 fingers)
    if (this.awaitingLoopIteration) {
      ctx.save();
      ctx.fillStyle = 'rgba(15, 23, 42, 0.94)';
      ctx.beginPath();
      ctx.roundRect(width / 2 - 165, 10, 330, 52, 14);
      ctx.fill();
      ctx.strokeStyle = '#38bdf8';
      ctx.lineWidth = 2;
      ctx.stroke();

      ctx.fillStyle = '#fef08a';
      ctx.font = 'bold 13px system-ui, sans-serif';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText('✌️ ชูนิ้วเลือกรอบ: 2 / 3 / 4 / 5 นิ้ว (เริ่มต้น 5x)', width / 2, 26);

      if (this.loopIterTarget && this.loopIterHoldTime > 0) {
        const pct = Math.min(1.0, this.loopIterHoldTime / 1000);
        ctx.fillStyle = 'rgba(255, 255, 255, 0.2)';
        ctx.fillRect(width / 2 - 140, 42, 280, 8);
        ctx.fillStyle = '#38bdf8';
        ctx.fillRect(width / 2 - 140, 42, 280 * pct, 8);
      }
      ctx.restore();
    }

    // 1. Mini Heart Progress Ring (Hot Pink 🫰)
    if (this.isMiniHeartActive && this.runHoldTime > 50) {
      const ratio = Math.min(1.0, this.runHoldTime / this.runTriggerThreshold);
      this.drawChargingRing(ctx, this.handCenter.x, this.handCenter.y - 45, ratio, 'RUN');
    }

    // 2. Cross Progress Ring (Crimson Red 🙅)
    if (this.isCrossActive && this.crossPoint && this.resetHoldTime > 50) {
      const ratio = Math.min(1.0, this.resetHoldTime / this.resetTriggerThreshold);
      this.drawChargingRing(ctx, this.crossPoint.x, this.crossPoint.y, ratio, 'RESET');
    }

    // 3. Undo Progress Ring (Amber/Red 👎)
    if (this.undoHoldTime > 50 && this.undoPoint) {
      const ratio = Math.min(1.0, this.undoHoldTime / this.undoTriggerThreshold);
      this.drawChargingRing(ctx, this.undoPoint.x, this.undoPoint.y, ratio, 'UNDO');
    }

    // 4. Command Progress Ring (Cyan/Gold/Purple)
    if (!inCooldown && this.gestureHoldTime > 50 && this.currentGesture && this.lastLandmarks) {
      const curThreshold = this.gestureTriggerThreshold;
      const ratio = Math.min(1.0, this.gestureHoldTime / curThreshold);
      this.drawChargingRing(ctx, this.handCenter.x, this.handCenter.y - 40, ratio, this.currentGesture);
    }

    // --- Confirmation Banners ---
    // 5a. Run Code Banner (Hot Pink)
    if (isRunAnim) {
      ctx.save();
      ctx.fillStyle = 'rgba(219, 39, 119, 0.94)';
      ctx.beginPath();
      ctx.roundRect(width / 2 - 140, 20, 280, 46, 23);
      ctx.fill();
      ctx.strokeStyle = '#fbcfe8';
      ctx.lineWidth = 2;
      ctx.stroke();

      ctx.font = 'bold 15px system-ui, sans-serif';
      ctx.fillStyle = '#ffffff';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText('🚀 สั่งรันโค้ดโปรแกรมแล้ว!', width / 2, 43);
      ctx.restore();
    }
    // 5b. Reset Code Banner (Vivid Red)
    else if (isResetAnim) {
      ctx.save();
      ctx.fillStyle = 'rgba(220, 38, 38, 0.94)';
      ctx.beginPath();
      ctx.roundRect(width / 2 - 140, 20, 280, 46, 23);
      ctx.fill();
      ctx.strokeStyle = '#fecaca';
      ctx.lineWidth = 2;
      ctx.stroke();

      ctx.font = 'bold 15px system-ui, sans-serif';
      ctx.fillStyle = '#ffffff';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText('❌ รีเซ็ตและล้างคำสั่งทั้งหมดแล้ว!', width / 2, 43);
      ctx.restore();
    }
    // 5c. Undo Confirmation Banner (Amber/Red)
    else if (isUndoAnim) {
      ctx.save();
      ctx.fillStyle = 'rgba(239, 68, 68, 0.94)';
      ctx.beginPath();
      ctx.roundRect(width / 2 - 130, 20, 260, 46, 23);
      ctx.fill();
      ctx.strokeStyle = '#fca5a5';
      ctx.lineWidth = 2;
      ctx.stroke();

      ctx.font = 'bold 15px system-ui, sans-serif';
      ctx.fillStyle = '#ffffff';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText('👎 ลบคำสั่งล่าสุดแล้ว!', width / 2, 43);
      ctx.restore();
    }
    // 5d. Block Added Banner (Emerald Green)
    else if (isTriggerAnim) {
      const meta = this.getGestureMeta(this.lastTriggeredGesture);
      ctx.save();
      ctx.fillStyle = 'rgba(16, 185, 129, 0.94)';
      ctx.beginPath();
      ctx.roundRect(width / 2 - 150, 20, 300, 46, 23);
      ctx.fill();
      ctx.strokeStyle = '#a7f3d0';
      ctx.lineWidth = 2;
      ctx.stroke();

      ctx.font = 'bold 15px system-ui, sans-serif';
      ctx.fillStyle = '#ffffff';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText(`✅ บันทึก: ${meta ? meta.label : ''}!`, width / 2, 43);
      ctx.restore();
    }

    // 6. AI Engine Status Banner (Top-Left Pill)
    ctx.save();
    if (this.aiError) {
      ctx.fillStyle = 'rgba(220, 38, 38, 0.92)';
      ctx.beginPath();
      ctx.roundRect(14, 14, 380, 32, 16);
      ctx.fill();
      ctx.strokeStyle = '#fecaca';
      ctx.lineWidth = 1.5;
      ctx.stroke();

      ctx.font = 'bold 12px system-ui, sans-serif';
      ctx.fillStyle = '#ffffff';
      ctx.textAlign = 'left';
      ctx.textBaseline = 'middle';
      ctx.fillText('⚠️ ' + this.aiError, 26, 30);
    } else if (!this.isHandsReady) {
      ctx.fillStyle = 'rgba(15, 23, 42, 0.88)';
      ctx.beginPath();
      ctx.roundRect(14, 14, 260, 32, 16);
      ctx.fill();
      ctx.strokeStyle = '#f59e0b';
      ctx.lineWidth = 1.5;
      ctx.stroke();

      ctx.font = 'bold 12px system-ui, sans-serif';
      ctx.fillStyle = '#fbbf24';
      ctx.textAlign = 'left';
      ctx.textBaseline = 'middle';
      ctx.fillText('⏳ ' + this.aiStatusText, 26, 30);
    } else {
      ctx.fillStyle = 'rgba(15, 23, 42, 0.85)';
      ctx.beginPath();
      ctx.roundRect(14, 14, 240, 32, 16);
      ctx.fill();
      ctx.strokeStyle = this.fingersCount > 0 || this.isMiniHeartActive || this.isCrossActive ? '#10b981' : 'rgba(56, 189, 248, 0.5)';
      ctx.lineWidth = 1.5;
      ctx.stroke();

      ctx.font = 'bold 12px system-ui, sans-serif';
      ctx.fillStyle = this.fingersCount > 0 || this.isMiniHeartActive || this.isCrossActive ? '#34d399' : '#38bdf8';
      ctx.textAlign = 'left';
      ctx.textBaseline = 'middle';
      let statusText = '🤖 AI แยกมือซ้าย-ขวาพร้อม';
      if (this.isCrossActive) {
        statusText = '🙅 กากบาท: รีเซ็ตโค้ด';
      } else if (this.isMiniHeartActive) {
        statusText = '🫰 มินิฮาร์ท: รันโค้ด';
      } else if (this.primaryHandSide) {
        const s = this.primaryHandSide === 'LEFT' ? 'มือซ้าย' : 'มือขวา';
        statusText = `🖐️ ${s} (${this.fingersCount} นิ้ว)`;
      }
      ctx.fillText(statusText, 26, 30);
    }
    ctx.restore();
  }

  drawChargingRing(ctx, cx, cy, ratio, gesture) {
    const meta = this.getGestureMeta(gesture);
    const ringR = 42;
    let color = '#38bdf8';
    if (gesture === 'RESET') color = '#ef4444';
    else if (gesture === 'RUN') color = '#ec4899';
    else if (gesture === 'UNDO') color = '#f59e0b';
    else if (gesture === 'START_LOOP' || gesture === 'FINISH_LOOP') color = '#a855f7';
    else if (gesture === 'TURN_RIGHT') color = '#fbbf24';
    else if (ratio > 0.65) color = '#34d399';

    ctx.save();
    // Background track ring
    ctx.beginPath();
    ctx.arc(cx, cy, ringR, 0, Math.PI * 2);
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.25)';
    ctx.lineWidth = 6;
    ctx.stroke();

    // Active progress arc
    ctx.beginPath();
    ctx.arc(cx, cy, ringR, -Math.PI / 2, -Math.PI / 2 + Math.PI * 2 * ratio);
    ctx.strokeStyle = color;
    ctx.lineWidth = 6;
    ctx.lineCap = 'round';
    ctx.stroke();

    // Floating badge above target
    if (meta) {
      ctx.fillStyle = 'rgba(15, 23, 42, 0.94)';
      ctx.beginPath();
      ctx.roundRect(cx - 80, cy - ringR - 38, 160, 30, 15);
      ctx.fill();
      ctx.strokeStyle = color;
      ctx.lineWidth = 1.5;
      ctx.stroke();

      ctx.font = 'bold 13px system-ui, sans-serif';
      ctx.fillStyle = '#ffffff';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText(`${meta.icon} ${meta.label}`, cx, cy - ringR - 23);
    }
    ctx.restore();
  }

  getGestureMeta(action) {
    if (!action) return null;
    const map = {
      FORWARD:     { label: 'เดินหน้า (1 นิ้ว)',      icon: '⬆️' },
      TURN_LEFT:   { label: 'หันซ้าย (ยกมือซ้าย)',     icon: '↩️' },
      TURN_RIGHT:  { label: 'หันขวา (ยกมือขวา)',      icon: '↪️' },
      START_LOOP:  { label: 'เปิดกล่องวนซ้ำ (3 นิ้ว)', icon: '🔁' },
      FINISH_LOOP: { label: 'ปิดกล่องวนซ้ำ (3 นิ้ว)', icon: '✅' },
      LOOP_2:      { label: 'วนซ้ำ 2 รอบ',           icon: '🔁2' },
      LOOP_3:      { label: 'วนซ้ำ 3 รอบ',           icon: '🔁3' },
      LOOP_4:      { label: 'วนซ้ำ 4 รอบ',           icon: '🔁4' },
      USE_KEY:     { label: 'ไขกุญแจ (3 นิ้ว)',       icon: '🔑' },
      RUN:         { label: 'รันโค้ด (มินิฮาร์ท)',     icon: '🫰' },
      RESET:       { label: 'รีเซ็ตโค้ดใหม่ (กากบาท)',   icon: '🙅' },
      UNDO:        { label: 'ยกเลิกล่าสุด (คว่ำมือ)',   icon: '👎' }
    };
    return map[action] || { label: action, icon: '👉' };
  }

  renderFallbackMode(msg) {
    if (!this.canvas) return;
    this.canvas.width = 640; this.canvas.height = 480;
    const ctx = this.ctx || this.canvas.getContext('2d');
    if (!ctx) return;
    ctx.fillStyle = '#111827'; ctx.fillRect(0, 0, 640, 480);
    ctx.fillStyle = '#94a3b8'; ctx.font = '20px system-ui, sans-serif'; ctx.textAlign = 'center';
    ctx.fillText('📷 สลับเข้าสู่โหมดหน้าจอสัมผัส / คลิกเลือกบล็อก', 320, 200);
    ctx.font = '14px system-ui, sans-serif'; ctx.fillStyle = '#60a5fa';
    ctx.fillText(msg || 'น้องๆ สามารถคลิกที่ปุ่มคำสั่งด้านล่างได้ทันที 100%', 320, 240);
  }
}

window.CameraEngine = CameraEngine;
