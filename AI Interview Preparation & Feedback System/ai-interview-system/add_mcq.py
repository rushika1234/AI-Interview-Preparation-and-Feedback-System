# Adds MCQ options to all questions and updates evaluate() in app.py

MCQ_DATA = {
    1:  {"options": ["A. LIFO structure: push/pop from top", "B. FIFO structure: enqueue/dequeue", "C. Random access like arrays", "D. Sorted binary tree"], "correctAnswer": "A"},
    2:  {"options": ["A. Both use pointer-based nodes", "B. Array is contiguous fixed-size O(1) access; Linked list uses nodes/pointers with dynamic size O(n) access", "C. Both have same access time O(1)", "D. Linked list uses index-based access"], "correctAnswer": "B"},
    3:  {"options": ["A. A tree where all nodes have equal values", "B. A tree sorted only in ascending order", "C. A tree where left child < parent < right child", "D. A tree where every node has exactly 2 children"], "correctAnswer": "C"},
    4:  {"options": ["A. LIFO: last element removed first", "B. FIFO: first element in is first out; enqueue adds, dequeue removes", "C. Random access data structure", "D. Sorted collection of elements"], "correctAnswer": "B"},
    5:  {"options": ["A. A linear sequential search technique", "B. A sorting algorithm", "C. Maps keys to values using a hash function; handles collisions via chaining/probing", "D. A tree traversal method"], "correctAnswer": "C"},
    6:  {"options": ["A. BFS uses stack; DFS uses queue", "B. BFS explores level-by-level using a queue; DFS explores depth-first using a stack/recursion", "C. Both use the same data structure", "D. BFS is always faster than DFS"], "correctAnswer": "B"},
    7:  {"options": ["A. A linear linked list structure", "B. A hash table variant", "C. A complete binary tree where parent >= children (max-heap) or parent <= children (min-heap)", "D. A doubly linked list"], "correctAnswer": "C"},
    8:  {"options": ["A. A linear structure with one open end", "B. A non-linear hierarchical structure with root, nodes, branches, and leaves", "C. A circular linked list", "D. A two-dimensional array"], "correctAnswer": "B"},
    9:  {"options": ["A. A sorting technique like quicksort", "B. A graph traversal algorithm", "C. Solves problems by breaking them into overlapping subproblems and storing results (memoization/tabulation)", "D. A greedy selection strategy"], "correctAnswer": "C"},
    10: {"options": ["A. An iterative loop structure", "B. A function that calls itself with a base case to stop infinite calls", "C. A technique that causes stack overflow intentionally", "D. A variant of binary search"], "correctAnswer": "B"},

    11: {"options": ["A. Must be infinite with no termination", "B. Finite, definite steps, has input/output, effective and feasible", "C. Only needs to produce output, no input required", "D. Must always use recursion"], "correctAnswer": "B"},
    12: {"options": ["A. Divides array in half each iteration", "B. Selects minimum element each pass", "C. Repeatedly compares and swaps adjacent elements if out of order until sorted", "D. Uses a pivot element to partition"], "correctAnswer": "C"},
    13: {"options": ["A. Works on unsorted arrays with O(n) complexity", "B. Repeatedly halves a sorted array to find target; O(log n) complexity", "C. Checks every element sequentially; O(n)", "D. Uses hashing for O(1) lookup"], "correctAnswer": "B"},
    14: {"options": ["A. In-place O(1) space sort using selection", "B. Pivot-based partitioning sort", "C. Divide-and-conquer: splits array, sorts halves, merges them; O(n log n)", "D. Selects minimum each pass"], "correctAnswer": "C"},
    15: {"options": ["A. Describes best-case performance only", "B. Describes upper-bound worst-case time/space complexity of an algorithm", "C. Measures only memory usage", "D. Counts the exact number of machine instructions"], "correctAnswer": "B"},
    16: {"options": ["A. Always O(n^2) regardless of input", "B. Stable sort using merge operations", "C. Selects a pivot, partitions array around it; average O(n log n)", "D. Runs in guaranteed linear O(n) time"], "correctAnswer": "C"},
    17: {"options": ["A. Both techniques are identical", "B. Greedy picks locally optimal choice at each step; DP solves overlapping subproblems storing results for global optimum", "C. Greedy always gives the globally optimal solution", "D. DP makes random choices each step"], "correctAnswer": "B"},
    18: {"options": ["A. Requires sorted array; O(log n)", "B. Uses binary splitting each iteration", "C. Checks each element one by one; O(n); works on unsorted data", "D. Uses hashing for constant time search"], "correctAnswer": "C"},
    19: {"options": ["A. Finds the longest path in a graph", "B. Sorts vertices of a weighted graph", "C. Finds shortest path from source to all vertices in weighted graph using greedy approach with priority queue", "D. Detects cycles in a directed graph"], "correctAnswer": "C"},
    20: {"options": ["A. Combines all subproblems first before dividing", "B. Breaks problem into smaller subproblems, solves recursively, then merges results", "C. Only works on pre-sorted input data", "D. Bottom-up iterative approach without recursion"], "correctAnswer": "B"},

    21: {"options": ["A. A component of the operating system kernel", "B. Software that manages databases: reduces redundancy, ensures integrity, provides security and concurrent access", "C. A programming language for data manipulation", "D. A network communication protocol"], "correctAnswer": "B"},
    22: {"options": ["A. A technique that increases data redundancy", "B. Adding more columns to existing tables", "C. Process of reducing redundancy: 1NF atomic values, 2NF no partial dependency, 3NF no transitive dependency", "D. A method of encrypting sensitive database data"], "correctAnswer": "C"},
    23: {"options": ["A. Both primary and foreign keys serve the same purpose", "B. Primary key uniquely identifies a row; Foreign key references the primary key of another table", "C. Foreign key must also be unique in its own table", "D. Primary key can be null if needed"], "correctAnswer": "B"},
    24: {"options": ["A. Both SQL and NoSQL are identical in structure", "B. SQL: relational, structured, fixed schema; NoSQL: non-relational, flexible schema (e.g. MongoDB, Cassandra)", "C. NoSQL is always slower than SQL", "D. SQL databases have no defined schema"], "correctAnswer": "B"},
    25: {"options": ["A. Algorithm, Compilation, Iteration, Design", "B. Atomicity, Consistency, Isolation, Durability — properties ensuring reliable database transactions", "C. Access Control, Identity, Data integrity", "D. Array, Collection, Index, Database"], "correctAnswer": "B"},
    26: {"options": ["A. Only combines rows from the same table", "B. INNER JOIN: matching rows both tables; LEFT: all left + matching right; RIGHT: all right + matching left; FULL: all rows both tables", "C. Works only without WHERE conditions", "D. Automatically removes duplicate rows from results"], "correctAnswer": "B"},
    27: {"options": ["A. Slows down all database queries", "B. A data structure (e.g. B-tree) on a column that speeds up search and retrieval operations", "C. Stores backup copies of data", "D. Enforces foreign key constraints"], "correctAnswer": "B"},
    28: {"options": ["A. Refers to a single SQL SELECT statement", "B. A logical unit of work that is atomic — either fully committed or fully rolled back, ensuring ACID properties", "C. A stored procedure in a database", "D. A table-level check constraint"], "correctAnswer": "B"},
    29: {"options": ["A. All three commands do the same thing", "B. DELETE: removes rows, supports rollback; DROP: removes entire table+structure; TRUNCATE: removes all rows fast, no rollback", "C. TRUNCATE keeps structure, DROP keeps data", "D. DELETE is DDL; DROP is DML"], "correctAnswer": "B"},
    30: {"options": ["A. A network topology diagram for routers", "B. Entity-Relationship diagram showing entities, attributes, relationships, and cardinality for DB design", "C. An algorithm flowchart for sorting", "D. A UML class diagram for software design"], "correctAnswer": "B"},

    31: {"options": ["A. Software that only manages the file system", "B. System software managing processes, memory, files, hardware and providing interface between user and hardware", "C. Software that only runs user applications", "D. Software that only handles network connections"], "correctAnswer": "B"},
    32: {"options": ["A. Both always share the same memory space", "B. Process: independent execution unit with own memory; Thread: lightweight unit within a process sharing process memory", "C. A thread is heavier and slower than a process", "D. Processes and threads are identical concepts"], "correctAnswer": "B"},
    33: {"options": ["A. Deadlock only requires one of the four conditions", "B. Mutual exclusion, Hold-and-wait, No preemption, Circular wait — all four must hold simultaneously", "C. Deadlock requires five or more conditions", "D. Only circular wait condition is needed"], "correctAnswer": "B"},
    34: {"options": ["A. Only FCFS scheduling algorithm exists", "B. FCFS (first-come), SJF (shortest job), Round Robin (time slices), Priority scheduling — each with different trade-offs", "C. All CPU scheduling algorithms give the same result", "D. Only preemptive scheduling is used in modern OS"], "correctAnswer": "B"},
    35: {"options": ["A. A direct extension of physical RAM chips", "B. Technique using disk space as extended RAM, allowing programs larger than physical memory via paging/swapping", "C. A type of CPU cache memory (L1/L2)", "D. Dedicated GPU memory for graphics"], "correctAnswer": "B"},
    36: {"options": ["A. Physically sorting memory pages by address", "B. Divides logical memory into fixed-size pages mapped to physical frames via page table, eliminating external fragmentation", "C. Compressing memory contents to save space", "D. Encrypting memory blocks for security"], "correctAnswer": "B"},
    37: {"options": ["A. Semaphore and mutex are the same thing", "B. Mutex: binary lock owned by one thread; Semaphore: integer counter controlling access by multiple threads for synchronization", "C. Semaphore is always binary (0 or 1) like mutex", "D. Mutex allows multiple threads in critical section"], "correctAnswer": "B"},
    38: {"options": ["A. Switching between different user accounts", "B. OS saves current process state (registers, PC) and loads another process's saved state to switch execution", "C. Dynamically changing CPU clock frequency", "D. Swapping hard disk sectors during defragmentation"], "correctAnswer": "B"},
    39: {"options": ["A. A normal and expected OS optimization behavior", "B. When excessive page faults cause OS to spend more time swapping pages than executing processes, severely degrading performance", "C. CPU overheating due to heavy computational load", "D. A type of memory leak in applications"], "correctAnswer": "B"},
    40: {"options": ["A. Only one type of kernel exists", "B. Monolithic: entire OS in kernel space; Microkernel: minimal kernel, services in user space; Hybrid: combination of both", "C. The kernel runs entirely in user space", "D. The kernel is just another application program"], "correctAnswer": "B"},

    41: {"options": ["A. The OSI model has only 4 layers", "B. 7 layers: Physical, Data Link, Network, Transport, Session, Presentation, Application (bottom to top)", "C. The TCP/IP model has 5 layers", "D. The OSI model has only 3 layers"], "correctAnswer": "B"},
    42: {"options": ["A. A protocol used only for web browsing (HTTP)", "B. Suite of protocols for reliable connection-oriented communication; IP handles addressing, TCP ensures reliable delivery", "C. A protocol used only for email (SMTP)", "D. Only works on local area networks (LAN)"], "correctAnswer": "B"},
    43: {"options": ["A. Both TCP and UDP are connectionless protocols", "B. TCP: reliable, ordered, connection-oriented, slower; UDP: fast, unreliable, connectionless — used for streaming/gaming", "C. UDP is more reliable and ordered than TCP", "D. TCP is faster than UDP"], "correctAnswer": "B"},
    44: {"options": ["A. Dynamic Network Switching system", "B. Domain Name System that resolves human-readable domain names (e.g. google.com) to IP addresses via distributed servers", "C. Data Network Security protocol", "D. Direct Node Selection algorithm"], "correctAnswer": "B"},
    45: {"options": ["A. HTTP and HTTPS are completely identical", "B. HTTP: unencrypted web protocol (port 80); HTTPS: HTTP secured with SSL/TLS encryption (port 443)", "C. HTTPS is significantly slower than HTTP always", "D. HTTP uses port 443 by default"], "correctAnswer": "B"},
    46: {"options": ["A. Both IPv4 and IPv6 use 32-bit addresses", "B. IPv4: 32-bit (~4 billion addresses); IPv6: 128-bit (vastly more addresses) solving IPv4 address exhaustion", "C. IPv6 uses 64-bit addresses", "D. IPv4 uses 64-bit addresses"], "correctAnswer": "B"},
    47: {"options": ["A. The process of combining multiple networks into one", "B. Dividing an IP network into smaller sub-networks using subnet mask to improve performance, security, and address management", "C. Encrypting all network traffic end-to-end", "D. The process of routing between different ISPs"], "correctAnswer": "B"},
    48: {"options": ["A. A hardware-only device for boosting network speed", "B. Security system that monitors and filters network traffic, blocking unauthorized access based on defined rules", "C. A tool that only blocks computer viruses", "D. A device that speeds up internet connection"], "correctAnswer": "B"},
    49: {"options": ["A. Hub, switch, and router all do the same thing", "B. Hub: broadcasts to all ports; Switch: forwards to specific port by MAC address; Router: routes packets between networks by IP", "C. Router works at Layer 2 (Data Link) using MAC addresses", "D. Switch broadcasts to all ports like a hub"], "correctAnswer": "B"},
    50: {"options": ["A. TCP uses a two-way handshake (SYN, ACK)", "B. SYN (client) → SYN-ACK (server) → ACK (client) — three steps to establish a TCP connection", "C. TCP uses a four-way handshake", "D. TCP needs no handshake; connection is immediate"], "correctAnswer": "B"},

    51: {"options": ["A. Loops, Classes, Objects, Methods", "B. Encapsulation, Inheritance, Polymorphism, Abstraction", "C. Compile, Link, Execute, Debug", "D. Input, Process, Output, Storage"], "correctAnswer": "B"},
    52: {"options": ["A. Only single inheritance exists in OOP", "B. Single, Multiple, Multilevel, Hierarchical, Hybrid — all allow reusing parent class properties and behaviors", "C. Only two types of inheritance exist", "D. Inheritance is not possible in all OOP languages"], "correctAnswer": "B"},
    53: {"options": ["A. The ability to have only one class in a program", "B. One interface, multiple implementations: compile-time (overloading) and runtime (overriding) polymorphism", "C. Only method overloading (compile-time) exists", "D. Only interfaces can achieve polymorphism"], "correctAnswer": "B"},
    54: {"options": ["A. Inheriting properties from a parent class", "B. Bundling data and methods together, hiding internal state using private variables with public getters/setters", "C. Creating multiple instances of a class", "D. Providing different implementations of the same method"], "correctAnswer": "B"},
    55: {"options": ["A. Showing all internal implementation details to users", "B. Hiding implementation complexity and showing only essential features through abstract classes and interfaces", "C. Making all class methods public by default", "D. Copying all methods from the parent class"], "correctAnswer": "B"},
    56: {"options": ["A. Class and object are identical concepts", "B. Class is the blueprint/template; Object is an instance of the class with actual data values in memory", "C. An object is more abstract than a class", "D. A class can only have one object at a time"], "correctAnswer": "B"},
    57: {"options": ["A. A method that destroys objects and frees memory", "B. Special method with same name as class, called automatically when object is created to initialize its state", "C. A static method that returns a value", "D. An abstract method that must be overridden"], "correctAnswer": "B"},
    58: {"options": ["A. Same class, same name but different parameters (overloading)", "B. Child class provides its own implementation of a parent class method with the same signature — resolved at runtime", "C. Two methods in the same class with same signature", "D. Replacing a static method with a new version"], "correctAnswer": "B"},
    59: {"options": ["A. A concrete class with full method implementations", "B. A contract declaring abstract method signatures that implementing classes must define; supports multiple inheritance", "C. A static utility class", "D. A final class that cannot be extended"], "correctAnswer": "B"},
    60: {"options": ["A. Abstract class and interface are identical", "B. Abstract: can have constructors, concrete methods, state; Interface: only declarations, supports multiple implementation", "C. Interface can have constructors like abstract class", "D. Abstract class allows multiple inheritance"], "correctAnswer": "B"},

    61: {"options": ["A. Compiled, statically typed, low-level language", "B. Interpreted, dynamically typed, high-level, readable, versatile, platform-independent language", "C. A language only for data science and ML tasks", "D. A low-level language close to machine code"], "correctAnswer": "B"},
    62: {"options": ["A. Both lists and tuples are immutable", "B. List: mutable, ordered; Tuple: immutable, ordered — tuples are faster and used for fixed data", "C. Tuples are mutable and lists are immutable", "D. Both lists and tuples are unordered"], "correctAnswer": "B"},
    63: {"options": ["A. An ordered immutable sequence like a tuple", "B. Mutable unordered collection of key-value pairs with O(1) average lookup using hashing", "C. A sorted list of unique values", "D. An immutable set of key-value pairs"], "correctAnswer": "B"},
    64: {"options": ["A. A class inheritance mechanism in Python", "B. Functions that wrap another function using @syntax to modify or extend its behavior without changing its code", "C. A module import mechanism for loading libraries", "D. A built-in exception handling mechanism"], "correctAnswer": "B"},
    65: {"options": ["A. A method for sorting list elements quickly", "B. Concise syntax [expr for item in iterable if condition] to create lists in one line instead of a loop", "C. A method for copying one list into another", "D. A way to convert a list to a tuple"], "correctAnswer": "B"},
    66: {"options": ["A. Both create a new reference to the same object", "B. Shallow copy: copies object, nested objects still shared; Deep copy: fully independent copy including all nested objects", "C. Deep copy is faster than shallow copy", "D. Shallow copy creates independent nested objects"], "correctAnswer": "B"},
    67: {"options": ["A. A shortcut for creating list comprehensions", "B. Functions using yield to produce values one at a time lazily, saving memory for large or infinite sequences", "C. A string formatting tool using f-strings", "D. Python's module import mechanism"], "correctAnswer": "B"},
    68: {"options": ["A. A mechanism that prevents all runtime errors", "B. try: risky code; except: catch specific exceptions; finally: always runs; raise: create exceptions; throws errors", "C. Only handles syntax errors at compile time", "D. An automatic error logging system"], "correctAnswer": "B"},
    69: {"options": ["A. Both == and is compare object values", "B. == compares values/content; is compares object identity (same memory address)", "C. is compares values while == compares memory addresses", "D. Both == and is compare memory addresses"], "correctAnswer": "B"},
    70: {"options": ["A. Module and package are the same thing with different names", "B. Module: single .py file with code; Package: directory with __init__.py containing multiple modules for organization", "C. A package is a single Python file", "D. A module is a folder containing Python files"], "correctAnswer": "B"},

    71: {"options": ["A. List all your personal problems and failures", "B. Brief background, education, key skills, relevant experience, and career goals aligned with the job role", "C. Only mention your hobbies and personal interests", "D. Read your resume word-for-word to the interviewer"], "correctAnswer": "B"},
    72: {"options": ["A. Claim you have absolutely no weaknesses", "B. Strengths: genuine skills you excel at; Weaknesses: real areas you are actively working to improve", "C. Only mention your strengths and ignore weaknesses", "D. Make up random strengths and weaknesses on the spot"], "correctAnswer": "B"},
    73: {"options": ["A. Say you only want the highest possible salary", "B. Research the company's culture, growth opportunities, role alignment, values, and how you can contribute", "C. Say any company offering a job would be fine", "D. Mention that you desperately need employment"], "correctAnswer": "B"},
    74: {"options": ["A. Say you want to be in the interviewer's exact position", "B. Describe career growth, skill development, leadership goals, and contribution aligned with company's long-term vision", "C. Say you plan to leave and start your own business", "D. Say you are completely unsure about your future plans"], "correctAnswer": "B"},
    75: {"options": ["A. Avoid all deadlines and high-pressure situations", "B. Prioritize tasks, create a plan, stay calm, communicate proactively, and focus on finding solutions", "C. Work continuously without any breaks", "D. Simply ignore all stress and pretend it doesn't exist"], "correctAnswer": "B"},
    76: {"options": ["A. State that you strongly prefer working alone always", "B. Describe a specific situation: your role, how you collaborated, communicated, overcame challenges, and the positive outcome", "C. Argue that teams are inefficient and slow", "D. Take all the credit for the team's achievements"], "correctAnswer": "B"},
    77: {"options": ["A. Only money and financial compensation motivate you", "B. Challenges, learning opportunities, achieving meaningful goals, contributing to team success, and personal growth", "C. Avoiding difficult work motivates you to perform better", "D. You have no specific source of motivation"], "correctAnswer": "B"},
    78: {"options": ["A. Argue back and defend yourself from all criticism", "B. Listen openly, accept constructive feedback, reflect on it, thank the person, and take action to improve", "C. Simply ignore all feedback you receive", "D. Get defensive and take criticism personally"], "correctAnswer": "B"},
    79: {"options": ["A. State the highest possible salary number without research", "B. Research market rates, provide a range based on experience/skills/location, remain open to negotiation", "C. Say you have absolutely no salary expectation", "D. Demand one exact salary figure with no flexibility"], "correctAnswer": "B"},
    80: {"options": ["A. Say you have no questions at all for the interviewer", "B. Ask about role expectations, team culture, growth opportunities, challenges, and company direction", "C. Only ask about vacation days and benefits", "D. Ask questions about the company's competitors"], "correctAnswer": "B"},

    81: {"options": ["A. All three do exactly the same thing", "B. HTML: structure/content; CSS: styling/layout; JavaScript: behavior/interactivity", "C. CSS is what adds functionality to web pages", "D. JavaScript defines the page structure"], "correctAnswer": "B"},
    82: {"options": ["A. A design approach that only works on desktop screens", "B. Design that adapts to different screen sizes using fluid grids, flexible images, and CSS media queries", "C. Using fixed pixel-based layouts for all devices", "D. A technique exclusively for mobile applications"], "correctAnswer": "B"},
    83: {"options": ["A. An API style only for internal database queries", "B. Representational State Transfer: stateless HTTP-based API using GET, POST, PUT, DELETE methods for resource operations", "C. An API that only accepts XML data format", "D. An API style only for internal enterprise systems"], "correctAnswer": "B"},
    84: {"options": ["A. Both GET and POST send data in the URL", "B. GET: retrieves data via URL parameters (visible); POST: sends data in request body (more secure for sensitive data)", "C. POST retrieves data while GET sends data", "D. GET is more secure than POST for sensitive data"], "correctAnswer": "B"},
    85: {"options": ["A. A new programming language for web development", "B. Asynchronous JavaScript technique that updates page content without full page reload using fetch or XMLHttpRequest", "C. A CSS animation and transition tool", "D. A server-side rendering technique for HTML"], "correctAnswer": "B"},
    86: {"options": ["A. Both cookies and sessions are stored on the server", "B. Cookie: stored in browser, persists across sessions; Session: stored server-side, more secure, ends when browser closes", "C. Sessions are stored in the browser like cookies", "D. Cookies and sessions are identical mechanisms"], "correctAnswer": "B"},
    87: {"options": ["A. A data format only usable within JavaScript code", "B. JavaScript Object Notation: lightweight, language-independent key-value data format for data exchange between systems", "C. Java Structured Object Notation for Java apps", "D. A binary data format for efficient storage"], "correctAnswer": "B"},
    88: {"options": ["A. An update designed to completely replace CSS", "B. Modern HTML with semantic elements, canvas, native video/audio, localStorage, geolocation, and improved accessibility", "C. A version designed exclusively for mobile websites", "D. An update designed to completely replace JavaScript"], "correctAnswer": "B"},
    89: {"options": ["A. A 3D layout and animation system", "B. One-dimensional layout model for arranging items in row or column with powerful alignment and space distribution", "C. A grid-based 2D layout system (that is CSS Grid)", "D. A CSS animation and keyframe system"], "correctAnswer": "B"},
    90: {"options": ["A. Both execute code in the exact same sequential order", "B. Synchronous: blocks execution until complete; Asynchronous: non-blocking, uses callbacks/promises/async-await", "C. Asynchronous code is always slower than synchronous", "D. Synchronous JavaScript uses multiple threads"], "correctAnswer": "B"},

    91: {"options": ["A. Platform-dependent language compiled to machine code", "B. Platform-independent (WORA), compiled to bytecode, runs on JVM, object-oriented, strongly typed, garbage collected", "C. Purely interpreted language, never compiled", "D. A language exclusively designed for Android development"], "correctAnswer": "B"},
    92: {"options": ["A. JDK, JRE, and JVM are all the same tool", "B. JDK: development kit with compiler+tools; JRE: runtime environment to run programs; JVM: virtual machine executing bytecode", "C. JVM includes the Java compiler", "D. JRE is the tool used for Java development"], "correctAnswer": "B"},
    93: {"options": ["A. Both == and .equals() compare memory addresses", "B. ==: compares object references (memory addresses); .equals(): compares actual content/value — always use .equals() for strings", "C. .equals() compares object references like ==", "D. Both == and .equals() compare content values"], "correctAnswer": "B"},
    94: {"options": ["A. Java only has public and private modifiers", "B. Public: everywhere; Private: same class only; Protected: class + subclasses + package; Default: same package only", "C. Java only has two access modifiers", "D. All access modifiers allow access from anywhere"], "correctAnswer": "B"},
    95: {"options": ["A. Abstract class and interface are identical in Java", "B. Abstract: has constructors, concrete+abstract methods, state; Interface: declarations only, supports multiple implementation", "C. Interface can have constructors like abstract class", "D. Abstract class supports multiple inheritance"], "correctAnswer": "B"},
    96: {"options": ["A. Exception handling only works for runtime errors", "B. try: code that may throw; catch: handles specific exceptions; finally: always runs; throw: creates; throws: declares", "C. Java has no finally block in exception handling", "D. Java handles all exceptions automatically"], "correctAnswer": "B"},
    97: {"options": ["A. ArrayList and LinkedList have identical performance", "B. ArrayList: dynamic array, fast random access O(1), slow insert/delete; LinkedList: nodes, fast insert/delete O(1), slow access O(n)", "C. LinkedList is faster for random index access", "D. ArrayList is slower than LinkedList for all operations"], "correctAnswer": "B"},
    98: {"options": ["A. Java only supports single-threaded execution", "B. Multiple threads run concurrently via Thread class or Runnable interface; synchronized prevents race conditions", "C. Java threads do not share any memory at all", "D. Java has no built-in multithreading support"], "correctAnswer": "B"},
    99: {"options": ["A. The Collections framework is only for sorting data", "B. Provides interfaces (List, Set, Map) and implementations (ArrayList, HashSet, HashMap) for reusable data structures", "C. Only ArrayList is available in the framework", "D. The framework contains no interfaces, only classes"], "correctAnswer": "B"},
    100: {"options": ["A. Java developers must manually free memory like in C", "B. JVM automatically reclaims heap memory from unreachable objects using Mark-and-Sweep; no manual free() needed", "C. Garbage collection only runs when explicitly called", "D. Java has no garbage collection mechanism"], "correctAnswer": "B"},
}

import ast, re

src = open('app.py', encoding='utf-8').read()

# Build new questionsDB with MCQ fields injected
lines = src.split('\n')
new_lines = []
in_qdb = False

for line in lines:
    if line.strip().startswith('{"id":') or line.strip().startswith('{"id" :'):
        # Extract id from this line
        m = re.search(r'"id":\s*(\d+)', line)
        if m:
            qid = int(m.group(1))
            mcq = MCQ_DATA.get(qid)
            if mcq and '"options"' not in line:
                # Insert options and correctAnswer before closing }
                opts_str = ', '.join(f'"{o}"' for o in mcq['options'])
                line = line.rstrip()
                if line.endswith('},'):
                    line = line[:-2] + f', "type": "mcq", "options": [{opts_str}], "correctAnswer": "{mcq["correctAnswer"]}"' + '},'
                elif line.endswith('}'):
                    line = line[:-1] + f', "type": "mcq", "options": [{opts_str}], "correctAnswer": "{mcq["correctAnswer"]}"' + '}'
    new_lines.append(line)

new_src = '\n'.join(new_lines)

# Replace evaluate function
OLD_EVAL = '''def evaluate(answer, keywords):
    if not answer or not answer.strip():
        return 0
    answer_lower = answer.lower()
    match = sum(1 for k in keywords if k.lower() in answer_lower)
    return int((match / len(keywords)) * 100)'''

NEW_EVAL = '''def evaluate(answer, keywords, q_type="mcq", correct_answer=None):
    if q_type == "mcq":
        if not answer or not correct_answer:
            return 0
        return 100 if answer.strip().upper() == correct_answer.strip().upper() else 0
    # text fallback: keyword matching
    if not answer or not answer.strip():
        return 0
    answer_lower = answer.lower()
    match = sum(1 for k in keywords if k.lower() in answer_lower)
    return int((match / len(keywords)) * 100)'''

new_src = new_src.replace(OLD_EVAL, NEW_EVAL)

# Update evaluate() call in get_feedback
new_src = new_src.replace(
    "score = evaluate(r.get('answer', ''), q['expectedKeywords'])",
    "score = evaluate(r.get('answer', ''), q['expectedKeywords'], q.get('type', 'mcq'), q.get('correctAnswer'))"
)

# Update detailed_feedback.append to include MCQ fields
OLD_DETAIL = '''        detailed_feedback.append({
            "questionId": q['id'],
            "question": q['question'],
            "category": q['category'],
            "difficulty": q['difficulty'],
            "yourAnswer": r.get('answer', ''),
            "score": score,
            "matchedKeywords": matched_kw,
            "missedKeywords": missed_kw[:5],
            "modelAnswer": get_model_answer(q['id']),
            "timeTaken": r.get('timeTaken', 0)
        })'''

NEW_DETAIL = '''        detailed_feedback.append({
            "questionId": q['id'],
            "question": q['question'],
            "category": q['category'],
            "difficulty": q['difficulty'],
            "type": q.get('type', 'mcq'),
            "options": q.get('options', []),
            "correctAnswer": q.get('correctAnswer', ''),
            "yourAnswer": r.get('answer', ''),
            "score": score,
            "matchedKeywords": matched_kw,
            "missedKeywords": missed_kw[:5],
            "modelAnswer": get_model_answer(q['id']),
            "timeTaken": r.get('timeTaken', 0)
        })'''

new_src = new_src.replace(OLD_DETAIL, NEW_DETAIL)

# Write updated file
with open('app.py', 'w', encoding='utf-8') as f:
    f.write(new_src)

# Verify
ast.parse(new_src)
mcq_count  = new_src.count('"type": "mcq"')
opts_count = new_src.count('"options":')
chk = "q.get('type'"
print(f'app.py updated OK')
print(f'  Questions with MCQ type: {mcq_count}')
print(f'  Questions with options : {opts_count}')
print(f'  evaluate() updated     : {"q_type" in new_src}')
print(f'  feedback route updated : {chk in new_src}')
print(f'  detail includes options: {"correctAnswer" in new_src}')
