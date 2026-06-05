import urllib.request
import json
import sys
import time

time.sleep(2)

BASE = 'http://127.0.0.1:5000'
tests = []

def get(path):
    r = urllib.request.urlopen(BASE + path, timeout=5)
    return json.loads(r.read())

def post(path, payload):
    data = json.dumps(payload).encode()
    req  = urllib.request.Request(BASE + path, data=data, headers={'Content-Type': 'application/json'})
    r    = urllib.request.urlopen(req, timeout=5)
    return json.loads(r.read())

def check(name, condition):
    tests.append((name, condition))

# --- 1. Register ---
r = post('/api/register', {'username': 'Rushika', 'email': 'rushika@test.com'})
check('POST /api/register', r.get('success') == True)

# --- 2. Login existing ---
r = post('/api/login', {'username': 'Rushika', 'email': 'rushika@test.com'})
check('POST /api/login (existing user)', r.get('success') == True)
uid = r.get('userId', 1)

# --- 3. Login new (auto-register) ---
r = post('/api/login', {'username': 'Sathvika', 'email': 'sathvika@test.com'})
check('POST /api/login (auto-register new user)', r.get('success') == True)

# --- 4. Stats ---
r = get('/api/stats')
check('GET /api/stats', r.get('success') == True and r['data']['totalQuestions'] == 90)
check('GET /api/stats has 9 categories', r['data']['totalCategories'] == 9)

# --- 5. All questions ---
r = get('/api/questions')
check('GET /api/questions returns 90', r.get('success') == True and r['total'] == 90)

# --- 6. Categories ---
r = get('/api/questions/categories')
check('GET /api/questions/categories returns 9', r.get('success') == True and len(r['data']) == 9)

# --- 7. Random (all) ---
r = get('/api/questions/random?count=10&category=all&difficulty=all')
check('GET /api/questions/random (all categories)', r.get('success') == True and len(r['data']) == 10)

# --- 8. Random by category ---
r = get('/api/questions/random?count=5&category=DBMS&difficulty=all')
all_dbms = all(q['category'] == 'DBMS' for q in r['data'])
check('GET /api/questions/random (DBMS only)', r.get('success') == True and all_dbms)

# --- 9. Random by difficulty ---
r = get('/api/questions/random?count=5&category=all&difficulty=Easy')
all_easy = all(q['difficulty'] == 'Easy' for q in r['data'])
check('GET /api/questions/random (Easy only)', r.get('success') == True and all_easy)

# --- 10. Category route ---
r = get('/api/questions/category/Python')
check('GET /api/questions/category/Python returns 10', r.get('success') == True and r['total'] == 10)

# --- 11. Add question ---
r = post('/api/questions/add', {
    'question': 'What is Flask?',
    'category': 'Python',
    'difficulty': 'Easy',
    'keywords': ['flask', 'python', 'web', 'framework']
})
check('POST /api/questions/add', r.get('success') == True)

# --- 12. Feedback with scored answers ---
responses = [
    {'questionId': 1,  'answer': 'A stack uses LIFO last in first out with push and pop operations', 'timeTaken': 30},
    {'questionId': 21, 'answer': 'DBMS is a database management system for data redundancy and integrity', 'timeTaken': 25},
    {'questionId': 51, 'answer': 'The four pillars of OOP are encapsulation inheritance polymorphism and abstraction', 'timeTaken': 20},
]
r = post('/api/feedback', {'responses': responses, 'userId': uid, 'username': 'Rushika', 'totalTime': 75})
check('POST /api/feedback (with answers)', r.get('success') == True)
check('feedback overallScore > 0', r['data']['overallScore'] > 0)

# --- 13. Feedback field completeness ---
d = r['data']
required_fields = ['overallScore', 'performance', 'totalQuestions', 'categoryAnalysis',
                   'recommendations', 'detailedFeedback', 'date', 'timeTaken', 'username']
check('feedback has all required fields', all(f in d for f in required_fields))

fb = d['detailedFeedback'][0]
check('detailedFeedback has matchedKeywords', 'matchedKeywords' in fb)
check('detailedFeedback has missedKeywords',  'missedKeywords'  in fb)
check('detailedFeedback has modelAnswer',     'modelAnswer'     in fb)
check('detailedFeedback has score',           'score'           in fb)
check('detailedFeedback has question text',   'question'        in fb)

# --- 14. Performance levels ---
score = d['overallScore']
perf  = d['performance']
valid_perfs = ['Excellent', 'Good', 'Average', 'Needs Improvement']
check('performance level is valid', perf in valid_perfs)

# --- 15. Feedback with empty/skipped answer ---
r = post('/api/feedback', {
    'responses': [{'questionId': 1, 'answer': '', 'timeTaken': 0}],
    'userId': uid, 'username': 'Test', 'totalTime': 0
})
check('feedback empty answer scores 0', r['data']['overallScore'] == 0)

# --- 16. History ---
r = get('/api/history/' + str(uid))
check('GET /api/history/<id>', r.get('success') == True and r['total'] >= 1)

# --- 17. Static file ---
r = urllib.request.urlopen(BASE + '/', timeout=5)
check('GET / serves index.html (200)', r.status == 200)

# --- 18. CORS / JSON headers ---
r = urllib.request.urlopen(BASE + '/api/stats', timeout=5)
ct = r.headers.get('Content-Type', '')
check('API returns JSON content-type', 'application/json' in ct)

# ---- RESULTS ----
print()
passed = sum(1 for _, v in tests if v)
failed = [(n, v) for n, v in tests if not v]

for name, ok in tests:
    status = '  PASS' if ok else '  FAIL'
    print(status + '  ' + name)

print()
print('=' * 50)
print(f'  Result: {passed} / {len(tests)} tests passed')
if failed:
    print(f'  FAILED: {[n for n,_ in failed]}')
print('=' * 50)
sys.exit(0 if passed == len(tests) else 1)
