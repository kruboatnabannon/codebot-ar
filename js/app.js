/**
 * CodeBot AR Adventure - Main Application Controller
 * Version 5.4 - Block Reordering, Practice vs Challenge Mode, Game Over & AR Emergency Photo
 * ผู้พัฒนา: นายเตชินท์ อินทมล ตำแหน่ง ครู โรงเรียนบ้านโนนป่าหว้านเชียงฮาย
 */

class AppController {
  constructor() {
    this.currentLevelIndex = 0;
    this.totalScore = 0;
    this.totalStars = 0;
    this.userBadges = [];
    this.codeSequence = [];

    // Game Mode: 'PRACTICE' (Free play, no timer, no lives) vs 'CHALLENGE' (Timer, 3 lives, Game Over)
    this.gameMode = 'PRACTICE';
    this.stageTimeLimit = 75;
    this.stageTimeLeft = 75;
    this.stageTimerInterval = null;
    this.playerLives = 3;
    this.maxLives = 3;

    // Active Learning & Classroom State
    this.pairModeActive = true;
    this.currentRole = 'DRIVER'; // 'DRIVER' or 'NAVIGATOR'
    this.roleTimer = 180; // 3 minutes per role swap
    this.roleTimerInterval = null;

    // Registered Student Information
    this.teamName = "ทีมนักสำรวจอวกาศ 01";
    this.driverName = "ต้นกล้า";
    this.navigatorName = "ฟ้าใส";
    this.gradeLevel = "p4";
    this.selectedStartGrade = "p4";
    this.selectedStartLevel = 0;
    this.modalGrade = "p4";
    this.unlockedLevels = this.loadUnlockedLevels();
    this.currentLevels = window.LEVELS_P4 || window.GAME_LEVELS || [];
    this.selectedPracticeLevelIndex = 0;
    this.gameStarted = false;

    // Drag-and-drop state
    this.draggedBlockIdx = null;

    // Winner Photo & Emergency Photo State
    this.latestWinnerPhotoData = null;
    this.isGameOverPhoto = false;
    this.activeLbTabGrade = 'p4';

    // Voice & Speech Settings
    this.autoSpeakKnowledge = localStorage.getItem('codebot_ar_auto_speak') !== 'false';
    this.ttsSpeed = parseFloat(localStorage.getItem('codebot_ar_tts_speed')) || 1.0;
    this.selectedVoiceUri = localStorage.getItem('codebot_ar_tts_voice') || '';
    this.voiceCharacter = localStorage.getItem('codebot_ar_voice_char') || 'female';
    this.ttsPitch = parseFloat(localStorage.getItem('codebot_ar_tts_pitch')) || (this.voiceCharacter === 'male' ? 0.82 : (this.voiceCharacter === 'robot' ? 1.38 : 1.1));

    // Engines
    this.cameraEngine = null;
    this.gameEngine = null;

    // Storage Keys
    this.STORAGE_KEY_LEADERBOARD_P4 = 'codebot_ar_leaderboard_p4';
    this.STORAGE_KEY_LEADERBOARD_P5 = 'codebot_ar_leaderboard_p5';
    this.STORAGE_KEY_RESEARCH = 'codebot_ar_research_data';

    // Auto level transition timer
    this.victoryTimer = null;

    // Mini-Quiz & Pedagogy State (ว 4.2)
    this.quizPassedCount = 0;
    this.currentQuizAnswered = false;
    this.passedQuizStages = new Set();
    this.benchmarkTopScore = 0;

    // Hands-Free Loop Recording State
    this.currentRecordingLoop = null;

    // Screen Wake Lock State (ป้องกันจอดับขณะวางเล่นบนมือถือ)
    this.wakeLockSentinel = null;
    this.wakeLockEnabled = true;
    this.videoWakeLockFallback = null;

    this.init();
  }

  async init() {
    // 1. Initialize Engines & TTS
    this.cameraEngine = new window.CameraEngine('ar-canvas', 'webcam-video');
    this.gameEngine = new window.GameEngine('grid-canvas');
    this.initTTSVoices();
    this.initWakeLock();

    // 2. Setup Camera Engine Trigger Hook
    this.cameraEngine.onZoneTrigger = (zoneId) => {
      this.handleBlockAction(zoneId);
    };

    // 2b. Undo gesture hook — 👎 นิ้วโป้งลง = ลบคำสั่งล่าสุด
    this.cameraEngine.onUndoTrigger = () => {
      this.removeLastBlock();
    };

    // 2c. Mini Heart gesture hook — 🫰 มินิฮาร์ท = รันโค้ดโปรแกรม
    this.cameraEngine.onRunTrigger = () => {
      if (this.gameEngine && this.gameEngine.isExecuting) return;
      if (this.codeSequence.length === 0) {
        this.showStatusToast('⚠️ ยังไม่มีคำสั่งในโปรแกรม! ชูนิ้วเลือกคำสั่งก่อนนะ', true);
        return;
      }
      if (window.soundEngine) window.soundEngine.playTouch();
      this.gameEngine.setCode(this.codeSequence);
      this.gameEngine.runAll();
      this.showStatusToast('🚀 สั่งรันโค้ดด้วยท่ามินิฮาร์ทสำเร็จ!', false);
    };

    // 2d. Cross gesture hook — 🙅 กากบาท = รีเซ็ตและล้างคำสั่งทั้งหมด
    this.cameraEngine.onResetTrigger = () => {
      if (this.codeSequence && this.codeSequence.length > 0) {
        this.lastDeletedCode = JSON.parse(JSON.stringify(this.codeSequence));
      }
      if (window.soundEngine) window.soundEngine.playError();
      if (this.gameEngine) {
        this.gameEngine.isExecuting = false;
        if (this.gameEngine.stepTimeout) {
          clearTimeout(this.gameEngine.stepTimeout);
          this.gameEngine.stepTimeout = null;
        }
        this.gameEngine.resetSimulation();
      }
      this.currentRecordingLoop = null;
      if (this.cameraEngine) {
        this.cameraEngine.isLoopRecordingMode = false;
        this.cameraEngine.awaitingLoopIteration = false;
      }
      this.codeSequence = [];
      this.renderTimeline();
      this.highlightActiveChip(-1);
      this.showUndoToast('รีเซ็ตและล้างคำสั่งทั้งหมดแล้ว');
    };

    // 2e. Hands-Free Loop Recording Hooks (ชู 3 นิ้ว เปิด/ปิดลูป และชู 2-4 นิ้วเลือกรอบ)
    this.cameraEngine.onStartLoopRecording = () => {
      this.startLoopRecordingMode();
    };
    this.cameraEngine.onFinishLoopRecording = () => {
      this.finishLoopRecordingMode();
    };
    this.cameraEngine.onSelectLoopIteration = (iter) => {
      this.setLoopRecordingIterations(iter);
    };

    // 3. Setup Game Engine Callbacks
    this.gameEngine.onStepChange = (activeBlockIdx, instr) => {
      this.highlightActiveChip(activeBlockIdx, instr);
    };

    this.gameEngine.onFinish = (result) => {
      this.handleGameFinished(result);
    };

    this.gameEngine.onStatusMsg = (msg, isError) => {
      this.showStatusToast(msg, isError);
    };

    // 4. Bind UI Events (including Welcome Screen, Modals, Buttons)
    this.bindDOMEvents();

    // 5. Update Grade Levels according to default
    this.updateGradeTrack(this.gradeLevel);

    // 6. Update Top Score Banners
    this.updateTopScoreBanners();

    // 7. Initialize gesture guide bar
    this.updateGestureGuideBar();

    // 8. Update HUD for initial mode
    this.updateGameModeUI();
    this.renderPracticeLevelSelector();
    this.renderWelcomeLevelSelector();
    this.renderWelcomeCartoonGrid();
  }

  updateGradeTrack(grade) {
    this.gradeLevel = grade;
    this.selectedStartGrade = grade;
    this.modalGrade = grade;
    this.activeLbTabGrade = grade;
    this.currentLevels = (grade === 'p5') ? (window.LEVELS_P5 || []) : (window.LEVELS_P4 || []);
    window.GAME_LEVELS = this.currentLevels;

    // Synchronize Welcome Grade buttons (Practice)
    const btnP4 = document.getElementById('btn-welcome-grade-p4');
    const btnP5 = document.getElementById('btn-welcome-grade-p5');
    if (btnP4) btnP4.classList.toggle('active', grade === 'p4');
    if (btnP5) btnP5.classList.toggle('active', grade === 'p5');

    // Synchronize Challenge Grade buttons (Challenge)
    const btnChalP4 = document.getElementById('btn-challenge-grade-p4');
    const btnChalP5 = document.getElementById('btn-challenge-grade-p5');
    if (btnChalP4) btnChalP4.classList.toggle('active', grade === 'p4');
    if (btnChalP5) btnChalP5.classList.toggle('active', grade === 'p5');

    const btnStartChal = document.getElementById('btn-start-challenge-direct');
    if (btnStartChal) {
      btnStartChal.innerHTML = `⚡ เริ่มประลองความเร็ว ชั้น ${grade === 'p5' ? 'ป.5' : 'ป.4'} (เริ่มด่านที่ 1) 🚀`;
    }

    const gradeSelect = document.getElementById('input-grade-level');
    if (gradeSelect) gradeSelect.value = grade;

    const standardTag = document.getElementById('level-standard-tag');
    if (standardTag) {
      standardTag.textContent = grade === 'p5' 
        ? 'วิทยาการคำนวณ ว 4.2 ป.5 (เหตุผลเชิงตรรกะ ลูปผสม เงื่อนไข ดีบัก)' 
        : 'วิทยาการคำนวณ ว 4.2 ป.4 (อัลกอริทึม ลำดับขั้นตอน ลูปพื้นฐาน)';
    }

    this.currentLevelIndex = 0;
    this.selectedPracticeLevelIndex = 0;
    if (this.gameStarted) {
      this.loadCurrentLevel(0, false);
    }
    this.renderPracticeLevelSelector();
    this.renderWelcomeLevelSelector();
    this.renderWelcomeCartoonGrid();
    this.renderCartoonLevelGrid(grade);
    const records = this.loadLeaderboardData(grade);
    this.benchmarkTopScore = (records && records.length > 0) ? records[0].score : 0;
    this.updateTopScoreBanners();
  }

  setGameMode(newMode) {
    this.gameMode = newMode;
    this.updateGameModeUI();

    if (this.gameStarted) {
      if (this.gameMode === 'CHALLENGE') {
        const records = this.loadLeaderboardData(this.gradeLevel);
        this.benchmarkTopScore = (records && records.length > 0) ? records[0].score : 0;
        this.resetLives();
        this.startStageTimer();
        this.showStatusToast('⚡ เริ่มโหมดประลองความเร็ว! จับเวลาและจำกัดพลังงาน ❤️', false);
      } else {
        this.stopStageTimer();
        this.showStatusToast('🛡️ สลับสู่โหมดฝึกซ้อม: ไม่จำกัดเวลา รันโค้ดได้ตามสบาย', false);
      }
    }
  }

  updateGameModeUI() {
    const isChallenge = (this.gameMode === 'CHALLENGE');

    // Welcome Screen Mode Choice Buttons (Practice vs Challenge)
    const btnChoicePractice = document.getElementById('btn-choice-mode-practice');
    const btnChoiceChallenge = document.getElementById('btn-choice-mode-challenge');
    if (btnChoicePractice) btnChoicePractice.classList.toggle('active', !isChallenge);
    if (btnChoiceChallenge) btnChoiceChallenge.classList.toggle('active', isChallenge);

    // In-game Mission Bar quick level select button: Only visible in Practice Mode!
    const btnQuickMenu = document.getElementById('btn-quick-menu');
    if (btnQuickMenu) {
      btnQuickMenu.style.display = isChallenge ? 'none' : 'inline-flex';
    }

    // Top Navigation HUD Elements
    const modePill = document.getElementById('nav-mode-pill');
    const modeIcon = document.getElementById('nav-mode-icon');
    const modeText = document.getElementById('nav-mode-text');
    const timerPill = document.getElementById('nav-timer-pill');
    const livesPill = document.getElementById('nav-lives-pill');

    if (modeIcon) modeIcon.textContent = isChallenge ? '⚡' : '🛡️';
    if (modeText) {
      modeText.textContent = isChallenge ? 'ประลองความเร็ว' : 'ฝึกซ้อม';
      modeText.style.color = isChallenge ? '#f87171' : '#34d399';
    }
    if (modePill) {
      modePill.style.borderColor = isChallenge ? '#ef4444' : '#10b981';
      modePill.style.background = isChallenge ? 'rgba(239, 68, 68, 0.15)' : 'rgba(16, 185, 129, 0.15)';
    }

    if (timerPill) timerPill.style.display = isChallenge ? 'flex' : 'none';
    if (livesPill) livesPill.style.display = isChallenge ? 'flex' : 'none';

    // Practice Level Selector Strip in Game Panel
    const practiceSelector = document.getElementById('practice-level-selector');
    if (practiceSelector) {
      practiceSelector.style.display = isChallenge ? 'none' : 'flex';
      if (!isChallenge) {
        this.renderPracticeLevelSelector();
      }
    }

    // Re-render grids if practice
    if (!isChallenge) {
      this.renderWelcomeCartoonGrid();
    }
  }

  loadUnlockedLevels() {
    try {
      const saved = localStorage.getItem('codebot_ar_unlocked_levels');
      if (saved) {
        const parsed = JSON.parse(saved);
        if (parsed && parsed.p4 >= 10 && parsed.p5 >= 10) return parsed;
      }
    } catch (e) {
      console.warn('Failed to load unlocked levels:', e);
    }
    // ปลดล็อกครบทุกด่าน 1-10 อิสระตามความต้องการของผู้เรียนและคุณครู (ไม่มีการล็อกด่าน)
    return { p4: 10, p5: 10 };
  }

  saveUnlockedLevels() {
    try {
      localStorage.setItem('codebot_ar_unlocked_levels', JSON.stringify(this.unlockedLevels));
    } catch (e) {
      console.warn('Failed to save unlocked levels:', e);
    }
  }

  unlockNextLevel(grade, levelNumber) {
    if (!this.unlockedLevels) this.unlockedLevels = { p4: 10, p5: 10 };
    const current = this.unlockedLevels[grade] || 10;
    if (levelNumber > current) {
      this.unlockedLevels[grade] = Math.min(10, levelNumber);
      this.saveUnlockedLevels();
    }
  }

  getPadlockSvg() {
    return `<div class="cartoon-padlock" title="ด่านนี้ยังถูกล็อกอยู่">
      <svg class="cartoon-padlock-svg" viewBox="0 0 28 32" width="22" height="25">
        <path d="M 7 14 V 8 C 7 4.1 10.1 1 14 1 C 17.9 1 21 4.1 21 8 V 14" fill="none" stroke="#e2e8f0" stroke-width="3" stroke-linecap="round"/>
        <path d="M 7 14 V 8 C 7 4.1 10.1 1 14 1 C 17.9 1 21 4.1 21 8 V 14" fill="none" stroke="#64748b" stroke-width="1.2" stroke-linecap="round"/>
        <rect x="3" y="12" width="22" height="18" rx="4" fill="#fbbf24" stroke="#b45309" stroke-width="2"/>
        <rect x="5" y="14" width="18" height="4" rx="2" fill="#fef08a" opacity="0.6"/>
        <circle cx="14" cy="20" r="2.2" fill="#78350f"/>
        <path d="M 14 21.5 V 25.5" stroke="#78350f" stroke-width="2" stroke-linecap="round"/>
      </svg>
    </div>`;
  }

  renderWelcomeCartoonGrid() {
    const grid = document.getElementById('welcome-cartoon-level-grid');
    if (!grid) return;
    grid.innerHTML = '';

    const levels = (this.selectedStartGrade === 'p5') ? (window.LEVELS_P5 || []) : (window.LEVELS_P4 || []);
    const total = levels.length || 10;
    const maxUnlocked = (this.unlockedLevels && this.unlockedLevels[this.selectedStartGrade]) || 6;

    this.updateWelcomeSelectedLevelUI();

    for (let i = 0; i < total; i++) {
      const level = levels[i];
      const isSelected = (i === this.selectedStartLevel);

      const tile = document.createElement('div');
      tile.className = 'cartoon-level-tile'
        + (isSelected ? ' active' : '');
      tile.setAttribute('data-level-index', i);

      const inner = document.createElement('div');
      inner.className = 'cartoon-level-tile-inner';

      const num = document.createElement('div');
      num.className = 'cartoon-level-tile-num';
      num.textContent = `${i + 1}`;
      inner.appendChild(num);

      const stars = document.createElement('div');
      stars.className = 'cartoon-level-tile-stars';
      stars.textContent = isSelected ? '⭐⭐⭐' : '⭐⭐';
      inner.appendChild(stars);

      tile.appendChild(inner);

      const onHover = () => {
        const previewTitle = document.getElementById('welcome-selected-level-title');
        const previewBadge = document.getElementById('welcome-selected-concept-badge');
        if (previewTitle && level) previewTitle.textContent = `ด่านที่ ${i + 1}: ${level.title}`;
        if (previewBadge && level) previewBadge.textContent = level.conceptBadge || 'ภารกิจ';
      };
      tile.addEventListener('mouseenter', onHover);
      tile.addEventListener('touchstart', onHover, { passive: true });

      tile.addEventListener('click', () => {
        if (window.soundEngine) window.soundEngine.playTouch();
        if (this.selectedStartLevel === i) {
          this.startMission();
          return;
        }
        this.selectedStartLevel = i;
        this.renderWelcomeCartoonGrid();

        const speakText = `ด่านที่ ${i + 1} ${level ? level.title : ''}`;
        this.speakKnowledgeText(speakText);
      });

      grid.appendChild(tile);
    }
  }

  updateWelcomeSelectedLevelUI() {
    const levels = (this.selectedStartGrade === 'p5') ? (window.LEVELS_P5 || []) : (window.LEVELS_P4 || []);
    const level = levels[this.selectedStartLevel] || levels[0];
    const previewTitle = document.getElementById('welcome-selected-level-title');
    const previewBadge = document.getElementById('welcome-selected-concept-badge');
    const quickStartBtn = document.getElementById('btn-quick-start');

    const gradeLabel = (this.selectedStartGrade === 'p5') ? 'ป.5' : 'ป.4';
    const levelNum = (this.selectedStartLevel + 1);

    if (previewTitle && level) {
      previewTitle.textContent = `ด่านที่ ${levelNum}: ${level.title}`;
    }
    if (previewBadge && level) {
      previewBadge.textContent = level.conceptBadge || 'ภารกิจ';
    }
    if (quickStartBtn) {
      quickStartBtn.innerHTML = `🚀 เริ่มเล่น ชั้น ${gradeLabel} ด่านที่ ${levelNum} ทันที!`;
    }
  }

  openGameMenu(initialView = 'levels') {
    this.pauseStageTimer();

    const isMuted = window.soundEngine ? window.soundEngine.muted : false;
    const soundIcon = document.getElementById('menu-sound-icon');
    if (soundIcon) soundIcon.textContent = isMuted ? '🔇' : '🔊';

    this.modalGrade = this.gradeLevel;
    this.renderCartoonLevelGrid(this.modalGrade);
    this.updateWakeLockUI();
    document.getElementById('game-menu-modal')?.classList.add('active');
  }

  closeGameMenu() {
    document.getElementById('game-menu-modal')?.classList.remove('active');
    if (this.gameMode === 'CHALLENGE' && this.gameStarted && !this.isGameOver) {
      this.resumeStageTimer();
    }
  }

  renderCartoonLevelGrid(targetGrade = null) {
    const grade = targetGrade || this.modalGrade || this.gradeLevel || 'p4';
    this.modalGrade = grade;

    const grid = document.getElementById('cartoon-level-grid');
    if (!grid) return;
    grid.innerHTML = '';

    const tabP4 = document.getElementById('modal-tab-grade-p4');
    const tabP5 = document.getElementById('modal-tab-grade-p5');
    if (tabP4) tabP4.classList.toggle('active', grade === 'p4');
    if (tabP5) tabP5.classList.toggle('active', grade === 'p5');

    const previewTitle = document.getElementById('level-tile-preview-title');
    const previewBadge = document.getElementById('level-tile-preview-badge');

    const levels = (grade === 'p5') ? (window.LEVELS_P5 || []) : (window.LEVELS_P4 || []);
    const total = levels.length || 10;
    const maxUnlocked = (this.unlockedLevels && this.unlockedLevels[grade]) || 6;

    const isCurrentGrade = (grade === this.gradeLevel);
    const activeLevel = isCurrentGrade && levels[this.currentLevelIndex] ? levels[this.currentLevelIndex] : levels[0];

    if (previewTitle && activeLevel) {
      const activeIdx = isCurrentGrade ? this.currentLevelIndex : 0;
      previewTitle.textContent = `ด่านที่ ${activeIdx + 1}: ${activeLevel.title}`;
    }
    if (previewBadge && activeLevel) {
      previewBadge.textContent = activeLevel.conceptBadge || 'ภารกิจ';
    }

    for (let i = 0; i < total; i++) {
      const level = levels[i];
      const isCurrent = isCurrentGrade && (i === this.currentLevelIndex);

      const tile = document.createElement('div');
      tile.className = 'cartoon-level-tile'
        + (isCurrent ? ' active' : '');
      tile.setAttribute('data-level-index', i);

      const inner = document.createElement('div');
      inner.className = 'cartoon-level-tile-inner';

      const num = document.createElement('div');
      num.className = 'cartoon-level-tile-num';
      num.textContent = `${i + 1}`;
      inner.appendChild(num);

      const stars = document.createElement('div');
      stars.className = 'cartoon-level-tile-stars';
      stars.textContent = isCurrent ? '⭐⭐⭐' : '⭐⭐';
      inner.appendChild(stars);

      tile.appendChild(inner);

      const updatePreview = () => {
        if (previewTitle && level) {
          previewTitle.textContent = `ด่านที่ ${i + 1}: ${level.title}`;
        }
        if (previewBadge && level) {
          previewBadge.textContent = level.conceptBadge || 'ภารกิจ';
        }
      };

      tile.addEventListener('mouseenter', updatePreview);
      tile.addEventListener('touchstart', updatePreview, { passive: true });

      tile.addEventListener('click', () => {
        if (window.soundEngine) window.soundEngine.playTouch();
        if (this.gradeLevel !== grade) {
          this.updateGradeTrack(grade);
        }
        this.selectLevelFromMenu(i);
      });

      grid.appendChild(tile);
    }
  }

  selectLevelFromMenu(index) {
    if (!this.currentLevels || index < 0 || index >= this.currentLevels.length) return;
    const level = this.currentLevels[index];
    this.selectedPracticeLevelIndex = index;
    this.loadCurrentLevel(index, false);
    this.closeGameMenu();

    const speakText = `ด่านที่ ${index + 1} ${level ? level.title : ''}`;
    this.speakKnowledgeText(speakText);

    this.showStatusToast(`🎯 เข้าสู่ด่านที่ ${index + 1}: ${level ? level.title : ''}`, false);
  }

  renderPracticeLevelSelector() {
    const container = document.getElementById('level-blocks-container');
    if (!container) return;

    container.innerHTML = '';
    const totalLevels = (this.currentLevels && this.currentLevels.length) ? this.currentLevels.length : 10;

    for (let i = 0; i < totalLevels; i++) {
      const level = this.currentLevels[i];
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'level-block-btn' + (i === this.currentLevelIndex ? ' active' : '');
      btn.textContent = `${i + 1}`;
      btn.setAttribute('data-level-index', i);
      const title = level ? `ด่านที่ ${i + 1}: ${level.title}` : `ด่านที่ ${i + 1}`;
      btn.setAttribute('title', title);

      btn.addEventListener('click', (e) => {
        e.preventDefault();
        if (window.soundEngine) window.soundEngine.playTouch();
        this.selectPracticeLevel(i);
      });

      container.appendChild(btn);
    }

    this.updatePracticeLevelHighlight(this.currentLevelIndex);
  }

  selectPracticeLevel(index) {
    if (!this.currentLevels || index < 0 || index >= this.currentLevels.length) return;
    const level = this.currentLevels[index];
    this.selectedPracticeLevelIndex = index;
    this.loadCurrentLevel(index, false);
    this.updatePracticeLevelHighlight(index);

    // Speak level name with TTS
    const speakText = `ด่านที่ ${index + 1} ${level.title}`;
    this.speakKnowledgeText(speakText);

    // Show status toast
    this.showStatusToast(`🎯 เข้าสู่ด่านที่ ${index + 1}: ${level.title}`, false);
  }

  updatePracticeLevelHighlight(index) {
    const container = document.getElementById('level-blocks-container');
    if (container) {
      const btns = container.querySelectorAll('.level-block-btn');
      btns.forEach((b, idx) => {
        b.classList.toggle('active', idx === index);
      });
    }

    const nameDisplay = document.getElementById('level-selected-name');
    if (nameDisplay && this.currentLevels && this.currentLevels[index]) {
      const lvl = this.currentLevels[index];
      const concept = lvl.conceptBadge ? ` (${lvl.conceptBadge})` : '';
      nameDisplay.textContent = `📌 กำลังเล่น: ด่านที่ ${index + 1} — ${lvl.title}${concept}`;
    }

    // Also update welcome screen blocks if visible
    const welcomeContainer = document.getElementById('welcome-level-blocks-container');
    if (welcomeContainer) {
      const wBtns = welcomeContainer.querySelectorAll('.level-block-btn');
      wBtns.forEach((b, idx) => {
        b.classList.toggle('active', idx === index);
      });
    }

    // Also update menu modal grid if visible
    const menuGrid = document.getElementById('menu-level-grid');
    if (menuGrid) {
      const cards = menuGrid.querySelectorAll('.menu-level-card');
      cards.forEach((c, idx) => {
        c.classList.toggle('active', idx === index);
      });
      const curLvl = (this.currentLevels && this.currentLevels[index]) ? this.currentLevels[index] : null;
      const activeElem = document.getElementById('menu-level-active-title');
      if (activeElem && curLvl) {
        activeElem.textContent = `กำลังเล่น: ด่านที่ ${index + 1} — ${curLvl.title}`;
      }
    }
  }

  renderWelcomeLevelSelector() {
    const container = document.getElementById('welcome-level-blocks-container');
    const preview = document.getElementById('welcome-level-title-preview');
    if (!container) return;

    container.innerHTML = '';
    const totalLevels = (this.currentLevels && this.currentLevels.length) ? this.currentLevels.length : 10;
    const currentIdx = (typeof this.selectedPracticeLevelIndex === 'number') ? this.selectedPracticeLevelIndex : 0;

    for (let i = 0; i < totalLevels; i++) {
      const level = this.currentLevels[i];
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'level-block-btn' + (i === currentIdx ? ' active' : '');
      btn.textContent = `${i + 1}`;
      btn.setAttribute('data-level-index', i);
      const title = level ? `ด่านที่ ${i + 1}: ${level.title}` : `ด่านที่ ${i + 1}`;
      btn.setAttribute('title', title);

      btn.addEventListener('click', (e) => {
        e.preventDefault();
        if (window.soundEngine) window.soundEngine.playTouch();
        this.selectedPracticeLevelIndex = i;
        if (preview && level) {
          preview.textContent = `ด่านที่ ${i + 1}: ${level.title}`;
        }
        const startBtn = document.getElementById('btn-start-mission');
        if (startBtn) {
          startBtn.innerHTML = `<span>🚀</span> เริ่มต้นการผจญภัยสู่ด่านที่ ${i + 1}`;
        }
        container.querySelectorAll('.level-block-btn').forEach((b, idx) => {
          b.classList.toggle('active', idx === i);
        });
        // Speak name
        const text = `ด่านที่ ${i + 1} ${level ? level.title : ''}`;
        this.speakKnowledgeText(text);
      });

      container.appendChild(btn);
    }

    if (preview && this.currentLevels && this.currentLevels[currentIdx]) {
      preview.textContent = `ด่านที่ ${currentIdx + 1}: ${this.currentLevels[currentIdx].title}`;
    }
  }

  startStageTimer() {
    this.stopStageTimer();
    if (this.gameMode !== 'CHALLENGE') return;

    // 75s for normal stages, 90s for stage 4 & 5
    this.stageTimeLimit = (this.currentLevelIndex >= 3) ? 90 : 75;
    this.stageTimeLeft = this.stageTimeLimit;

    this.updateTimerDisplay();

    this.stageTimerInterval = setInterval(() => {
      this.stageTimeLeft--;
      this.updateTimerDisplay();

      if (this.stageTimeLeft <= 0) {
        this.stopStageTimer();
        this.triggerGameOver('⏰ หมดเวลาภารกิจ (Time is Up)! คุณใช้เวลาเกินกำหนด');
      }
    }, 1000);
  }

  stopStageTimer() {
    if (this.stageTimerInterval) {
      clearInterval(this.stageTimerInterval);
      this.stageTimerInterval = null;
    }
  }

  pauseStageTimer() {
    if (this.stageTimerInterval) {
      clearInterval(this.stageTimerInterval);
      this.stageTimerInterval = null;
    }
  }

  resumeStageTimer() {
    if (this.gameMode !== 'CHALLENGE' || !this.gameStarted) return;
    if (this.stageTimerInterval) return; // already running
    if (this.stageTimeLeft <= 0 || this.playerLives <= 0) return;
    const activeModal = document.querySelector('.modal-overlay.active');
    if (activeModal) return; // do not resume if any modal is still open

    this.stageTimerInterval = setInterval(() => {
      this.stageTimeLeft--;
      this.updateTimerDisplay();

      if (this.stageTimeLeft <= 0) {
        this.stopStageTimer();
        this.triggerGameOver('⏰ หมดเวลาภารกิจ (Time is Up)! คุณใช้เวลาเกินกำหนด');
      }
    }, 1000);
  }

  updateTimerDisplay() {
    const timerText = document.getElementById('nav-timer-text');
    const timerPill = document.getElementById('nav-timer-pill');
    if (!timerText) return;

    const mins = Math.floor(Math.max(0, this.stageTimeLeft) / 60);
    const secs = Math.max(0, this.stageTimeLeft) % 60;
    const formatted = `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
    timerText.textContent = formatted;

    if (timerPill) {
      timerPill.classList.remove('timer-warning', 'timer-danger');
      if (this.stageTimeLeft <= 15) {
        timerPill.classList.add('timer-danger');
      } else if (this.stageTimeLeft <= 30) {
        timerPill.classList.add('timer-warning');
      }
    }
  }

  resetLives() {
    this.playerLives = this.maxLives;
    this.updateLivesHUD();
  }

  updateLivesHUD() {
    const livesText = document.getElementById('nav-lives-text');
    if (!livesText) return;
    let hearts = '';
    for (let i = 0; i < this.maxLives; i++) {
      hearts += (i < this.playerLives) ? '❤️' : '🤍';
    }
    livesText.textContent = hearts;
  }

  loseLife(reason) {
    if (this.gameMode !== 'CHALLENGE') return;
    this.playerLives = Math.max(0, this.playerLives - 1);
    this.updateLivesHUD();

    if (this.playerLives <= 0) {
      this.stopStageTimer();
      this.triggerGameOver(`💥 พลังงานแบตเตอรี่หุ่นยนต์หมดลงแล้ว (0/${this.maxLives} ❤️) สาเหตุ: ${reason}`);
    } else {
      this.showStatusToast(`⚠️ เสียพลังงาน 1 ดวง! เหลือ ${this.playerLives}/${this.maxLives} ❤️ (${reason})`, true);
    }
  }

  checkIsTopScore() {
    if (this.totalScore <= 0) return false;
    const records = this.loadLeaderboardData(this.gradeLevel);
    if (!records || records.length === 0) {
      return true; // First recorded score is #1
    }
    // Must strictly exceed the benchmark top score established before this run
    if (this.benchmarkTopScore > 0) {
      return this.totalScore > this.benchmarkTopScore;
    }
    // If benchmark was 0 (no other teams on leaderboard), check other records
    const otherRecords = records.filter(r => r.teamName !== this.teamName);
    if (otherRecords.length === 0) return true;
    return this.totalScore > otherRecords[0].score;
  }

  triggerGameOver(reason) {
    if (this.gameEngine) {
      this.gameEngine.isExecuting = false;
      this.gameEngine.isStepMode = false;
      if (this.gameEngine.stepTimeout) {
        clearTimeout(this.gameEngine.stepTimeout);
        this.gameEngine.stepTimeout = null;
      }
      this.gameEngine.resetSimulation();
    }
    this.stopStageTimer();

    if (window.soundEngine) window.soundEngine.playError();

    const modal = document.getElementById('game-over-modal');
    if (!modal) return;

    const reasonElem = document.getElementById('game-over-reason-text');
    if (reasonElem) reasonElem.textContent = reason;

    const scoreElem = document.getElementById('game-over-score-val');
    if (scoreElem) scoreElem.textContent = `${this.totalScore.toLocaleString()} XP`;

    const starsElem = document.getElementById('game-over-stars-val');
    if (starsElem) starsElem.textContent = `${this.totalStars} ⭐`;

    const gradeElem = document.getElementById('game-over-grade-val');
    if (gradeElem) gradeElem.textContent = (this.gradeLevel === 'p5') ? 'ป.5' : 'ป.4';

    // Top Score Check in Challenge Mode:
    // Only allow photo if score strictly exceeds previous top score
    const isTopScore = (this.gameMode === 'CHALLENGE') && this.checkIsTopScore();
    const btnGameOverPhoto = document.getElementById('btn-take-game-over-photo');
    const gameOverTopBanner = document.getElementById('game-over-top-banner');

    if (isTopScore) {
      this.saveLeaderboardEntry(0, 0);
      this.updateTopScoreBanners();

      if (btnGameOverPhoto) {
        btnGameOverPhoto.style.display = 'flex';
        btnGameOverPhoto.innerHTML = `📸 ถ่ายภาพเกียรติยศบันทึกสถิติสูงสุด (${this.totalScore.toLocaleString()} XP)`;
      }
      if (gameOverTopBanner) {
        gameOverTopBanner.style.display = 'block';
        gameOverTopBanner.innerHTML = `👑 ยอดเยี่ยมมาก! คุณทำลายสถิติคะแนนสูงสุดอันดับ 1 ของห้อง (${this.totalScore.toLocaleString()} XP)`;
      }
      if (window.soundEngine) window.soundEngine.playSuccess();
    } else {
      if (btnGameOverPhoto) {
        btnGameOverPhoto.style.display = 'none';
      }
      if (gameOverTopBanner) {
        gameOverTopBanner.style.display = 'none';
      }
    }

    modal.classList.add('active');
  }

  switchWelcomeScreen(screenName) {
    const stepMode = document.getElementById('welcome-step-1');
    const stepPractice = document.getElementById('welcome-step-practice');
    const stepChallenge = document.getElementById('welcome-step-challenge');

    if (stepMode) stepMode.style.display = (screenName === 'mode' || !screenName) ? 'block' : 'none';
    if (stepPractice) stepPractice.style.display = (screenName === 'practice') ? 'block' : 'none';
    if (stepChallenge) stepChallenge.style.display = (screenName === 'challenge') ? 'block' : 'none';

    const welcome = document.getElementById('welcome-screen');
    if (welcome) {
      welcome.classList.remove('hidden');
      welcome.style.display = 'flex';
      welcome.scrollTop = 0;
    }

    if (screenName === 'practice') {
      this.gameMode = 'PRACTICE';
      this.updateGameModeUI();
      this.renderWelcomeCartoonGrid();
    } else if (screenName === 'challenge') {
      this.gameMode = 'CHALLENGE';
      this.updateGameModeUI();
    }
  }

  switchWelcomeStep(stepNumber) {
    if (stepNumber === 'practice' || stepNumber === 2) {
      this.switchWelcomeScreen('practice');
    } else if (stepNumber === 'challenge') {
      this.switchWelcomeScreen('challenge');
    } else {
      this.switchWelcomeScreen('mode');
    }
  }

  async startMission() {
    const teamInput = document.getElementById('input-team-name');
    const driverInput = document.getElementById('input-driver-name');
    const navInput = document.getElementById('input-navigator-name');
    const gradeSelect = document.getElementById('input-grade-level');

    if (teamInput && teamInput.value.trim()) this.teamName = teamInput.value.trim();
    if (driverInput && driverInput.value.trim()) this.driverName = driverInput.value.trim();
    if (navInput && navInput.value.trim()) this.navigatorName = navInput.value.trim();

    // Priority: selectedStartGrade from Welcome selection
    const chosenGrade = this.selectedStartGrade || (gradeSelect ? gradeSelect.value : null) || this.gradeLevel || 'p4';
    this.gradeLevel = chosenGrade;
    this.updateGradeTrack(this.gradeLevel);

    // Immediately hide the welcome screen for instant response
    const welcome = document.getElementById('welcome-screen');
    if (welcome) {
      welcome.classList.add('hidden');
      welcome.style.display = 'none';
    }

    const targetStartLevel = (typeof this.selectedStartLevel === 'number')
      ? this.selectedStartLevel
      : ((this.gameMode === 'PRACTICE' && typeof this.selectedPracticeLevelIndex === 'number')
        ? this.selectedPracticeLevelIndex
        : 0);

    const teamBadge = document.getElementById('team-name-badge');
    if (teamBadge) teamBadge.textContent = `🚀 ทีม: ${this.teamName}`;

    this.updateRoleDisplay();

    if (window.soundEngine) window.soundEngine.playItem();

    this.gameStarted = true;
    this.startRoleTimer();
    this.requestWakeLock();

    this.loadCurrentLevel(targetStartLevel, true);

    if (this.gameMode === 'CHALLENGE') {
      const records = this.loadLeaderboardData(this.gradeLevel);
      this.benchmarkTopScore = (records && records.length > 0) ? records[0].score : 0;
      this.resetLives();
      this.startStageTimer();
    }

    try {
      await this.cameraEngine.startCamera();
    } catch (e) {
      console.warn('Camera failed to start:', e);
      this.showStatusToast('⚠️ ไม่พบกล้อง สลับเข้าสู่โหมดสัมผัส/คลิกปุ่ม 100%', true);
    }
  }

  bindDOMEvents() {
    // Mode Choice Buttons on Welcome Screen: Click -> Switch to dedicated screen
    document.getElementById('btn-choice-mode-practice')?.addEventListener('click', () => {
      if (window.soundEngine) window.soundEngine.playTouch();
      this.switchWelcomeScreen('practice');
      this.speakKnowledgeText('โหมดฝึกซ้อม เลือกชั้นและเลือกระดับด่านได้อิสระ');
    });

    document.getElementById('btn-choice-mode-challenge')?.addEventListener('click', () => {
      if (window.soundEngine) window.soundEngine.playTouch();
      this.switchWelcomeScreen('challenge');
      this.speakKnowledgeText('โหมดแข่งขันประลองความเร็ว ลุย 10 ด่านต่อเนื่อง');
    });

    // Back to Mode Buttons on Sub-screens (Return to Screen 1)
    document.getElementById('btn-practice-back-mode')?.addEventListener('click', () => {
      this.returnToWelcomeScreen();
    });

    document.getElementById('btn-challenge-back-mode')?.addEventListener('click', () => {
      this.returnToWelcomeScreen();
    });

    // Practice Mode Grade Buttons (ป.4 vs ป.5)
    document.getElementById('btn-welcome-grade-p4')?.addEventListener('click', () => {
      if (window.soundEngine) window.soundEngine.playTouch();
      this.selectedStartGrade = 'p4';
      this.updateGradeTrack('p4');
      this.speakKnowledgeText('เลือกชั้นประถมศึกษาปีที่ 4');
    });

    document.getElementById('btn-welcome-grade-p5')?.addEventListener('click', () => {
      if (window.soundEngine) window.soundEngine.playTouch();
      this.selectedStartGrade = 'p5';
      this.updateGradeTrack('p5');
      this.speakKnowledgeText('เลือกชั้นประถมศึกษาปีที่ 5');
    });

    // Challenge Mode Grade Buttons (ป.4 vs ป.5)
    document.getElementById('btn-challenge-grade-p4')?.addEventListener('click', () => {
      if (window.soundEngine) window.soundEngine.playTouch();
      this.selectedStartGrade = 'p4';
      this.updateGradeTrack('p4');
      this.speakKnowledgeText('ประลองระดับชั้นประถมศึกษาปีที่ 4');
    });

    document.getElementById('btn-challenge-grade-p5')?.addEventListener('click', () => {
      if (window.soundEngine) window.soundEngine.playTouch();
      this.selectedStartGrade = 'p5';
      this.updateGradeTrack('p5');
      this.speakKnowledgeText('ประลองระดับชั้นประถมศึกษาปีที่ 5');
    });

    // Start Challenge Direct Button (Always Starts at Level 1)
    document.getElementById('btn-start-challenge-direct')?.addEventListener('click', () => {
      const chalTeam = document.getElementById('input-team-name');
      const chalDriver = document.getElementById('input-driver-name');
      const chalNav = document.getElementById('input-navigator-name');
      if (chalTeam && chalTeam.value.trim()) this.teamName = chalTeam.value.trim();
      if (chalDriver && chalDriver.value.trim()) this.driverName = chalDriver.value.trim();
      if (chalNav && chalNav.value.trim()) this.navigatorName = chalNav.value.trim();

      this.gameMode = 'CHALLENGE';
      this.selectedStartLevel = 0; // Challenge always starts at level 1!
      this.startMission();
    });

    // Level Select Modal Grade Tabs
    document.getElementById('modal-tab-grade-p4')?.addEventListener('click', () => {
      if (window.soundEngine) window.soundEngine.playTouch();
      this.renderCartoonLevelGrid('p4');
    });

    document.getElementById('modal-tab-grade-p5')?.addEventListener('click', () => {
      if (window.soundEngine) window.soundEngine.playTouch();
      this.renderCartoonLevelGrid('p5');
    });

    // Quick Start Practice Button
    document.getElementById('btn-quick-start')?.addEventListener('click', () => {
      this.gameMode = 'PRACTICE';
      this.startMission();
    });

    document.getElementById('nav-mode-pill')?.addEventListener('click', () => {
      const nextMode = (this.gameMode === 'PRACTICE') ? 'CHALLENGE' : 'PRACTICE';
      this.setGameMode(nextMode);
    });

    document.getElementById('btn-open-welcome')?.addEventListener('click', () => {
      this.returnToWelcomeScreen();
    });

    document.getElementById('btn-prev-level')?.addEventListener('click', () => {
      if (this.currentLevelIndex > 0) {
        this.loadCurrentLevel(this.currentLevelIndex - 1, true);
      }
    });

    document.getElementById('btn-next-level')?.addEventListener('click', () => {
      if (this.currentLevelIndex < this.currentLevels.length - 1) {
        this.loadCurrentLevel(this.currentLevelIndex + 1, true);
      }
    });

    document.getElementById('btn-run-code')?.addEventListener('click', () => {
      if (window.soundEngine) window.soundEngine.playTouch();
      this.gameEngine.setCode(this.codeSequence);
      this.gameEngine.runAll();
    });

    document.getElementById('btn-step-code')?.addEventListener('click', () => {
      if (window.soundEngine) window.soundEngine.playTouch();
      this.gameEngine.setCode(this.codeSequence);
      this.gameEngine.executeSingleStep();
    });

    document.getElementById('btn-reset-sim')?.addEventListener('click', () => {
      if (window.soundEngine) window.soundEngine.playTouch();
      if (this.gameEngine) {
        this.gameEngine.isExecuting = false;
        this.gameEngine.isStepMode = false;
        if (this.gameEngine.stepTimeout) {
          clearTimeout(this.gameEngine.stepTimeout);
          this.gameEngine.stepTimeout = null;
        }
        this.gameEngine.resetSimulation();
      }
      this.highlightActiveChip(-1);
      this.showStatusToast('🔄 รีเซ็ตตำแหน่งหุ่นยนต์เรียบร้อย', false);
    });

    document.getElementById('btn-clear-code')?.addEventListener('click', () => {
      if (this.codeSequence && this.codeSequence.length > 0) {
        this.lastDeletedCode = JSON.parse(JSON.stringify(this.codeSequence));
      }
      if (window.soundEngine) window.soundEngine.playError();
      if (this.gameEngine) {
        this.gameEngine.isExecuting = false;
        if (this.gameEngine.stepTimeout) {
          clearTimeout(this.gameEngine.stepTimeout);
          this.gameEngine.stepTimeout = null;
        }
        this.gameEngine.resetSimulation();
      }
      this.currentRecordingLoop = null;
      if (this.cameraEngine) {
        this.cameraEngine.isLoopRecordingMode = false;
        this.cameraEngine.awaitingLoopIteration = false;
      }
      this.codeSequence = [];
      this.renderTimeline();
      this.highlightActiveChip(-1);
      this.showUndoToast('ล้างบล็อกคำสั่งทั้งหมดแล้ว');
    });

    document.getElementById('btn-toggle-camera-mode')?.addEventListener('click', (e) => {
      if (!this.cameraEngine) return;
      this.cameraEngine.isDetectionEnabled = !this.cameraEngine.isDetectionEnabled;
      const enabled = this.cameraEngine.isDetectionEnabled;
      e.currentTarget.innerHTML = enabled ? '📷 ตรวจจับ: เปิด' : '📷 ตรวจจับ: ปิด';
      if (enabled) {
        e.currentTarget.classList.remove('btn-danger');
        e.currentTarget.classList.add('btn-secondary');
      } else {
        e.currentTarget.classList.remove('btn-secondary');
        e.currentTarget.classList.add('btn-danger');
      }
    });

    document.getElementById('btn-open-knowledge')?.addEventListener('click', () => {
      this.showKnowledgeModal();
    });

    document.getElementById('btn-close-knowledge')?.addEventListener('click', () => {
      this.cancelSpeech();
      this.closeModal('knowledge-modal');
    });

    document.getElementById('btn-start-knowledge')?.addEventListener('click', () => {
      this.cancelSpeech();
      this.closeModal('knowledge-modal');
    });

    const toggleAutoSpeak = document.getElementById('toggle-auto-speak');
    if (toggleAutoSpeak) {
      toggleAutoSpeak.checked = this.autoSpeakKnowledge;
      toggleAutoSpeak.addEventListener('change', (e) => {
        this.autoSpeakKnowledge = e.target.checked;
        localStorage.setItem('codebot_ar_auto_speak', e.target.checked ? 'true' : 'false');
      });
    }

    const speedSelect = document.getElementById('select-tts-speed');
    if (speedSelect) {
      const savedSpeedMode = localStorage.getItem('codebot_ar_tts_speed_mode') || 'normal';
      speedSelect.value = savedSpeedMode;
      this.ttsSpeedMode = savedSpeedMode;

      speedSelect.addEventListener('change', (e) => {
        this.ttsSpeedMode = e.target.value;
        localStorage.setItem('codebot_ar_tts_speed_mode', this.ttsSpeedMode);
        const labels = { slow: '🐢 ช้า (ชัดเจน)', normal: '🚶 ปกติ (พอดีคำ)', fast: '🐇 เร็ว (กระชับ)' };
        this.showStatusToast(`⚡ ความเร็วเสียง: ${labels[this.ttsSpeedMode] || this.ttsSpeedMode}`, false);

        if ('speechSynthesis' in window && window.speechSynthesis.speaking) {
          const level = this.currentLevels[this.currentLevelIndex];
          if (level && level.knowledge) {
            const textToSpeak = level.knowledge.ttsNarration || `${level.knowledge.title}. ${level.knowledge.description}. ${level.knowledge.takeaway}`;
            this.speakKnowledgeText(textToSpeak);
          }
        }
      });
    }

    document.getElementById('btn-speak-knowledge')?.addEventListener('click', () => {
      if ('speechSynthesis' in window && window.speechSynthesis.speaking) {
        this.cancelSpeech();
      } else {
        const level = this.currentLevels[this.currentLevelIndex];
        if (level && level.knowledge) {
          const textToSpeak = level.knowledge.ttsNarration || `${level.knowledge.title}. ${level.knowledge.description}. ${level.knowledge.takeaway}`;
          this.speakKnowledgeText(textToSpeak);
        }
      }
    });

    document.getElementById('btn-victory-next')?.addEventListener('click', () => {
      this.advanceToNextLevel();
    });

    document.getElementById('btn-take-winner-photo')?.addEventListener('click', () => {
      if (this.victoryTimer) {
        clearInterval(this.victoryTimer);
        this.victoryTimer = null;
      }
      this.cancelSpeech();
      this.isGameOverPhoto = false;
      this.openWinnerPhotoModal();
    });

    // Game Over Modal Action buttons
    document.getElementById('btn-close-game-over')?.addEventListener('click', () => {
      this.closeModal('game-over-modal');
    });

    document.getElementById('btn-retry-mission')?.addEventListener('click', () => {
      this.closeModal('game-over-modal');
      this.loadCurrentLevel(this.currentLevelIndex, false);
      if (this.gameMode === 'CHALLENGE') {
        const records = this.loadLeaderboardData(this.gradeLevel);
        this.benchmarkTopScore = (records && records.length > 0) ? records[0].score : 0;
        this.resetLives();
        this.startStageTimer();
      }
      this.showStatusToast('🔄 เริ่มท้าทายด่านนี้ใหม่อีกครั้ง!', false);
    });

    document.getElementById('btn-switch-to-practice')?.addEventListener('click', () => {
      this.closeModal('game-over-modal');
      this.setGameMode('PRACTICE');
      this.loadCurrentLevel(this.currentLevelIndex, false);
    });

    document.getElementById('btn-take-game-over-photo')?.addEventListener('click', () => {
      this.closeModal('game-over-modal');
      this.isGameOverPhoto = true;
      this.openWinnerPhotoModal();
    });

    // Certificate buttons
    document.getElementById('btn-victory-cert')?.addEventListener('click', () => {
      if (this.victoryTimer) {
        clearInterval(this.victoryTimer);
        this.victoryTimer = null;
      }
      this.cancelSpeech();
      this.openCertificateModal();
    });

    document.getElementById('btn-open-certificate')?.addEventListener('click', () => {
      this.openCertificateModal();
    });

    document.getElementById('btn-close-certificate')?.addEventListener('click', () => {
      this.closeModal('certificate-modal');
    });

    document.getElementById('btn-print-certificate')?.addEventListener('click', () => {
      this.printCertificate();
    });

    document.getElementById('btn-download-cert-png')?.addEventListener('click', () => {
      this.downloadCertificatePNG();
    });

    document.getElementById('btn-cert-home')?.addEventListener('click', () => {
      this.returnToWelcomeScreen();
    });

    document.getElementById('btn-close-winner-photo')?.addEventListener('click', () => {
      this.closeModal('winner-photo-modal');
    });

    document.getElementById('btn-retake-photo')?.addEventListener('click', () => {
      this.captureWinnerPhoto();
    });

    document.getElementById('btn-download-winner-photo')?.addEventListener('click', () => {
      this.downloadWinnerPhoto();
    });

    document.getElementById('btn-use-photo-in-cert')?.addEventListener('click', () => {
      this.closeModal('winner-photo-modal');
      this.openCertificateModal();
    });

    // Leaderboard buttons
    document.getElementById('btn-open-leaderboard')?.addEventListener('click', () => {
      this.openLeaderboardModal(this.gradeLevel);
    });

    document.getElementById('nav-top-score-pill')?.addEventListener('click', () => {
      this.openLeaderboardModal(this.gradeLevel);
    });

    document.getElementById('btn-close-leaderboard')?.addEventListener('click', () => {
      this.closeModal('leaderboard-modal');
    });

    document.getElementById('tab-lb-p4')?.addEventListener('click', () => {
      this.openLeaderboardModal('p4');
    });

    document.getElementById('tab-lb-p5')?.addEventListener('click', () => {
      this.openLeaderboardModal('p5');
    });

    document.getElementById('btn-export-csv')?.addEventListener('click', () => {
      this.exportResearchCSV();
    });

    document.getElementById('btn-clear-leaderboard')?.addEventListener('click', () => {
      this.clearClassroomLeaderboard();
    });

    document.getElementById('btn-swap-role')?.addEventListener('click', () => {
      this.swapPairRoles();
    });

    document.getElementById('btn-toggle-sound')?.addEventListener('click', (e) => {
      const isMuted = window.soundEngine.toggleMute();
      e.currentTarget.innerHTML = isMuted ? '🔇' : '🔊';
      e.currentTarget.title = isMuted ? 'เสียง: ปิด' : 'เสียง: เปิด';
      const menuSoundBtn = document.getElementById('btn-menu-toggle-sound');
      if (menuSoundBtn) {
        menuSoundBtn.textContent = isMuted ? '🔇 เสียง: ปิด' : '🔊 เสียง: เปิด';
      }
    });

    // Game Menu & Cartoon Level Selector Modal (Reference Image Match)
    document.getElementById('btn-open-game-menu')?.addEventListener('click', () => {
      if (window.soundEngine) window.soundEngine.playTouch();
      this.openGameMenu('levels');
    });

    document.getElementById('btn-quick-menu')?.addEventListener('click', () => {
      if (window.soundEngine) window.soundEngine.playTouch();
      this.openGameMenu('levels');
    });

    document.getElementById('btn-menu-level-back')?.addEventListener('click', () => {
      if (window.soundEngine) window.soundEngine.playTouch();
      this.closeGameMenu();
    });

    document.getElementById('btn-close-level-select')?.addEventListener('click', () => {
      this.closeGameMenu();
    });

    document.getElementById('btn-close-game-menu')?.addEventListener('click', () => {
      this.closeGameMenu();
    });

    document.getElementById('btn-menu-resume')?.addEventListener('click', () => {
      if (window.soundEngine) window.soundEngine.playTouch();
      this.closeGameMenu();
    });

    // Universal Return to Home handler (Header, Menu modal, Victory modal, Game over modal, Leaderboard, Cert, etc.)
    const handleReturnHome = (e) => {
      if (e) e.stopPropagation();
      if (window.soundEngine) window.soundEngine.playTouch();
      this.returnToWelcomeScreen();
    };

    [
      'btn-menu-back-home',
      'btn-top-menu-back-home',
      'btn-header-back-home',
      'header-brand-home',
      'btn-quick-home',
      'btn-practice-back-mode',
      'btn-challenge-back-mode',
      'btn-cert-home',
      'btn-victory-home',
      'btn-game-over-home',
      'btn-leaderboard-home',
      'btn-open-welcome'
    ].forEach(id => {
      document.getElementById(id)?.addEventListener('click', handleReturnHome);
    });

    document.querySelectorAll('.action-go-home').forEach(el => {
      el.addEventListener('click', handleReturnHome);
    });

    document.getElementById('btn-menu-toggle-sound')?.addEventListener('click', (e) => {
      const isMuted = window.soundEngine.toggleMute();
      const soundIcon = document.getElementById('menu-sound-icon');
      if (soundIcon) soundIcon.textContent = isMuted ? '🔇' : '🔊';
      const topSoundBtn = document.getElementById('btn-toggle-sound');
      if (topSoundBtn) {
        topSoundBtn.innerHTML = isMuted ? '🔇' : '🔊';
        topSoundBtn.title = isMuted ? 'เสียง: ปิด' : 'เสียง: เปิด';
      }
    });

    document.getElementById('btn-toggle-wakelock')?.addEventListener('click', () => {
      if (window.soundEngine) window.soundEngine.playTouch();
      this.toggleWakeLock();
    });

    document.getElementById('btn-menu-toggle-wakelock')?.addEventListener('click', () => {
      if (window.soundEngine) window.soundEngine.playTouch();
      this.toggleWakeLock();
    });

    document.getElementById('btn-menu-restart-level')?.addEventListener('click', () => {
      if (window.soundEngine) window.soundEngine.playTouch();
      this.closeGameMenu();
      this.loadCurrentLevel(this.currentLevelIndex, false);
      this.showStatusToast('🔄 เริ่มเล่นด่านนี้ใหม่อีกครั้ง!', false);
    });

    document.querySelectorAll('.modal-overlay').forEach(modal => {
      modal.addEventListener('click', (e) => {
        if (e.target === modal) {
          if (modal.id === 'knowledge-modal') this.cancelSpeech();
          if (modal.id === 'game-menu-modal') this.closeGameMenu();
          else modal.classList.remove('active');
        }
      });
    });
  }

  loadCurrentLevel(index, showModal = true) {
    if (this.victoryTimer) {
      clearInterval(this.victoryTimer);
      this.victoryTimer = null;
    }
    this.currentLevelIndex = index;
    const level = this.currentLevels[index];
    if (!level) return;

    if (level.prefilledCode && level.prefilledCode.length > 0) {
      this.codeSequence = JSON.parse(JSON.stringify(level.prefilledCode));
    } else {
      this.codeSequence = [];
    }

    this.currentRecordingLoop = null;
    if (this.cameraEngine) {
      this.cameraEngine.isLoopRecordingMode = false;
      this.cameraEngine.awaitingLoopIteration = false;
    }

    this.gameEngine.loadLevel(level);
    this.gameEngine.setCode(this.codeSequence);

    this.cameraEngine.setAvailableBlocks(level.availableBlocks);

    const gradeLabel = this.gradeLevel === 'p5' ? 'ป.5' : 'ป.4';
    const titleElem = document.getElementById('level-title-display');
    if (titleElem) titleElem.textContent = `[${gradeLabel}] ภารกิจที่ ${index + 1}/${this.currentLevels.length}: ${level.title}`;
    const conceptElem = document.getElementById('level-concept-badge');
    if (conceptElem) conceptElem.textContent = level.conceptBadge;
    const goalElem = document.getElementById('mission-goal-desc') || document.getElementById('level-hint-text');
    if (goalElem) goalElem.textContent = `ภารกิจ: ${level.hint || level.description || ''}`;

    const prevBtn = document.getElementById('btn-prev-level');
    const nextBtn = document.getElementById('btn-next-level');
    if (prevBtn) prevBtn.disabled = (index === 0);
    if (nextBtn) nextBtn.disabled = (index === this.currentLevels.length - 1);

    this.updatePracticeLevelHighlight(index);

    this.renderBottomTouchButtons(level.availableBlocks);
    this.renderTimeline();

    if (this.gameMode === 'CHALLENGE') {
      this.resetLives();
      this.startStageTimer();
    }

    if (showModal) {
      this.showKnowledgeModal();
    }
  }

  renderBottomTouchButtons(availableBlockIds) {
    const container = document.getElementById('ar-bottom-buttons') || document.getElementById('touch-blocks-container');
    if (!container) return;

    container.innerHTML = '';

    // Separate into Directional/Motion blocks and Action/Loop blocks
    const motionOrder = ['TURN_LEFT', 'FORWARD', 'TURN_RIGHT'];
    const motionBlocks = [];
    const actionBlocks = [];

    // Spatial order: Left -> Forward -> Right
    motionOrder.forEach(id => {
      if (availableBlockIds.includes(id)) {
        motionBlocks.push(id);
      }
    });

    // Action blocks (loops, keys)
    availableBlockIds.forEach(id => {
      if (!motionOrder.includes(id)) {
        actionBlocks.push(id);
      }
    });

    // Always guarantee LOOP_CUSTOM is available as an accessible touch button
    if (!actionBlocks.some(id => id.startsWith('LOOP'))) {
      actionBlocks.push('LOOP_CUSTOM');
    }

    const createControllerButton = (blockId, isDpad = false) => {
      const meta = window.BLOCK_CATALOG[blockId];
      if (!meta) return null;

      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = `ctrl-btn ${isDpad ? 'dpad-btn' : 'action-btn'} block-${meta.type} block-${blockId.toLowerCase()}`;
      btn.setAttribute('data-block-id', blockId);
      btn.title = `คลิกเพื่อใส่คำสั่ง "${meta.label || meta.shortLabel}"`;

      let iconHTML = `<span class="ctrl-icon">${meta.icon}</span>`;
      if (blockId === 'FORWARD') {
        iconHTML = `<span class="ctrl-icon dpad-icon-forward">▲</span>`;
      } else if (blockId === 'TURN_LEFT') {
        iconHTML = `<span class="ctrl-icon dpad-icon-turn">⤹</span>`;
      } else if (blockId === 'TURN_RIGHT') {
        iconHTML = `<span class="ctrl-icon dpad-icon-turn">⤸</span>`;
      }

      btn.innerHTML = `
        ${iconHTML}
        <span class="ctrl-label">${meta.shortLabel}</span>
      `;

      btn.addEventListener('click', () => {
        this.handleBlockAction(blockId);
      });

      return btn;
    };

    const pod = document.createElement('div');
    pod.className = 'game-controller-pod';

    // 1. D-PAD Deck (Motion: Left, Forward, Right)
    if (motionBlocks.length > 0) {
      const dpadDeck = document.createElement('div');
      dpadDeck.className = 'controller-deck dpad-deck';
      
      const badge = document.createElement('span');
      badge.className = 'deck-title-badge dpad-badge';
      badge.textContent = '🎮 ทิศทาง';
      dpadDeck.appendChild(badge);

      const dpadButtonsWrap = document.createElement('div');
      dpadButtonsWrap.className = 'deck-buttons dpad-buttons-wrap';

      motionBlocks.forEach(id => {
        const btn = createControllerButton(id, true);
        if (btn) dpadButtonsWrap.appendChild(btn);
      });

      dpadDeck.appendChild(dpadButtonsWrap);
      pod.appendChild(dpadDeck);
    }

    // 2. Action Deck (Loops & Keys)
    if (actionBlocks.length > 0) {
      const actionDeck = document.createElement('div');
      actionDeck.className = 'controller-deck action-deck';

      const badge = document.createElement('span');
      badge.className = 'deck-title-badge action-badge';
      badge.textContent = '⚡ แอ็กชัน';
      actionDeck.appendChild(badge);

      const actionButtonsWrap = document.createElement('div');
      actionButtonsWrap.className = 'deck-buttons action-buttons-wrap';

      actionBlocks.forEach(id => {
        const btn = createControllerButton(id, false);
        if (btn) actionButtonsWrap.appendChild(btn);
      });

      actionDeck.appendChild(actionButtonsWrap);
      pod.appendChild(actionDeck);
    }

    container.appendChild(pod);
  }

  updateGestureGuideBar() {
    const bar = document.getElementById('gesture-guide-bar');
    if (!bar) return;

    bar.innerHTML = `
      <div class="guide-chip"><span class="chip-badge">☝️ 1 นิ้ว</span> เดินหน้า</div>
      <div class="guide-chip" style="border-color: rgba(56, 189, 248, 0.4);"><span class="chip-badge" style="background: rgba(56, 189, 248, 0.2); color: #38bdf8;">🖐️ มือซ้าย</span> หันซ้าย</div>
      <div class="guide-chip" style="border-color: rgba(251, 191, 36, 0.4);"><span class="chip-badge" style="background: rgba(251, 191, 36, 0.2); color: #fbbf24;">🖐️ มือขวา</span> หันขวา</div>
      <div class="guide-chip" style="border-color: rgba(168, 85, 247, 0.4);"><span class="chip-badge" style="background: rgba(168, 85, 247, 0.2); color: #c084fc;">🤟 3 นิ้ว</span> เปิด/ปิดลูป</div>
      <div class="guide-chip" style="border-color: rgba(236, 72, 153, 0.4);"><span class="chip-badge" style="background: rgba(236, 72, 153, 0.2); color: #f472b6;">🫰 มินิฮาร์ท</span> รันโค้ด</div>
      <div class="guide-chip" style="border-color: rgba(239, 68, 68, 0.4);"><span class="chip-badge" style="background: rgba(239, 68, 68, 0.2); color: #f87171;">🙅 กากบาท</span> รีเซ็ต</div>
      <div class="guide-chip" style="border-color: rgba(245, 158, 11, 0.4);"><span class="chip-badge" style="background: rgba(245, 158, 11, 0.2); color: #fbbf24;">👎 คว่ำมือ</span> ลบล่าสุด</div>
    `;
  }

  handleBlockAction(blockId) {
    if (this.gameEngine.isExecuting) return;

    const meta = window.BLOCK_CATALOG[blockId];
    if (!meta) return;

    if (window.soundEngine) window.soundEngine.playGrab();

    // If currently recording inside a loop
    if (this.currentRecordingLoop) {
      if (blockId === 'FORWARD' || blockId === 'TURN_LEFT' || blockId === 'TURN_RIGHT' || blockId === 'USE_KEY') {
        if (!this.currentRecordingLoop.subActions) this.currentRecordingLoop.subActions = [];
        this.currentRecordingLoop.subActions.push(blockId);
        this.showStatusToast(`➕ เพิ่ม [${meta.shortLabel}] ในกล่องวนซ้ำ (${this.currentRecordingLoop.subActions.length} คำสั่ง)`, false);
        this.renderTimeline();
        return;
      }
    }

    if (meta.type === 'loop' || blockId === 'LOOP_CUSTOM' || blockId.startsWith('LOOP_')) {
      let iter = 5;
      if (blockId === 'LOOP_2') iter = 2;
      else if (blockId === 'LOOP_3') iter = 3;
      else if (blockId === 'LOOP_4') iter = 4;
      else if (blockId === 'LOOP_5') iter = 5;

      this.codeSequence.push({
        id: 'step_' + Date.now() + '_' + Math.random().toString(36).substr(2, 4),
        type: 'loop',
        action: 'LOOP_CUSTOM',
        iterations: iter,
        subActions: ['FORWARD']
      });
      this.showStatusToast(`➕ เพิ่ม [กล่องวนซ้ำ ${iter}x] ปรับแต่งคำสั่งภายในได้เลย!`, false);
    } else {
      this.codeSequence.push({
        id: 'step_' + Date.now() + '_' + Math.random().toString(36).substr(2, 4),
        action: blockId
      });
      this.showStatusToast(`➕ เพิ่มคำสั่ง [${meta.shortLabel}] ในโปรแกรมแล้ว`, false);
    }

    this.renderTimeline();
  }

  moveBlock(fromIdx, toIdx) {
    if (this.gameEngine && this.gameEngine.isExecuting) return;
    if (fromIdx < 0 || fromIdx >= this.codeSequence.length) return;
    if (toIdx < 0 || toIdx >= this.codeSequence.length) return;
    if (fromIdx === toIdx) return;

    const [movedItem] = this.codeSequence.splice(fromIdx, 1);
    this.codeSequence.splice(toIdx, 0, movedItem);

    if (window.soundEngine) window.soundEngine.playTouch();
    this.renderTimeline();
    this.gameEngine.resetSimulation();
    this.showStatusToast(`↕️ สลับคำสั่งที่ ${fromIdx + 1} ➔ ${toIdx + 1} สำเร็จ`, false);
  }

  moveSubAction(loopIdx, fromSubIdx, toSubIdx) {
    if (this.gameEngine && this.gameEngine.isExecuting) return;
    const loopItem = this.codeSequence[loopIdx];
    if (!loopItem || !loopItem.subActions) return;
    if (fromSubIdx < 0 || fromSubIdx >= loopItem.subActions.length) return;
    if (toSubIdx < 0 || toSubIdx >= loopItem.subActions.length) return;
    if (fromSubIdx === toSubIdx) return;

    const [movedSub] = loopItem.subActions.splice(fromSubIdx, 1);
    loopItem.subActions.splice(toSubIdx, 0, movedSub);

    if (window.soundEngine) window.soundEngine.playTouch();
    this.renderTimeline();
    this.gameEngine.resetSimulation();
  }

  removeLastBlock() {
    if (this.gameEngine && this.gameEngine.isExecuting) {
      this.gameEngine.isExecuting = false;
      if (this.gameEngine.stepTimeout) {
        clearTimeout(this.gameEngine.stepTimeout);
        this.gameEngine.stepTimeout = null;
      }
      this.gameEngine.resetSimulation();
    }

    // If currently recording inside a loop
    if (this.currentRecordingLoop && this.currentRecordingLoop.subActions) {
      if (this.currentRecordingLoop.subActions.length > 0) {
        const removedSub = this.currentRecordingLoop.subActions.pop();
        const subMeta = window.BLOCK_CATALOG[removedSub];
        this.showStatusToast(`👎 ลบคำสั่ง [${subMeta ? subMeta.shortLabel : removedSub}] ออกจากลูปแล้ว`, false);
        this.renderTimeline();
        return;
      } else {
        // subActions is empty, pop the entire loop
        const loopIdx = this.codeSequence.indexOf(this.currentRecordingLoop);
        if (loopIdx !== -1) {
          this.codeSequence.splice(loopIdx, 1);
        } else {
          this.codeSequence.pop();
        }
        this.currentRecordingLoop = null;
        if (this.cameraEngine) {
          this.cameraEngine.isLoopRecordingMode = false;
          this.cameraEngine.awaitingLoopIteration = false;
        }
        this.showStatusToast(`👎 ยกเลิกการสร้างกล่องลูปแล้ว`, false);
        this.renderTimeline();
        return;
      }
    }

    if (this.codeSequence.length === 0) {
      this.showStatusToast('⚠️ ไม่มีคำสั่งให้ลบแล้ว', true);
      return;
    }
    const removed = this.codeSequence.pop();
    const meta = window.BLOCK_CATALOG[removed.action];
    this.showStatusToast(`👎 ลบคำสั่ง [${meta ? meta.shortLabel : (removed.type === 'loop' ? 'กล่องวนซ้ำ' : removed.action)}] ออกแล้ว`, false);
    this.renderTimeline();
    this.gameEngine.resetSimulation();
  }

  startLoopRecordingMode() {
    if (this.gameEngine && this.gameEngine.isExecuting) return;
    const newLoop = {
      id: 'step_' + Date.now() + '_' + Math.random().toString(36).substr(2, 4),
      type: 'loop',
      action: 'LOOP_CUSTOM',
      iterations: 5,
      subActions: [],
      isRecording: true
    };
    this.codeSequence.push(newLoop);
    this.currentRecordingLoop = newLoop;
    if (window.soundEngine) window.soundEngine.playGrab();
    this.renderTimeline();
    this.showStatusToast('🔁 เริ่มบันทึกคำสั่งในลูป (ตั้ง 5x ไว้ก่อน)! ชูนิ้วสั่งเดินหน้า/เลี้ยว (เสร็จแล้วชู 3 นิ้ว)', false);
  }

  finishLoopRecordingMode() {
    if (this.currentRecordingLoop) {
      if (!this.currentRecordingLoop.subActions || this.currentRecordingLoop.subActions.length === 0) {
        this.currentRecordingLoop.subActions = ['FORWARD'];
      }
      this.currentRecordingLoop.isRecording = false;
      if (!this.currentRecordingLoop.iterations) {
        this.currentRecordingLoop.iterations = 5;
      }
    }
    if (window.soundEngine) window.soundEngine.playTouch();
    this.renderTimeline();
    this.showStatusToast('✅ ปิดลูปเรียบร้อย (ตั้ง 5x ไว้แล้ว หรือชูนิ้ว 2-5 นิ้วเพื่อเปลี่ยนรอบ)', false);
  }

  setLoopRecordingIterations(iter) {
    if (this.currentRecordingLoop) {
      this.currentRecordingLoop.iterations = iter;
      this.currentRecordingLoop.isRecording = false;
      this.currentRecordingLoop = null;
    } else {
      for (let i = this.codeSequence.length - 1; i >= 0; i--) {
        if (this.codeSequence[i].type === 'loop' || this.codeSequence[i].action === 'LOOP_CUSTOM') {
          this.codeSequence[i].iterations = iter;
          this.codeSequence[i].isRecording = false;
          break;
        }
      }
    }
    if (window.soundEngine) window.soundEngine.playSuccess();
    this.renderTimeline();
    this.showStatusToast(`🎉 บันทึกลูปสำเร็จ: ทำซ้ำ ${iter} รอบ!`, false);
  }

  renderTimeline() {
    const container = document.getElementById('code-sequence-list');
    if (!container) return;

    if (this.codeSequence.length === 0) {
      container.innerHTML = `<div class="empty-sequence-hint">ยังไม่มีคำสั่งโปรแกรม<br>ทำท่าทางหน้ากล้อง หรือคลิกปุ่มด้านล่างเพื่อเพิ่มคำสั่ง</div>`;
      return;
    }

    container.innerHTML = '';
    this.codeSequence.forEach((item, idx) => {
      const isLoop = (item.type === 'loop' || item.action === 'LOOP_CUSTOM' || item.subActions);

      if (isLoop) {
        const loopChip = document.createElement('div');
        const isRec = (item.isRecording || item === this.currentRecordingLoop);
        loopChip.className = `chip-loop-container ${item.bug ? 'chip-bug' : ''} ${isRec ? 'chip-loop-recording' : ''}`;
        loopChip.id = `chip-${idx}`;
        loopChip.draggable = true;
        loopChip.setAttribute('data-index', idx);

        const iter = item.iterations || 5;
        const subActs = item.subActions || ['FORWARD'];

        let subChipsHtml = '';
        if (subActs.length === 0) {
          subChipsHtml = '<div style="color: #c084fc; font-size: 0.82rem; font-style: italic; padding: 4px 6px;">(กำลังรอคำสั่ง... ชูนิ้วเดินหน้า/เลี้ยว หรือกดปุ่ม + ด้านล่าง)</div>';
        } else {
          subActs.forEach((sa, sIdx) => {
            const sMeta = window.BLOCK_CATALOG[sa] || { icon: '👉', shortLabel: sa };
            subChipsHtml += `
              <div class="loop-sub-chip" id="chip-${idx}-sub-${sIdx}">
                <span class="sub-move-btn sub-move-left" data-loop-idx="${idx}" data-sub-from="${sIdx}" data-sub-to="${sIdx - 1}" title="เลื่อนซ้าย" ${sIdx === 0 ? 'style="opacity:0.25;cursor:default;"' : ''}>◀</span>
                <span>${sMeta.icon} ${sMeta.shortLabel}</span>
                <span class="sub-move-btn sub-move-right" data-loop-idx="${idx}" data-sub-from="${sIdx}" data-sub-to="${sIdx + 1}" title="เลื่อนขวา" ${sIdx === subActs.length - 1 ? 'style="opacity:0.25;cursor:default;"' : ''}>▶</span>
                <span class="sub-delete-btn" data-loop-idx="${idx}" data-sub-idx="${sIdx}" title="ลบคำสั่งนี้ในลูป">✕</span>
              </div>
            `;
          });
        }

        loopChip.innerHTML = `
          <div class="loop-header">
            <span class="chip-drag-handle" title="คลิกลากเพื่อสลับลำดับคำสั่ง">⋮⋮</span>
            <span class="chip-line-no">${idx + 1}</span>
            <span class="loop-icon">🔁</span>
            <span class="loop-title">วนซ้ำ</span>
            ${isRec ? '<span class="loop-rec-badge" style="background:#ef4444; color:#fff; font-size:10px; padding:2px 7px; border-radius:999px; font-weight:bold;">🔴 กำลังบันทึก</span>' : ''}
            <div class="loop-iter-selector">
              <button class="iter-btn ${iter === 2 ? 'active' : ''}" data-loop-idx="${idx}" data-times="2">2x</button>
              <button class="iter-btn ${iter === 3 ? 'active' : ''}" data-loop-idx="${idx}" data-times="3">3x</button>
              <button class="iter-btn ${iter === 4 ? 'active' : ''}" data-loop-idx="${idx}" data-times="4">4x</button>
              <button class="iter-btn ${iter === 5 ? 'active' : ''}" data-loop-idx="${idx}" data-times="5">5x</button>
            </div>
            <div class="chip-actions-group">
              <button class="chip-move-btn btn-move-up" data-from="${idx}" data-to="${idx - 1}" title="เลื่อนขึ้น" ${idx === 0 ? 'disabled style="opacity:0.25;cursor:default;"' : ''}>⬆️</button>
              <button class="chip-move-btn btn-move-down" data-from="${idx}" data-to="${idx + 1}" title="เลื่อนลง" ${idx === this.codeSequence.length - 1 ? 'disabled style="opacity:0.25;cursor:default;"' : ''}>⬇️</button>
              <div class="delete-chip-btn" data-loop-idx="${idx}" title="ลบลูปนี้">✕</div>
            </div>
          </div>
          <div class="loop-inner-body">
            <div class="loop-sub-chips">${subChipsHtml}</div>
            <div class="loop-add-sub-actions">
              <span class="add-sub-label">+ ใส่ในลูป:</span>
              <button class="btn-sub-add" data-loop-idx="${idx}" data-add="FORWARD">⬆️ เดินหน้า</button>
              <button class="btn-sub-add" data-loop-idx="${idx}" data-add="TURN_LEFT">↩️ หันซ้าย</button>
              <button class="btn-sub-add" data-loop-idx="${idx}" data-add="TURN_RIGHT">↪️ หันขวา</button>
              <button class="btn-sub-add" data-loop-idx="${idx}" data-add="USE_KEY">🔑 ไขกุญแจ</button>
            </div>
          </div>
        `;

        this.attachChipDragAndDrop(loopChip, idx);

        loopChip.querySelectorAll('.iter-btn').forEach(b => {
          b.addEventListener('click', (e) => {
            e.stopPropagation();
            if (this.gameEngine.isExecuting) return;
            item.iterations = parseInt(b.getAttribute('data-times'), 10) || 5;
            if (window.soundEngine) window.soundEngine.playTouch();
            this.renderTimeline();
          });
        });

        loopChip.querySelectorAll('.sub-move-btn').forEach(b => {
          b.addEventListener('click', (e) => {
            e.stopPropagation();
            const lIdx = parseInt(b.getAttribute('data-loop-idx'), 10);
            const fromS = parseInt(b.getAttribute('data-sub-from'), 10);
            const toS = parseInt(b.getAttribute('data-sub-to'), 10);
            this.moveSubAction(lIdx, fromS, toS);
          });
        });

        loopChip.querySelectorAll('.sub-delete-btn').forEach(b => {
          b.addEventListener('click', (e) => {
            e.stopPropagation();
            if (this.gameEngine.isExecuting) return;
            const sIdx = parseInt(b.getAttribute('data-sub-idx'), 10);
            if (item.subActions && item.subActions.length > 1) {
              item.subActions.splice(sIdx, 1);
            } else {
              this.showStatusToast('⚠️ ในลูปต้องมีคำสั่งอย่างน้อย 1 อย่างนะ', true);
            }
            if (window.soundEngine) window.soundEngine.playError();
            this.renderTimeline();
          });
        });

        loopChip.querySelectorAll('.btn-sub-add').forEach(b => {
          b.addEventListener('click', (e) => {
            e.stopPropagation();
            if (this.gameEngine.isExecuting) return;
            const addAct = b.getAttribute('data-add');
            if (!item.subActions) item.subActions = [];
            item.subActions.push(addAct);
            if (window.soundEngine) window.soundEngine.playGrab();
            this.renderTimeline();
          });
        });

        loopChip.querySelector('.btn-move-up')?.addEventListener('click', (e) => {
          e.stopPropagation();
          this.moveBlock(idx, idx - 1);
        });

        loopChip.querySelector('.btn-move-down')?.addEventListener('click', (e) => {
          e.stopPropagation();
          this.moveBlock(idx, idx + 1);
        });

        loopChip.querySelector('.delete-chip-btn')?.addEventListener('click', (e) => {
          e.stopPropagation();
          if (this.gameEngine && this.gameEngine.isExecuting) {
            this.gameEngine.isExecuting = false;
            if (this.gameEngine.stepTimeout) {
              clearTimeout(this.gameEngine.stepTimeout);
              this.gameEngine.stepTimeout = null;
            }
            this.gameEngine.resetSimulation();
          }
          this.codeSequence.splice(idx, 1);
          this.renderTimeline();
          this.gameEngine.resetSimulation();
        });

        container.appendChild(loopChip);
      } else {
        const meta = window.BLOCK_CATALOG[item.action];
        if (!meta) return;

        const chip = document.createElement('div');
        chip.className = `code-chip ${item.bug ? 'chip-bug' : ''}`;
        chip.id = `chip-${idx}`;
        chip.draggable = true;
        chip.setAttribute('data-index', idx);

        chip.innerHTML = `
          <div class="chip-left-group">
            <span class="chip-drag-handle" title="คลิกลากเพื่อสลับลำดับคำสั่ง">⋮⋮</span>
            <span class="chip-line-no">${idx + 1}</span>
            <span class="chip-icon">${meta.icon}</span>
            <span class="chip-label">${meta.label}</span>
          </div>
          <div class="chip-actions-group">
            <button class="chip-move-btn btn-move-up" data-from="${idx}" data-to="${idx - 1}" title="เลื่อนขึ้น" ${idx === 0 ? 'disabled style="opacity:0.25;cursor:default;"' : ''}>⬆️</button>
            <button class="chip-move-btn btn-move-down" data-from="${idx}" data-to="${idx + 1}" title="เลื่อนลง" ${idx === this.codeSequence.length - 1 ? 'disabled style="opacity:0.25;cursor:default;"' : ''}>⬇️</button>
            <div class="delete-chip-btn" title="ลบคำสั่งนี้">✕</div>
          </div>
        `;

        this.attachChipDragAndDrop(chip, idx);

        chip.querySelector('.btn-move-up')?.addEventListener('click', (e) => {
          e.stopPropagation();
          this.moveBlock(idx, idx - 1);
        });

        chip.querySelector('.btn-move-down')?.addEventListener('click', (e) => {
          e.stopPropagation();
          this.moveBlock(idx, idx + 1);
        });

        chip.querySelector('.delete-chip-btn').addEventListener('click', (e) => {
          e.stopPropagation();
          if (this.gameEngine && this.gameEngine.isExecuting) {
            this.gameEngine.isExecuting = false;
            if (this.gameEngine.stepTimeout) {
              clearTimeout(this.gameEngine.stepTimeout);
              this.gameEngine.stepTimeout = null;
            }
            this.gameEngine.resetSimulation();
          }
          this.codeSequence.splice(idx, 1);
          this.renderTimeline();
          this.gameEngine.resetSimulation();
        });

        container.appendChild(chip);
      }
    });

    container.scrollTop = container.scrollHeight;
  }

  attachChipDragAndDrop(element, idx) {
    element.addEventListener('dragstart', (e) => {
      this.draggedBlockIdx = idx;
      element.classList.add('dragging');
      e.dataTransfer.effectAllowed = 'move';
      e.dataTransfer.setData('text/plain', idx);
    });

    element.addEventListener('dragend', () => {
      element.classList.remove('dragging');
      document.querySelectorAll('.drag-over').forEach(el => el.classList.remove('drag-over'));
      this.draggedBlockIdx = null;
    });

    element.addEventListener('dragover', (e) => {
      e.preventDefault();
      e.dataTransfer.dropEffect = 'move';
      element.classList.add('drag-over');
    });

    element.addEventListener('dragleave', () => {
      element.classList.remove('drag-over');
    });

    element.addEventListener('drop', (e) => {
      e.preventDefault();
      element.classList.remove('drag-over');
      if (this.draggedBlockIdx !== null && this.draggedBlockIdx !== idx) {
        this.moveBlock(this.draggedBlockIdx, idx);
      }
    });
  }

  highlightActiveChip(idx, instr) {
    document.querySelectorAll('.code-chip, .chip-loop-container').forEach(c => c.classList.remove('active-step'));
    document.querySelectorAll('.loop-sub-chip').forEach(c => c.classList.remove('active-sub'));

    if (idx >= 0) {
      const chip = document.getElementById(`chip-${idx}`);
      if (chip) {
        chip.classList.add('active-step');
        chip.scrollIntoView({ behavior: 'smooth', inline: 'center', block: 'nearest' });

        if (instr && instr.isLoop && typeof instr.subIndex === 'number') {
          const subChip = document.getElementById(`chip-${idx}-sub-${instr.subIndex}`);
          if (subChip) subChip.classList.add('active-sub');
        }
      }
    }
  }

  handleGameFinished(result) {
    if (result.success) {
      this.stopStageTimer();

      const earnedStars = result.stars || 1;
      const basePoints = 200;
      const starBonus = earnedStars * 100;
      const efficiencyBonus = Math.max(0, (result.maxAllowedForBonus - result.codeBlocksUsed) * 20);

      // In Challenge mode, add Time Bonus (10 XP per remaining second)
      let timeBonus = 0;
      if (this.gameMode === 'CHALLENGE' && this.stageTimeLeft > 0) {
        timeBonus = this.stageTimeLeft * 10;
      }

      const stageScore = basePoints + starBonus + efficiencyBonus + timeBonus;

      this.totalScore += stageScore;
      this.totalStars += earnedStars;

      const scoreElem = document.getElementById('stat-total-score');
      if (scoreElem) scoreElem.textContent = this.totalScore;
      const starsElem = document.getElementById('stat-total-stars');
      if (starsElem) starsElem.textContent = this.totalStars;

      let badgeEarned = null;
      if (this.currentLevelIndex === 0) badgeEarned = "🏅 ตรานักคิดอัลกอริทึม (Algorithm Scout)";
      else if (this.currentLevelIndex === 1) badgeEarned = "🧭 ตราผู้วางแผนทิศทาง (Navigation Master)";
      else if (this.currentLevelIndex === 2) badgeEarned = "⚡ ตราจอมเวทวนลูป (Loop Master)";
      else if (this.currentLevelIndex === 3) badgeEarned = "🐞 ตรานักสืบแก้บั๊ก (Super Bug Hunter)";
      else if (this.currentLevelIndex === 4) badgeEarned = "🏆 ตราแชมป์จักรวาลโค้ดดิ้ง (Grand Cosmic Master)";

      if (badgeEarned && !this.userBadges.includes(badgeEarned)) {
        this.userBadges.push(badgeEarned);
      }

      this.saveLeaderboardEntry(stageScore, earnedStars);
      this.updateTopScoreBanners();
      this.unlockNextLevel(this.gradeLevel, this.currentLevelIndex + 2);
      this.renderCartoonLevelGrid(this.modalGrade);
      this.renderWelcomeCartoonGrid();

      this.showVictoryModal(earnedStars, stageScore, badgeEarned, result.codeBlocksUsed, timeBonus);
    } else {
      // Failed run: In Challenge mode, lose 1 life!
      if (this.gameMode === 'CHALLENGE') {
        this.loseLife(result.errorReason || 'เขียนโปรแกรมไม่ตรงตามเป้าหมาย');
      }
    }
  }

  advanceToNextLevel() {
    if (this.victoryTimer) {
      clearInterval(this.victoryTimer);
      this.victoryTimer = null;
    }
    this.cancelSpeech();
    this.closeModal('victory-modal');
    if (this.currentLevelIndex < this.currentLevels.length - 1) {
      this.loadCurrentLevel(this.currentLevelIndex + 1, true);
    } else {
      this.openCertificateModal();
    }
  }

  showVictoryModal(stars, score, badge, blocksCount, timeBonus = 0) {
    const modal = document.getElementById('victory-modal');
    if (!modal) return;

    const starSpans = modal.querySelectorAll('.victory-stars .star');
    starSpans.forEach((s, idx) => {
      if (idx < stars) {
        s.classList.add('earned');
      } else {
        s.classList.remove('earned');
      }
    });

    const scoreText = document.getElementById('victory-score-text');
    if (scoreText) {
      let extraInfo = `+${score} XP (ใช้โค้ด ${blocksCount} บล็อก)`;
      if (timeBonus > 0) {
        extraInfo += ` | ⚡ Time Bonus: +${timeBonus} XP`;
      }
      extraInfo += ` | คะแนนรวม: ${this.totalScore} XP`;
      scoreText.innerHTML = extraInfo;
    }

    const badgeBox = document.getElementById('victory-badge-box');
    if (badgeBox) {
      if (badge) {
        badgeBox.textContent = badge;
        badgeBox.style.display = 'inline-flex';
      } else {
        badgeBox.style.display = 'none';
      }
    }

    // Setup Mini-Quiz for current level
    this.setupVictoryQuiz();

    const isLastLevel = (this.currentLevelIndex >= this.currentLevels.length - 1);
    const finalActions = document.getElementById('victory-final-actions');
    if (finalActions) {
      finalActions.style.display = isLastLevel ? 'flex' : 'none';
    }

    const nextBtn = document.getElementById('btn-victory-next');
    const countdownSecSpan = document.getElementById('victory-countdown-sec');

    if (nextBtn) {
      nextBtn.innerHTML = isLastLevel ? '📜 รับเกียรติบัตรแชมเปี้ยน 🏆' : 'ลุยด่านต่อไป 🚀 (5 วิ...)';
    }
    if (countdownSecSpan) {
      countdownSecSpan.textContent = '5';
    }

    modal.classList.add('active');

    // Auto-advance countdown timer (5 seconds)
    if (this.victoryTimer) {
      clearInterval(this.victoryTimer);
      this.victoryTimer = null;
    }
    let timeLeft = 5;
    this.victoryTimer = setInterval(() => {
      timeLeft--;
      if (countdownSecSpan) {
        countdownSecSpan.textContent = timeLeft;
      }
      if (nextBtn) {
        nextBtn.innerHTML = isLastLevel 
          ? `📜 รับเกียรติบัตรแชมเปี้ยน 🏆 (${timeLeft} วิ...)` 
          : `ลุยด่านต่อไป 🚀 (${timeLeft} วิ...)`;
      }
      if (timeLeft <= 0) {
        clearInterval(this.victoryTimer);
        this.victoryTimer = null;
        this.advanceToNextLevel();
      }
    }, 1000);
  }

  setupVictoryQuiz() {
    const quizBox = document.getElementById('victory-quiz-box');
    if (quizBox) {
      quizBox.style.display = 'none';
    }
  }

  handleQuizAnswer(chosenIdx, quiz, btnClicked, optionsList, feedbackBox, stageKey) {
    if (this.currentQuizAnswered) return;

    const isCorrect = (chosenIdx === quiz.correctIndex);
    if (isCorrect) {
      this.currentQuizAnswered = true;
      btnClicked.classList.add('correct');

      optionsList.querySelectorAll('.quiz-option-btn').forEach(b => {
        if (b !== btnClicked) b.classList.add('disabled');
      });

      const isFirstTime = !this.passedQuizStages.has(stageKey);
      if (isFirstTime) {
        this.passedQuizStages.add(stageKey);
        this.quizPassedCount++;
        this.totalScore += 100;

        const scoreElem = document.getElementById('stat-total-score');
        if (scoreElem) scoreElem.textContent = this.totalScore;

        const victoryScoreText = document.getElementById('victory-score-text');
        if (victoryScoreText) {
          victoryScoreText.innerHTML += ` <span style="color:#10b981; font-weight:800;">(+100 XP มินิควิซ!)</span>`;
        }
      }

      if (window.soundEngine) window.soundEngine.playSuccess();

      if (feedbackBox) {
        feedbackBox.className = 'quiz-feedback-box correct';
        feedbackBox.innerHTML = `🎉 <strong>ถูกต้องยอดเยี่ยม! (+100 XP)</strong><br>${quiz.explanation}`;
        feedbackBox.style.display = 'block';
      }

      this.showStatusToast('🎉 ตอบมินิควิซถูกต้อง! ได้รับโบนัส +100 XP', false);
    } else {
      btnClicked.classList.add('wrong');
      setTimeout(() => btnClicked.classList.remove('wrong'), 800);

      if (window.soundEngine) window.soundEngine.playError();

      if (feedbackBox) {
        feedbackBox.className = 'quiz-feedback-box wrong';
        feedbackBox.innerHTML = `💡 <strong>ยังไม่ถูกต้องนะ</strong> ลองอ่านคำถามทบทวนอีกครั้ง แล้วเลือกคำตอบใหม่ได้เลยครับ 😊`;
        feedbackBox.style.display = 'block';
      }
    }
  }

  speakCurrentQuiz(quiz) {
    if (!quiz) {
      const currentLevel = this.currentLevels[this.currentLevelIndex];
      quiz = currentLevel ? currentLevel.quiz : null;
    }
    if (!quiz) return;

    const textToSpeak = quiz.tts || `${quiz.question}. ${quiz.options.map((o, i) => `ข้อ ${i + 1} ${o}`).join('. ')}`;
    this.speakThai(textToSpeak);
  }

  showKnowledgeModal() {
    const level = this.currentLevels[this.currentLevelIndex];
    if (!level || !level.knowledge) return;

    this.pauseStageTimer();

    const t = document.getElementById('km-title');
    if (t) t.textContent = level.knowledge.title;
    const d = document.getElementById('km-desc');
    if (d) d.textContent = level.knowledge.description;
    const ta = document.getElementById('km-takeaway');
    if (ta) ta.textContent = level.knowledge.takeaway;
    const at = document.getElementById('km-active-tip');
    if (at) at.textContent = level.knowledge.activeTip;

    document.getElementById('knowledge-modal')?.classList.add('active');

    // Auto-speak if setting is enabled
    const toggle = document.getElementById('toggle-auto-speak');
    const canAutoSpeak = toggle ? toggle.checked : (this.autoSpeakKnowledge !== false);
    if (canAutoSpeak) {
      const textToSpeak = level.knowledge.ttsNarration || `${level.knowledge.title}. ${level.knowledge.description}. ${level.knowledge.takeaway}`;
      this.speakKnowledgeText(textToSpeak);
    }
  }

  initTTSVoices() {
    if (!('speechSynthesis' in window)) return;
    const populate = () => {
      this.updateVoiceDropdown();
    };
    populate();
    if (window.speechSynthesis.onvoiceschanged !== undefined) {
      window.speechSynthesis.onvoiceschanged = populate;
    }
  }

  updateVoiceDropdown() {
    const voiceSelect = document.getElementById('select-tts-voice');
    if (!voiceSelect || !('speechSynthesis' in window)) return;

    const voices = window.speechSynthesis.getVoices();
    const thaiVoices = voices.filter(v => v.lang === 'th-TH' || v.lang.startsWith('th'));
    if (thaiVoices.length === 0) return;

    const savedVoice = this.selectedVoiceUri || localStorage.getItem('codebot_ar_tts_voice') || '';
    voiceSelect.innerHTML = '<option value="">เสียง: เริ่มต้นระบบ</option>';
    thaiVoices.forEach(v => {
      const opt = document.createElement('option');
      opt.value = v.voiceURI || v.name;
      opt.textContent = `${v.name}${v.name.includes('Siri') ? ' (Siri)' : ''}`;
      if (v.voiceURI === savedVoice || v.name === savedVoice) opt.selected = true;
      voiceSelect.appendChild(opt);
    });
  }

  playRobotChirp() {
    try {
      const AudioCtx = window.AudioContext || window.webkitAudioContext;
      if (!AudioCtx) return;
      if (!this._robotAudioCtx) {
        this._robotAudioCtx = new AudioCtx();
      }
      const ctx = this._robotAudioCtx;
      if (ctx.state === 'suspended') {
        ctx.resume();
      }

      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.type = 'sawtooth';

      const now = ctx.currentTime;
      osc.frequency.setValueAtTime(880, now);
      osc.frequency.exponentialRampToValueAtTime(1760, now + 0.08);
      osc.frequency.setValueAtTime(1320, now + 0.09);
      osc.frequency.exponentialRampToValueAtTime(2200, now + 0.18);

      gain.gain.setValueAtTime(0.12, now);
      gain.gain.exponentialRampToValueAtTime(0.01, now + 0.22);

      osc.connect(gain);
      gain.connect(ctx.destination);

      osc.start(now);
      osc.stop(now + 0.23);
    } catch (e) {
      // AudioContext permitted only after user gesture or ignored if unavailable
    }
  }

  applyVoiceCharacter(charKey, isManual = false) {
    this.voiceCharacter = charKey || 'female';
    localStorage.setItem('codebot_ar_voice_char', this.voiceCharacter);

    const speedSelect = document.getElementById('select-tts-speed');
    const voiceSelect = document.getElementById('select-tts-voice');
    const voices = ('speechSynthesis' in window) ? window.speechSynthesis.getVoices() : [];
    const thaiVoices = voices.filter(v => v.lang === 'th-TH' || v.lang.startsWith('th'));

    if (this.voiceCharacter === 'female') {
      this.ttsPitch = 1.1;
      this.ttsSpeed = 1.0;
      const fVoice = thaiVoices.find(v => /female|kanya|narisa/i.test(v.name));
      if (fVoice && voiceSelect) {
        voiceSelect.value = fVoice.voiceURI || fVoice.name;
        this.selectedVoiceUri = voiceSelect.value;
      }
    } else if (this.voiceCharacter === 'male') {
      this.ttsPitch = 0.82;
      this.ttsSpeed = 0.98;
      const mVoice = thaiVoices.find(v => /male|man|siri.*male/i.test(v.name));
      if (mVoice && voiceSelect) {
        voiceSelect.value = mVoice.voiceURI || mVoice.name;
        this.selectedVoiceUri = voiceSelect.value;
      }
    } else if (this.voiceCharacter === 'robot') {
      this.ttsPitch = 1.38;
      this.ttsSpeed = 1.08;
    }

    localStorage.setItem('codebot_ar_tts_pitch', String(this.ttsPitch));
    localStorage.setItem('codebot_ar_tts_speed', String(this.ttsSpeed));

    if (speedSelect) {
      speedSelect.value = String(this.ttsSpeed);
    }

    if (isManual) {
      const labels = {
        female: '👩‍🏫 ครูใจดี (ครูผู้หญิง)',
        male: '👨‍🏫 ครูพี่เลี้ยง (ครูผู้ชาย)',
        robot: '🤖 หุ่นยนต์โค้ดบอท (ไซไฟ)',
        custom: '⚙️ ปรับแต่งเอง (Custom)'
      };
      this.showStatusToast(`🔊 เลือกโทนเสียง: ${labels[this.voiceCharacter] || this.voiceCharacter}`, false);
      if (this.voiceCharacter === 'robot') {
        this.playRobotChirp();
      }
    }
  }

  cleanThaiTextForTTS(text) {
    if (!text) return '';
    let cleaned = text;

    // 1. Remove all Unicode emojis and symbols so speech synthesizer NEVER speaks emoji names like "หลอดไฟ", "จับมือ"
    cleaned = cleaned.replace(/[\u{1F300}-\u{1F9FF}\u{2600}-\u{26FF}\u{2700}-\u{27BF}\u{1F000}-\u{1F02F}\u{1F0A0}-\u{1F0FF}\u{1F100}-\u{1F64F}\u{1F680}-\u{1F6FF}\u{1FA00}-\u{1FAFF}\u{FE00}-\u{FE0F}\u{200D}]/gu, '');

    // 2. Remove "ระดับชั้น" that causes TTS phoneme tokenizer to slur as "ระดับชัน"
    cleaned = cleaned.replace(/ระดับชั้น\s*/g, '');
    cleaned = cleaned.replace(/ระดับ\s*ชั้น\s*/g, '');

    // 3. Pronounce grades cleanly with spaces so tones are pronounced accurately
    cleaned = cleaned.replace(/ป\.4\/1/g, 'ปอ สี่ ทับ หนึ่ง');
    cleaned = cleaned.replace(/ป\.4\/2/g, 'ปอ สี่ ทับ สอง');
    cleaned = cleaned.replace(/ป\.5\/1/g, 'ปอ ห้า ทับ หนึ่ง');
    cleaned = cleaned.replace(/ป\.5\/2/g, 'ปอ ห้า ทับ สอง');
    cleaned = cleaned.replace(/ป\.4/g, 'ปอ สี่');
    cleaned = cleaned.replace(/ป\.5/g, 'ปอ ห้า');
    cleaned = cleaned.replace(/ปอสี่/g, 'ปอ สี่');
    cleaned = cleaned.replace(/ปอห้า/g, 'ปอ ห้า');
    cleaned = cleaned.replace(/ว\s*4\.2/g, 'วอ สี่ จุด สอง');

    // 4. Remove any parenthetical English terms that cause stumbling or robotic mispronunciation
    cleaned = cleaned.replace(/\([^)]*[a-zA-Z]+[^)]*\)/g, '');

    // 5. Natural friendly phrasing for coding terminology in Thai classroom
    cleaned = cleaned.replace(/CodeBot/gi, 'โค้ดบอท');
    cleaned = cleaned.replace(/Active Learning/gi, 'การเรียนรู้เชิงรุก');
    cleaned = cleaned.replace(/Active Tip/gi, 'ข้อแนะนำ');
    cleaned = cleaned.replace(/Active Goal/gi, 'เป้าหมาย');
    cleaned = cleaned.replace(/Driver/gi, 'ผู้สั่งการ');
    cleaned = cleaned.replace(/Navigator/gi, 'ผู้นำทาง');
    cleaned = cleaned.replace(/Loop/gi, 'ลูป');
    cleaned = cleaned.replace(/Debugging/gi, 'ดีบักกิ้ง');
    cleaned = cleaned.replace(/Debug/gi, 'ดีบัก');
    cleaned = cleaned.replace(/Top Score/gi, 'ท็อปสกอร์');

    // Phonetic clarity for words that can be mumbled by compact TTS engines
    cleaned = cleaned.replace(/แชมเปี้ยน/g, 'แชม เปี้ยน');
    cleaned = cleaned.replace(/เลเซอร์/g, 'เล เซอร์');
    cleaned = cleaned.replace(/ซิกแซก/g, 'ซิก แซก');
    cleaned = cleaned.replace(/อุกกาบาต/g, 'อุก กา บาต');
    cleaned = cleaned.replace(/จัตุรัส/g, 'จัด ตุ รัด');

    // Breathing pauses on polite sentence endings (. triggers natural 350-400ms sentence pause)
    cleaned = cleaned.replace(/นะครับ/g, ' นะครับ. ');
    cleaned = cleaned.replace(/(?<!นะ)ครับ/g, ' ครับ. ');
    cleaned = cleaned.replace(/นะคะ/g, ' นะคะ. ');
    cleaned = cleaned.replace(/(?<!นะ)ค่ะ/g, ' ค่ะ. ');

    // Clause transition pauses (, triggers natural 200-250ms clause pause)
    cleaned = cleaned.replace(/\s*เพื่อให้/g, ', เพื่อให้');
    cleaned = cleaned.replace(/\s*แต่ถ้า/g, ', แต่ถ้า');
    cleaned = cleaned.replace(/\s*ดังนั้น/g, ', ดังนั้น');
    cleaned = cleaned.replace(/\s*เช่น/g, ', เช่น');
    cleaned = cleaned.replace(/\s*ถ้าหาก/g, ', ถ้าหาก');

    // 6. Clean punctuation symbols: preserve periods and commas, convert others to space
    cleaned = cleaned.replace(/[:;•\-_/\\*~()➔\[\]!]/g, ' ');
    cleaned = cleaned.replace(/\s*\.\s*/g, '. ');
    cleaned = cleaned.replace(/\s*,\s*/g, ', ');
    cleaned = cleaned.replace(/\s+/g, ' ').trim();

    return cleaned;
  }

  getBestThaiVoice() {
    if (!('speechSynthesis' in window)) return null;
    const voices = window.speechSynthesis.getVoices();
    const thaiVoices = voices.filter(v => v.lang === 'th-TH' || v.lang.startsWith('th') || /thai/i.test(v.name));
    if (thaiVoices.length === 0) return null;

    if (this.selectedVoiceUri) {
      const match = thaiVoices.find(v => v.voiceURI === this.selectedVoiceUri || v.name === this.selectedVoiceUri);
      if (match) return match;
    }

    // Rank voices by clarity & neural fidelity:
    // 1. Google (Chrome on Mac/Win/Android - crystal clear neural audio)
    // 2. Siri (Apple Neural Siri on iOS/macOS)
    // 3. Premium / Enhanced / Natural
    // 4. Narisa (clear standard)
    // 5. Kanya (standard non-compact)
    // 6. Compact / legacy
    const ranked = thaiVoices.slice().sort((a, b) => {
      const getScore = (v) => {
        const name = (v.name || '').toLowerCase();
        if (name.includes('google')) return 100;
        if (name.includes('siri')) return 90;
        if (name.includes('enhanced') || name.includes('premium') || name.includes('natural')) return 80;
        if (name.includes('narisa')) return 70;
        if (name.includes('kanya') && !name.includes('compact')) return 60;
        if (name.includes('compact')) return 30;
        return 50;
      };
      return getScore(b) - getScore(a);
    });

    return ranked[0];
  }

  getCalibratedTTSRate() {
    const ua = (typeof navigator !== 'undefined' && navigator.userAgent) ? navigator.userAgent : '';
    const platform = (typeof navigator !== 'undefined' && navigator.platform) ? navigator.platform : '';
    const touchPoints = (typeof navigator !== 'undefined' && navigator.maxTouchPoints) ? navigator.maxTouchPoints : 0;

    const isIOS = /iPhone|iPad|iPod/i.test(ua) || (platform === 'MacIntel' && touchPoints > 1);
    const isAndroid = /Android/i.test(ua);
    const isMobile = isIOS || isAndroid || /Mobile/i.test(ua);

    const speedMode = this.ttsSpeedMode || localStorage.getItem('codebot_ar_tts_speed_mode') || 'normal';

    // Baseline calibrated for clear classroom instruction:
    // - iOS WebKit: default 1.0 is ~2x fast. Calibrated natural rate is 0.80 (calm storytelling pace)
    // - Android mobile: calibrated natural rate is 0.82
    // - Desktop (MacBook / PC): calibrated rate is 0.88 (articulate and clear, avoids swallowing consonants)
    let baseRate = 0.88;
    if (isIOS) {
      baseRate = 0.80;
    } else if (isMobile) {
      baseRate = 0.82;
    }

    if (speedMode === 'slow') {
      return Number((baseRate * 0.85).toFixed(2)); // ~0.70 - 0.75
    } else if (speedMode === 'fast') {
      return Number((baseRate * 1.20).toFixed(2)); // ~0.98 - 1.05
    }
    return baseRate;
  }

  speakKnowledgeText(rawText) {
    if (!('speechSynthesis' in window)) {
      this.showStatusToast('⚠️ เบราว์เซอร์นี้ไม่รองรับระบบสังเคราะห์เสียง', true);
      return;
    }

    window.speechSynthesis.cancel();

    if (this.voiceCharacter === 'robot') {
      this.playRobotChirp();
    }

    const cleanedText = this.cleanThaiTextForTTS(rawText);
    if (!cleanedText) return;

    const utterance = new SpeechSynthesisUtterance(cleanedText);
    utterance.lang = 'th-TH';

    // 1. Calibrated speaking rate (solves mobile speaking too fast & desktop clarity)
    utterance.rate = this.getCalibratedTTSRate();

    // 2. Native formant pitch 1.0 (avoids distortion/muffling on Mac Kanya & mobile TTS)
    utterance.pitch = (this.voiceCharacter === 'robot') ? 1.35 : 1.0;

    // 3. Best Thai voice selection: Google Neural > Siri > Enhanced > Narisa > Kanya
    const bestVoice = this.getBestThaiVoice();
    if (bestVoice) {
      utterance.voice = bestVoice;
    }

    const btn = document.getElementById('btn-speak-knowledge');
    if (btn) {
      btn.innerHTML = '⏹️ หยุดเสียง';
      btn.classList.add('btn-danger');
      btn.classList.remove('btn-secondary');
    }

    utterance.onend = () => {
      if (btn) {
        btn.innerHTML = '🔊 ฟังซ้ำ';
        btn.classList.remove('btn-danger');
        btn.classList.add('btn-secondary');
      }
    };

    utterance.onerror = () => {
      if (btn) {
        btn.innerHTML = '🔊 ฟังซ้ำ';
        btn.classList.remove('btn-danger');
        btn.classList.add('btn-secondary');
      }
    };

    // Slight delay when robot chirp plays so sound effect precedes the speech cleanly
    if (this.voiceCharacter === 'robot') {
      setTimeout(() => {
        window.speechSynthesis.speak(utterance);
      }, 160);
    } else {
      window.speechSynthesis.speak(utterance);
    }
  }

  cancelSpeech() {
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
      const btn = document.getElementById('btn-speak-knowledge');
      if (btn) {
        btn.innerHTML = '🔊 ฟังโจทย์';
        btn.classList.remove('btn-danger');
        btn.classList.add('btn-secondary');
      }
    }
  }

  // LocalStorage Leaderboard & Top Score System
  getLeaderboardStorageKey(grade) {
    return (grade === 'p5') ? this.STORAGE_KEY_LEADERBOARD_P5 : this.STORAGE_KEY_LEADERBOARD_P4;
  }

  loadLeaderboardData(grade) {
    try {
      const key = this.getLeaderboardStorageKey(grade);
      const data = localStorage.getItem(key);
      return data ? JSON.parse(data) : [];
    } catch (e) {
      return [];
    }
  }

  saveLeaderboardEntry(stageScore, stars) {
    try {
      const key = this.getLeaderboardStorageKey(this.gradeLevel);
      const records = this.loadLeaderboardData(this.gradeLevel);
      const now = new Date();
      const timeStr = `${now.toLocaleDateString('th-TH')} ${now.toLocaleTimeString('th-TH', { hour: '2-digit', minute: '2-digit' })}`;

      // Check if this team already has an entry
      const existingIdx = records.findIndex(r => r.teamName === this.teamName);
      if (existingIdx >= 0) {
        if (this.totalScore > records[existingIdx].score) {
          records[existingIdx].score = this.totalScore;
          records[existingIdx].stars = this.totalStars;
          records[existingIdx].time = timeStr;
          records[existingIdx].driver = this.driverName;
          records[existingIdx].navigator = this.navigatorName;
          if (this.latestWinnerPhotoData) records[existingIdx].photo = this.latestWinnerPhotoData;
        }
      } else {
        records.push({
          teamName: this.teamName,
          driver: this.driverName,
          navigator: this.navigatorName,
          grade: this.gradeLevel,
          score: this.totalScore,
          stars: this.totalStars,
          time: timeStr,
          photo: this.latestWinnerPhotoData || null
        });
      }

      records.sort((a, b) => b.score - a.score);
      localStorage.setItem(key, JSON.stringify(records));
      this.updateTopScoreBanners();
    } catch (e) {
      console.warn('Leaderboard save failed:', e);
    }
  }

  updateTopScoreBanners() {
    const records = this.loadLeaderboardData(this.gradeLevel);
    const topPillText = document.getElementById('nav-top-score-text');
    const welcomeTopVal = document.getElementById('welcome-top-score-val');

    if (records.length > 0) {
      const champ = records[0];
      const str = `👑 ${champ.teamName} (${champ.score.toLocaleString()} XP)`;
      if (topPillText) topPillText.textContent = str;
      if (welcomeTopVal) welcomeTopVal.textContent = str;
    } else {
      const def = 'ยังไม่มีสถิติห้อง (เริ่มเล่นเพื่อเป็นที่ 1!)';
      if (topPillText) topPillText.textContent = 'Top Score: -';
      if (welcomeTopVal) welcomeTopVal.textContent = def;
    }
  }

  openLeaderboardModal(grade) {
    this.pauseStageTimer();
    this.activeLbTabGrade = grade;
    const tabP4 = document.getElementById('tab-lb-p4');
    const tabP5 = document.getElementById('tab-lb-p5');

    if (grade === 'p5') {
      tabP5?.classList.add('btn-primary');
      tabP5?.classList.remove('btn-secondary');
      tabP4?.classList.remove('btn-primary');
      tabP4?.classList.add('btn-secondary');
    } else {
      tabP4?.classList.add('btn-primary');
      tabP4?.classList.remove('btn-secondary');
      tabP5?.classList.remove('btn-primary');
      tabP5?.classList.add('btn-secondary');
    }

    const tbody = document.getElementById('leaderboard-tbody');
    if (!tbody) return;
    tbody.innerHTML = '';

    const records = this.loadLeaderboardData(grade);
    if (records.length === 0) {
      tbody.innerHTML = `
        <tr>
          <td colspan="5" style="text-align: center; color: #94a3b8; padding: 24px;">
            ยังไม่มีข้อมูลคะแนนของระดับชั้นนี้ในเครื่อง<br>
            <span style="font-size: 0.8rem; color: #38bdf8;">เล่นผ่านด่านเพื่อบันทึกชื่อทีมขึ้นกระดานคะแนนห้องเรียน!</span>
          </td>
        </tr>
      `;
    } else {
      records.forEach((r, idx) => {
        const tr = document.createElement('tr');
        const rankMedal = (idx === 0) ? '🥇 1' : (idx === 1) ? '🥈 2' : (idx === 2) ? '🥉 3' : `${idx + 1}`;
        const photoThumb = r.photo 
          ? `<img src="${r.photo}" style="width: 38px; height: 28px; border-radius: 4px; object-fit: cover; border: 1px solid #fbbf24;">`
          : '<span style="font-size: 1.2rem;">👤</span>';

        tr.innerHTML = `
          <td style="font-weight: bold; color: ${idx === 0 ? '#fbbf24' : '#ffffff'};">${rankMedal}</td>
          <td>
            <div style="font-weight: bold; color: #38bdf8;">${r.teamName}</div>
            <div style="font-size: 0.78rem; color: #94a3b8;">${r.driver} & ${r.navigator}</div>
          </td>
          <td>${photoThumb}</td>
          <td style="color: #facc15; font-weight: bold;">⭐ ${r.stars}</td>
          <td style="color: #34d399; font-weight: 800;">${r.score.toLocaleString()} XP</td>
        </tr>
        `;
        tbody.appendChild(tr);
      });
    }

    document.getElementById('leaderboard-modal')?.classList.add('active');
  }

  clearClassroomLeaderboard() {
    if (confirm(`คุณครูต้องการล้างสถิติคะแนนห้องเรียนของชั้น ป.${this.activeLbTabGrade === 'p5' ? '5' : '4'} ทั้งหมดเพื่อเริ่มคาบเรียนใหม่ใช่หรือไม่?`)) {
      localStorage.removeItem(this.getLeaderboardStorageKey(this.activeLbTabGrade));
      this.updateTopScoreBanners();
      this.openLeaderboardModal(this.activeLbTabGrade);
      this.showStatusToast('🗑️ ล้างสถิติกระดานคะแนนห้องเรียนเรียบร้อย', false);
    }
  }

  // Teacher Action Research CSV Export
  exportResearchCSV() {
    const dataP4 = this.loadLeaderboardData('p4');
    const dataP5 = this.loadLeaderboardData('p5');
    const allRecords = [
      ...dataP4.map(r => ({ ...r, gradeLabel: 'ป.4' })),
      ...dataP5.map(r => ({ ...r, gradeLabel: 'ป.5' }))
    ];

    if (allRecords.length === 0) {
      alert('ยังไม่มีข้อมูลการเล่นในระบบ');
      return;
    }

    let csvContent = '\uFEFF'; // UTF-8 BOM for Excel in Thai
    csvContent += 'ระดับชั้น,ชื่อทีม,ผู้ควบคุม (Driver),ผู้วางแผน (Navigator),คะแนนสะสม (XP),ดาวสะสม (Stars),เวลาที่บันทึก\n';

    allRecords.forEach(r => {
      csvContent += `"${r.gradeLabel}","${r.teamName}","${r.driver}","${r.navigator}",${r.score},${r.stars},"${r.time}"\n`;
    });

    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `CodeBot_AR_Research_Data_${new Date().toISOString().slice(0,10)}.csv`;
    link.click();
    URL.revokeObjectURL(url);
    this.showStatusToast('📊 ส่งออกข้อมูล CSV งานวิจัยในชั้นเรียนสำเร็จ!', false);
  }

  // Winner & Emergency AR Photo Capture Modal
  openWinnerPhotoModal() {
    this.pauseStageTimer();
    const modal = document.getElementById('winner-photo-modal');
    if (!modal) return;

    modal.classList.add('active');
    this.captureWinnerPhoto();
  }

  captureWinnerPhoto() {
    const canvas = document.getElementById('winner-photo-canvas');
    const video = document.getElementById('webcam-video');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    const width = canvas.width;
    const height = canvas.height;

    ctx.save();
    if (video && video.readyState >= 2) {
      // Draw mirrored video frame with cover aspect-ratio scaling to prevent distortion
      const vWidth = video.videoWidth || 640;
      const vHeight = video.videoHeight || 480;
      const vAspect = vWidth / vHeight;
      const cAspect = width / height;
      let sx = 0, sy = 0, sWidth = vWidth, sHeight = vHeight;

      if (vAspect > cAspect) {
        sWidth = vHeight * cAspect;
        sx = (vWidth - sWidth) / 2;
      } else {
        sHeight = vWidth / cAspect;
        sy = (vHeight - sHeight) / 2;
      }

      ctx.translate(width, 0);
      ctx.scale(-1, 1);
      ctx.drawImage(video, sx, sy, sWidth, sHeight, 0, 0, width, height);
    } else {
      ctx.fillStyle = '#0f172a';
      ctx.fillRect(0, 0, width, height);
      ctx.fillStyle = '#38bdf8';
      ctx.font = 'bold 28px system-ui, sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText('🤖 ยอดนักสำรวจ CodeBot AR', width / 2, height / 2);
    }
    ctx.restore();

    // Draw Frame based on Victory vs Emergency Game Over
    ctx.save();
    const isOver = this.isGameOverPhoto;
    const primaryColor = isOver ? '#ef4444' : '#f59e0b';
    const secondaryColor = isOver ? '#f97316' : '#38bdf8';
    const bannerTitle = isOver 
      ? '🚨 EMERGENCY MISSION OVER • HEROES WHO TRIED' 
      : '🏆 WINNER • CODEBOT AR SPACE EXPLORER';

    // Outer Border
    ctx.lineWidth = 10;
    ctx.strokeStyle = primaryColor;
    ctx.strokeRect(10, 10, width - 20, height - 20);

    ctx.lineWidth = 3;
    ctx.strokeStyle = secondaryColor;
    ctx.strokeRect(18, 18, width - 36, height - 36);

    // Top Header Banner (centered on 800px width)
    ctx.fillStyle = 'rgba(15, 23, 42, 0.92)';
    ctx.beginPath();
    ctx.roundRect(width / 2 - 280, 24, 560, 46, 23);
    ctx.fill();
    ctx.strokeStyle = primaryColor;
    ctx.lineWidth = 2;
    ctx.stroke();

    ctx.font = 'bold 16px system-ui, sans-serif';
    ctx.fillStyle = isOver ? '#f87171' : '#fbbf24';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(bannerTitle, width / 2, 47);

    // Bottom Information Card (dedicated layout, no overlapping)
    ctx.fillStyle = 'rgba(15, 23, 42, 0.94)';
    ctx.beginPath();
    ctx.roundRect(24, height - 100, width - 48, 80, 16);
    ctx.fill();
    ctx.strokeStyle = secondaryColor;
    ctx.lineWidth = 2;
    ctx.stroke();

    // Left info: Team and roles
    ctx.textAlign = 'left';
    ctx.textBaseline = 'alphabetic';
    ctx.fillStyle = '#ffffff';
    ctx.font = 'bold 17px system-ui, sans-serif';
    ctx.fillText(`🚀 ทีม: ${this.teamName} (ป.${this.gradeLevel === 'p5' ? '5' : '4'}) [${this.gameMode === 'CHALLENGE' ? 'โหมดประลอง' : 'โหมดฝึกซ้อม'}]`, 42, height - 68);

    ctx.font = '14px system-ui, sans-serif';
    ctx.fillStyle = '#93c5fd';
    ctx.fillText(`🎮 ผู้สั่งการ (Driver): ${this.driverName}  |  🗺️ ผู้นำทาง (Navigator): ${this.navigatorName}`, 42, height - 38);

    // Right info: Score and Teacher attribution
    ctx.textAlign = 'right';
    ctx.fillStyle = isOver ? '#fca5a5' : '#fbbf24';
    ctx.font = 'bold 18px system-ui, sans-serif';
    ctx.fillText(`${this.totalScore.toLocaleString()} XP  ⭐ ${this.totalStars} ดาว`, width - 42, height - 68);

    ctx.fillStyle = '#a7f3d0';
    ctx.font = '12px system-ui, sans-serif';
    ctx.fillText('โรงเรียนบ้านโนนป่าหว้านเชียงฮาย สพป.หนองบัวลำภู เขต 2 • นายเตชินท์ อินทมล ตำแหน่ง ครู', width - 42, height - 38);

    ctx.restore();

    this.latestWinnerPhotoData = canvas.toDataURL('image/png');
    this.saveLeaderboardEntry(0, 0);
  }

  downloadWinnerPhoto() {
    const canvas = document.getElementById('winner-photo-canvas');
    if (!canvas) return;
    const a = document.createElement('a');
    a.href = canvas.toDataURL('image/png');
    const tag = this.isGameOverPhoto ? 'Emergency' : 'Winner';
    a.download = `CodeBot_${tag}_${this.teamName}_${Date.now()}.png`;
    a.click();
    this.showStatusToast('💾 ดาวน์โหลดภาพถ่ายเกียรติยศเรียบร้อย!', false);
  }

  // Official E-Certificate Generator (A4 Landscape, High-Res 1200x848)
  openCertificateModal() {
    this.pauseStageTimer();
    this.latestWinnerPhotoData = this.latestWinnerPhotoData || null;
    const modal = document.getElementById('certificate-modal');
    if (!modal) return;
    modal.classList.add('active');
    this.generateCertificate();
    if (window.soundEngine) {
      window.soundEngine.playCelebration();
    }
  }

  generateCertificate() {
    const canvas = document.getElementById('certificate-canvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const w = canvas.width;
    const h = canvas.height;

    // 1. Rich Deep Navy Blue Gradient
    const bgGrad = ctx.createLinearGradient(0, 0, w, h);
    bgGrad.addColorStop(0, '#060b18');
    bgGrad.addColorStop(0.5, '#0b1633');
    bgGrad.addColorStop(1, '#081126');
    ctx.fillStyle = bgGrad;
    ctx.fillRect(0, 0, w, h);

    // 2. Golden Borders
    ctx.save();
    ctx.lineWidth = 16;
    ctx.strokeStyle = '#b45309';
    ctx.strokeRect(24, 24, w - 48, h - 48);

    ctx.lineWidth = 4;
    ctx.strokeStyle = '#f59e0b';
    ctx.strokeRect(38, 38, w - 76, h - 76);

    ctx.lineWidth = 1;
    ctx.strokeStyle = '#fde68a';
    ctx.strokeRect(46, 46, w - 92, h - 92);

    // Corner Ornaments
    const drawCorner = (cx, cy) => {
      ctx.fillStyle = '#f59e0b';
      ctx.beginPath();
      ctx.arc(cx, cy, 14, 0, Math.PI * 2);
      ctx.fill();
      ctx.strokeStyle = '#ffffff';
      ctx.lineWidth = 2;
      ctx.stroke();
    };
    drawCorner(46, 46);
    drawCorner(w - 46, 46);
    drawCorner(46, h - 46);
    drawCorner(w - 46, h - 46);
    ctx.restore();

    // 3. Header & School Seal
    ctx.save();
    ctx.textAlign = 'center';

    ctx.font = '46px system-ui';
    ctx.fillText('🤖', w / 2, 110);

    ctx.fillStyle = '#fef08a';
    ctx.font = 'bold 34px system-ui, "TH Sarabun New", sans-serif';
    ctx.fillText('โรงเรียนบ้านโนนป่าหว้านเชียงฮาย', w / 2, 160);

    ctx.fillStyle = '#94a3b8';
    ctx.font = '18px system-ui, sans-serif';
    ctx.fillText('สังกัดสำนักงานเขตพื้นที่การศึกษาประถมศึกษาหนองบัวลำภู เขต 2', w / 2, 192);

    // Gold Divider Line
    ctx.strokeStyle = '#f59e0b';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(w / 2 - 280, 215);
    ctx.lineTo(w / 2 + 280, 215);
    ctx.stroke();

    ctx.fillStyle = '#f59e0b';
    ctx.beginPath();
    ctx.arc(w / 2, 215, 6, 0, Math.PI * 2);
    ctx.fill();

    // Certificate Heading
    ctx.fillStyle = '#ffffff';
    ctx.font = '24px system-ui, sans-serif';
    ctx.fillText('เกียรติบัตรฉบับนี้ให้ไว้เพื่อแสดงว่า', w / 2, 260);

    // Recipient Names
    ctx.fillStyle = '#fbbf24';
    ctx.font = 'bold 38px system-ui, sans-serif';
    ctx.fillText(`${this.driverName}   และ   ${this.navigatorName}`, w / 2, 315);

    ctx.fillStyle = '#38bdf8';
    ctx.font = 'bold 22px system-ui, sans-serif';
    ctx.fillText(`ทีมนักสำรวจ: "${this.teamName}"`, w / 2, 355);

    // Body Text
    ctx.fillStyle = '#e2e8f0';
    ctx.font = '20px system-ui, sans-serif';
    ctx.fillText('ได้ผ่านการฝึกอบรมและปฏิบัติกิจกรรมการเรียนรู้เชิงรุก (Active Learning)', w / 2, 405);

    ctx.fillStyle = '#34d399';
    ctx.font = 'bold 22px system-ui, sans-serif';
    ctx.fillText('รายวิชาพื้นฐานวิทยาศาสตร์และเทคโนโลยี (วิทยาการคำนวณ ว 4.2)', w / 2, 442);

    ctx.fillStyle = '#ffffff';
    ctx.font = '20px system-ui, sans-serif';
    ctx.fillText(`ด้วยสื่อนวัตกรรมการเรียนรู้เสมือนจริง CodeBot AR Adventure ระดับชั้นประถมศึกษาปีที่ ${this.gradeLevel === 'p5' ? '๕ (ป.5)' : '๔ (ป.4)'}`, w / 2, 480);

    // Scores & Stars
    ctx.fillStyle = '#fbbf24';
    ctx.font = 'bold 22px system-ui, sans-serif';
    ctx.fillText(`ผลการเรียนรู้: ยอดเยี่ยม (★★★)   |   ${this.totalScore.toLocaleString()} XP (${this.totalStars} ⭐)`, w / 2, 525);

    // Thai Date
    const now = new Date();
    const thaiMonths = ['มกราคม', 'กุมภาพันธ์', 'มีนาคม', 'เมษายน', 'พฤษภาคม', 'มิถุนายน', 'กรกฎาคม', 'สิงหาคม', 'กันยายน', 'ตุลาคม', 'พฤศจิกายน', 'ธันวาคม'];
    const thaiDateStr = `ให้ไว้ ณ วันที่ ${now.getDate()} เดือน ${thaiMonths[now.getMonth()]} พ.ศ. ${now.getFullYear() + 543}`;

    ctx.fillStyle = '#94a3b8';
    ctx.font = '18px system-ui, sans-serif';
    ctx.fillText(thaiDateStr, w / 2, 575);

    // Embedded Student Photo
    if (this.latestWinnerPhotoData) {
      const img = new Image();
      img.src = this.latestWinnerPhotoData;
      if (img.complete && img.naturalWidth > 0) {
        ctx.save();
        ctx.lineWidth = 4;
        ctx.strokeStyle = '#f59e0b';
        ctx.strokeRect(w - 240, 250, 160, 120);
        ctx.drawImage(img, w - 240, 250, 160, 120);
        ctx.restore();
      }
    }

    // Signatures
    ctx.textAlign = 'center';
    ctx.fillStyle = '#f8fafc';
    ctx.font = 'bold 20px system-ui, sans-serif';
    ctx.fillText('นายเตชินท์ อินทมล', w / 2 - 250, 680);
    ctx.fillStyle = '#94a3b8';
    ctx.font = '16px system-ui, sans-serif';
    ctx.fillText('(นายเตชินท์ อินทมล)', w / 2 - 250, 706);
    ctx.fillText('ตำแหน่ง ครู โรงเรียนบ้านโนนป่าหว้านเชียงฮาย', w / 2 - 250, 730);
    ctx.fillText('ครูผู้สอน / ผู้พัฒนานวัตกรรม', w / 2 - 250, 754);

    ctx.strokeStyle = 'rgba(255, 255, 255, 0.3)';
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(w / 2 - 370, 660);
    ctx.lineTo(w / 2 - 130, 660);
    ctx.stroke();

    ctx.fillStyle = '#f8fafc';
    ctx.font = 'bold 20px system-ui, sans-serif';
    ctx.fillText('ผู้อำนวยการโรงเรียน', w / 2 + 250, 680);
    ctx.fillStyle = '#94a3b8';
    ctx.font = '16px system-ui, sans-serif';
    ctx.fillText('( ............................................................ )', w / 2 + 250, 706);
    ctx.fillText('ผู้อำนวยการโรงเรียนบ้านโนนป่าหว้านเชียงฮาย', w / 2 + 250, 730);
    ctx.fillText('ประธานกรรมการบริหารสถานศึกษา', w / 2 + 250, 754);

    ctx.beginPath();
    ctx.moveTo(w / 2 + 130, 660);
    ctx.lineTo(w / 2 + 370, 660);
    ctx.stroke();

    // Official Gold Stamp
    ctx.fillStyle = 'rgba(245, 158, 11, 0.15)';
    ctx.beginPath();
    ctx.arc(w / 2, 700, 48, 0, Math.PI * 2);
    ctx.fill();
    ctx.strokeStyle = '#f59e0b';
    ctx.lineWidth = 3;
    ctx.stroke();

    ctx.fillStyle = '#fbbf24';
    ctx.font = 'bold 12px system-ui';
    ctx.fillText('OFFICIAL SEAL', w / 2, 692);
    ctx.fillText('CERTIFIED 2026', w / 2, 712);
    ctx.restore();
  }

  printCertificate() {
    window.print();
  }

  downloadCertificatePNG() {
    const canvas = document.getElementById('certificate-canvas');
    if (!canvas) return;
    const a = document.createElement('a');
    a.href = canvas.toDataURL('image/png');
    const safeTeam = (this.teamName || 'Hero').replace(/[^a-zA-Z0-9ก-๙_-]/g, '_');
    a.download = `CodeBot_Certificate_${safeTeam}_${Date.now()}.png`;
    a.click();
    this.showStatusToast('💾 ดาวน์โหลดเกียรติบัตรอิเล็กทรอนิกส์สำเร็จ!', false);
    if (window.soundEngine) window.soundEngine.playSuccess();
  }

  returnToWelcomeScreen() {
    // 1. Close all active modals and game menu
    const activeModals = document.querySelectorAll('.modal-overlay.active');
    activeModals.forEach(m => m.classList.remove('active'));
    this.closeGameMenu();

    // 2. Stop all timers
    if (this.victoryTimer) {
      clearInterval(this.victoryTimer);
      this.victoryTimer = null;
    }
    if (this.roleTimerInterval) {
      clearInterval(this.roleTimerInterval);
      this.roleTimerInterval = null;
    }
    this.pauseStageTimer();
    this.stopStageTimer();
    this.stopRoleTimer();

    // 3. Halt robot simulation execution
    if (this.gameEngine) {
      this.gameEngine.isExecuting = false;
      if (this.gameEngine.stepTimeout) {
        clearTimeout(this.gameEngine.stepTimeout);
        this.gameEngine.stepTimeout = null;
      }
      this.gameEngine.resetSimulation();
    }

    // 4. Cancel speech synthesis if active
    this.cancelSpeech();

    // 5. Reset camera loop recording flags
    this.currentRecordingLoop = null;
    if (this.cameraEngine) {
      this.cameraEngine.isLoopRecordingMode = false;
      this.cameraEngine.awaitingLoopIteration = false;
    }

    // 6. Reset gameStarted flag
    this.gameStarted = false;

    // 7. Show Welcome Screen and switch to Step 'mode'
    const welcome = document.getElementById('welcome-screen');
    if (welcome) {
      this.switchWelcomeScreen('mode');
      this.updateTopScoreBanners();
      this.updateGameModeUI();
      welcome.classList.remove('hidden');
      welcome.style.display = 'flex';
      welcome.scrollTop = 0;
    }

    // 8. Audio and toast feedback
    if (window.soundEngine) {
      window.soundEngine.playTurn();
    }
    this.showStatusToast('🏠 กลับสู่หน้าหลักพร้อมเริ่มภารกิจใหม่แล้ว!', false);
  }

  closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) modal.classList.remove('active');
    if (modalId === 'knowledge-modal') {
      this.cancelSpeech();
    }
    // Resume stage timer if no modal is active
    setTimeout(() => {
      const activeModals = document.querySelectorAll('.modal-overlay.active');
      if (activeModals.length === 0 && this.gameStarted && this.gameMode === 'CHALLENGE' && this.playerLives > 0) {
        this.resumeStageTimer();
      }
    }, 120);
  }

  // Active Learning Pair Programming Timer & Swapping
  startRoleTimer() {
    if (this.roleTimerInterval) clearInterval(this.roleTimerInterval);
    this.roleTimerInterval = setInterval(() => {
      if (!this.gameStarted) return;
      this.roleTimer--;

      const mins = Math.floor(this.roleTimer / 60);
      const secs = this.roleTimer % 60;
      const text = `${mins}:${secs < 10 ? '0' : ''}${secs}`;
      const timerDisplay = document.getElementById('role-timer-text');
      if (timerDisplay) timerDisplay.textContent = text;

      if (this.roleTimer <= 0) {
        this.swapPairRoles();
        this.showStatusToast('🔔 ถึงเวลาสลับบทบาท Driver 🔄 Navigator แล้ว!', false);
        this.roleTimer = 180;
      }
    }, 1000);
  }

  swapPairRoles() {
    this.currentRole = (this.currentRole === 'DRIVER') ? 'NAVIGATOR' : 'DRIVER';
    if (window.soundEngine) window.soundEngine.playTurn();
    this.updateRoleDisplay();
    this.showStatusToast(`🔄 สลับหน้าที่: ${this.currentRole === 'DRIVER' ? this.driverName + ' เป็น Driver' : this.navigatorName + ' เป็น Navigator'}`, false);
  }

  updateRoleDisplay() {
    const badge = document.getElementById('active-role-badge');
    if (!badge) return;

    if (this.currentRole === 'DRIVER') {
      badge.textContent = `🎮 Driver: ${this.driverName} (คุมหน้ากล้อง)`;
      badge.style.background = 'rgba(59, 130, 246, 0.2)';
      badge.style.borderColor = '#3b82f6';
      badge.style.color = '#93c5fd';
    } else {
      badge.textContent = `🗺️ Navigator: ${this.navigatorName} (วางแผน & ตรวจบั๊ก)`;
      badge.style.background = 'rgba(168, 85, 247, 0.2)';
      badge.style.borderColor = '#a855f7';
      badge.style.color = '#d8b4fe';
    }
  }

  showStatusToast(msg, isError) {
    const banner = document.getElementById('status-toast');
    if (!banner) return;

    banner.textContent = msg;
    banner.style.color = isError ? '#f87171' : '#34d399';
    banner.style.borderColor = isError ? '#ef4444' : '#10b981';
    banner.style.opacity = '1';

    setTimeout(() => {
      banner.style.opacity = '0.85';
    }, 4000);
  }

  showUndoToast(msg) {
    const banner = document.getElementById('status-toast');
    if (!banner) return;

    if (this.lastDeletedCode && this.lastDeletedCode.length > 0) {
      banner.innerHTML = `
        <div style="display: flex; align-items: center; justify-content: space-between; width: 100%;">
          <span>🗑️ ${msg} (${this.lastDeletedCode.length} คำสั่ง)</span>
          <button id="btn-undo-deleted" style="padding: 2px 10px; background: #2563eb; border: 1px solid #93c5fd; border-radius: 6px; color: #fff; font-size: 0.8rem; font-weight: 800; cursor: pointer; display: inline-flex; align-items: center; gap: 4px; box-shadow: 0 0 8px rgba(59,130,246,0.6);">
            ↩️ กู้คืนโค้ดทันที
          </button>
        </div>
      `;
      banner.style.color = '#fbbf24';
      banner.style.borderColor = '#f59e0b';
      banner.style.opacity = '1';

      document.getElementById('btn-undo-deleted')?.addEventListener('click', () => {
        if (this.lastDeletedCode && this.lastDeletedCode.length > 0) {
          this.codeSequence = JSON.parse(JSON.stringify(this.lastDeletedCode));
          this.lastDeletedCode = null;
          this.renderTimeline();
          this.showStatusToast('✅ กู้คืนบล็อกคำสั่งเดิมเรียบร้อยแล้ว!', false);
          if (window.soundEngine) window.soundEngine.playVictory();
        }
      });
    } else {
      this.showStatusToast(msg, false);
    }
  }

  // ==========================================
  // Screen Wake Lock API (ป้องกันจอดับบนมือถือ)
  // ==========================================
  initWakeLock() {
    // 1. User gesture triggers wake lock request (required by mobile browsers)
    const onUserInteraction = () => {
      if (this.wakeLockEnabled && !this.wakeLockSentinel) {
        this.requestWakeLock();
      }
    };
    ['touchstart', 'touchend', 'click', 'pointerdown'].forEach(evt => {
      document.addEventListener(evt, onUserInteraction, { passive: true });
    });

    // 2. Re-acquire wake lock if user switches tabs and returns
    document.addEventListener('visibilitychange', async () => {
      if (document.visibilityState === 'visible' && this.wakeLockEnabled) {
        await this.requestWakeLock();
      }
    });

    // 3. Attempt initial request
    this.requestWakeLock();
  }

  async requestWakeLock() {
    if (!this.wakeLockEnabled) return false;

    if ('wakeLock' in navigator) {
      try {
        if (this.wakeLockSentinel !== null && !this.wakeLockSentinel.released) {
          this.updateWakeLockUI(true);
          return true;
        }
        this.wakeLockSentinel = await navigator.wakeLock.request('screen');
        console.log('🔆 Screen Wake Lock activated: จอดับอัตโนมัติถูกปิดแล้ว');
        this.wakeLockSentinel.addEventListener('release', () => {
          this.wakeLockSentinel = null;
          this.updateWakeLockUI(false);
        });
        this.updateWakeLockUI(true);
        return true;
      } catch (err) {
        console.warn('Wake Lock request failed, using fallback:', err.name, err.message);
        this.ensureVideoWakeLockFallback();
        this.updateWakeLockUI(false);
        return false;
      }
    } else {
      this.ensureVideoWakeLockFallback();
      this.updateWakeLockUI(true);
      return false;
    }
  }

  async releaseWakeLock() {
    if (this.wakeLockSentinel) {
      try {
        await this.wakeLockSentinel.release();
      } catch (e) {}
      this.wakeLockSentinel = null;
    }
    if (this.videoWakeLockFallback) {
      try {
        this.videoWakeLockFallback.pause();
      } catch (e) {}
    }
    this.updateWakeLockUI(false);
  }

  toggleWakeLock() {
    this.wakeLockEnabled = !this.wakeLockEnabled;
    if (this.wakeLockEnabled) {
      this.requestWakeLock();
      this.showStatusToast('🔆 เปิดระบบล็อกหน้าจอ: จอจะไม่ดับขณะเล่น!', false);
    } else {
      this.releaseWakeLock();
      this.showStatusToast('💤 ปิดระบบล็อกหน้าจอ: จอจะดับตามเวลาตั้งค่าของเครื่อง', false);
    }
    this.updateWakeLockUI();
  }

  updateWakeLockUI(isActive = null) {
    const active = (isActive !== null) ? isActive : (this.wakeLockEnabled && (this.wakeLockSentinel !== null || !('wakeLock' in navigator)));
    
    // Top bar icon
    const topBtn = document.getElementById('btn-toggle-wakelock');
    if (topBtn) {
      topBtn.innerHTML = active ? '🔆' : '💤';
      topBtn.title = active ? 'ป้องกันจอดับ: เปิดอยู่ (แตะเพื่อปิด)' : 'ป้องกันจอดับ: ปิดอยู่ (แตะเพื่อเปิด)';
      topBtn.style.background = active ? 'rgba(16, 185, 129, 0.25)' : 'rgba(239, 68, 68, 0.2)';
      topBtn.style.borderColor = active ? '#10b981' : '#ef4444';
      topBtn.style.color = active ? '#34d399' : '#f87171';
    }

    // Modal menu button
    const menuBtn = document.getElementById('btn-menu-toggle-wakelock');
    if (menuBtn) {
      menuBtn.style.background = active ? 'rgba(16, 185, 129, 0.25)' : 'rgba(239, 68, 68, 0.2)';
      menuBtn.style.borderColor = active ? '#10b981' : '#ef4444';
      menuBtn.style.color = active ? '#34d399' : '#f87171';
      menuBtn.innerHTML = `<span id="menu-wakelock-icon">${active ? '🔆' : '💤'}</span> จอไม่ดับ: ${active ? 'เปิด' : 'ปิด'}`;
    }
  }

  ensureVideoWakeLockFallback() {
    if (this.videoWakeLockFallback) {
      this.videoWakeLockFallback.play().catch(() => {});
      return;
    }
    try {
      const video = document.createElement('video');
      video.setAttribute('playsinline', '');
      video.setAttribute('webkit-playsinline', '');
      video.setAttribute('muted', '');
      video.setAttribute('loop', '');
      video.muted = true;
      video.style.position = 'fixed';
      video.style.width = '1px';
      video.style.height = '1px';
      video.style.top = '-50px';
      video.style.opacity = '0.01';
      video.style.pointerEvents = 'none';

      const canvas = document.createElement('canvas');
      canvas.width = 2;
      canvas.height = 2;
      if (canvas.captureStream) {
        video.srcObject = canvas.captureStream(1);
        document.body.appendChild(video);
        video.play().catch(() => {});
        this.videoWakeLockFallback = video;
      }
    } catch (e) {
      // Ignored
    }
  }
}

// Bootstrap once DOM is ready
window.addEventListener('DOMContentLoaded', () => {
  window.app = new AppController();
});
