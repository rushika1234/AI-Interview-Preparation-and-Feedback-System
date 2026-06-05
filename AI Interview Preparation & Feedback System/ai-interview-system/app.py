from flask import Flask, request, jsonify, send_from_directory
import random
from datetime import datetime
import os

app = Flask(__name__, static_folder='frontend')

# ================= IN-MEMORY DATABASE =================
usersDB = []
interviewResultsDB = []

questionsDB = [
    # Data Structures
    {"id": 1, "question": "What is a stack and how does it work?", "category": "Data Structures", "difficulty": "Easy", "expectedKeywords": ["lifo", "last in first out", "push", "pop", "stack"], "type": "mcq", "options": ["A. LIFO structure: push/pop from top", "B. FIFO structure: enqueue/dequeue", "C. Random access like arrays", "D. Sorted binary tree"], "correctAnswer": "A"},
    {"id": 2, "question": "Explain the difference between an array and a linked list.", "category": "Data Structures", "difficulty": "Easy", "expectedKeywords": ["array", "linked list", "contiguous", "pointer", "node", "dynamic"], "type": "mcq", "options": ["A. Both use pointer-based nodes", "B. Array is contiguous fixed-size O(1) access; Linked list uses nodes/pointers with dynamic size O(n) access", "C. Both have same access time O(1)", "D. Linked list uses index-based access"], "correctAnswer": "B"},
    {"id": 3, "question": "What is a binary search tree?", "category": "Data Structures", "difficulty": "Medium", "expectedKeywords": ["binary", "tree", "left", "right", "search", "node", "root"], "type": "mcq", "options": ["A. A tree where all nodes have equal values", "B. A tree sorted only in ascending order", "C. A tree where left child < parent < right child", "D. A tree where every node has exactly 2 children"], "correctAnswer": "C"},
    {"id": 4, "question": "What is a queue and where is it used?", "category": "Data Structures", "difficulty": "Easy", "expectedKeywords": ["fifo", "first in first out", "enqueue", "dequeue", "queue"], "type": "mcq", "options": ["A. LIFO: last element removed first", "B. FIFO: first element in is first out; enqueue adds, dequeue removes", "C. Random access data structure", "D. Sorted collection of elements"], "correctAnswer": "B"},
    {"id": 5, "question": "Explain hashing and hash tables.", "category": "Data Structures", "difficulty": "Medium", "expectedKeywords": ["hash", "key", "value", "collision", "bucket", "function"], "type": "mcq", "options": ["A. A linear sequential search technique", "B. A sorting algorithm", "C. Maps keys to values using a hash function; handles collisions via chaining/probing", "D. A tree traversal method"], "correctAnswer": "C"},
    {"id": 6, "question": "What is a graph? Explain BFS and DFS.", "category": "Data Structures", "difficulty": "Hard", "expectedKeywords": ["graph", "vertex", "edge", "bfs", "dfs", "breadth", "depth"], "type": "mcq", "options": ["A. BFS uses stack; DFS uses queue", "B. BFS explores level-by-level using a queue; DFS explores depth-first using a stack/recursion", "C. Both use the same data structure", "D. BFS is always faster than DFS"], "correctAnswer": "B"},
    {"id": 7, "question": "What is a heap data structure?", "category": "Data Structures", "difficulty": "Medium", "expectedKeywords": ["heap", "max heap", "min heap", "priority", "tree", "root"], "type": "mcq", "options": ["A. A linear linked list structure", "B. A hash table variant", "C. A complete binary tree where parent >= children (max-heap) or parent <= children (min-heap)", "D. A doubly linked list"], "correctAnswer": "C"},
    {"id": 8, "question": "What are trees and their types?", "category": "Data Structures", "difficulty": "Medium", "expectedKeywords": ["tree", "binary", "node", "leaf", "root", "child", "parent"], "type": "mcq", "options": ["A. A linear structure with one open end", "B. A non-linear hierarchical structure with root, nodes, branches, and leaves", "C. A circular linked list", "D. A two-dimensional array"], "correctAnswer": "B"},
    {"id": 9, "question": "What is dynamic programming?", "category": "Data Structures", "difficulty": "Hard", "expectedKeywords": ["dynamic", "programming", "optimal", "subproblem", "memoization", "overlapping"], "type": "mcq", "options": ["A. A sorting technique like quicksort", "B. A graph traversal algorithm", "C. Solves problems by breaking them into overlapping subproblems and storing results (memoization/tabulation)", "D. A greedy selection strategy"], "correctAnswer": "C"},
    {"id": 10, "question": "What is recursion and when should it be used?", "category": "Data Structures", "difficulty": "Easy", "expectedKeywords": ["recursion", "base case", "function", "call", "stack"], "type": "mcq", "options": ["A. An iterative loop structure", "B. A function that calls itself with a base case to stop infinite calls", "C. A technique that causes stack overflow intentionally", "D. A variant of binary search"], "correctAnswer": "B"},

    # Algorithms
    {"id": 11, "question": "What is an algorithm? List its properties.", "category": "Algorithms", "difficulty": "Easy", "expectedKeywords": ["algorithm", "finite", "definite", "input", "output", "effective"], "type": "mcq", "options": ["A. Must be infinite with no termination", "B. Finite, definite steps, has input/output, effective and feasible", "C. Only needs to produce output, no input required", "D. Must always use recursion"], "correctAnswer": "B"},
    {"id": 12, "question": "Explain bubble sort algorithm.", "category": "Algorithms", "difficulty": "Easy", "expectedKeywords": ["bubble", "sort", "swap", "compare", "adjacent", "pass"], "type": "mcq", "options": ["A. Divides array in half each iteration", "B. Selects minimum element each pass", "C. Repeatedly compares and swaps adjacent elements if out of order until sorted", "D. Uses a pivot element to partition"], "correctAnswer": "C"},
    {"id": 13, "question": "What is binary search? Explain with complexity.", "category": "Algorithms", "difficulty": "Easy", "expectedKeywords": ["binary", "search", "sorted", "mid", "half", "log n", "o(log n)"], "type": "mcq", "options": ["A. Works on unsorted arrays with O(n) complexity", "B. Repeatedly halves a sorted array to find target; O(log n) complexity", "C. Checks every element sequentially; O(n)", "D. Uses hashing for O(1) lookup"], "correctAnswer": "B"},
    {"id": 14, "question": "What is merge sort and how does it work?", "category": "Algorithms", "difficulty": "Medium", "expectedKeywords": ["merge", "sort", "divide", "conquer", "recursive", "merge", "sorted"], "type": "mcq", "options": ["A. In-place O(1) space sort using selection", "B. Pivot-based partitioning sort", "C. Divide-and-conquer: splits array, sorts halves, merges them; O(n log n)", "D. Selects minimum each pass"], "correctAnswer": "C"},
    {"id": 15, "question": "Explain time complexity and Big O notation.", "category": "Algorithms", "difficulty": "Medium", "expectedKeywords": ["time complexity", "big o", "o(n)", "o(1)", "notation", "worst case"], "type": "mcq", "options": ["A. Describes best-case performance only", "B. Describes upper-bound worst-case time/space complexity of an algorithm", "C. Measures only memory usage", "D. Counts the exact number of machine instructions"], "correctAnswer": "B"},
    {"id": 16, "question": "What is quicksort and what is its average complexity?", "category": "Algorithms", "difficulty": "Medium", "expectedKeywords": ["quick", "sort", "pivot", "partition", "o(n log n)", "divide"], "type": "mcq", "options": ["A. Always O(n^2) regardless of input", "B. Stable sort using merge operations", "C. Selects a pivot, partitions array around it; average O(n log n)", "D. Runs in guaranteed linear O(n) time"], "correctAnswer": "C"},
    {"id": 17, "question": "What is the difference between greedy and dynamic programming?", "category": "Algorithms", "difficulty": "Hard", "expectedKeywords": ["greedy", "dynamic", "optimal", "local", "global", "subproblem"], "type": "mcq", "options": ["A. Both techniques are identical", "B. Greedy picks locally optimal choice at each step; DP solves overlapping subproblems storing results for global optimum", "C. Greedy always gives the globally optimal solution", "D. DP makes random choices each step"], "correctAnswer": "B"},
    {"id": 18, "question": "Explain linear search and its complexity.", "category": "Algorithms", "difficulty": "Easy", "expectedKeywords": ["linear", "search", "sequential", "o(n)", "unsorted"], "type": "mcq", "options": ["A. Requires sorted array; O(log n)", "B. Uses binary splitting each iteration", "C. Checks each element one by one; O(n); works on unsorted data", "D. Uses hashing for constant time search"], "correctAnswer": "C"},
    {"id": 19, "question": "What is Dijkstra's algorithm?", "category": "Algorithms", "difficulty": "Hard", "expectedKeywords": ["dijkstra", "shortest", "path", "graph", "weighted", "greedy"], "type": "mcq", "options": ["A. Finds the longest path in a graph", "B. Sorts vertices of a weighted graph", "C. Finds shortest path from source to all vertices in weighted graph using greedy approach with priority queue", "D. Detects cycles in a directed graph"], "correctAnswer": "C"},
    {"id": 20, "question": "What is the concept of divide and conquer?", "category": "Algorithms", "difficulty": "Medium", "expectedKeywords": ["divide", "conquer", "subproblem", "merge", "recursive", "solve"], "type": "mcq", "options": ["A. Combines all subproblems first before dividing", "B. Breaks problem into smaller subproblems, solves recursively, then merges results", "C. Only works on pre-sorted input data", "D. Bottom-up iterative approach without recursion"], "correctAnswer": "B"},

    # DBMS
    {"id": 21, "question": "What is a DBMS and what are its advantages?", "category": "DBMS", "difficulty": "Easy", "expectedKeywords": ["database", "management", "data", "redundancy", "integrity", "security"], "type": "mcq", "options": ["A. A component of the operating system kernel", "B. Software that manages databases: reduces redundancy, ensures integrity, provides security and concurrent access", "C. A programming language for data manipulation", "D. A network communication protocol"], "correctAnswer": "B"},
    {"id": 22, "question": "What is normalization? Explain 1NF, 2NF, 3NF.", "category": "DBMS", "difficulty": "Medium", "expectedKeywords": ["normalization", "1nf", "2nf", "3nf", "redundancy", "dependency", "atomic"], "type": "mcq", "options": ["A. A technique that increases data redundancy", "B. Adding more columns to existing tables", "C. Process of reducing redundancy: 1NF atomic values, 2NF no partial dependency, 3NF no transitive dependency", "D. A method of encrypting sensitive database data"], "correctAnswer": "C"},
    {"id": 23, "question": "What is a primary key and foreign key?", "category": "DBMS", "difficulty": "Easy", "expectedKeywords": ["primary", "key", "foreign", "unique", "reference", "constraint"], "type": "mcq", "options": ["A. Both primary and foreign keys serve the same purpose", "B. Primary key uniquely identifies a row; Foreign key references the primary key of another table", "C. Foreign key must also be unique in its own table", "D. Primary key can be null if needed"], "correctAnswer": "B"},
    {"id": 24, "question": "Explain the difference between SQL and NoSQL.", "category": "DBMS", "difficulty": "Medium", "expectedKeywords": ["sql", "nosql", "relational", "structured", "schema", "mongodb", "flexible"], "type": "mcq", "options": ["A. Both SQL and NoSQL are identical in structure", "B. SQL: relational, structured, fixed schema; NoSQL: non-relational, flexible schema (e.g. MongoDB, Cassandra)", "C. NoSQL is always slower than SQL", "D. SQL databases have no defined schema"], "correctAnswer": "B"},
    {"id": 25, "question": "What are ACID properties in DBMS?", "category": "DBMS", "difficulty": "Medium", "expectedKeywords": ["acid", "atomicity", "consistency", "isolation", "durability", "transaction"], "type": "mcq", "options": ["A. Algorithm, Compilation, Iteration, Design", "B. Atomicity, Consistency, Isolation, Durability — properties ensuring reliable database transactions", "C. Access Control, Identity, Data integrity", "D. Array, Collection, Index, Database"], "correctAnswer": "B"},
    {"id": 26, "question": "What is a JOIN in SQL? Explain types.", "category": "DBMS", "difficulty": "Medium", "expectedKeywords": ["join", "inner", "outer", "left", "right", "full", "tables"], "type": "mcq", "options": ["A. Only combines rows from the same table", "B. INNER JOIN: matching rows both tables; LEFT: all left + matching right; RIGHT: all right + matching left; FULL: all rows both tables", "C. Works only without WHERE conditions", "D. Automatically removes duplicate rows from results"], "correctAnswer": "B"},
    {"id": 27, "question": "What is an index in a database?", "category": "DBMS", "difficulty": "Medium", "expectedKeywords": ["index", "search", "fast", "retrieval", "b-tree", "performance"], "type": "mcq", "options": ["A. Slows down all database queries", "B. A data structure (e.g. B-tree) on a column that speeds up search and retrieval operations", "C. Stores backup copies of data", "D. Enforces foreign key constraints"], "correctAnswer": "B"},
    {"id": 28, "question": "What is a transaction in DBMS?", "category": "DBMS", "difficulty": "Easy", "expectedKeywords": ["transaction", "commit", "rollback", "begin", "atomic", "unit"], "type": "mcq", "options": ["A. Refers to a single SQL SELECT statement", "B. A logical unit of work that is atomic — either fully committed or fully rolled back, ensuring ACID properties", "C. A stored procedure in a database", "D. A table-level check constraint"], "correctAnswer": "B"},
    {"id": 29, "question": "What is the difference between DELETE, DROP and TRUNCATE?", "category": "DBMS", "difficulty": "Medium", "expectedKeywords": ["delete", "drop", "truncate", "rows", "table", "rollback", "structure"], "type": "mcq", "options": ["A. All three commands do the same thing", "B. DELETE: removes rows, supports rollback; DROP: removes entire table+structure; TRUNCATE: removes all rows fast, no rollback", "C. TRUNCATE keeps structure, DROP keeps data", "D. DELETE is DDL; DROP is DML"], "correctAnswer": "B"},
    {"id": 30, "question": "Explain ER diagram and its components.", "category": "DBMS", "difficulty": "Easy", "expectedKeywords": ["er", "entity", "relationship", "attribute", "diagram", "cardinality"], "type": "mcq", "options": ["A. A network topology diagram for routers", "B. Entity-Relationship diagram showing entities, attributes, relationships, and cardinality for DB design", "C. An algorithm flowchart for sorting", "D. A UML class diagram for software design"], "correctAnswer": "B"},

    # Operating Systems
    {"id": 31, "question": "What is an operating system and its functions?", "category": "Operating Systems", "difficulty": "Easy", "expectedKeywords": ["operating system", "process", "memory", "file", "management", "hardware"], "type": "mcq", "options": ["A. Software that only manages the file system", "B. System software managing processes, memory, files, hardware and providing interface between user and hardware", "C. Software that only runs user applications", "D. Software that only handles network connections"], "correctAnswer": "B"},
    {"id": 32, "question": "What is a process and a thread? How are they different?", "category": "Operating Systems", "difficulty": "Medium", "expectedKeywords": ["process", "thread", "memory", "lightweight", "execution", "context"], "type": "mcq", "options": ["A. Both always share the same memory space", "B. Process: independent execution unit with own memory; Thread: lightweight unit within a process sharing process memory", "C. A thread is heavier and slower than a process", "D. Processes and threads are identical concepts"], "correctAnswer": "B"},
    {"id": 33, "question": "What is deadlock? Explain conditions for deadlock.", "category": "Operating Systems", "difficulty": "Medium", "expectedKeywords": ["deadlock", "mutual exclusion", "hold", "wait", "no preemption", "circular"], "type": "mcq", "options": ["A. Deadlock only requires one of the four conditions", "B. Mutual exclusion, Hold-and-wait, No preemption, Circular wait — all four must hold simultaneously", "C. Deadlock requires five or more conditions", "D. Only circular wait condition is needed"], "correctAnswer": "B"},
    {"id": 34, "question": "Explain CPU scheduling algorithms.", "category": "Operating Systems", "difficulty": "Medium", "expectedKeywords": ["scheduling", "fcfs", "sjf", "round robin", "priority", "cpu"], "type": "mcq", "options": ["A. Only FCFS scheduling algorithm exists", "B. FCFS (first-come), SJF (shortest job), Round Robin (time slices), Priority scheduling — each with different trade-offs", "C. All CPU scheduling algorithms give the same result", "D. Only preemptive scheduling is used in modern OS"], "correctAnswer": "B"},
    {"id": 35, "question": "What is virtual memory?", "category": "Operating Systems", "difficulty": "Medium", "expectedKeywords": ["virtual", "memory", "page", "swap", "physical", "address space"], "type": "mcq", "options": ["A. A direct extension of physical RAM chips", "B. Technique using disk space as extended RAM, allowing programs larger than physical memory via paging/swapping", "C. A type of CPU cache memory (L1/L2)", "D. Dedicated GPU memory for graphics"], "correctAnswer": "B"},
    {"id": 36, "question": "What is paging in OS?", "category": "Operating Systems", "difficulty": "Medium", "expectedKeywords": ["paging", "page", "frame", "table", "memory", "fragmentation"], "type": "mcq", "options": ["A. Physically sorting memory pages by address", "B. Divides logical memory into fixed-size pages mapped to physical frames via page table, eliminating external fragmentation", "C. Compressing memory contents to save space", "D. Encrypting memory blocks for security"], "correctAnswer": "B"},
    {"id": 37, "question": "What are semaphores and mutexes?", "category": "Operating Systems", "difficulty": "Hard", "expectedKeywords": ["semaphore", "mutex", "synchronization", "lock", "binary", "critical section"], "type": "mcq", "options": ["A. Semaphore and mutex are the same thing", "B. Mutex: binary lock owned by one thread; Semaphore: integer counter controlling access by multiple threads for synchronization", "C. Semaphore is always binary (0 or 1) like mutex", "D. Mutex allows multiple threads in critical section"], "correctAnswer": "B"},
    {"id": 38, "question": "Explain the concept of context switching.", "category": "Operating Systems", "difficulty": "Medium", "expectedKeywords": ["context", "switching", "process", "save", "restore", "state", "scheduler"], "type": "mcq", "options": ["A. Switching between different user accounts", "B. OS saves current process state (registers, PC) and loads another process's saved state to switch execution", "C. Dynamically changing CPU clock frequency", "D. Swapping hard disk sectors during defragmentation"], "correctAnswer": "B"},
    {"id": 39, "question": "What is thrashing in OS?", "category": "Operating Systems", "difficulty": "Hard", "expectedKeywords": ["thrashing", "page", "fault", "swap", "performance", "working set"], "type": "mcq", "options": ["A. A normal and expected OS optimization behavior", "B. When excessive page faults cause OS to spend more time swapping pages than executing processes, severely degrading performance", "C. CPU overheating due to heavy computational load", "D. A type of memory leak in applications"], "correctAnswer": "B"},
    {"id": 40, "question": "What is a kernel and what are its types?", "category": "Operating Systems", "difficulty": "Easy", "expectedKeywords": ["kernel", "monolithic", "micro", "hybrid", "core", "os"], "type": "mcq", "options": ["A. Only one type of kernel exists", "B. Monolithic: entire OS in kernel space; Microkernel: minimal kernel, services in user space; Hybrid: combination of both", "C. The kernel runs entirely in user space", "D. The kernel is just another application program"], "correctAnswer": "B"},

    # Computer Networks
    {"id": 41, "question": "What is the OSI model? Name all layers.", "category": "Computer Networks", "difficulty": "Easy", "expectedKeywords": ["osi", "physical", "data link", "network", "transport", "session", "presentation", "application"], "type": "mcq", "options": ["A. The OSI model has only 4 layers", "B. 7 layers: Physical, Data Link, Network, Transport, Session, Presentation, Application (bottom to top)", "C. The TCP/IP model has 5 layers", "D. The OSI model has only 3 layers"], "correctAnswer": "B"},
    {"id": 42, "question": "What is TCP/IP and how does it work?", "category": "Computer Networks", "difficulty": "Medium", "expectedKeywords": ["tcp", "ip", "transmission", "protocol", "connection", "reliable", "packet"], "type": "mcq", "options": ["A. A protocol used only for web browsing (HTTP)", "B. Suite of protocols for reliable connection-oriented communication; IP handles addressing, TCP ensures reliable delivery", "C. A protocol used only for email (SMTP)", "D. Only works on local area networks (LAN)"], "correctAnswer": "B"},
    {"id": 43, "question": "What is the difference between TCP and UDP?", "category": "Computer Networks", "difficulty": "Medium", "expectedKeywords": ["tcp", "udp", "reliable", "unreliable", "connection", "fast", "stream"], "type": "mcq", "options": ["A. Both TCP and UDP are connectionless protocols", "B. TCP: reliable, ordered, connection-oriented, slower; UDP: fast, unreliable, connectionless — used for streaming/gaming", "C. UDP is more reliable and ordered than TCP", "D. TCP is faster than UDP"], "correctAnswer": "B"},
    {"id": 44, "question": "What is DNS and how does it work?", "category": "Computer Networks", "difficulty": "Easy", "expectedKeywords": ["dns", "domain", "name", "ip", "resolve", "server"], "type": "mcq", "options": ["A. Dynamic Network Switching system", "B. Domain Name System that resolves human-readable domain names (e.g. google.com) to IP addresses via distributed servers", "C. Data Network Security protocol", "D. Direct Node Selection algorithm"], "correctAnswer": "B"},
    {"id": 45, "question": "What is HTTP and HTTPS?", "category": "Computer Networks", "difficulty": "Easy", "expectedKeywords": ["http", "https", "protocol", "secure", "ssl", "tls", "web"], "type": "mcq", "options": ["A. HTTP and HTTPS are completely identical", "B. HTTP: unencrypted web protocol (port 80); HTTPS: HTTP secured with SSL/TLS encryption (port 443)", "C. HTTPS is significantly slower than HTTP always", "D. HTTP uses port 443 by default"], "correctAnswer": "B"},
    {"id": 46, "question": "What is an IP address? Difference between IPv4 and IPv6.", "category": "Computer Networks", "difficulty": "Easy", "expectedKeywords": ["ip", "address", "ipv4", "ipv6", "bits", "32", "128"], "type": "mcq", "options": ["A. Both IPv4 and IPv6 use 32-bit addresses", "B. IPv4: 32-bit (~4 billion addresses); IPv6: 128-bit (vastly more addresses) solving IPv4 address exhaustion", "C. IPv6 uses 64-bit addresses", "D. IPv4 uses 64-bit addresses"], "correctAnswer": "B"},
    {"id": 47, "question": "What is subnetting?", "category": "Computer Networks", "difficulty": "Hard", "expectedKeywords": ["subnet", "mask", "network", "host", "cidr", "bits", "divide"], "type": "mcq", "options": ["A. The process of combining multiple networks into one", "B. Dividing an IP network into smaller sub-networks using subnet mask to improve performance, security, and address management", "C. Encrypting all network traffic end-to-end", "D. The process of routing between different ISPs"], "correctAnswer": "B"},
    {"id": 48, "question": "What is a firewall?", "category": "Computer Networks", "difficulty": "Easy", "expectedKeywords": ["firewall", "security", "filter", "packet", "block", "network"], "type": "mcq", "options": ["A. A hardware-only device for boosting network speed", "B. Security system that monitors and filters network traffic, blocking unauthorized access based on defined rules", "C. A tool that only blocks computer viruses", "D. A device that speeds up internet connection"], "correctAnswer": "B"},
    {"id": 49, "question": "What is the difference between hub, switch and router?", "category": "Computer Networks", "difficulty": "Medium", "expectedKeywords": ["hub", "switch", "router", "broadcast", "mac", "ip", "layer"], "type": "mcq", "options": ["A. Hub, switch, and router all do the same thing", "B. Hub: broadcasts to all ports; Switch: forwards to specific port by MAC address; Router: routes packets between networks by IP", "C. Router works at Layer 2 (Data Link) using MAC addresses", "D. Switch broadcasts to all ports like a hub"], "correctAnswer": "B"},
    {"id": 50, "question": "What is the three-way handshake in TCP?", "category": "Computer Networks", "difficulty": "Medium", "expectedKeywords": ["syn", "syn-ack", "ack", "handshake", "connection", "tcp", "establish"], "type": "mcq", "options": ["A. TCP uses a two-way handshake (SYN, ACK)", "B. SYN (client) → SYN-ACK (server) → ACK (client) — three steps to establish a TCP connection", "C. TCP uses a four-way handshake", "D. TCP needs no handshake; connection is immediate"], "correctAnswer": "B"},

    # OOP
    {"id": 51, "question": "What are the four pillars of OOP?", "category": "OOP", "difficulty": "Easy", "expectedKeywords": ["encapsulation", "inheritance", "polymorphism", "abstraction", "oop"], "type": "mcq", "options": ["A. Loops, Classes, Objects, Methods", "B. Encapsulation, Inheritance, Polymorphism, Abstraction", "C. Compile, Link, Execute, Debug", "D. Input, Process, Output, Storage"], "correctAnswer": "B"},
    {"id": 52, "question": "What is inheritance and its types?", "category": "OOP", "difficulty": "Easy", "expectedKeywords": ["inheritance", "single", "multiple", "multilevel", "parent", "child", "base"], "type": "mcq", "options": ["A. Only single inheritance exists in OOP", "B. Single, Multiple, Multilevel, Hierarchical, Hybrid — all allow reusing parent class properties and behaviors", "C. Only two types of inheritance exist", "D. Inheritance is not possible in all OOP languages"], "correctAnswer": "B"},
    {"id": 53, "question": "What is polymorphism? Give an example.", "category": "OOP", "difficulty": "Medium", "expectedKeywords": ["polymorphism", "overloading", "overriding", "method", "compile", "runtime"], "type": "mcq", "options": ["A. The ability to have only one class in a program", "B. One interface, multiple implementations: compile-time (overloading) and runtime (overriding) polymorphism", "C. Only method overloading (compile-time) exists", "D. Only interfaces can achieve polymorphism"], "correctAnswer": "B"},
    {"id": 54, "question": "What is encapsulation?", "category": "OOP", "difficulty": "Easy", "expectedKeywords": ["encapsulation", "data hiding", "private", "public", "getter", "setter"], "type": "mcq", "options": ["A. Inheriting properties from a parent class", "B. Bundling data and methods together, hiding internal state using private variables with public getters/setters", "C. Creating multiple instances of a class", "D. Providing different implementations of the same method"], "correctAnswer": "B"},
    {"id": 55, "question": "What is abstraction in OOP?", "category": "OOP", "difficulty": "Easy", "expectedKeywords": ["abstraction", "abstract", "interface", "hide", "implementation", "essential"], "type": "mcq", "options": ["A. Showing all internal implementation details to users", "B. Hiding implementation complexity and showing only essential features through abstract classes and interfaces", "C. Making all class methods public by default", "D. Copying all methods from the parent class"], "correctAnswer": "B"},
    {"id": 56, "question": "What is the difference between class and object?", "category": "OOP", "difficulty": "Easy", "expectedKeywords": ["class", "object", "blueprint", "instance", "template", "attributes"], "type": "mcq", "options": ["A. Class and object are identical concepts", "B. Class is the blueprint/template; Object is an instance of the class with actual data values in memory", "C. An object is more abstract than a class", "D. A class can only have one object at a time"], "correctAnswer": "B"},
    {"id": 57, "question": "What is a constructor?", "category": "OOP", "difficulty": "Easy", "expectedKeywords": ["constructor", "initialize", "object", "class", "same name", "no return"], "type": "mcq", "options": ["A. A method that destroys objects and frees memory", "B. Special method with same name as class, called automatically when object is created to initialize its state", "C. A static method that returns a value", "D. An abstract method that must be overridden"], "correctAnswer": "B"},
    {"id": 58, "question": "What is method overriding?", "category": "OOP", "difficulty": "Medium", "expectedKeywords": ["overriding", "parent", "child", "same method", "runtime", "polymorphism"], "type": "mcq", "options": ["A. Same class, same name but different parameters (overloading)", "B. Child class provides its own implementation of a parent class method with the same signature — resolved at runtime", "C. Two methods in the same class with same signature", "D. Replacing a static method with a new version"], "correctAnswer": "B"},
    {"id": 59, "question": "What is an interface in OOP?", "category": "OOP", "difficulty": "Medium", "expectedKeywords": ["interface", "abstract", "implement", "contract", "method", "class"], "type": "mcq", "options": ["A. A concrete class with full method implementations", "B. A contract declaring abstract method signatures that implementing classes must define; supports multiple inheritance", "C. A static utility class", "D. A final class that cannot be extended"], "correctAnswer": "B"},
    {"id": 60, "question": "What is the difference between abstract class and interface?", "category": "OOP", "difficulty": "Medium", "expectedKeywords": ["abstract", "interface", "method", "constructor", "multiple", "implement"], "type": "mcq", "options": ["A. Abstract class and interface are identical", "B. Abstract: can have constructors, concrete methods, state; Interface: only declarations, supports multiple implementation", "C. Interface can have constructors like abstract class", "D. Abstract class allows multiple inheritance"], "correctAnswer": "B"},

    # Python
    {"id": 61, "question": "What is Python and what are its key features?", "category": "Python", "difficulty": "Easy", "expectedKeywords": ["python", "interpreted", "dynamic", "high level", "readable", "versatile"], "type": "mcq", "options": ["A. Compiled, statically typed, low-level language", "B. Interpreted, dynamically typed, high-level, readable, versatile, platform-independent language", "C. A language only for data science and ML tasks", "D. A low-level language close to machine code"], "correctAnswer": "B"},
    {"id": 62, "question": "What are Python lists and tuples? How are they different?", "category": "Python", "difficulty": "Easy", "expectedKeywords": ["list", "tuple", "mutable", "immutable", "ordered", "sequence"], "type": "mcq", "options": ["A. Both lists and tuples are immutable", "B. List: mutable, ordered; Tuple: immutable, ordered — tuples are faster and used for fixed data", "C. Tuples are mutable and lists are immutable", "D. Both lists and tuples are unordered"], "correctAnswer": "B"},
    {"id": 63, "question": "What is a Python dictionary?", "category": "Python", "difficulty": "Easy", "expectedKeywords": ["dictionary", "key", "value", "hash", "mutable", "unordered"], "type": "mcq", "options": ["A. An ordered immutable sequence like a tuple", "B. Mutable unordered collection of key-value pairs with O(1) average lookup using hashing", "C. A sorted list of unique values", "D. An immutable set of key-value pairs"], "correctAnswer": "B"},
    {"id": 64, "question": "What are decorators in Python?", "category": "Python", "difficulty": "Hard", "expectedKeywords": ["decorator", "function", "wrapper", "modify", "syntax", "@"], "type": "mcq", "options": ["A. A class inheritance mechanism in Python", "B. Functions that wrap another function using @syntax to modify or extend its behavior without changing its code", "C. A module import mechanism for loading libraries", "D. A built-in exception handling mechanism"], "correctAnswer": "B"},
    {"id": 65, "question": "What is list comprehension in Python?", "category": "Python", "difficulty": "Medium", "expectedKeywords": ["list", "comprehension", "concise", "loop", "expression", "iterable"], "type": "mcq", "options": ["A. A method for sorting list elements quickly", "B. Concise syntax [expr for item in iterable if condition] to create lists in one line instead of a loop", "C. A method for copying one list into another", "D. A way to convert a list to a tuple"], "correctAnswer": "B"},
    {"id": 66, "question": "What is the difference between deep copy and shallow copy?", "category": "Python", "difficulty": "Medium", "expectedKeywords": ["deep", "shallow", "copy", "reference", "nested", "object"], "type": "mcq", "options": ["A. Both create a new reference to the same object", "B. Shallow copy: copies object, nested objects still shared; Deep copy: fully independent copy including all nested objects", "C. Deep copy is faster than shallow copy", "D. Shallow copy creates independent nested objects"], "correctAnswer": "B"},
    {"id": 67, "question": "What are Python generators?", "category": "Python", "difficulty": "Hard", "expectedKeywords": ["generator", "yield", "iterator", "lazy", "memory", "next"], "type": "mcq", "options": ["A. A shortcut for creating list comprehensions", "B. Functions using yield to produce values one at a time lazily, saving memory for large or infinite sequences", "C. A string formatting tool using f-strings", "D. Python's module import mechanism"], "correctAnswer": "B"},
    {"id": 68, "question": "What is exception handling in Python?", "category": "Python", "difficulty": "Medium", "expectedKeywords": ["exception", "try", "except", "finally", "raise", "error"], "type": "mcq", "options": ["A. A mechanism that prevents all runtime errors", "B. try: risky code; except: catch specific exceptions; finally: always runs; raise: create exceptions; throws errors", "C. Only handles syntax errors at compile time", "D. An automatic error logging system"], "correctAnswer": "B"},
    {"id": 69, "question": "What is the difference between == and is in Python?", "category": "Python", "difficulty": "Medium", "expectedKeywords": ["==", "is", "equality", "identity", "value", "reference", "object"], "type": "mcq", "options": ["A. Both == and is compare object values", "B. == compares values/content; is compares object identity (same memory address)", "C. is compares values while == compares memory addresses", "D. Both == and is compare memory addresses"], "correctAnswer": "B"},
    {"id": 70, "question": "What are Python modules and packages?", "category": "Python", "difficulty": "Easy", "expectedKeywords": ["module", "package", "import", "namespace", "file", "__init__"], "type": "mcq", "options": ["A. Module and package are the same thing with different names", "B. Module: single .py file with code; Package: directory with __init__.py containing multiple modules for organization", "C. A package is a single Python file", "D. A module is a folder containing Python files"], "correctAnswer": "B"},

    # HR Questions
    {"id": 71, "question": "Tell me about yourself.", "category": "HR", "difficulty": "Easy", "expectedKeywords": ["background", "skills", "experience", "education", "goal", "passion", "work"], "type": "mcq", "options": ["A. List all your personal problems and failures", "B. Brief background, education, key skills, relevant experience, and career goals aligned with the job role", "C. Only mention your hobbies and personal interests", "D. Read your resume word-for-word to the interviewer"], "correctAnswer": "B"},
    {"id": 72, "question": "What are your strengths and weaknesses?", "category": "HR", "difficulty": "Easy", "expectedKeywords": ["strength", "weakness", "improve", "skill", "learning", "challenge"], "type": "mcq", "options": ["A. Claim you have absolutely no weaknesses", "B. Strengths: genuine skills you excel at; Weaknesses: real areas you are actively working to improve", "C. Only mention your strengths and ignore weaknesses", "D. Make up random strengths and weaknesses on the spot"], "correctAnswer": "B"},
    {"id": 73, "question": "Why do you want to join our company?", "category": "HR", "difficulty": "Easy", "expectedKeywords": ["company", "growth", "opportunity", "culture", "values", "contribute", "role"], "type": "mcq", "options": ["A. Say you only want the highest possible salary", "B. Research the company's culture, growth opportunities, role alignment, values, and how you can contribute", "C. Say any company offering a job would be fine", "D. Mention that you desperately need employment"], "correctAnswer": "B"},
    {"id": 74, "question": "Where do you see yourself in 5 years?", "category": "HR", "difficulty": "Easy", "expectedKeywords": ["goal", "career", "grow", "leadership", "skill", "contribute", "future"], "type": "mcq", "options": ["A. Say you want to be in the interviewer's exact position", "B. Describe career growth, skill development, leadership goals, and contribution aligned with company's long-term vision", "C. Say you plan to leave and start your own business", "D. Say you are completely unsure about your future plans"], "correctAnswer": "B"},
    {"id": 75, "question": "How do you handle pressure and stress?", "category": "HR", "difficulty": "Medium", "expectedKeywords": ["pressure", "stress", "priority", "manage", "calm", "deadline", "organize"], "type": "mcq", "options": ["A. Avoid all deadlines and high-pressure situations", "B. Prioritize tasks, create a plan, stay calm, communicate proactively, and focus on finding solutions", "C. Work continuously without any breaks", "D. Simply ignore all stress and pretend it doesn't exist"], "correctAnswer": "B"},
    {"id": 76, "question": "Describe a situation where you worked in a team.", "category": "HR", "difficulty": "Medium", "expectedKeywords": ["team", "collaborate", "communicate", "role", "goal", "together", "result"], "type": "mcq", "options": ["A. State that you strongly prefer working alone always", "B. Describe a specific situation: your role, how you collaborated, communicated, overcame challenges, and the positive outcome", "C. Argue that teams are inefficient and slow", "D. Take all the credit for the team's achievements"], "correctAnswer": "B"},
    {"id": 77, "question": "What motivates you?", "category": "HR", "difficulty": "Easy", "expectedKeywords": ["motivate", "challenge", "goal", "achieve", "learn", "passion", "growth"], "type": "mcq", "options": ["A. Only money and financial compensation motivate you", "B. Challenges, learning opportunities, achieving meaningful goals, contributing to team success, and personal growth", "C. Avoiding difficult work motivates you to perform better", "D. You have no specific source of motivation"], "correctAnswer": "B"},
    {"id": 78, "question": "How do you handle criticism or negative feedback?", "category": "HR", "difficulty": "Medium", "expectedKeywords": ["feedback", "improve", "listen", "accept", "positive", "learn", "grow"], "type": "mcq", "options": ["A. Argue back and defend yourself from all criticism", "B. Listen openly, accept constructive feedback, reflect on it, thank the person, and take action to improve", "C. Simply ignore all feedback you receive", "D. Get defensive and take criticism personally"], "correctAnswer": "B"},
    {"id": 79, "question": "What are your salary expectations?", "category": "HR", "difficulty": "Medium", "expectedKeywords": ["salary", "expectation", "market", "experience", "negotiate", "range"], "type": "mcq", "options": ["A. State the highest possible salary number without research", "B. Research market rates, provide a range based on experience/skills/location, remain open to negotiation", "C. Say you have absolutely no salary expectation", "D. Demand one exact salary figure with no flexibility"], "correctAnswer": "B"},
    {"id": 80, "question": "Do you have any questions for us?", "category": "HR", "difficulty": "Easy", "expectedKeywords": ["question", "role", "team", "culture", "growth", "expect", "learn"], "type": "mcq", "options": ["A. Say you have no questions at all for the interviewer", "B. Ask about role expectations, team culture, growth opportunities, challenges, and company direction", "C. Only ask about vacation days and benefits", "D. Ask questions about the company's competitors"], "correctAnswer": "B"},

    # Web Development
    {"id": 81, "question": "What is the difference between HTML, CSS and JavaScript?", "category": "Web Development", "difficulty": "Easy", "expectedKeywords": ["html", "css", "javascript", "structure", "style", "behavior", "web"], "type": "mcq", "options": ["A. All three do exactly the same thing", "B. HTML: structure/content; CSS: styling/layout; JavaScript: behavior/interactivity", "C. CSS is what adds functionality to web pages", "D. JavaScript defines the page structure"], "correctAnswer": "B"},
    {"id": 82, "question": "What is responsive web design?", "category": "Web Development", "difficulty": "Easy", "expectedKeywords": ["responsive", "mobile", "screen", "media query", "flexible", "layout"], "type": "mcq", "options": ["A. A design approach that only works on desktop screens", "B. Design that adapts to different screen sizes using fluid grids, flexible images, and CSS media queries", "C. Using fixed pixel-based layouts for all devices", "D. A technique exclusively for mobile applications"], "correctAnswer": "B"},
    {"id": 83, "question": "What is REST API?", "category": "Web Development", "difficulty": "Medium", "expectedKeywords": ["rest", "api", "get", "post", "put", "delete", "stateless", "http"], "type": "mcq", "options": ["A. An API style only for internal database queries", "B. Representational State Transfer: stateless HTTP-based API using GET, POST, PUT, DELETE methods for resource operations", "C. An API that only accepts XML data format", "D. An API style only for internal enterprise systems"], "correctAnswer": "B"},
    {"id": 84, "question": "What is the difference between GET and POST methods?", "category": "Web Development", "difficulty": "Easy", "expectedKeywords": ["get", "post", "url", "body", "secure", "data", "request"], "type": "mcq", "options": ["A. Both GET and POST send data in the URL", "B. GET: retrieves data via URL parameters (visible); POST: sends data in request body (more secure for sensitive data)", "C. POST retrieves data while GET sends data", "D. GET is more secure than POST for sensitive data"], "correctAnswer": "B"},
    {"id": 85, "question": "What is AJAX?", "category": "Web Development", "difficulty": "Medium", "expectedKeywords": ["ajax", "asynchronous", "javascript", "xml", "request", "update", "page"], "type": "mcq", "options": ["A. A new programming language for web development", "B. Asynchronous JavaScript technique that updates page content without full page reload using fetch or XMLHttpRequest", "C. A CSS animation and transition tool", "D. A server-side rendering technique for HTML"], "correctAnswer": "B"},
    {"id": 86, "question": "What is a cookie and a session?", "category": "Web Development", "difficulty": "Medium", "expectedKeywords": ["cookie", "session", "browser", "server", "store", "user", "stateless"], "type": "mcq", "options": ["A. Both cookies and sessions are stored on the server", "B. Cookie: stored in browser, persists across sessions; Session: stored server-side, more secure, ends when browser closes", "C. Sessions are stored in the browser like cookies", "D. Cookies and sessions are identical mechanisms"], "correctAnswer": "B"},
    {"id": 87, "question": "What is JSON?", "category": "Web Development", "difficulty": "Easy", "expectedKeywords": ["json", "javascript", "object", "notation", "key", "value", "data"], "type": "mcq", "options": ["A. A data format only usable within JavaScript code", "B. JavaScript Object Notation: lightweight, language-independent key-value data format for data exchange between systems", "C. Java Structured Object Notation for Java apps", "D. A binary data format for efficient storage"], "correctAnswer": "B"},
    {"id": 88, "question": "What is the purpose of HTML5?", "category": "Web Development", "difficulty": "Easy", "expectedKeywords": ["html5", "semantic", "canvas", "video", "audio", "local storage", "modern"], "type": "mcq", "options": ["A. An update designed to completely replace CSS", "B. Modern HTML with semantic elements, canvas, native video/audio, localStorage, geolocation, and improved accessibility", "C. A version designed exclusively for mobile websites", "D. An update designed to completely replace JavaScript"], "correctAnswer": "B"},
    {"id": 89, "question": "What is CSS Flexbox?", "category": "Web Development", "difficulty": "Medium", "expectedKeywords": ["flexbox", "flex", "container", "item", "layout", "align", "justify"], "type": "mcq", "options": ["A. A 3D layout and animation system", "B. One-dimensional layout model for arranging items in row or column with powerful alignment and space distribution", "C. A grid-based 2D layout system (that is CSS Grid)", "D. A CSS animation and keyframe system"], "correctAnswer": "B"},
    {"id": 90, "question": "What is the difference between synchronous and asynchronous JavaScript?", "category": "Web Development", "difficulty": "Hard", "expectedKeywords": ["synchronous", "asynchronous", "callback", "promise", "async", "await", "event loop"], "type": "mcq", "options": ["A. Both execute code in the exact same sequential order", "B. Synchronous: blocks execution until complete; Asynchronous: non-blocking, uses callbacks/promises/async-await", "C. Asynchronous code is always slower than synchronous", "D. Synchronous JavaScript uses multiple threads"], "correctAnswer": "B"},

    # Java
    {"id": 91,  "question": "What is Java and what are its key features?", "category": "Java", "difficulty": "Easy", "expectedKeywords": ["java", "platform independent", "object oriented", "compiled", "jvm", "bytecode"], "type": "mcq", "options": ["A. Platform-dependent language compiled to machine code", "B. Platform-independent (WORA), compiled to bytecode, runs on JVM, object-oriented, strongly typed, garbage collected", "C. Purely interpreted language, never compiled", "D. A language exclusively designed for Android development"], "correctAnswer": "B"},
    {"id": 92,  "question": "What is the difference between JDK, JRE and JVM?", "category": "Java", "difficulty": "Easy", "expectedKeywords": ["jdk", "jre", "jvm", "development kit", "runtime", "virtual machine", "compiler"], "type": "mcq", "options": ["A. JDK, JRE, and JVM are all the same tool", "B. JDK: development kit with compiler+tools; JRE: runtime environment to run programs; JVM: virtual machine executing bytecode", "C. JVM includes the Java compiler", "D. JRE is the tool used for Java development"], "correctAnswer": "B"},
    {"id": 93,  "question": "What is the difference between == and .equals() in Java?", "category": "Java", "difficulty": "Easy", "expectedKeywords": ["==", "equals", "reference", "value", "object", "comparison", "string"], "type": "mcq", "options": ["A. Both == and .equals() compare memory addresses", "B. ==: compares object references (memory addresses); .equals(): compares actual content/value — always use .equals() for strings", "C. .equals() compares object references like ==", "D. Both == and .equals() compare content values"], "correctAnswer": "B"},
    {"id": 94,  "question": "What are access modifiers in Java?", "category": "Java", "difficulty": "Easy", "expectedKeywords": ["public", "private", "protected", "default", "access", "modifier", "class"], "type": "mcq", "options": ["A. Java only has public and private modifiers", "B. Public: everywhere; Private: same class only; Protected: class + subclasses + package; Default: same package only", "C. Java only has two access modifiers", "D. All access modifiers allow access from anywhere"], "correctAnswer": "B"},
    {"id": 95,  "question": "What is the difference between abstract class and interface in Java?", "category": "Java", "difficulty": "Medium", "expectedKeywords": ["abstract", "interface", "implements", "extends", "multiple", "method", "constructor"], "type": "mcq", "options": ["A. Abstract class and interface are identical in Java", "B. Abstract: has constructors, concrete+abstract methods, state; Interface: declarations only, supports multiple implementation", "C. Interface can have constructors like abstract class", "D. Abstract class supports multiple inheritance"], "correctAnswer": "B"},
    {"id": 96,  "question": "What is exception handling in Java?", "category": "Java", "difficulty": "Medium", "expectedKeywords": ["exception", "try", "catch", "finally", "throw", "throws", "runtime"], "type": "mcq", "options": ["A. Exception handling only works for runtime errors", "B. try: code that may throw; catch: handles specific exceptions; finally: always runs; throw: creates; throws: declares", "C. Java has no finally block in exception handling", "D. Java handles all exceptions automatically"], "correctAnswer": "B"},
    {"id": 97,  "question": "What is the difference between ArrayList and LinkedList in Java?", "category": "Java", "difficulty": "Medium", "expectedKeywords": ["arraylist", "linkedlist", "dynamic", "index", "node", "insertion", "access"], "type": "mcq", "options": ["A. ArrayList and LinkedList have identical performance", "B. ArrayList: dynamic array, fast random access O(1), slow insert/delete; LinkedList: nodes, fast insert/delete O(1), slow access O(n)", "C. LinkedList is faster for random index access", "D. ArrayList is slower than LinkedList for all operations"], "correctAnswer": "B"},
    {"id": 98,  "question": "What is multithreading in Java?", "category": "Java", "difficulty": "Medium", "expectedKeywords": ["thread", "multithreading", "concurrent", "runnable", "synchronized", "process", "parallel"], "type": "mcq", "options": ["A. Java only supports single-threaded execution", "B. Multiple threads run concurrently via Thread class or Runnable interface; synchronized prevents race conditions", "C. Java threads do not share any memory at all", "D. Java has no built-in multithreading support"], "correctAnswer": "B"},
    {"id": 99,  "question": "What is the Collections framework in Java?", "category": "Java", "difficulty": "Medium", "expectedKeywords": ["collections", "list", "set", "map", "arraylist", "hashmap", "iterator"], "type": "mcq", "options": ["A. The Collections framework is only for sorting data", "B. Provides interfaces (List, Set, Map) and implementations (ArrayList, HashSet, HashMap) for reusable data structures", "C. Only ArrayList is available in the framework", "D. The framework contains no interfaces, only classes"], "correctAnswer": "B"},
    {"id": 100, "question": "What is Java garbage collection?", "category": "Java", "difficulty": "Hard", "expectedKeywords": ["garbage", "collection", "jvm", "memory", "heap", "unreachable", "gc"], "type": "mcq", "options": ["A. Java developers must manually free memory like in C", "B. JVM automatically reclaims heap memory from unreachable objects using Mark-and-Sweep; no manual free() needed", "C. Garbage collection only runs when explicitly called", "D. Java has no garbage collection mechanism"], "correctAnswer": "B"},
]

# ================= HELPER FUNCTIONS =================
def evaluate(answer, keywords, q_type="mcq", correct_answer=None):
    if q_type == "mcq":
        if not answer or not correct_answer:
            return 0
        return 100 if answer.strip().upper() == correct_answer.strip().upper() else 0
    # text fallback: keyword matching
    if not answer or not answer.strip():
        return 0
    answer_lower = answer.lower()
    match = sum(1 for k in keywords if k.lower() in answer_lower)
    return int((match / len(keywords)) * 100)

def get_performance_level(score):
    if score >= 90: return "Excellent"
    if score >= 70: return "Good"
    if score >= 50: return "Average"
    return "Needs Improvement"

def get_recommendations(score, weak_categories):
    recs = []
    if score >= 80:
        recs.append("You are performing well! Practice advanced and tricky questions.")
    elif score >= 50:
        recs.append("Good effort! Focus on improving your weak areas.")
        for cat in weak_categories:
            recs.append(f"Focus on {cat} - review core concepts and practice more questions.")
    else:
        recs.append("Keep practicing daily! Study the basics thoroughly.")
        recs.append("Take multiple mock interviews to build confidence.")
        recs.append("Review your textbooks and notes regularly.")
        for cat in weak_categories:
            recs.append(f"Revise {cat} fundamentals from scratch.")
    return recs

def get_model_answer(question_id):
    model_answers = {
        1:  "A stack is a linear data structure that follows the LIFO (Last In First Out) principle. Elements are added (push) and removed (pop) from the same end called the top.",
        2:  "An array stores elements in contiguous memory with fixed size and allows O(1) access by index. A linked list stores elements in nodes connected by pointers, allowing dynamic size but O(n) access time.",
        3:  "A Binary Search Tree is a tree where each node has at most two children, and the left child has a smaller value while the right child has a larger value than the parent node.",
        21: "DBMS (Database Management System) is software that manages databases. Advantages include data redundancy reduction, data integrity, security, backup & recovery, and concurrent access.",
        22: "Normalization reduces data redundancy. 1NF: atomic values. 2NF: no partial dependency. 3NF: no transitive dependency.",
        51: "The four pillars of OOP are: Encapsulation (data hiding), Inheritance (code reuse), Polymorphism (many forms), and Abstraction (hiding complexity).",
        71: "Structure: Briefly introduce your background, education, key skills, relevant experiences, and career goals. Relate them to the role you are applying for.",
        91: "Java is a high-level, object-oriented, platform-independent programming language. Key features: Write Once Run Anywhere (WORA) via JVM, strongly typed, automatic garbage collection, multithreading support.",
        92: "JDK (Java Development Kit) is for developers — includes compiler and tools. JRE (Java Runtime Environment) runs Java programs — includes JVM and libraries. JVM (Java Virtual Machine) executes bytecode on any platform.",
        93: "== compares object references (memory addresses). .equals() compares the actual content/value of objects. For strings, always use .equals() to compare content.",
        94: "Public: accessible everywhere. Private: only within the same class. Protected: same class and subclasses. Default (no modifier): same package only.",
        95: "Abstract class can have constructors, concrete methods, and state. Interface only has abstract methods (Java 8+ allows default methods). A class can implement multiple interfaces but extend only one abstract class.",
        96: "Exception handling uses try-catch-finally blocks. try: code that may throw, catch: handles specific exceptions, finally: always executes. throw creates exceptions, throws declares them in method signatures.",
        97: "ArrayList uses a dynamic array — fast random access O(1), slow insertion/deletion. LinkedList uses doubly linked nodes — fast insertion/deletion O(1), slow random access O(n).",
        98: "Multithreading allows concurrent execution of multiple threads within one process. Implemented via Thread class or Runnable interface. synchronized keyword prevents race conditions.",
        99: "Java Collections Framework provides interfaces (List, Set, Map) and implementations (ArrayList, HashSet, HashMap). It offers reusable data structures with consistent APIs.",
        100: "Garbage collection automatically frees heap memory by removing objects with no references. JVM runs GC using algorithms like Mark-and-Sweep. Developers cannot explicitly free memory like in C/C++.",
    }
    return model_answers.get(question_id, "Study the core concepts of this topic and practice explaining them clearly and concisely.")

# ================= STATIC FILES =================
@app.route('/')
def serve_index():
    return send_from_directory('frontend', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('frontend', filename)

# ================= USER MODULE =================
@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    if not data or not data.get('username') or not data.get('email'):
        return jsonify({"success": False, "message": "Name and email are required"}), 400
    for user in usersDB:
        if user['email'] == data['email']:
            return jsonify({"success": False, "message": "Email already registered"}), 400
    user = {
        "id": len(usersDB) + 1,
        "username": data['username'],
        "email": data['email'],
        "password": data.get('password', ''),
        "createdAt": datetime.now().isoformat()
    }
    usersDB.append(user)
    return jsonify({"success": True, "message": "User registered successfully", "userId": user['id'], "username": user['username']})

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    if not data:
        return jsonify({"success": False, "message": "Invalid request"}), 400
    for user in usersDB:
        if user['email'] == data.get('email'):
            return jsonify({"success": True, "message": "Login successful", "userId": user['id'], "username": user['username']})
    # Auto-register for demo ease
    user = {
        "id": len(usersDB) + 1,
        "username": data.get('username', data.get('email', 'User').split('@')[0]),
        "email": data.get('email', ''),
        "password": data.get('password', ''),
        "createdAt": datetime.now().isoformat()
    }
    usersDB.append(user)
    return jsonify({"success": True, "message": "Login successful", "userId": user['id'], "username": user['username']})

# ================= QUESTION MODULE =================
@app.route('/api/questions', methods=['GET'])
def get_all_questions():
    return jsonify({"success": True, "data": questionsDB, "total": len(questionsDB)})

@app.route('/api/questions/categories', methods=['GET'])
def get_categories():
    cats = list(set(q['category'] for q in questionsDB))
    result = []
    for cat in sorted(cats):
        count = len([q for q in questionsDB if q['category'] == cat])
        result.append({"name": cat, "count": count})
    return jsonify({"success": True, "data": result})

@app.route('/api/questions/category/<category>', methods=['GET'])
def get_by_category(category):
    result = [q for q in questionsDB if q['category'].lower() == category.lower()]
    return jsonify({"success": True, "data": result, "total": len(result)})

@app.route('/api/questions/random', methods=['GET'])
def get_random():
    count = int(request.args.get('count', 10))
    category = request.args.get('category', 'all')
    difficulty = request.args.get('difficulty', 'all')
    pool = questionsDB.copy()
    if category.lower() != 'all':
        pool = [q for q in pool if q['category'].lower() == category.lower()]
    if difficulty.lower() != 'all':
        pool = [q for q in pool if q['difficulty'].lower() == difficulty.lower()]
    random.shuffle(pool)
    return jsonify({"success": True, "data": pool[:count]})

@app.route('/api/questions/add', methods=['POST'])
def add_question():
    data = request.json
    new_q = {
        "id": max(q['id'] for q in questionsDB) + 1,
        "question": data['question'],
        "category": data['category'],
        "difficulty": data.get('difficulty', 'Medium'),
        "expectedKeywords": data.get('keywords', [])
    }
    questionsDB.append(new_q)
    return jsonify({"success": True, "message": "Question added", "id": new_q['id']})

# ================= FEEDBACK & EVALUATION MODULE =================
@app.route('/api/feedback', methods=['POST'])
def get_feedback():
    data = request.json
    if not data or 'responses' not in data:
        return jsonify({"success": False, "message": "No responses provided"}), 400

    responses = data['responses']
    user_id = data.get('userId', 1)
    username = data.get('username', 'User')

    if not responses:
        return jsonify({"success": False, "message": "Empty responses"}), 400

    total_score = 0
    category_scores = {}
    detailed_feedback = []

    for r in responses:
        q = next((x for x in questionsDB if x['id'] == r.get('questionId')), None)
        if not q:
            continue

        score = evaluate(r.get('answer', ''), q['expectedKeywords'], q.get('type', 'mcq'), q.get('correctAnswer'))
        total_score += score

        cat = q['category']
        if cat not in category_scores:
            category_scores[cat] = {"total": 0, "score": 0, "count": 0}
        category_scores[cat]["total"] += 100
        category_scores[cat]["score"] += score
        category_scores[cat]["count"] += 1

        matched_kw = [k for k in q['expectedKeywords'] if k.lower() in r.get('answer', '').lower()]
        missed_kw = [k for k in q['expectedKeywords'] if k.lower() not in r.get('answer', '').lower()]

        detailed_feedback.append({
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
        })

    avg_score = int(total_score / len(responses)) if responses else 0

    category_analysis = []
    weak_categories = []
    for cat, data_c in category_scores.items():
        percent = int((data_c['score'] / data_c['total']) * 100) if data_c['total'] > 0 else 0
        category_analysis.append({"category": cat, "score": percent, "count": data_c['count']})
        if percent < 50:
            weak_categories.append(cat)

    result = {
        "userId": user_id,
        "username": username,
        "userEmail": data.get('userEmail', ''),
        "overallScore": avg_score,
        "performance": get_performance_level(avg_score),
        "totalQuestions": len(responses),
        "categoryAnalysis": sorted(category_analysis, key=lambda x: x['score'], reverse=True),
        "recommendations": get_recommendations(avg_score, weak_categories),
        "detailedFeedback": detailed_feedback,
        "date": datetime.now().isoformat(),
        "timeTaken": data.get('totalTime', 0)
    }

    interviewResultsDB.append(result)
    return jsonify({"success": True, "data": result})

# ================= PERFORMANCE TRACKING MODULE =================
@app.route('/api/history/<int:user_id>', methods=['GET'])
def get_history(user_id):
    user_results = [r for r in interviewResultsDB if r.get('userId') == user_id]
    return jsonify({"success": True, "data": user_results, "total": len(user_results)})

@app.route('/api/history/email/<path:email>', methods=['GET'])
def get_history_by_email(email):
    user_results = [r for r in interviewResultsDB if r.get('userEmail', '').lower() == email.lower()]
    return jsonify({"success": True, "data": user_results, "total": len(user_results)})

@app.route('/api/stats', methods=['GET'])
def get_stats():
    return jsonify({
        "success": True,
        "data": {
            "totalQuestions": len(questionsDB),
            "totalCategories": len(set(q['category'] for q in questionsDB)),
            "totalUsers": len(usersDB),
            "totalInterviews": len(interviewResultsDB)
        }
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
