"""
Palindrome Checker Core Module
Implements custom Stack (LIFO) and Queue (FIFO) data structures
and provides the algorithmic core for palindrome verification with detailed step counts.
"""

from typing import List, Tuple, Dict, Any, Optional
import string


class Stack:
    """
    Custom Stack Implementation following LIFO (Last-In, First-Out) principle.
    """
    def __init__(self):
        self._items: List[str] = []
        self.operation_count: int = 0

    def push(self, item: str) -> None:
        """Push an element onto the top of the stack. (Step cost: 1)"""
        self._items.append(item)
        self.operation_count += 1

    def pop(self) -> str:
        """Remove and return the element at the top of the stack. (Step cost: 1)"""
        if self.is_empty():
            raise IndexError("pop from empty stack")
        self.operation_count += 1
        return self._items.pop()

    def peek(self) -> Optional[str]:
        """Return the element at the top without removing it. (Step cost: 1)"""
        if self.is_empty():
            return None
        self.operation_count += 1
        return self._items[-1]

    def is_empty(self) -> bool:
        """Check if the stack is empty. (Step cost: 1)"""
        self.operation_count += 1
        return len(self._items) == 0

    def size(self) -> int:
        """Return the number of elements in the stack."""
        return len(self._items)

    def get_items(self) -> List[str]:
        """Return a copy of the internal items (bottom to top)."""
        return list(self._items)

    def clear(self) -> None:
        """Reset the stack."""
        self._items.clear()
        self.operation_count = 0

    def __repr__(self) -> str:
        return f"Stack(bottom->top={self._items})"


class Queue:
    """
    Custom Queue Implementation following FIFO (First-In, First-Out) principle.
    """
    def __init__(self):
        self._items: List[str] = []
        self.operation_count: int = 0

    def enqueue(self, item: str) -> None:
        """Insert an element at the rear of the queue. (Step cost: 1)"""
        self._items.append(item)
        self.operation_count += 1

    def dequeue(self) -> str:
        """Remove and return the element from the front of the queue. (Step cost: 1)"""
        if self.is_empty():
            raise IndexError("dequeue from empty queue")
        self.operation_count += 1
        return self._items.pop(0)

    def peek(self) -> Optional[str]:
        """Return the element at the front without removing it. (Step cost: 1)"""
        if self.is_empty():
            return None
        self.operation_count += 1
        return self._items[0]

    def is_empty(self) -> bool:
        """Check if the queue is empty. (Step cost: 1)"""
        self.operation_count += 1
        return len(self._items) == 0

    def size(self) -> int:
        """Return the number of elements in the queue."""
        return len(self._items)

    def get_items(self) -> List[str]:
        """Return a copy of the internal items (front to rear)."""
        return list(self._items)

    def clear(self) -> None:
        """Reset the queue."""
        self._items.clear()
        self.operation_count = 0

    def __repr__(self) -> str:
        return f"Queue(front->rear={self._items})"


class StepEvent:
    """
    Encapsulates a single step event during the algorithm execution for visualization and tracing.
    """
    def __init__(
        self,
        step_number: int,
        phase: str,
        action: str,
        char: Optional[str] = None,
        stack_char: Optional[str] = None,
        queue_char: Optional[str] = None,
        is_match: Optional[bool] = None,
        stack_state: Optional[List[str]] = None,
        queue_state: Optional[List[str]] = None,
        description: str = "",
        total_steps_so_far: int = 0
    ):
        self.step_number = step_number
        self.phase = phase  # "PREPROCESS", "INSERT", "COMPARE", "COMPLETE"
        self.action = action
        self.char = char
        self.stack_char = stack_char
        self.queue_char = queue_char
        self.is_match = is_match
        self.stack_state = stack_state or []
        self.queue_state = queue_state or []
        self.description = description
        self.total_steps_so_far = total_steps_so_far

    def to_dict(self) -> Dict[str, Any]:
        return {
            "step_number": self.step_number,
            "phase": self.phase,
            "action": self.action,
            "char": self.char,
            "stack_char": self.stack_char,
            "queue_char": self.queue_char,
            "is_match": self.is_match,
            "stack_state": self.stack_state,
            "queue_state": self.queue_state,
            "description": self.description,
            "total_steps_so_far": self.total_steps_so_far,
        }


class PalindromeResult:
    """
    Stores comprehensive result of a palindrome evaluation including complexities and step count.
    """
    def __init__(
        self,
        original_text: str,
        cleaned_text: str,
        is_palindrome: bool,
        steps: List[StepEvent],
        total_step_count: int,
        comparisons_made: int,
        mismatch_index: Optional[int] = None,
        mismatch_details: Optional[str] = None,
        time_complexity: str = "O(N)",
        space_complexity: str = "O(N)",
        metrics: Optional[Dict[str, Any]] = None
    ):
        self.original_text = original_text
        self.cleaned_text = cleaned_text
        self.is_palindrome = is_palindrome
        self.steps = steps
        self.total_step_count = total_step_count
        self.comparisons_made = comparisons_made
        self.mismatch_index = mismatch_index
        self.mismatch_details = mismatch_details
        self.time_complexity = time_complexity
        self.space_complexity = space_complexity
        self.metrics = metrics or {}


class PalindromeChecker:
    """
    Palindrome Checker using Stack (LIFO) and Queue (FIFO).
    """
    def __init__(self, ignore_case: bool = True, ignore_spaces_and_punct: bool = True):
        self.ignore_case = ignore_case
        self.ignore_spaces_and_punct = ignore_spaces_and_punct
        self.stack = Stack()
        self.queue = Queue()

    def clean_text(self, text: str) -> Tuple[str, int]:
        """
        Preprocesses input text according to configuration.
        Returns:
            Tuple of (cleaned_text, step_count)
        """
        steps = 0
        cleaned_chars = []
        for ch in text:
            steps += 1  # iteration check
            if self.ignore_spaces_and_punct:
                steps += 1  # punctuation check
                if ch in string.whitespace or ch in string.punctuation:
                    continue
            if self.ignore_case:
                steps += 1  # lowercasing step
                cleaned_chars.append(ch.lower())
            else:
                cleaned_chars.append(ch)
            steps += 1  # append step

        return "".join(cleaned_chars), steps

    def check(self, text: str) -> PalindromeResult:
        """
        Full evaluation of text for palindrome property with complete step-by-step trace.
        """
        self.stack.clear()
        self.queue.clear()
        trace: List[StepEvent] = []
        step_counter = 0

        # Phase 1: Preprocessing
        step_counter += 1
        cleaned_text, preprocess_steps = self.clean_text(text)
        step_counter += preprocess_steps

        trace.append(StepEvent(
            step_number=len(trace) + 1,
            phase="PREPROCESS",
            action="CLEAN_TEXT",
            description=f"Preprocessed input: '{text}' -> '{cleaned_text}' (len={len(cleaned_text)})",
            total_steps_so_far=step_counter
        ))

        # Handle empty string edge case
        if len(cleaned_text) == 0:
            step_counter += 1
            trace.append(StepEvent(
                step_number=len(trace) + 1,
                phase="COMPLETE",
                action="FINISH",
                description="Empty string after preprocessing is vacuously considered a palindrome.",
                total_steps_so_far=step_counter
            ))
            return PalindromeResult(
                original_text=text,
                cleaned_text=cleaned_text,
                is_palindrome=True,
                steps=trace,
                total_step_count=step_counter,
                comparisons_made=0,
                metrics={"N": len(text), "M": 0, "preprocess_steps": preprocess_steps}
            )

        # Phase 2: Populate Stack (push) and Queue (enqueue)
        # For each character:
        # 1 step (push onto Stack) + 1 step (enqueue into Queue)
        for idx, ch in enumerate(cleaned_text):
            self.stack.push(ch)
            self.queue.enqueue(ch)
            step_counter += 2

            trace.append(StepEvent(
                step_number=len(trace) + 1,
                phase="INSERT",
                action=f"PUSH_AND_ENQUEUE",
                char=ch,
                stack_state=self.stack.get_items(),
                queue_state=self.queue.get_items(),
                description=f"Index {idx}: Pushed '{ch}' to Stack & Enqueued '{ch}' to Queue",
                total_steps_so_far=step_counter
            ))

        # Phase 3: Character Comparison (Pop from Stack vs Dequeue from Queue)
        # Stack.pop() returns characters in REVERSE order (LIFO)
        # Queue.dequeue() returns characters in ORIGINAL order (FIFO)
        comparisons_made = 0
        is_palindrome = True
        mismatch_index: Optional[int] = None
        mismatch_details: Optional[str] = None

        comp_idx = 0
        while not self.stack.is_empty() and not self.queue.is_empty():
            step_counter += 2  # isEmpty checks
            stack_char = self.stack.pop()
            queue_char = self.queue.dequeue()
            step_counter += 2  # pop & dequeue operations
            comparisons_made += 1
            step_counter += 1  # comparison operation

            matched = (stack_char == queue_char)

            trace.append(StepEvent(
                step_number=len(trace) + 1,
                phase="COMPARE",
                action="COMPARE_CHARS",
                stack_char=stack_char,
                queue_char=queue_char,
                is_match=matched,
                stack_state=self.stack.get_items(),
                queue_state=self.queue.get_items(),
                description=(
                    f"Comp #{comparisons_made}: Stack Top '{stack_char}' vs Queue Front '{queue_char}' "
                    f"-> {'MATCH' if matched else 'MISMATCH'}"
                ),
                total_steps_so_far=step_counter
            ))

            if not matched:
                is_palindrome = False
                mismatch_index = comp_idx
                mismatch_details = (
                    f"Mismatch at comparison #{comparisons_made}: "
                    f"Stack (reverse) had '{stack_char}' while Queue (forward) had '{queue_char}'."
                )
                break

            comp_idx += 1

        # Phase 4: Final Verification
        step_counter += 1
        trace.append(StepEvent(
            step_number=len(trace) + 1,
            phase="COMPLETE",
            action="VERDICT",
            is_match=is_palindrome,
            description=(
                f"Result: The string '{text}' is "
                f"{'a valid PALINDROME' if is_palindrome else 'NOT a palindrome'}."
            ),
            total_steps_so_far=step_counter
        ))

        # Metrics collection
        N = len(text)
        M = len(cleaned_text)
        metrics = {
            "input_length": N,
            "cleaned_length": M,
            "preprocess_steps": preprocess_steps,
            "insertion_steps": 2 * M,
            "comparison_steps": comparisons_made * 5,  # pop(1) + deq(1) + is_empty(2) + comp(1)
            "comparisons_made": comparisons_made,
            "stack_ops": self.stack.operation_count,
            "queue_ops": self.queue.operation_count,
        }

        return PalindromeResult(
            original_text=text,
            cleaned_text=cleaned_text,
            is_palindrome=is_palindrome,
            steps=trace,
            total_step_count=step_counter,
            comparisons_made=comparisons_made,
            mismatch_index=mismatch_index,
            mismatch_details=mismatch_details,
            time_complexity="O(N)",
            space_complexity="O(N)",
            metrics=metrics
        )
