content = r"""// =============================================
//  AI Interview System - Frontend Logic
// =============================================

// ===== STATE =====
let currentUser   = null;
let questions     = [];
let currentIndex  = 0;
let responses     = [];
let interviewStart = null;
let questionStart  = null;
let timerInterval  = null;
let lastResult     = null;
let allHistory     = [];

const CAT_ICONS = {
  'Data Structures' : '🌲',
  'Algorithms'      : '⚙️',
  'DBMS'            : '🗄️',
  'Operating Systems': '💻',
  'Computer Networks': '🌐',
  'OOP'             : '📦',
  'Python'          : '🐍',
  'HR'              : '🤝',
  'Web Development' : '🌍',
};

const API = {
  async post(url, data) {
    const r = await fetch(url, { method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(data) });
    return r.json();
  },
  async get(url) { return (await fetch(url)).json(); }
};
const sleep = ms => new Promise(r => setTimeout(r, ms));
function show(id) { const e=document.getElementById(id); if(e) e.style.display='block'; }
function hide(id) { const e=document.getElementById(id); if(e) e.style.display='none'; }

// =============================================
//  LOGIN
// =============================================
async function handleLogin() {
  const name  = document.getElementById('loginName').value.trim();
  const email = document.getElementById('loginEmail').value.trim();
  const err   = document.getElementById('loginError');
  if (!name)  { err.textContent = 'Please enter your full name.'; return; }
  if (!email || !email.includes('@')) { err.textContent = 'Please enter a valid email.'; return; }
  err.textContent = '';
  try {
    const res = await API.post('/api/login', { username: name, email });
    if (res.success) {
      currentUser = { id: res.userId, name: res.username, email };
      document.getElementById('loginPage').classList.remove('active');
      document.getElementById('dashboardPage').classList.add('active');
      document.getElementById('welcomeUser').textContent = 'Welcome, ' + currentUser.name;
      await loadDashboard();
    } else {
      err.textContent = res.message || 'Login failed.';
    }
  } catch(ex) {
    err.textContent = 'Cannot reach server. Make sure Flask is running on port 5000.';
  }
}

function logout() {
  currentUser = null; lastResult = null;
  questions = []; responses = []; allHistory = []; currentIndex = 0;
  clearInterval(timerInterval);
  ['loginName','loginEmail'].forEach(id => document.getElementById(id).value = '');
  document.getElementById('dashboardPage').classList.remove('active');
  document.getElementById('loginPage').classList.add('active');
}

// =============================================
//  DASHBOARD
// =============================================
async function loadDashboard() {
  await Promise.all([loadStats(), loadCategories()]);
}

async function loadStats() {
  try {
    const res = await API.get('/api/stats');
    if (!res.success) return;
    const d = res.data;
    document.getElementById('dashboardStats').innerHTML =
      '<div class="stat-card"><div class="stat-value">' + d.totalQuestions + '</div><div class="stat-label">Total Questions</div></div>' +
      '<div class="stat-card"><div class="stat-value">' + d.totalCategories + '</div><div class="stat-label">Categories</div></div>' +
      '<div class="stat-card"><div class="stat-value">' + allHistory.length + '</div><div class="stat-label">Interviews Taken</div></div>' +
      '<div class="stat-card"><div class="stat-value">' + (lastResult ? lastResult.overallScore + '%' : '&mdash;') + '</div><div class="stat-label">Last Score</div></div>';
  } catch(e) {}
}

async function loadCategories() {
  try {
    const res = await API.get('/api/questions/categories');
    if (!res.success) return;
    const grid = document.getElementById('categoriesGrid');
    const sel  = document.getElementById('categorySelect');
    grid.innerHTML = '';
    sel.innerHTML  = '<option value="all">Random (All Categories)</option>';
    res.data.forEach(cat => {
      const icon = CAT_ICONS[cat.name] || '📝';
      grid.innerHTML +=
        '<div class="cat-card" onclick="startCategoryInterview(\'' + cat.name + '\')">' +
        '<div class="cat-icon">' + icon + '</div>' +
        '<div class="cat-name">' + cat.name + '</div>' +
        '<div class="cat-count">' + cat.count + ' Questions</div></div>';
      sel.innerHTML += '<option value="' + cat.name + '">' + cat.name + '</option>';
    });
  } catch(e) {}
}

function startCategoryInterview(cat) {
  document.getElementById('categorySelect').value = cat;
  showTab('mock');
}

// =============================================
//  TABS
// =============================================
function showTab(tab) {
  const order = ['home','mock','results','history'];
  document.querySelectorAll('.tab-btn').forEach((b,i) => b.classList.toggle('active', order[i] === tab));
  document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
  document.getElementById('tab-' + tab).classList.add('active');
}

// =============================================
//  INTERVIEW - START
// =============================================
async function startInterview() {
  const count = Math.min(30, Math.max(1, parseInt(document.getElementById('questionCount').value) || 10));
  const cat   = document.getElementById('categorySelect').value;
  const diff  = document.getElementById('difficultySelect').value;
  try {
    const url = '/api/questions/random?count=' + count + '&category=' + encodeURIComponent(cat) + '&difficulty=' + diff;
    const res = await API.get(url);
    if (!res.success || !res.data.length) { alert('No questions found. Try different options.'); return; }
    questions = res.data; responses = []; currentIndex = 0; interviewStart = Date.now();
    show('interviewPanel'); hide('interviewConfig'); hide('processingPanel');
    document.getElementById('totalQNum').textContent = questions.length;
    renderQuestion();
  } catch(e) { alert('Failed to load questions. Check Flask server.'); }
}

// =============================================
//  INTERVIEW - QUESTION
// =============================================
function renderQuestion() {
  if (currentIndex >= questions.length) { finishInterview(); return; }
  const q = questions[currentIndex];
  questionStart = Date.now();
  document.getElementById('currentQNum').textContent  = currentIndex + 1;
  document.getElementById('qNum').textContent         = currentIndex + 1;
  document.getElementById('qCategory').textContent    = q.category;
  document.getElementById('qDifficulty').textContent  = q.difficulty;
  document.getElementById('questionText').textContent = q.question;
  document.getElementById('answerInput').value = '';
  document.getElementById('answerInput').focus();
  document.getElementById('progressBar').style.width  = (currentIndex / questions.length * 100) + '%';
  resetTimer();
}

function resetTimer() {
  clearInterval(timerInterval);
  let s = 0;
  timerInterval = setInterval(() => {
    s++;
    document.getElementById('timer').textContent =
      String(Math.floor(s/60)).padStart(2,'0') + ':' + String(s%60).padStart(2,'0');
  }, 1000);
}

function submitAnswer() { recordResponse(document.getElementById('answerInput').value.trim()); }
function skipQuestion()  { recordResponse(''); }

function recordResponse(answer) {
  responses.push({ questionId: questions[currentIndex].id, answer, timeTaken: Math.floor((Date.now()-questionStart)/1000) });
  currentIndex++;
  renderQuestion();
}

// =============================================
//  INTERVIEW - FINISH
// =============================================
async function finishInterview() {
  clearInterval(timerInterval);
  hide('interviewPanel'); show('processingPanel');
  const fill   = document.getElementById('processingFill');
  const stepIds= ['step1','step2','step3','step4'];
  stepIds.forEach((id, i) => {
    setTimeout(() => {
      const el = document.getElementById(id);
      if (el) { el.classList.add('done'); el.textContent = '✅ ' + el.textContent.replace('⏳ ',''); }
      if (fill) fill.style.width = ((i+1)/stepIds.length*100) + '%';
    }, 400 + i*500);
  });
  const totalTime = Math.floor((Date.now()-interviewStart)/1000);
  try {
    await sleep(2500);
    const res = await API.post('/api/feedback', { responses, userId: currentUser.id, username: currentUser.name, totalTime });
    hide('processingPanel');
    if (res.success) {
      lastResult = res.data; allHistory.unshift(res.data);
      renderResults(res.data); renderHistory(); showTab('results'); loadStats();
    } else { alert('Failed to generate feedback.'); resetInterviewUI(); }
  } catch(e) { alert('Server error while submitting.'); resetInterviewUI(); }
}

function resetInterviewUI() {
  hide('processingPanel'); hide('interviewPanel'); show('interviewConfig');
  const fill = document.getElementById('processingFill');
  if (fill) fill.style.width = '0%';
  ['step1','step2','step3','step4'].forEach((id,i) => {
    const labels = ['Evaluating answer relevance...','Checking keyword accuracy...','Calculating performance scores...','Generating feedback & recommendations...'];
    const el = document.getElementById(id);
    if (el) { el.className='p-step'; el.textContent='⏳ ' + labels[i]; }
  });
}

// =============================================
//  RESULTS
// =============================================
function getPerfClass(p)   { return {'Excellent':'perf-excellent','Good':'perf-good','Average':'perf-average','Needs Improvement':'perf-needs'}[p]||'perf-needs'; }
function getCircleClass(p) { return {'Excellent':'excellent','Good':'good','Average':'average','Needs Improvement':'needs'}[p]||'needs'; }

function renderResults(data) {
  const sorted    = [...data.categoryAnalysis].sort((a,b)=>b.score-a.score);
  const strengths = sorted.filter(c=>c.score>=70).slice(0,3);
  const weaknesses= sorted.filter(c=>c.score< 70).slice(0,3);

  const strengthsHtml = strengths.length
    ? strengths.map(s=>'<div class="strength-item">&#10003; '+s.category+': '+s.score+'%</div>').join('')
    : '<div class="strength-item">Keep practicing to build strengths!</div>';

  const weaknessHtml  = weaknesses.length
    ? weaknesses.map(w=>'<div class="weakness-item">&#10007; '+w.category+': '+w.score+'%</div>').join('')
    : '<div style="color:#34d399;font-size:0.85rem;padding:0.4rem">No major weak areas!</div>';

  const catBarsHtml = data.categoryAnalysis.map(c => {
    const cls = c.score>=70?'bar-green':c.score>=40?'bar-yellow':'bar-red';
    return '<div class="cat-row">' +
      '<div class="cat-row-header"><span>'+c.category+' <span style="color:#606080">('+c.count+' Qs)</span></span>' +
      '<span style="font-weight:700;color:#fff">'+c.score+'%</span></div>' +
      '<div class="cat-bar-wrap"><div class="cat-bar '+cls+'" style="width:0%" data-width="'+c.score+'%"></div></div></div>';
  }).join('');

  const recsHtml = data.recommendations.map(r=>'<li>'+r+'</li>').join('');

  const detailHtml = data.detailedFeedback.map((f,i) => {
    const sc     = f.score>=70?'score-high':f.score>=40?'score-mid':'score-low';
    const ansCls = f.yourAnswer?(f.score>=40?'':'low'):'skipped';
    const ansText= f.yourAnswer||'No answer provided (skipped)';
    const kwHits = (f.matchedKeywords||[]).slice(0,5).map(k=>'<span class="kw-hit">'+k+'</span>').join(', ');
    const kwMiss = (f.missedKeywords||[]).slice(0,5).map(k=>'<span class="kw-miss">'+k+'</span>').join(', ');
    return '<div class="feedback-item">' +
      '<div class="fb-meta"><span class="fb-cat-badge">'+f.category+'</span><span class="fb-diff-badge">'+f.difficulty+'</span></div>' +
      '<div class="fb-question">Q'+(i+1)+': '+f.question+'</div>' +
      '<div class="fb-answer '+ansCls+'"><strong>Your Answer:</strong> '+ansText+'</div>' +
      '<span class="fb-score '+sc+'">Score: '+f.score+'%</span>' +
      (kwHits?'<div class="fb-keywords">Matched: '+kwHits+'</div>':'') +
      (kwMiss?'<div class="fb-keywords">Missed keywords: '+kwMiss+'</div>':'') +
      '<div class="fb-model"><div class="fb-model-label">Key Points / Model Answer</div>'+f.modelAnswer+'</div></div>';
  }).join('');

  const mins = Math.floor(data.timeTaken/60), secs = data.timeTaken%60;
  const date = new Date(data.date).toLocaleString();
  const cc = getCircleClass(data.performance);
  const pc = getPerfClass(data.performance);
  const summary = data.overallScore>=70
    ? 'Great performance! Keep it up and aim higher.'
    : 'Keep practicing! Regular revision will improve your scores.';

  document.getElementById('resultsContainer').innerHTML =
    '<div class="results-header">' +
      '<div class="score-circle-wrap"><div class="score-circle '+cc+'">' +
        '<div class="score-num">'+data.overallScore+'</div>' +
        '<div class="score-denom">out of 100</div></div></div>' +
      '<div><span class="perf-badge '+pc+'">'+data.performance+'</span></div>' +
      '<div class="results-meta">'+data.totalQuestions+' Questions &nbsp;&middot;&nbsp; '+data.username+' &nbsp;&middot;&nbsp; '+mins+'m '+secs+'s &nbsp;&middot;&nbsp; '+date+'</div>' +
    '</div>' +
    '<div class="card"><div class="card-header">&#128202; Overall Analysis</div>' +
      '<p style="color:#8888bb;font-size:0.85rem;margin-bottom:1.2rem">'+summary+'</p>' +
      '<div class="results-grid">' +
        '<div><div class="analysis-title">&#10003; Strengths</div>'+strengthsHtml+'</div>' +
        '<div><div class="analysis-title">&#10007; Weaknesses</div>'+weaknessHtml+'</div>' +
      '</div></div>' +
    '<div class="card"><div class="card-header">&#128200; Category-wise Performance</div>'+catBarsHtml+'</div>' +
    '<div class="card"><div class="card-header">&#128161; Recommendations</div><ul class="recs-list">'+recsHtml+'</ul></div>' +
    '<div class="card"><div class="card-header">&#128221; Detailed Feedback ('+data.totalQuestions+' Questions)</div>'+detailHtml+'</div>' +
    '<div class="retry-btn-wrap"><button class="btn-primary" onclick="retryInterview()" style="padding:0.9rem 2.5rem;font-size:1rem">&#128260; Try Another Interview</button></div>';

  requestAnimationFrame(() => {
    document.querySelectorAll('.cat-bar[data-width]').forEach(bar => {
      setTimeout(() => { bar.style.width = bar.dataset.width; }, 100);
    });
  });
}

// =============================================
//  HISTORY
// =============================================
function renderHistory() {
  const c = document.getElementById('historyContainer');
  if (!allHistory.length) {
    c.innerHTML = '<div class="no-results" style="padding:2rem"><p>No interviews completed yet.</p></div>';
    return;
  }
  c.innerHTML = allHistory.map((r,i) => {
    const date = new Date(r.date).toLocaleString();
    const mins = Math.floor(r.timeTaken/60), secs = r.timeTaken%60;
    return '<div class="history-item">' +
      '<div class="hi-left">' +
        '<div style="color:#fff;font-weight:700">Interview #'+(allHistory.length-i)+'</div>' +
        '<div class="hi-date">'+date+'</div>' +
        '<div class="hi-questions">'+r.totalQuestions+' Questions &nbsp;&middot;&nbsp; '+mins+'m '+secs+'s</div>' +
      '</div>' +
      '<div class="hi-right">' +
        '<span class="perf-badge '+getPerfClass(r.performance)+'">'+r.performance+'</span>' +
        '<div class="hi-score">'+r.overallScore+'%</div>' +
      '</div></div>';
  }).join('');
}

function retryInterview() { resetInterviewUI(); showTab('mock'); }

// =============================================
//  KEYBOARD SHORTCUTS
// =============================================
document.addEventListener('keydown', e => {
  if (e.ctrlKey && e.key === 'Enter') {
    const p = document.getElementById('interviewPanel');
    if (p && p.style.display !== 'none') submitAnswer();
  }
  if (e.key === 'Enter' && document.getElementById('loginPage').classList.contains('active')) {
    handleLogin();
  }
});
"""

with open('frontend/app.js', 'w', encoding='utf-8') as f:
    f.write(content)

size = len(content)
lines = content.count('\n')
print('Done. Size:', size, 'bytes, Lines:', lines)
