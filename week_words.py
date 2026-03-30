import streamlit as st
import streamlit.components.v1 as components
import json
from constants import *

st.set_page_config(page_title="Vocab Golf", layout="wide", page_icon="⛳")

# full word bank
VOCAB_JSON = json.dumps(VOCAB_SIXTH_TEST)

# ─────────────────────────────────────────────
# RENDER GAME
# ─────────────────────────────────────────────
GAME_HTML = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Fredoka+One&family=Nunito:wght@500;700;800&display=swap');

  * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: 'Nunito', sans-serif; }}

  html, body {{
    height: 100%;
    margin: 0;
  }}

  body {{
    background: linear-gradient(135deg, #1a3a2a, #2d6a4f);
    padding: 10px;
    overflow: hidden;
    box-sizing: border-box;
    height:max;
  }}

  #app {{
    display: grid;
    grid-template-columns: 1fr clamp(260px, 30vw, 380px);
    grid-template-rows: auto 1fr;
    gap: 10px;
    height: calc(80% - 20px);
    overflow:hidden;
  }}

  /* ── Header ── */
  #header {{
    grid-column: 1 / -1;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }}
  #logo {{
    font-family: 'Fredoka One', cursive;
    font-size: clamp(1rem, 2.5vw, 1.6rem);
    color: white;
    text-shadow: 0 2px 10px rgba(0,0,0,0.4);
  }}
  #logo span {{ color: #ffd700; }}
  #chips {{ display: flex; gap: 8px; flex-wrap: wrap; }}
  .chip {{
    background: rgba(255,255,255,0.15);
    border: 1.5px solid rgba(255,255,255,0.28);
    border-radius: 30px;
    padding: 4px 14px;
    color: white;
    font-weight: 800;
    font-size: clamp(0.62rem, 1.2vw, 0.8rem);
    backdrop-filter: blur(6px);
  }}
  .chip span {{ color: #ffd700; }}

  /* ── Left: Game canvas ── */
  #game-col {{
    display: flex;
    flex-direction: column;
    gap: 8px;
    min-width: 0;
    min-height: 0;
  }}
  #canvas-wrap {{
    flex: 1;
    border-radius: 14px;
    overflow: hidden;
    box-shadow: 0 6px 28px rgba(0,0,0,0.4);
    border: 3px solid rgba(255,255,255,0.18);
  }}
  #golf {{ display: block; width: 100%; height: 100%; }}

  #power-row {{
    display: flex;
    align-items: center;
    gap: 10px;
    background: rgba(255,255,255,0.1);
    border-radius: 10px;
    padding: 7px 14px;
  }}
  #power-row label {{ color:white; font-weight:800; font-size:0.76rem; letter-spacing:1px; white-space:nowrap; }}
  #power {{ flex:1; accent-color:#ffd700; height:4px; }}
  #pval  {{ color:#ffd700; font-weight:800; min-width:22px; font-size:0.86rem; }}

  /* ── Right: Q&A panel ── */
  #qa-col {{
    display: flex;
    flex-direction: column;
    gap: 8px;
    min-width: 0;
    min-height: 0;  /* allow flex child to shrink below content size */
  }}

  #feedback {{
    border-radius: 10px;
    padding: 9px 13px;
    font-weight: 700;
    font-size: 0.84rem;
    line-height: 1.4;
    display: none;
    flex-shrink: 0;  /* never squish the feedback bar */
  }}
  #feedback.success {{ display:block; background:#e8f5e9; color:#2d6a4f; border-left:4px solid #43d67c; }}
  #feedback.error   {{ display:block; background:#fff0f0; color:#c00;    border-left:4px solid #ff5252; }}

  #qa-panel {{
    background: rgba(255,255,255,0.97);
    border-radius: 16px;
    padding: 16px;
    box-shadow: 0 6px 28px rgba(0,0,0,0.25);
    flex: 1;
    min-height: 0;        /* critical: lets flex shrink the panel to fit */
    display: flex;
    flex-direction: column;
    gap: 10px;
    overflow-y: auto;     /* scroll INSIDE the panel, not the page */
  }}

  /* Question anatomy */
  .q-badge {{
    display: inline-block;
    background: #1a3a2a;
    color: white;
    font-size: 0.6rem;
    font-weight: 800;
    letter-spacing: 2px;
    text-transform: uppercase;
    padding: 3px 10px;
    border-radius: 20px;
  }}
  .q-word {{
    font-family: 'Fredoka One', cursive;
    font-size: clamp(1.2rem, 2.8vw, 1.6rem);
    color: #1a3a2a;
    line-height: 1.1;
  }}
  .q-instruction {{
    font-size: 0.8rem;
    color: #888;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }}
  /* The sentence shown in context questions */
  .q-sentence {{
    background: #f0f7ff;
    border-left: 4px solid #4a90d9;
    border-radius: 0 8px 8px 0;
    padding: 10px 12px;
    font-size: 0.9rem;
    font-weight: 700;
    color: #1a3a2a;
    line-height: 1.5;
    font-style: italic;
  }}
  /* The word highlighted in the sentence */
  .q-sentence .hl {{
    background: #ffd700;
    color: #1a3a2a;
    padding: 1px 4px;
    border-radius: 4px;
    font-style: normal;
    font-weight: 800;
  }}
  .q-def {{
    background: #f9f9f9;
    border-radius: 8px;
    padding: 10px 12px;
    font-size: 0.9rem;
    font-weight: 700;
    color: #333;
    line-height: 1.5;
  }}
  .divider {{ border:none; border-top:2px solid #f0f0f0; }}

  /* Answer input */
  #answer-input {{
    width: 100%;
    border: 2px solid #ddd;
    border-radius: 10px;
    padding: 9px 13px;
    font-size: 0.92rem;
    font-family: 'Nunito', sans-serif;
    font-weight: 700;
    color: #1a3a2a;
    background: #fafafa;
    outline: none;
    transition: border-color 0.2s, box-shadow 0.2s;
  }}
  #answer-input:focus {{
    border-color: #4caf50;
    box-shadow: 0 0 0 3px rgba(76,175,80,0.15);
    background: white;
  }}
  #answer-input::placeholder {{ color:#bbb; font-weight:500; }}

  /* Buttons */
  .btn-primary {{
    width: 100%;
    padding: 10px;
    background: linear-gradient(135deg, #2d6a4f, #40916c);
    color: white;
    border: none;
    border-radius: 10px;
    font-family: 'Nunito', sans-serif;
    font-weight: 800;
    font-size: 0.9rem;
    cursor: pointer;
    box-shadow: 0 4px 12px rgba(45,106,79,0.3);
    transition: transform 0.1s, box-shadow 0.1s;
  }}
  .btn-primary:hover {{ transform:translateY(-1px); box-shadow:0 6px 16px rgba(45,106,79,0.4); }}
  .btn-primary:active {{ transform:translateY(0); }}

  .btn-choice {{
    width: 100%;
    padding: 10px 12px;
    background: #f7f7f7;
    border: 2px solid #e8e8e8;
    border-radius: 10px;
    font-family: 'Nunito', sans-serif;
    font-weight: 700;
    font-size: 0.85rem;
    color: #1a3a2a;
    cursor: pointer;
    text-align: left;
    line-height: 1.35;
    transition: background 0.15s, border-color 0.15s;
  }}
  .btn-choice:hover  {{ background:#e8f5e9; border-color:#66bb6a; }}
  .btn-choice.correct {{ background:#e8f5e9; border-color:#43d67c; color:#2d6a4f; pointer-events:none; }}
  .btn-choice.wrong   {{ background:#fff0f0; border-color:#ff5252; color:#c00;    pointer-events:none; }}

  #choices-area {{ display:flex; flex-direction:column; gap:6px; }}
  #text-area    {{ display:flex; flex-direction:column; gap:7px; }}

  /* Start / hole-complete screens */
  .center-screen {{
    text-align: center;
    padding: 16px 0;
    display: flex;
    flex-direction: column;
    gap: 8px;
    align-items: center;
  }}
  .big-emoji {{ font-size: 2.6rem; }}
  .center-screen h2 {{
    font-family: 'Fredoka One', cursive;
    color: #1a3a2a;
    font-size: 1.35rem;
  }}
  .center-screen p {{
    color: #666;
    font-size: 0.84rem;
    font-weight: 600;
    line-height: 1.4;
    max-width: 260px;
  }}
  .score-label {{
    font-family: 'Fredoka One', cursive;
    font-size: 1.25rem;
  }}

  /* Word bank for fill-in questions */
  #word-bank {{
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    padding: 8px 0 2px;
  }}
  .word-tile {{
    background: #e8f5e9;
    border: 2px solid #a5d6a7;
    border-radius: 8px;
    padding: 5px 12px;
    font-family: 'Fredoka One', cursive;
    font-size: 0.88rem;
    color: #1a3a2a;
    cursor: pointer;
    transition: background 0.15s, border-color 0.15s, transform 0.1s;
    user-select: none;
  }}
  .word-tile:hover {{ background:#c8e6c9; border-color:#66bb6a; transform:translateY(-1px); }}
  .word-tile.used  {{ opacity:0.35; pointer-events:none; text-decoration:line-through; }}

  /* Scorecard */
  .sc-wrap {{
    background: #f5f5f5;
    border-radius: 10px;
    padding: 10px;
  }}
  .sc-wrap h4 {{
    font-size: 0.7rem;
    font-weight: 800;
    letter-spacing: 1px;
    text-transform: uppercase;
    color: #999;
    margin-bottom: 6px;
  }}
  table.sc {{
    width: 100%;
    border-collapse: collapse;
    font-size: 0.78rem;
  }}
  table.sc th {{
    background: #1a3a2a;
    color: white;
    padding: 5px 8px;
    text-align: center;
    font-weight: 800;
  }}
  table.sc td {{
    padding: 4px 8px;
    text-align: center;
    border-bottom: 1px solid #eee;
    font-weight: 600;
  }}
</style>
</head>
<body>
<div id="app">

  <!-- HEADER -->
  <div id="header">
    <div id="logo">⛳ Vocab <span>Golf</span></div>
    <div id="chips">
      <div class="chip">Hole <span id="c-hole">1</span></div>
      <div class="chip">Par <span id="c-par">3</span></div>
      <div class="chip">Strokes <span id="c-strokes">0</span></div>
      <div class="chip">Total <span id="c-total">0</span></div>
    </div>
  </div>

  <!-- LEFT: CANVAS -->
  <div id="game-col">
    <div id="canvas-wrap">
      <canvas id="golf"></canvas>
    </div>
    <div id="power-row">
      <label for="power">POWER</label>
      <input type="range" id="power" min="4" max="28" value="14">
      <span id="pval">14</span>
    </div>
  </div>

  <!-- RIGHT: Q&A -->
  <div id="qa-col">
    <div id="feedback"></div>
    <div id="qa-panel"><!-- filled by JS --></div>
  </div>

</div>
<script>
// ═══════════════════════════════════════
// VOCAB DATA
// ═══════════════════════════════════════
const VOCAB = {VOCAB_JSON};

// ═══════════════════════════════════════
// GAME STATE
// ═══════════════════════════════════════
const G = {{
  holeNum:      1,
  par:          3,
  strokes:      0,
  totalScore:   0,
  wrongStreak:  0,
  difficulty:   0,
  canShoot:     false,
  holeComplete: false,
  showQuestion: false,
  currentQ:     null,
  scorecard:    [],
}};

function parFor(h) {{ return h <= 3 ? 3 : h <= 6 ? 4 : 5; }}

function updateChips() {{
  document.getElementById('c-hole').textContent    = G.holeNum;
  document.getElementById('c-par').textContent     = G.par;
  document.getElementById('c-strokes').textContent = G.strokes;
  const t = G.totalScore;
  document.getElementById('c-total').textContent   = t > 0 ? '+'+t : ''+t;
}}

// ═══════════════════════════════════════
// QUESTION ENGINE
// Three types:
//   'context'    — show example sentence, choose which definition applies
//   'definition' — show the definition, choose the matching word meaning
//   'fill_in'    — show the definition, type the word
// ═══════════════════════════════════════
function shuffle(arr) {{ return [...arr].sort(() => Math.random() - 0.5); }}

// ── Exhausting question queue ──────────────────────────────────────────────
// Builds one "card" per (word × meaning) pair, shuffles them, then pops one
// at a time. When the deck runs out it reshuffles so the game never stalls.
// This guarantees every word/meaning is seen once before any repeats.
let _qDeck = [];

function buildDeck() {{
  const cards = [];
  VOCAB.forEach(wordEntry => {{
    wordEntry.meanings.forEach(meaning => {{
      cards.push({{ wordEntry, meaning }});
    }});
  }});
  _qDeck = shuffle(cards);
}}

function pickQuestion() {{
  if (_qDeck.length === 0) buildDeck(); // reshuffle when exhausted
  const {{ wordEntry, meaning }} = _qDeck.pop();

  const qtypes = ['context', 'context', 'definition', 'fill_in']; // context weighted 2x
  const qtype  = qtypes[Math.floor(Math.random() * qtypes.length)];

  if (qtype === 'fill_in') {{
    const otherWords = VOCAB.map(v => v.word).filter(w => w !== wordEntry.word);
    const bank = shuffle([wordEntry.word, ...shuffle(otherWords).slice(0, 3)]);
    return {{
      qtype,
      word:    wordEntry.word,
      meaning,
      prompt:  meaning.def,
      answer:  wordEntry.word,
      choices: null,
      _bank:   bank,
    }};
  }}

  const choices = shuffle([meaning.def, ...meaning.distractors.slice(0, 2)]);

  if (qtype === 'context') {{
    return {{
      qtype,
      word:    wordEntry.word,
      meaning,
      prompt:  meaning.example,
      answer:  meaning.def,
      choices,
    }};
  }}

  // 'definition' type
  const siblingDefs    = wordEntry.meanings.filter(m => m.def !== meaning.def).map(m => m.def);
  const allDistractors = shuffle([...siblingDefs, ...meaning.distractors]);
  const defChoices     = shuffle([meaning.def, ...allDistractors.slice(0, 2)]);
  return {{
    qtype: 'definition',
    word:    wordEntry.word,
    meaning,
    prompt:  meaning.example,
    answer:  meaning.def,
    choices: defChoices,
  }};
}}

// Build the initial deck immediately so the first question is always unique
buildDeck();

// ═══════════════════════════════════════
// FEEDBACK
// ═══════════════════════════════════════
function showFeedback(msg, type) {{
  const el = document.getElementById('feedback');
  el.textContent = msg;
  el.className = type;
  clearTimeout(showFeedback._t);
  showFeedback._t = setTimeout(() => el.className = '', 3800);
}}

// ═══════════════════════════════════════
// PANEL RENDERER
// ═══════════════════════════════════════
function renderPanel() {{
  const panel = document.getElementById('qa-panel');
  if (G.holeComplete)   {{ renderHoleComplete(panel); }}
  else if (!G.showQuestion) {{ renderStart(panel); }}
  else {{ renderQuestion(panel); }}
  panel.scrollTop = 0;  // always snap back to top — no manual scrolling needed
}}

// ── Start screen ──
function renderStart(panel) {{
  panel.innerHTML = `
    <div class="center-screen">
      <div class="big-emoji">🏌️</div>
      <h2>Ready to tee off?</h2>
      <p>Answer a vocabulary question to earn your first shot. Each correct answer unlocks a putt!</p>
      <button class="btn-primary" style="width:auto;padding:10px 28px" onclick="getQuestion()">
        📖 Get Question
      </button>
    </div>`;
}}

function getQuestion() {{
  G.currentQ     = pickQuestion();
  G.showQuestion = true;
  renderPanel();
}}

// ── Active question ──
function renderQuestion(panel) {{
  const {{ qtype, word, meaning, prompt, answer, choices }} = G.currentQ;

  const badgeText = {{
    context:    'IN CONTEXT',
    definition: 'WHICH MEANING?',
    fill_in:    'FILL IN THE BLANK',
  }}[qtype];

  // Highlight the target word inside the sentence
  function highlightWord(sentence, w) {{
    const re = new RegExp(`\\\\b(${{w}}|${{w.charAt(0).toUpperCase() + w.slice(1)}})(ed|ing|s|es|d)?\\\\b`, 'g');
    return sentence.replace(re, m => `<span class="hl">${{m}}</span>`);
  }}

  let topHTML = `<span class="q-badge">${{badgeText}}</span>`;

  if (qtype === 'context') {{
    // Show the word as the title, sentence below it
    topHTML += `
      <div class="q-word">${{word}}</div>
      <div class="q-instruction">How is the word used in this sentence?</div>
      <div class="q-sentence">${{highlightWord(prompt, word)}}</div>
      <div class="q-instruction" style="margin-top:2px">Choose the correct definition:</div>`;
  }} else if (qtype === 'definition') {{
    // Show the sentence, ask which definition applies
    topHTML += `
      <div class="q-word">${{word}}</div>
      <div class="q-instruction">Read the sentence, then pick the matching definition:</div>
      <div class="q-sentence">${{highlightWord(prompt, word)}}</div>`;
  }} else {{
    // fill_in: show definition, type the word — with a word bank
    const bank = G.currentQ._bank || [];
    const bankHTML = bank.length ? `
      <div style="font-size:0.72rem;font-weight:800;color:#888;letter-spacing:1px;text-transform:uppercase;margin-top:4px">WORD BANK</div>
      <div id="word-bank">${{bank.map(w =>
        `<div class="word-tile" onclick="pickFromBank(this,'${{w}}')">${{w}}</div>`
      ).join('')}}</div>` : '';
    topHTML += `
      <div class="q-instruction">What word fits this definition?</div>
      <div class="q-def">${{prompt}}</div>
      ${{bankHTML}}`;
  }}

  let answerHTML = '';
  if (choices) {{
    answerHTML = `<div id="choices-area">${{
      choices.map((c, i) =>
        `<button class="btn-choice" onclick="submitChoice(${{i}})">${{c}}</button>`
      ).join('')
    }}</div>`;
  }} else {{
    answerHTML = `
      <div id="text-area">
        <input id="answer-input" type="text"
               placeholder="Type the word here…"
               onkeydown="if(event.key==='Enter') submitText()">
        <button class="btn-primary" onclick="submitText()">Submit ➜</button>
      </div>`;
  }}

  panel.innerHTML = `
    ${{topHTML}}
    <hr class="divider">
    ${{answerHTML}}
  `;

  const inp = document.getElementById('answer-input');
  if (inp) setTimeout(() => inp.focus(), 40);
}}

// ── Submissions ──
function submitChoice(idx) {{
  const {{ choices, answer, word }} = G.currentQ;
  const chosen  = choices[idx];
  const correct = chosen === answer;
  document.querySelectorAll('.btn-choice').forEach((b, i) => {{
    b.disabled = true;
    if (choices[i] === answer) b.classList.add('correct');
    else if (i === idx && !correct) b.classList.add('wrong');
  }});
  setTimeout(() => correct ? onCorrect() : onWrong(word, answer), 900);
}}

function pickFromBank(el, word) {{
  const inp = document.getElementById('answer-input');
  if (inp) {{ inp.value = word; inp.focus(); }}
  document.querySelectorAll('.word-tile').forEach(t => t.classList.remove('used'));
  el.classList.add('used');
}}

function submitText() {{
  const inp = document.getElementById('answer-input');
  if (!inp || !inp.value.trim()) return;
  const {{ word }} = G.currentQ;
  const correct = inp.value.trim().toLowerCase() === word.toLowerCase();
  correct ? onCorrect() : onWrong(word, word);
}}

function onCorrect() {{
  G.wrongStreak  = 0;
  G.canShoot     = true;
  G.showQuestion = false;
  showFeedback('✅ Correct! Take your shot!', 'success');
  renderPanel();
  updateObstacles();
}}

function onWrong(word, correctAnswer) {{
  G.wrongStreak++;
  if (G.wrongStreak >= 2) {{
    G.difficulty = Math.min(3, G.difficulty + 1);
    showFeedback(`❌ Wrong again! Course got harder. Answer: "${{correctAnswer}}"`, 'error');
    updateObstacles();
  }} else {{
    showFeedback(`❌ Not quite. The answer was: "${{correctAnswer}}"`, 'error');
  }}
  G.currentQ = pickQuestion();
  renderPanel();
}}

// ── Hole complete ──
function renderHoleComplete(panel) {{
  const diff = G.strokes - G.par;
  const infos = [
    [d => d <= -2, '🦅', 'Eagle!',       '#43d67c'],
    [d => d === -1,'🐦', 'Birdie!',      '#43d67c'],
    [d => d === 0, '⛳', 'Even Par',     '#ffd700'],
    [d => d === 1, '😬', 'Bogey',        '#ffa500'],
    [d => d === 2, '😅', 'Double Bogey', '#ff7043'],
    [() => true,   '🌧️', `+${{diff}}`,  '#ff5252'],
  ];
  const [, emoji, label, color] = infos.find(([fn]) => fn(diff));

  const rows = G.scorecard.map(e => {{
    const d = e.strokes - e.par;
    const c = d <= 0 ? '#43d67c' : d === 1 ? '#ffa500' : '#ff5252';
    return `<tr>
      <td>${{e.hole}}</td><td>${{e.par}}</td><td>${{e.strokes}}</td>
      <td style="color:${{c}};font-weight:800">${{e.result}}</td>
    </tr>`;
  }}).join('');

  const tot = G.totalScore;
  const tc  = tot <= 0 ? '#43d67c' : '#ff5252';
  const tl  = tot > 0 ? '+'+tot : ''+tot;

  panel.innerHTML = `
    <div class="center-screen">
      <div class="big-emoji">${{emoji}}</div>
      <h2>Hole ${{G.holeNum}} Complete!</h2>
      <p>${{G.strokes}} stroke${{G.strokes!==1?'s':''}} &middot; Par ${{G.par}}</p>
      <div class="score-label" style="color:${{color}}">${{label}}</div>
      <button class="btn-primary" style="width:auto;padding:10px 28px" onclick="nextHole()">
        ➜ Next Hole
      </button>
    </div>
    ${{G.scorecard.length ? `
    <div class="sc-wrap">
      <h4>📋 Scorecard</h4>
      <table class="sc">
        <thead><tr><th>Hole</th><th>Par</th><th>Strokes</th><th>Result</th></tr></thead>
        <tbody>${{rows}}</tbody>
        <tfoot>
          <tr style="background:#ececec">
            <td colspan="3" style="text-align:right;font-weight:800;padding-right:10px">Total</td>
            <td style="color:${{tc}};font-weight:900">${{tl}}</td>
          </tr>
        </tfoot>
      </table>
    </div>` : ''}}
  `;
}}

function nextHole() {{
  G.holeNum++;
  G.par          = parFor(G.holeNum);
  G.strokes      = 0;
  G.holeComplete = false;
  G.canShoot     = false;
  G.wrongStreak  = 0;
  G.difficulty   = Math.min(G.holeNum - 1, 3);
  G.showQuestion = false;
  G.currentQ     = null;
  resetBall();
  updateObstacles();
  updateChips();
  renderPanel();
}}

// ═══════════════════════════════════════
// CANVAS / PHYSICS
// ═══════════════════════════════════════
const canvas = document.getElementById('golf');
const ctx    = canvas.getContext('2d');
const WORLD_W = 2000;

let W, H, GY;

function resizeCanvas() {{
  doResize();
}}

const GRAV = 0.28, FRIC = 0.993, BOUNCE = 0.32, ROLL = 0.95;
let cam  = {{ x: 0 }};
let ball = {{ x: 120, y: 0, vx: 0, vy: 0, r: 8 }};
let hole = {{ x: 1820, y: 0, r: 13 }};
let _initialized = false;

function resetBall() {{
  ball = {{ x: 120, y: GY, vx: 0, vy: 0, r: 8 }};
  cam  = {{ x: 0 }};
  _stuckFrames = 0;
  moving = false;
}}

let OBS = [];
function updateObstacles() {{ OBS = buildObs(G.difficulty); }}
function buildObs(d) {{
  const o = [];
  if (d >= 1) {{ o.push({{t:'sand',  x:520,  w:180}}); o.push({{t:'sand',  x:1200, w:160}}); }}
  if (d >= 2)    o.push({{t:'water', x:860,  w:200}});
  if (d >= 3) {{ o.push({{t:'water', x:1480, w:150}}); o.push({{t:'sand',  x:320,  w:130}}); }}
  return o;
}}
function obsAt(x) {{ for (const o of OBS) if (x > o.x && x < o.x + o.w) return o; return null; }}

// Aiming
let aiming = false, aimX = 0, aimY = 0, moving = false;

function getPos(e) {{
  const r = canvas.getBoundingClientRect();
  return {{
    x: (e.clientX - r.left) * (W / r.width)  + cam.x,
    y: (e.clientY - r.top)  * (H / r.height),
  }};
}}

canvas.addEventListener('mousedown', e => {{
  if (!G.canShoot || moving || G.holeComplete) return;
  aiming = true;
  const p = getPos(e); aimX = p.x; aimY = p.y;
}});
canvas.addEventListener('mousemove', e => {{
  if (!aiming) return;
  const p = getPos(e); aimX = p.x; aimY = p.y;
}});
canvas.addEventListener('mouseup', () => {{
  if (!aiming || !G.canShoot) return;
  aiming = false;
  const dx = (ball.x - cam.x) - (aimX - cam.x);
  const dy = ball.y - aimY;
  if (Math.sqrt(dx*dx + dy*dy) < 5) return;
  const pow = parseFloat(document.getElementById('power').value);
  ball.vx = dx * 0.13 * pow / 10;
  ball.vy = dy * 0.13 * pow / 10;
  moving = true;
  G.strokes++;
  G.canShoot     = false;
  G.showQuestion = true;
  G.currentQ     = pickQuestion();
  updateChips();
  renderPanel();
}});

['touchstart','touchmove','touchend'].forEach(ev => {{
  canvas.addEventListener(ev, e => {{
    e.preventDefault();
    const t = e.touches[0] || e.changedTouches[0];
    canvas.dispatchEvent(new MouseEvent(
      ev==='touchstart'?'mousedown':ev==='touchmove'?'mousemove':'mouseup',
      {{ clientX:t.clientX, clientY:t.clientY }}
    ));
  }}, {{ passive:false }});
}});

const slider = document.getElementById('power');
const pval   = document.getElementById('pval');
slider.addEventListener('input', () => pval.textContent = slider.value);

let _stuckFrames = 0;

function updatePhysics() {{
  if (!moving) return;
  ball.vy += GRAV;
  ball.x  += ball.vx; ball.y += ball.vy;
  ball.vx *= FRIC;    ball.vy *= FRIC;

  // Ceiling clamp — prevent ball escaping top
  if (ball.y - ball.r < 0) {{
    ball.y = ball.r;
    ball.vy = Math.abs(ball.vy) * BOUNCE;
  }}

  const o = obsAt(ball.x);
  if (ball.y >= GY) {{
    ball.y = GY; ball.vy *= -BOUNCE; ball.vx *= ROLL;
    if (o && o.t === 'sand')  {{ ball.vx *= 0.62; ball.vy *= 0.35; }}
    if (o && o.t === 'water') {{
      showFeedback('💧 Water hazard! +1 stroke penalty.', 'error');
      // Place before the water hazard, clamped to valid range
      const safeX = Math.max(ball.r + 10, Math.min(WORLD_W - ball.r - 10, o.x - 40));
      ball.x = safeX; ball.y = GY; ball.vx = 0; ball.vy = 0;
      _stuckFrames = 0;
      moving = false; G.strokes++; updateChips();
      return;
    }}
  }}

  // Hard world bounds — bounce off left/right walls
  if (ball.x - ball.r < ball.r) {{
    ball.x = ball.r * 2; ball.vx = Math.abs(ball.vx) * 0.5;
  }} else if (ball.x + ball.r > WORLD_W - ball.r) {{
    ball.x = WORLD_W - ball.r * 2; ball.vx = -Math.abs(ball.vx) * 0.5;
  }}

  const dx = ball.x - hole.x, dy = ball.y - hole.y;
  if (Math.sqrt(dx*dx + dy*dy) < hole.r + ball.r - 5) {{
    ball.x = hole.x; ball.y = hole.y; ball.vx = 0; ball.vy = 0;
    _stuckFrames = 0;
    moving = false; onHoleComplete();
    return;
  }}

  const speed = Math.sqrt(ball.vx*ball.vx + ball.vy*ball.vy);
  if (speed < 0.12 && ball.y >= GY - 1) {{
    ball.vx = 0; ball.vy = 0; moving = false;
    _stuckFrames = 0;
  }} else if (speed < 0.5) {{
    // Stuck-in-corner / slow creep detection
    _stuckFrames++;
    if (_stuckFrames > 120) {{
      // Force stop — ball is crawling and going nowhere
      ball.vx = 0; ball.vy = 0; moving = false;
      _stuckFrames = 0;
    }}
  }} else {{
    _stuckFrames = 0;
  }}

  cam.x += (ball.x - W/2 - cam.x) * 0.09;
  cam.x = Math.max(0, Math.min(cam.x, WORLD_W - W));
}}

function onHoleComplete() {{
  G.holeComplete = true;
  const diff   = G.strokes - G.par;
  G.totalScore += diff;
  const lmap   = {{'-2':'Eagle 🦅','-1':'Birdie 🐦','0':'Even Par 🤝','1':'Bogey 😬','2':'Double Bogey 😅'}};
  const result = lmap[String(diff)] || (diff > 0 ? `+${{diff}} 🌧️` : `${{diff}} 🦅`);
  G.scorecard.push({{ hole: G.holeNum, par: G.par, strokes: G.strokes, result }});
  updateChips();
  renderPanel();
}}

// ═══════════════════════════════════════
// DRAWING
// ═══════════════════════════════════════
function drawSky() {{
  const g = ctx.createLinearGradient(0,0,0,GY);
  g.addColorStop(0,'#3aa8d8'); g.addColorStop(1,'#c5ecff');
  ctx.fillStyle = g; ctx.fillRect(0,0,W,GY);
  [[0.08,0.12,60],[0.28,0.2,46],[0.54,0.1,70],[0.74,0.18,53],[0.9,0.13,62]]
    .forEach(([fx,fy,s]) => {{
      const wx = fx*WORLD_W - cam.x, cy = fy*GY;
      ctx.fillStyle = 'rgba(255,255,255,0.86)';
      ctx.beginPath();
      ctx.arc(wx,cy,s*.5,0,Math.PI*2);     ctx.arc(wx+s*.4,cy-s*.1,s*.38,0,Math.PI*2);
      ctx.arc(wx+s*.8,cy,s*.42,0,Math.PI*2); ctx.arc(wx+s*.35,cy+s*.1,s*.32,0,Math.PI*2);
      ctx.fill();
    }});
}}

function drawGround() {{
  ctx.fillStyle='#388e3c'; ctx.fillRect(-cam.x,GY,WORLD_W,H-GY);
  ctx.fillStyle='#66bb6a'; ctx.fillRect(90-cam.x,GY,WORLD_W-160,H-GY);
  ctx.fillStyle='#81c784';
  ctx.beginPath(); ctx.ellipse(120-cam.x,GY,58,16,0,0,Math.PI*2); ctx.fill();
  ctx.fillStyle='#a5d6a7';
  ctx.beginPath(); ctx.ellipse(hole.x-cam.x,GY,130,30,0,0,Math.PI*2); ctx.fill();
}}

function drawObs() {{
  for (const o of OBS) {{
    const rx = o.x - cam.x;
    if (o.t === 'sand') {{
      ctx.fillStyle='#f9e07f'; ctx.strokeStyle='#c9a227'; ctx.lineWidth=1.5;
      ctx.beginPath(); ctx.ellipse(rx+o.w/2,GY+1,o.w/2,15,0,0,Math.PI*2);
      ctx.fill(); ctx.stroke();
      ctx.fillStyle='rgba(180,140,0,0.18)';
      for(let i=0;i<5;i++) {{ ctx.beginPath(); ctx.arc(rx+12+i*26,GY-1,4,0,Math.PI*2); ctx.fill(); }}
      ctx.fillStyle='#7a5a0a'; ctx.font='bold 10px sans-serif'; ctx.textAlign='center';
      ctx.fillText('SAND', rx+o.w/2, GY-11);
    }} else {{
      ctx.fillStyle='#29b6f6'; ctx.strokeStyle='#0277bd'; ctx.lineWidth=1.5;
      ctx.beginPath(); ctx.ellipse(rx+o.w/2,GY+3,o.w/2,19,0,0,Math.PI*2);
      ctx.fill(); ctx.stroke();
      ctx.strokeStyle='rgba(255,255,255,0.38)'; ctx.lineWidth=1.2;
      [0,1,2].forEach(i => {{
        ctx.beginPath(); ctx.ellipse(rx+o.w/2,GY+4,14+i*10,4,0,0,Math.PI*2); ctx.stroke();
      }});
      ctx.fillStyle='#014a7a'; ctx.font='bold 10px sans-serif'; ctx.textAlign='center';
      ctx.fillText('WATER', rx+o.w/2, GY-12);
    }}
  }}
}}

function drawFlag() {{
  const hx = hole.x - cam.x, hy = hole.y;
  ctx.beginPath(); ctx.ellipse(hx,hy,12,4,0,0,Math.PI*2);
  ctx.fillStyle='#111'; ctx.fill();
  ctx.strokeStyle='#555'; ctx.lineWidth=2;
  ctx.beginPath(); ctx.moveTo(hx,hy); ctx.lineTo(hx,hy-68); ctx.stroke();
  ctx.fillStyle='#e53935';
  ctx.beginPath(); ctx.moveTo(hx,hy-68); ctx.lineTo(hx+24,hy-58); ctx.lineTo(hx,hy-48);
  ctx.closePath(); ctx.fill();
  if (!G.holeComplete) {{
    const dist = Math.round((hole.x - ball.x) / 8);
    if (dist > 0 && dist < 999) {{
      ctx.fillStyle='rgba(0,0,0,0.5)'; ctx.font='bold 11px sans-serif'; ctx.textAlign='center';
      ctx.fillText(dist+'y', hx, hy-78);
    }}
  }}
}}

function drawBall() {{
  const bx = ball.x - cam.x, by = ball.y;
  ctx.fillStyle='rgba(0,0,0,0.14)';
  ctx.beginPath(); ctx.ellipse(bx,GY+2,9,3,0,0,Math.PI*2); ctx.fill();
  const g = ctx.createRadialGradient(bx-2,by-2,1,bx,by,ball.r);
  g.addColorStop(0,'#fff'); g.addColorStop(1,'#ccc');
  ctx.fillStyle=g; ctx.beginPath(); ctx.arc(bx,by,ball.r,0,Math.PI*2);
  ctx.fill(); ctx.strokeStyle='#bbb'; ctx.lineWidth=0.5; ctx.stroke();
}}

function drawAimLine() {{
  if (!aiming || !G.canShoot) return;
  const bx = ball.x-cam.x, by = ball.y;
  const axS = aimX-cam.x, ayS = aimY;
  const pow = parseFloat(slider.value);
  let sx=ball.x, sy=ball.y, svx=(bx-axS)*0.13*pow/10, svy=(by-ayS)*0.13*pow/10;
  ctx.fillStyle='rgba(255,255,255,0.62)';
  for(let i=0;i<18;i++) {{
    svy+=GRAV; sx+=svx; sy+=svy; svx*=FRIC; svy*=FRIC;
    if(sy>GY) {{ sy=GY; svy*=-BOUNCE; svx*=ROLL; }}
    ctx.beginPath(); ctx.arc(sx-cam.x,sy,2.4*(1-i/20),0,Math.PI*2); ctx.fill();
  }}
  ctx.strokeStyle='rgba(255,80,80,0.72)'; ctx.lineWidth=1.5;
  ctx.setLineDash([5,4]);
  ctx.beginPath(); ctx.moveTo(bx,by); ctx.lineTo(axS,ayS); ctx.stroke();
  ctx.setLineDash([]);
}}

function drawHUD() {{
  if (G.difficulty > 0) {{
    ctx.fillStyle='rgba(180,30,30,0.76)';
    ctx.beginPath(); ctx.roundRect(W-126,8,118,24,12); ctx.fill();
    ctx.fillStyle='white'; ctx.font='bold 10px sans-serif'; ctx.textAlign='center';
    ctx.fillText('DIFFICULTY +'+G.difficulty, W-67, 24);
  }}
  let msg='';
  if (G.canShoot && !moving && !G.holeComplete)
    msg = '🖱️  Drag from ball · release to shoot';
  else if (!G.canShoot && !G.holeComplete && !G.showQuestion)
    msg = 'Get a question to unlock your shot';
  else if (!G.canShoot && !G.holeComplete && G.showQuestion)
    msg = 'Answer the question →';
  if (msg) {{
    ctx.font='700 11px sans-serif';
    const tw = ctx.measureText(msg).width + 26;
    ctx.fillStyle='rgba(0,0,0,0.44)';
    ctx.beginPath(); ctx.roundRect(W/2-tw/2, H-32, tw, 22, 11); ctx.fill();
    ctx.fillStyle = G.canShoot ? '#fff' : 'rgba(255,255,180,0.94)';
    ctx.textAlign='center';
    ctx.fillText(msg, W/2, H-17);
  }}
}}

// ═══════════════════════════════════════
// LOOP + INIT
// ═══════════════════════════════════════
function loop() {{
  updatePhysics();
  ctx.clearRect(0,0,W,H);
  drawSky(); drawGround(); drawObs(); drawFlag(); drawAimLine(); drawBall(); drawHUD();
  requestAnimationFrame(loop);
}}

// ── Dynamic sizing via ResizeObserver ──
// This correctly handles large external monitors, window resizes,
// and Streamlit's iframe—no hardcoded heights needed.
function doResize() {{
  const wrap = document.getElementById('canvas-wrap');
  if (!wrap) return;
  W = wrap.clientWidth  || 600;
  H = wrap.clientHeight || 400;
  if (H < 50) return; // layout not ready yet
  canvas.width  = W;
  canvas.height = H;
  GY = Math.round(H * 0.82);
  hole.y = GY;

  if (!_initialized) {{
    // First valid resize — seat ball and start game
    ball.x = 120; ball.y = GY; ball.vx = 0; ball.vy = 0;
    _initialized = true;
    updateObstacles();
    updateChips();
    renderPanel();
    loop();
  }} else {{
    // Subsequent resize — re-seat ball if it's above ground
    if (!moving && ball.y !== GY) ball.y = GY;
    cam.x = Math.max(0, Math.min(cam.x, WORLD_W - W));
  }}
}}

// Use ResizeObserver so we react to *actual* layout changes, not just window resize
const _ro = new ResizeObserver(() => doResize());
_ro.observe(document.getElementById('canvas-wrap'));

// ── Tell Streamlit to size the iframe to fill the viewport ──
function reportHeight() {{
  // Use the parent window's inner height if accessible, else fall back to screen
  const h = window.innerHeight || screen.height || 900;
  window.parent.postMessage({{type:'streamlit:setFrameHeight', height: h}}, '*');
}}
window.addEventListener('load', () => {{ reportHeight(); setTimeout(reportHeight, 300); }});
window.addEventListener('resize', reportHeight);

</script>
</body>
</html>
"""

components.html(GAME_HTML, height=1200, scrolling=False)