"""Direct patch of app.js using exact strings found in the file."""
path = 'frontend/app.js'
js   = open(path, encoding='utf-8').read()

# --- 1. Add Java to CAT_ICONS ---
js = js.replace(
    "  'Python'          : '\U0001f40d',\n  'HR'              : '\U0001f91d',",
    "  'Python'          : '\U0001f40d',\n  'Java'            : '\u2615',\n  'HR'              : '\U0001f91d',"
)

# --- 2. Add localStorage helpers after CAT_ICONS closing brace ---
STORAGE = (
    "\n// =============================================\n"
    "//  LOCALSTORAGE - persist history by email\n"
    "// =============================================\n"
    "function storageKey(email) {\n"
    "  return 'ai_interview_' + email.toLowerCase().trim();\n"
    "}\n"
    "function saveHistory(email, history) {\n"
    "  try { localStorage.setItem(storageKey(email), JSON.stringify(history)); } catch (_) {}\n"
    "}\n"
    "function loadHistory(email) {\n"
    "  try {\n"
    "    const raw = localStorage.getItem(storageKey(email));\n"
    "    return raw ? JSON.parse(raw) : [];\n"
    "  } catch (_) { return []; }\n"
    "}\n"
)
js = js.replace(
    "};\n\nconst API = {",
    "};" + STORAGE + "\nconst API = {"
)

# --- 3. Restore history on login, right after currentUser is set ---
js = js.replace(
    "      currentUser = { id: res.userId, name: res.username, email };\n"
    "      document.getElementById('loginPage').classList.remove('active');",
    "      currentUser = { id: res.userId, name: res.username, email };\n"
    "      // Restore persisted history for this email\n"
    "      allHistory = loadHistory(email);\n"
    "      lastResult = allHistory.length > 0 ? allHistory[0] : null;\n"
    "      document.getElementById('loginPage').classList.remove('active');"
)

# --- 4. Call renderHistory() after loadDashboard() in login ---
js = js.replace(
    "      await loadDashboard();\n    } else {",
    "      await loadDashboard();\n      renderHistory();\n    } else {"
)

# --- 5. Add userEmail to feedback POST ---
js = js.replace(
    "      userId: currentUser.id, username: currentUser.name, totalTime",
    "      userId: currentUser.id, username: currentUser.name, userEmail: currentUser.email, totalTime"
)

# --- 6. Save to localStorage after each interview finishes ---
js = js.replace(
    "      lastResult = res.data; allHistory.unshift(res.data);\n"
    "      renderResults(res.data); renderHistory(); showTab('results'); loadStats();",
    "      lastResult = res.data; allHistory.unshift(res.data);\n"
    "      saveHistory(currentUser.email, allHistory);\n"
    "      renderResults(res.data); renderHistory(); showTab('results'); loadStats();"
)

# --- 7. Make history rows clickable ---
js = js.replace(
    "    return '<div class=history-item>'",
    "    return '<div class=history-item onclick=viewHistoryResult(' + i + ') style=cursor:pointer>'"
)

# --- 8. Add viewHistoryResult function before retryInterview ---
VIEW_FN = (
    "// Click a history row to re-view that result\n"
    "function viewHistoryResult(index) {\n"
    "  const result = allHistory[index];\n"
    "  if (!result) return;\n"
    "  renderResults(result);\n"
    "  showTab('results');\n"
    "}\n\n"
)
js = js.replace(
    "function retryInterview() { resetInterviewUI(); showTab('mock'); }",
    VIEW_FN + "function retryInterview() { resetInterviewUI(); showTab('mock'); }"
)

with open(path, 'w', encoding='utf-8') as f:
    f.write(js)

# Verify
checks = [
    ('Java icon',        'Java' in js),
    ('storageKey',       'storageKey' in js),
    ('saveHistory',      'saveHistory' in js),
    ('loadHistory',      'loadHistory' in js),
    ('userEmail sent',   'userEmail: currentUser.email' in js),
    ('history restored', 'loadHistory(email)' in js),
    ('persist finish',   'saveHistory(currentUser.email' in js),
    ('viewHistoryResult','viewHistoryResult' in js),
]
print('app.js:', len(js), 'bytes')
all_ok = True
for name, ok in checks:
    if not ok: all_ok = False
    print(('  OK' if ok else '  MISSING'), '-', name)
print('All OK!' if all_ok else 'Some FAILED - check replacements.')
