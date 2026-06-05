html = open('frontend/index.html', encoding='utf-8').read()
required = [
    'loginPage','dashboardPage','loginName','loginEmail','loginError',
    'welcomeUser','tab-home','tab-mock','tab-results','tab-history',
    'dashboardStats','categoriesGrid','interviewConfig','interviewPanel',
    'processingPanel','resultsContainer','historyContainer',
    'questionCount','categorySelect','difficultySelect',
    'currentQNum','totalQNum','qCategory','qDifficulty','timer',
    'progressBar','qNum','questionText','answerInput',
    'step1','step2','step3','step4','processingFill'
]
missing = [r for r in required if ('id="' + r + '"') not in html]
if missing:
    print('MISSING IDs:', missing)
else:
    print('All', len(required), 'required element IDs present in HTML - OK')
