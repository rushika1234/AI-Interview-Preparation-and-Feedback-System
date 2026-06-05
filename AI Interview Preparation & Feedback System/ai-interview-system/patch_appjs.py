"""Patches app.js with localStorage persistence and Java icon."""
import re

path = 'frontend/app.js'
src  = open(path, encoding='utf-8').read()

# 1. Add Java to CAT_ICONS (insert after Python line)
src = src.replace(
    "  'Python':            '🐍',\n  'HR':",
    "  'Python':            '🐍',\n  'Java':              '☕',\n  'HR':"
)

# 2. Add localStorage helpers right after the CAT_ICONS closing brace
STORAGE_HELPERS = '''
// =============================================
//  LOCALSTORAGE — persist history by email
// =============================================
function storageKey(email) {
  return 'ai_interview_' + email.toLowerCase().trim();
}
function saveHistory(email, history) {
  try { localStorage.setItem(storageKey(email), JSON.stringify(history)); } catch (_) {}
}
function loadHistory(email) {
  try {
    const raw = localStorage.getItem(storageKey(email));
    return raw ? JSON.parse(raw) : [];
  } catch (_) { return []; }
}
'''
src = src.replace(
    "// ===== API =====",
    STORAGE_HELPERS + "// ===== API ====="
)

# 3. In handleLogin: restore history from localStorage after currentUser is set
OLD_LOGIN_BLOCK = (
    "      currentUser = { id: res.userId, name: res.username, email };\n"
    "      $('loginPage').classList.remove('active');"
)
NEW_LOGIN_BLOCK = (
    "      currentUser = { id: res.userId, name: res.username, email };\n"
    "\n"
    "      // Restore persisted history for this email\n"
    "      allHistory = loadHistory(email);\n"
    "      lastResult = allHistory.length > 0 ? allHistory[0] : null;\n"
    "\n"
    "      $('loginPage').classList.remove('active');"
)
src = src.replace(OLD_LOGIN_BLOCK, NEW_LOGIN_BLOCK)

# 4. In handleLogin after loadDashboard: call renderHistory()
src = src.replace(
    "      await loadDashboard();\n    } else {",
    "      await loadDashboard();\n      renderHistory();   // restore history tab on login\n    } else {"
)

# 5. In finishInterview POST call: add userEmail field
src = src.replace(
    "      userId:    currentUser.id,\n      username:  currentUser.name,\n      totalTime,",
    "      userId:    currentUser.id,\n      username:  currentUser.name,\n      userEmail: currentUser.email,\n      totalTime,"
)

# 6. After lastResult = res.data: save to localStorage and call renderHistory
OLD_SAVE = (
    "      lastResult = res.data;\n"
    "      allHistory.unshift(res.data);\n"
    "      renderResults(res.data);\n"
    "      renderHistory();"
)
NEW_SAVE = (
    "      lastResult = res.data;\n"
    "      allHistory.unshift(res.data);\n"
    "      saveHistory(currentUser.email, allHistory);  // persist by email\n"
    "      renderResults(res.data);\n"
    "      renderHistory();"
)
src = src.replace(OLD_SAVE, NEW_SAVE)

# 7. Make history items clickable — add onclick and viewHistoryResult function
OLD_HIST_ITEM = "    return `\n      <div class=\"history-item\">"
NEW_HIST_ITEM  = "    return `\n      <div class=\"history-item\" onclick=\"viewHistoryResult(${i})\" style=\"cursor:pointer\" title=\"Click to view full result\">"
src = src.replace(OLD_HIST_ITEM, NEW_HIST_ITEM)

# 8. Add viewHistoryResult before retryInterview
VIEW_FN = '''
// Click a history row to re-view that full result
function viewHistoryResult(index) {
  const result = allHistory[index];
  if (!result) return;
  renderResults(result);
  showTab('results');
}
'''
src = src.replace(
    "function retryInterview()",
    VIEW_FN + "function retryInterview()"
)

with open(path, 'w', encoding='utf-8') as f:
    f.write(src)

# Verify
checks = {
    'Java icon':              "'Java'" in src,
    'storageKey':             'storageKey' in src,
    'saveHistory':            'saveHistory' in src,
    'loadHistory':            'loadHistory' in src,
    'userEmail sent':         'userEmail: currentUser.email' in src,
    'history restored login': 'loadHistory(email)' in src,
    'viewHistoryResult':      'viewHistoryResult' in src,
    'history clickable':      'onclick="viewHistoryResult' in src,
    'persist after finish':   'saveHistory(currentUser.email' in src,
    'renderHistory on login': 'renderHistory();   // restore' in src,
}

print(f"\napp.js size: {len(src)} bytes")
all_ok = True
for name, result in checks.items():
    status = 'OK' if result else 'MISSING'
    if not result: all_ok = False
    print(f"  {status} - {name}")

print('\nAll checks passed!' if all_ok else '\nSome checks FAILED.')
