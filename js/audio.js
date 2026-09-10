/**
 * CodeBot AR Sound Engine
 * Uses Web Audio API to synthesize rich retro/sci-fi game sounds natively
 * Zero external audio files required, 100% offline and low-latency
 */

class SoundEngine {
  constructor() {
    this.ctx = null;
    this.muted = false;
    this.initialized = false;
  }

  init() {
    if (this.initialized) return;
    try {
      const AudioContext = window.AudioContext || window.webkitAudioContext;
      this.ctx = new AudioContext();
      this.initialized = true;
    } catch (e) {
      console.warn('Web Audio API not supported on this browser', e);
    }
  }

  ensureContext() {
    if (!this.initialized) this.init();
    if (this.ctx && this.ctx.state === 'suspended') {
      this.ctx.resume();
    }
  }

  playBeep(freq = 440, type = 'sine', duration = 0.1, gainValue = 0.15) {
    if (this.muted) return;
    this.ensureContext();
    if (!this.ctx) return;

    try {
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();

      osc.type = type;
      osc.frequency.setValueAtTime(freq, this.ctx.currentTime);

      gain.gain.setValueAtTime(gainValue, this.ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + duration);

      osc.connect(gain);
      gain.connect(this.ctx.destination);

      osc.start();
      osc.stop(this.ctx.currentTime + duration);
    } catch (err) {
      // Audio autoplay policy fallback
    }
  }

  // Triggered when an AR touch block is tapped or clicked
  playTouch() {
    this.playBeep(659.25, 'triangle', 0.08, 0.2); // E5
  }

  // Triggered when holding hand over block to grab it
  playGrab() {
    if (this.muted) return;
    this.ensureContext();
    if (!this.ctx) return;
    this.playBeep(440, 'sine', 0.06, 0.2);
    setTimeout(() => {
      this.playBeep(784, 'triangle', 0.12, 0.25);
    }, 60);
  }

  // When robot takes a step
  playStep() {
    this.playBeep(330, 'sine', 0.05, 0.15); // E4
  }

  // Robot turns left/right
  playTurn() {
    this.playBeep(493.88, 'sine', 0.06, 0.15); // B4
  }

  // When an item or battery is picked up
  playItem() {
    if (this.muted) return;
    this.ensureContext();
    if (!this.ctx) return;

    const now = this.ctx.currentTime;
    const osc = this.ctx.createOscillator();
    const gain = this.ctx.createGain();

    osc.type = 'triangle';
    osc.frequency.setValueAtTime(523.25, now); // C5
    osc.frequency.exponentialRampToValueAtTime(1046.5, now + 0.15); // C6

    gain.gain.setValueAtTime(0.2, now);
    gain.gain.exponentialRampToValueAtTime(0.01, now + 0.15);

    osc.connect(gain);
    gain.connect(this.ctx.destination);

    osc.start(now);
    osc.stop(now + 0.15);
  }

  // Level Victory fanfare
  playVictory() {
    if (this.muted) return;
    this.ensureContext();
    if (!this.ctx) return;

    const notes = [523.25, 659.25, 783.99, 1046.50]; // C5, E5, G5, C6
    notes.forEach((freq, idx) => {
      setTimeout(() => {
        this.playBeep(freq, 'triangle', 0.25, 0.25);
      }, idx * 120);
    });
  }

  // Star sound
  playStar(index = 0) {
    const freqs = [587.33, 739.99, 880.00]; // D5, F#5, A5
    const freq = freqs[index] || 880.00;
    this.playBeep(freq, 'sine', 0.3, 0.25);
  }

  // Success chime (when loop or mission task succeeds)
  playSuccess() {
    this.playStar(1);
  }

  // Error / collision / bug detected
  playError() {
    if (this.muted) return;
    this.ensureContext();
    if (!this.ctx) return;

    const now = this.ctx.currentTime;
    const osc = this.ctx.createOscillator();
    const gain = this.ctx.createGain();

    osc.type = 'sawtooth';
    osc.frequency.setValueAtTime(180, now);
    osc.frequency.linearRampToValueAtTime(80, now + 0.25);

    gain.gain.setValueAtTime(0.2, now);
    gain.gain.exponentialRampToValueAtTime(0.01, now + 0.25);

    osc.connect(gain);
    gain.connect(this.ctx.destination);

    osc.start(now);
    osc.stop(now + 0.25);
  }

  // Synthetic crowd applause & cheering using Web Audio noise bursts & resonant filters
  playApplause(duration = 3.0) {
    if (this.muted) return;
    this.ensureContext();
    if (!this.ctx) return;

    try {
      const now = this.ctx.currentTime;
      const sampleRate = this.ctx.sampleRate;
      const bufferSize = Math.floor(sampleRate * duration);
      const noiseBuffer = this.ctx.createBuffer(1, bufferSize, sampleRate);
      const output = noiseBuffer.getChannelData(0);
      for (let i = 0; i < bufferSize; i++) {
        output[i] = (Math.random() * 2 - 1);
      }

      // 1. Crowd ambient cheer/wash
      const ambientSource = this.ctx.createBufferSource();
      ambientSource.buffer = noiseBuffer;

      const ambientFilter = this.ctx.createBiquadFilter();
      ambientFilter.type = 'bandpass';
      ambientFilter.frequency.setValueAtTime(1000, now);
      ambientFilter.Q.setValueAtTime(1.2, now);

      const ambientGain = this.ctx.createGain();
      ambientGain.gain.setValueAtTime(0.001, now);
      ambientGain.gain.linearRampToValueAtTime(0.16, now + 0.35);
      ambientGain.gain.setValueAtTime(0.16, now + duration - 0.7);
      ambientGain.gain.exponentialRampToValueAtTime(0.001, now + duration);

      ambientSource.connect(ambientFilter);
      ambientFilter.connect(ambientGain);
      ambientGain.connect(this.ctx.destination);

      ambientSource.start(now);
      ambientSource.stop(now + duration);

      // 2. Overlapping individual handclap bursts
      const clapCount = 32;
      for (let c = 0; c < clapCount; c++) {
        const clapDelay = Math.random() * (duration - 0.35);
        const clapTime = now + clapDelay;
        const clapLen = 0.025 + Math.random() * 0.04;

        const clapSource = this.ctx.createBufferSource();
        clapSource.buffer = noiseBuffer;

        const clapFilter = this.ctx.createBiquadFilter();
        clapFilter.type = 'bandpass';
        clapFilter.frequency.setValueAtTime(1100 + Math.random() * 700, clapTime);
        clapFilter.Q.setValueAtTime(2.8, clapTime);

        const clapGain = this.ctx.createGain();
        clapGain.gain.setValueAtTime(0.001, clapTime);
        clapGain.gain.linearRampToValueAtTime(0.2, clapTime + 0.004);
        clapGain.gain.exponentialRampToValueAtTime(0.001, clapTime + clapLen);

        clapSource.connect(clapFilter);
        clapFilter.connect(clapGain);
        clapGain.connect(this.ctx.destination);

        clapSource.start(clapTime);
        clapSource.stop(clapTime + clapLen);
      }
    } catch (e) {
      console.warn('Error synthesizing applause:', e);
    }
  }

  // Triumphant Fanfare + Crowd Applause Celebration
  playCelebration() {
    this.playApplause(3.5);

    // Triumphant brass-style celebration fanfare
    const fanfareNotes = [
      { freq: 523.25, time: 0.0, dur: 0.18 },  // C5
      { freq: 659.25, time: 0.16, dur: 0.18 }, // E5
      { freq: 783.99, time: 0.32, dur: 0.22 }, // G5
      { freq: 1046.50, time: 0.54, dur: 0.45 }, // C6
      { freq: 880.00, time: 0.95, dur: 0.22 }, // A5
      { freq: 1046.50, time: 1.18, dur: 0.28 }, // C6
      { freq: 1174.66, time: 1.45, dur: 0.3 }, // D6
      { freq: 1318.51, time: 1.75, dur: 0.8 }  // E6 high triumphant finale
    ];

    fanfareNotes.forEach(note => {
      setTimeout(() => {
        this.playBeep(note.freq, 'triangle', note.dur, 0.22);
      }, note.time * 1000);
    });
  }

  toggleMute() {
    this.muted = !this.muted;
    return this.muted;
  }
}

window.soundEngine = new SoundEngine();
