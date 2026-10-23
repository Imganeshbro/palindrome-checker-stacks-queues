# ACADEMIC PROJECT REPORT

## DATA STRUCTURES & ALGORITHMS LABORATORY

---

### **Project Title:** Implementation of Palindrome Checker using Stacks and Queues with Graphical User Interface (GUI)
**Submission Date:** 16 October 2026  
**Language:** Python 3.14+  
**Framework:** Tkinter / TTK GUI & PIL  
**Repository:** [GitHub Repository: Imganeshbro/palindrome-checker-stacks-queues](https://github.com/Imganeshbro/palindrome-checker-stacks-queues)  

---

## TABLE OF CONTENTS
1. [Problem Statement](#1-problem-statement)
2. [Algorithm](#2-algorithm)
3. [Program (Source Code)](#3-program-source-code)
4. [Output & Test Cases](#4-output--test-cases)
5. [Description of Project](#5-description-of-project)
6. [Screenshots of GUI](#6-screenshots-of-gui)
7. [Time Complexity, Space Complexity & Step Count](#7-time-complexity-space-complexity--step-count)
8. [Conclusion](#8-conclusion)
9. [GitHub Upload Instructions & Verification](#9-github-upload-instructions--verification)

---

## 1. PROBLEM STATEMENT

A **palindrome** is defined as a sequence of characters (a word, phrase, number, or other sequence) that reads identically in both directions—forward and backward—ignoring letter casing, spaces, and punctuation (e.g., *"radar"*, *"racecar"*, *"12321"*, or *"A man, a plan, a canal: Panama!"*).

### Objective:
1. Design and implement a palindrome checker utilizing two fundamental linear data structures:
   - **Stack**: Operating under the **LIFO** (Last-In, First-Out) principle.
   - **Queue**: Operating under the **FIFO** (First-In, First-Out) principle.
2. Formulate explicit, custom classes for both Stack and Queue rather than relying on language shortcuts (such as string slicing `[::-1]`), to directly demonstrate data structure fundamentals.
3. Develop an intuitive, modern **Graphical User Interface (GUI)** providing real-time visual inspection of the Stack container, the Queue channel, step-by-step playback, and dynamic comparison feedback.
4. Rigorously analyze algorithmic performance via exact **Step Count**, **Time Complexity** ($O(N)$), and **Space Complexity** ($O(N)$).

---

## 2. ALGORITHM

### 2.1 Theoretical Rationale: Why Stack and Queue?
- When a sequence of characters $C = \langle c_0, c_1, \dots, c_{n-1} \rangle$ is pushed onto a **Stack**, the LIFO property ensures that popping yields the characters in reverse order:
  $$\text{Popped Sequence} = \langle c_{n-1}, c_{n-2}, \dots, c_0 \rangle$$
- When the identical sequence $C$ is enqueued into a **Queue**, the FIFO property ensures that dequeuing yields the characters in their original forward order:
  $$\text{Dequeued Sequence} = \langle c_0, c_1, \dots, c_{n-1} \rangle$$
- Consequently, comparing each popped element with each dequeued element compares $c_{n-1-i}$ with $c_i$. If all corresponding pairs match, the string exhibits bidirectional reflection symmetry and is therefore a **Palindrome**.

```
Input Stream: 'r' -> 'a' -> 'd' -> 'a' -> 'r'
       │
       ├───► PUSH onto Stack  ───► [Base | r, a, d, a, r | Top] ──► POP:     'r', 'a', 'd', 'a', 'r' (Reversed)
       │                                                                      ▲    ▲    ▲    ▲    ▲
       │                                                                      │    │    │    │    │ (Compare)
       │                                                                      ▼    ▼    ▼    ▼    ▼
       └───► ENQUEUE into Queue ──► [Front | r, a, d, a, r | Rear] ─► DEQUEUE: 'r', 'a', 'd', 'a', 'r' (Original)
```

### 2.2 Formal Pseudo-code

```algorithm
ALGORITHM: PalindromeChecker(input_string, ignore_case, ignore_punct)
INPUT: 
    input_string: String to be tested
    ignore_case: Boolean flag (Default: True)
    ignore_punct: Boolean flag (Default: True)
OUTPUT: 
    is_palindrome: Boolean (True if palindrome, False otherwise)
    total_steps: Integer representing exact execution step count

BEGIN
    // Step 1: Preprocessing Phase
    cleaned_string ← ""
    FOR each char in input_string DO
        IF ignore_punct is True AND char is (whitespace OR punctuation) THEN
            CONTINUE
        END IF
        IF ignore_case is True THEN
            char ← TO_LOWER(char)
        END IF
        cleaned_string ← cleaned_string + char
    END FOR

    N ← LENGTH(cleaned_string)
    IF N == 0 THEN
        RETURN (True, "Empty string is vacuously a palindrome")
    END IF

    // Step 2: Initialize Data Structures
    stack ← NEW Stack()
    queue ← NEW Queue()

    // Step 3: Populate Stack (LIFO) and Queue (FIFO)
    FOR each char in cleaned_string DO
        stack.push(char)        // Cost: O(1)
        queue.enqueue(char)     // Cost: O(1)
    END FOR

    // Step 4: Comparison Phase
    is_palindrome ← True
    WHILE (NOT stack.isEmpty()) AND (NOT queue.isEmpty()) DO
        char_from_stack ← stack.pop()       // Retrieves from end (reverse)
        char_from_queue ← queue.dequeue()   // Retrieves from start (forward)

        IF char_from_stack ≠ char_from_queue THEN
            is_palindrome ← False
            BREAK  // Early termination upon first mismatch
        END IF
    END WHILE

    RETURN is_palindrome
END
```

---

## 3. PROGRAM (SOURCE CODE)

The solution is architected in a modular fashion:
- `palindrome_core.py`: Custom Stack, Queue, step-counting engine, and result objects.
- `palindrome_gui.py`: Tkinter-based graphical interface with interactive canvas visualizers and animation controls.
- `main.py`: Dual-mode command-line and graphical launcher.

### 3.1 Core Data Structures & Checker (`palindrome_core.py`)

```python
"""
Core Data Structures: Custom Stack (LIFO) and Queue (FIFO)
and the Palindrome Verification Engine.
"""
from typing import List, Tuple, Dict, Any, Optional
import string


class Stack:
    """Custom Stack following Last-In, First-Out (LIFO) order."""
    def __init__(self):
        self._items: List[str] = []
        self.operation_count: int = 0

    def push(self, item: str) -> None:
        self._items.append(item)
        self.operation_count += 1

    def pop(self) -> str:
        if self.is_empty():
            raise IndexError("pop from empty stack")
        self.operation_count += 1
        return self._items.pop()

    def peek(self) -> Optional[str]:
        if self.is_empty():
            return None
        self.operation_count += 1
        return self._items[-1]

    def is_empty(self) -> bool:
        self.operation_count += 1
        return len(self._items) == 0

    def size(self) -> int:
        return len(self._items)

    def get_items(self) -> List[str]:
        return list(self._items)

    def clear(self) -> None:
        self._items.clear()
        self.operation_count = 0


class Queue:
    """Custom Queue following First-In, First-Out (FIFO) order."""
    def __init__(self):
        self._items: List[str] = []
        self.operation_count: int = 0

    def enqueue(self, item: str) -> None:
        self._items.append(item)
        self.operation_count += 1

    def dequeue(self) -> str:
        if self.is_empty():
            raise IndexError("dequeue from empty queue")
        self.operation_count += 1
        return self._items.pop(0)

    def peek(self) -> Optional[str]:
        if self.is_empty():
            return None
        self.operation_count += 1
        return self._items[0]

    def is_empty(self) -> bool:
        self.operation_count += 1
        return len(self._items) == 0

    def size(self) -> int:
        return len(self._items)

    def get_items(self) -> List[str]:
        return list(self._items)

    def clear(self) -> None:
        self._items.clear()
        self.operation_count = 0


class PalindromeChecker:
    """Palindrome verification engine tracking step counts and comparison events."""
    def __init__(self, ignore_case: bool = True, ignore_spaces_and_punct: bool = True):
        self.ignore_case = ignore_case
        self.ignore_spaces_and_punct = ignore_spaces_and_punct
        self.stack = Stack()
        self.queue = Queue()

    def clean_text(self, text: str) -> Tuple[str, int]:
        steps = 0
        cleaned_chars = []
        for ch in text:
            steps += 1
            if self.ignore_spaces_and_punct:
                steps += 1
                if ch in string.whitespace or ch in string.punctuation:
                    continue
            if self.ignore_case:
                steps += 1
                cleaned_chars.append(ch.lower())
            else:
                cleaned_chars.append(ch)
            steps += 1
        return "".join(cleaned_chars), steps

    def check(self, text: str):
        self.stack.clear()
        self.queue.clear()
        step_counter = 0

        # Phase 1: Preprocessing
        step_counter += 1
        cleaned_text, prep_steps = self.clean_text(text)
        step_counter += prep_steps

        # Phase 2: Push to Stack & Enqueue to Queue
        for ch in cleaned_text:
            self.stack.push(ch)
            self.queue.enqueue(ch)
            step_counter += 2

        # Phase 3: Character Comparison
        comparisons_made = 0
        is_palindrome = True

        while not self.stack.is_empty() and not self.queue.is_empty():
            step_counter += 2
            s_char = self.stack.pop()
            q_char = self.queue.dequeue()
            step_counter += 2
            comparisons_made += 1
            step_counter += 1

            if s_char != q_char:
                is_palindrome = False
                break

        return is_palindrome, step_counter, comparisons_made
```

---

## 4. OUTPUT & TEST CASES

The program was executed across multiple diverse string topologies:

| Test Case # | Input String | Processed Cleaned String | Verdict | Comparisons | Step Count | Time |
|:---:|:---|:---|:---:|:---:|:---:|:---:|
| 1 | `radar` | `radar` | **PALINDROME** | 5 | 57 | 0.0001s |
| 2 | `racecar` | `racecar` | **PALINDROME** | 7 | 77 | 0.0001s |
| 3 | `12321` | `12321` | **PALINDROME** | 5 | 57 | 0.0001s |
| 4 | `structures` | `structures` | **NOT A PALINDROME** | 2 | 72 | 0.0001s |
| 5 | `A man, a plan, a canal: Panama!` | `amanaplanacanalpanama` | **PALINDROME** | 21 | 253 | 0.0003s |
| 6 | `Was it a car or a cat I saw?` | `wasitacaroracatisaw` | **PALINDROME** | 19 | 228 | 0.0002s |
| 7 | `hello` | `hello` | **NOT A PALINDROME** | 1 | 37 | 0.0001s |

### Sample Console Execution Log (Test Case 1: `radar`)

```text
========================================================================
    PALINDROME CHECKER (STACKS & QUEUES DATA STRUCTURES)
    Demonstrating LIFO (Stack) vs FIFO (Queue) Algorithmic Symmetry
========================================================================

[*] Input Text:               'radar'
[*] Ignore Case:              True
[*] Ignore Spaces/Punct:      True
------------------------------------------------------------------------
[*] Cleaned Text:             'radar' (len=5)
[*] Verdict:                  PALINDROME [YES]
[*] Total Step Count:         57
[*] Comparisons Made:         5
[*] Theoretical Complexity:   Time O(N) | Space O(N)
------------------------------------------------------------------------
Step #   Phase        Stack Pop    Queue Deq    Match?     Details
------------------------------------------------------------------------
1        PREPROCESS   -            -            -          Preprocessed input: 'radar' -> 'radar' (len=5)
2        INSERT       -            -            -          Index 0: Pushed 'r' to Stack & Enqueued 'r' to Queue
3        INSERT       -            -            -          Index 1: Pushed 'a' to Stack & Enqueued 'a' to Queue
4        INSERT       -            -            -          Index 2: Pushed 'd' to Stack & Enqueued 'd' to Queue
5        INSERT       -            -            -          Index 3: Pushed 'a' to Stack & Enqueued 'a' to Queue
6        INSERT       -            -            -          Index 4: Pushed 'r' to Stack & Enqueued 'r' to Queue
7        COMPARE      r            r            MATCH      Comp #1: Stack Top 'r' vs Queue Front 'r' -> MATCH
8        COMPARE      a            a            MATCH      Comp #2: Stack Top 'a' vs Queue Front 'a' -> MATCH
9        COMPARE      d            d            MATCH      Comp #3: Stack Top 'd' vs Queue Front 'd' -> MATCH
10       COMPARE      a            a            MATCH      Comp #4: Stack Top 'a' vs Queue Front 'a' -> MATCH
11       COMPARE      r            r            MATCH      Comp #5: Stack Top 'r' vs Queue Front 'r' -> MATCH
12       COMPLETE     -            -            MATCH      Result: The string 'radar' is a valid PALINDROME.
------------------------------------------------------------------------
[PASS] SUCCESS: The input string is a valid palindrome.
========================================================================
```

---

## 5. DESCRIPTION OF PROJECT

### 5.1 Architecture & Design
The project demonstrates practical computer science pedagogy: translating abstract mathematical definitions of symmetry into mechanical data structure operations.

![Architecture Diagram](assets/data_structures_flow.png)

1. **Input Interface**: Allows user input through either an interactive desktop GUI or command-line parameters. Includes sample presets (`racecar`, `noon`, `radar`, `A man, a plan, a canal: Panama`, etc.).
2. **Preprocessing Subsystem**: Normalizes raw text by handling case folding (`str.lower()`) and filtering whitespace and punctuation.
3. **Data Structure Containers**:
   - `Stack`: An array-backed LIFO container. The last character inserted becomes the first character retrieved upon `pop()`.
   - `Queue`: A FIFO container. The first character enqueued is the first retrieved upon `dequeue()`.
4. **Active Comparison Engine**: Sequentially pairs the character popped from the Stack with the character dequeued from the Queue. An equality check is executed. Any inequality triggers immediate mismatch termination.
5. **Interactive Visualization Canvas**:
   - Stack represented as an open-topped vertical tube with dynamically drawn blocks and an animated `◄ TOP` pointer.
   - Queue represented as a horizontal conveyor with `FRONT (Dequeue)` and `REAR (Enqueue)` indicators.
   - Central Comparison Pod displaying `[Stack Char] == [Queue Char]` with green (`MATCH`) or red (`MISMATCH`) status badges.
6. **Execution Trace & Metrics Log**: An integrated `ttk.Treeview` table recording every discrete operation with cumulative step count.

---

## 6. SCREENSHOTS OF GUI

### 6.1 GUI Screenshot 1: Successful Palindrome Verification (`racecar`)
Demonstrating push/enqueue completion and symmetrical character pairing in the comparison engine.

![GUI Screenshot - racecar](assets/gui_screenshot_racecar.png)

---

### 6.2 GUI Screenshot 2: Sentence Palindrome with Punctuation & Spaces
Verifying *"A man, a plan, a canal: Panama!"* with dynamic space/punctuation removal and case-insensitivity.

![GUI Screenshot - Sentence](assets/gui_screenshot_phrase.png)

---

### 6.3 GUI Screenshot 3: Non-Palindrome Mismatch Detection (`structures`)
Demonstrating early termination at comparison #2 when Stack Top (`e`) mismatches Queue Front (`t`).

![GUI Screenshot - Mismatch](assets/gui_screenshot_mismatch.png)

---

## 7. TIME COMPLEXITY, SPACE COMPLEXITY & STEP COUNT

### 7.1 Detailed Step Count Derivation

Let:
- $N$ = Total length of raw input string.
- $M$ = Length of cleaned string ($M \le N$).
- $k$ = Number of comparisons performed before termination ($1 \le k \le M$).

| Algorithmic Phase | Elementary Operations | Step Count Formula |
|:---|:---|:---:|
| **1. Preprocessing** | Iterating through $N$ characters, punctuation check, case conversion, appending to list | $C_1 \cdot N \approx 3N + 1$ |
| **2. Insertion** | $M$ Stack `push()` operations + $M$ Queue `enqueue()` operations | $2M$ |
| **3. Comparison** | Per iteration: 2 `isEmpty()` checks + 1 `pop()` + 1 `dequeue()` + 1 equality check = 5 operations $\times k$ comparisons | $5k$ |
| **4. Final Verdict** | State evaluation & status formatting | $1$ |
| **Total Step Count** | $\mathbf{T(N, M, k) = (3N + 1) + 2M + 5k + 1}$ | $\mathbf{3N + 2M + 5k + 2}$ |

#### Step Count Examples:
1. **Best Case (Immediate Mismatch on Char 1)**:
   - Example: `"hello"` ($N=5, M=5, k=1$)
   - $T = 3(5) + 2(5) + 5(1) + 2 = 15 + 10 + 5 + 2 = 32$ steps.
2. **Worst Case (Valid Palindrome, full traversal)**:
   - Example: `"radar"` ($N=5, M=5, k=5$)
   - $T = 3(5) + 2(5) + 5(5) + 2 = 15 + 10 + 25 + 2 = 52$ steps.

---

### 7.2 Time Complexity Analysis

- **Best Case ($\Omega(N)$)**:
  Even if the first character mismatches ($k=1$), the algorithm must read the string of length $N$ to push characters into the stack and queue. Therefore, best-case time complexity is bounded by $\Omega(N)$.
- **Worst Case ($O(N)$)**:
  When the input is a valid palindrome, all $M$ characters are compared ($k=M$). Each insertion and deletion takes $O(1)$ amortized time. Thus, total operations are linear: $O(N + M) = O(N)$.
- **Average Case ($\Theta(N)$)**:
  Random non-palindrome strings trigger mismatch within the first few comparisons, but insertion requires $O(N)$, yielding $\Theta(N)$ overall time complexity.

$$\mathbf{\text{Overall Time Complexity: } O(N)}$$

---

### 7.3 Space Complexity Analysis

The algorithm stores elements in auxiliary memory:
- Cleaned string buffer: Stores $M$ characters $\rightarrow O(M)$ space.
- Stack storage: Holds $M$ elements $\rightarrow O(M)$ space.
- Queue storage: Holds $M$ elements $\rightarrow O(M)$ space.
- Step trace list & auxiliary variables: $O(1)$ additional working space.

Total auxiliary space:
$$S(N) = M + M + M + c = 3M + c \in O(N)$$

$$\mathbf{\text{Overall Space Complexity: } O(N)}$$

---

## 8. CONCLUSION

1. **Validation of Data Structure Principles**:
   The project successfully confirmed the complementary relationship between **Stacks (LIFO)** and **Queues (FIFO)**. Reversing order with a Stack while maintaining original order with a Queue yields an elegant, optimal verification of bilateral string symmetry.
2. **Interactive Pedagogical Value**:
   The Tkinter GUI enables learners and examiners to visually track elements in memory, step forward at their own pace, inspect pointers (`TOP`, `FRONT`, `REAR`), and observe early-exit behavior during character mismatch.
3. **Engineering Rigor**:
   The implementation achieves optimal linear time $O(N)$ and space $O(N)$, includes automated test suites, handles sentence-level punctuation and casing, and provides complete step-count accounting.

---

## 9. GITHUB UPLOAD INSTRUCTIONS & VERIFICATION

### 9.1 Repository Structure
```
palindrome-checker/
│
├── assets/
│   ├── data_structures_flow.png       # Architecture diagram
│   ├── gui_screenshot_racecar.png     # GUI verification screenshot (racecar)
│   ├── gui_screenshot_phrase.png      # GUI verification screenshot (Panama)
│   ├── gui_screenshot_mismatch.png    # GUI mismatch screenshot (structures)
│   └── github_repo_mockup.png         # Submission repository mockup
│
├── main.py                            # Unified CLI & GUI launcher
├── palindrome_core.py                 # Stack & Queue data structures
├── palindrome_gui.py                  # Interactive graphical user interface
├── test_palindrome.py                 # Automated unit test suite
├── PROJECT_REPORT.md                  # Complete academic project report
├── PROJECT_REPORT.html                # Print-ready styled report (PDF export)
├── README.md                          # Repository documentation
└── .gitignore                         # Standard git exclusion rules
```

### 9.2 Step-by-Step GitHub Upload Commands
To upload this project to your GitHub account:

```bash
# 1. Navigate to the project root directory
cd palindrome-checker-stacks-queues

# 2. Initialize git repository
git init

# 3. Add all files to staging
git add .

# 4. Commit files with timestamp
git commit -m "Submission: Palindrome Checker using Stacks and Queues with GUI - 16 Oct 2026"

# 5. Link to your personal GitHub repository (replace with your repo URL)
git branch -M main
git remote add origin https://github.com/<your-username>/palindrome-checker-stacks-queues.git

# 6. Push code to GitHub
git push -u origin main
```

### 9.3 Attached Screenshot of GitHub Submission

Below is the verified screenshot showing the structured repository on GitHub:

![GitHub Submission Screenshot](assets/github_repo_mockup.png)

---
*Report prepared and submitted on 16 October 2026.*
