"""
Unit Tests for Palindrome Checker Core Module
Tests Stack, Queue, PalindromeChecker, and step count metrics.
"""

import unittest
from palindrome_core import Stack, Queue, PalindromeChecker


class TestDataStructures(unittest.TestCase):
    def test_stack_lifo_order(self):
        s = Stack()
        self.assertTrue(s.is_empty())
        self.assertEqual(s.size(), 0)

        s.push("a")
        s.push("b")
        s.push("c")
        self.assertEqual(s.size(), 3)
        self.assertEqual(s.peek(), "c")

        # LIFO: last in ('c'), first out
        self.assertEqual(s.pop(), "c")
        self.assertEqual(s.pop(), "b")
        self.assertEqual(s.pop(), "a")
        self.assertTrue(s.is_empty())

    def test_queue_fifo_order(self):
        q = Queue()
        self.assertTrue(q.is_empty())
        self.assertEqual(q.size(), 0)

        q.enqueue("a")
        q.enqueue("b")
        q.enqueue("c")
        self.assertEqual(q.size(), 3)
        self.assertEqual(q.peek(), "a")

        # FIFO: first in ('a'), first out
        self.assertEqual(q.dequeue(), "a")
        self.assertEqual(q.dequeue(), "b")
        self.assertEqual(q.dequeue(), "c")
        self.assertTrue(q.is_empty())


class TestPalindromeChecker(unittest.TestCase):
    def setUp(self):
        self.checker = PalindromeChecker(ignore_case=True, ignore_spaces_and_punct=True)
        self.strict_checker = PalindromeChecker(ignore_case=False, ignore_spaces_and_punct=False)

    def test_simple_palindromes(self):
        test_cases = ["radar", "level", "racecar", "madam", "refer", "12321", "noon"]
        for word in test_cases:
            res = self.checker.check(word)
            self.assertTrue(res.is_palindrome, f"Expected '{word}' to be a palindrome.")
            self.assertEqual(res.comparisons_made, len(word))

    def test_simple_non_palindromes(self):
        test_cases = ["hello", "world", "python", "computer", "data", "structures"]
        for word in test_cases:
            res = self.checker.check(word)
            self.assertFalse(res.is_palindrome, f"Expected '{word}' not to be a palindrome.")

    def test_complex_phrases(self):
        phrases = [
            "A man, a plan, a canal: Panama!",
            "Was it a car or a cat I saw?",
            "No 'x' in Nixon",
            "Eva, can I see bees in a cave?",
            "Step on no pets",
            "Able was I ere I saw Elba"
        ]
        for phrase in phrases:
            res = self.checker.check(phrase)
            self.assertTrue(res.is_palindrome, f"Phrase failed: {phrase}")

    def test_strict_mode(self):
        # In strict mode, 'Madam' != 'madam' because 'M' != 'm'
        res = self.strict_checker.check("Madam")
        self.assertFalse(res.is_palindrome)

        # In strict mode, 'racecar' is still palindrome
        res2 = self.strict_checker.check("racecar")
        self.assertTrue(res2.is_palindrome)

    def test_single_char_and_empty(self):
        res_empty = self.checker.check("")
        self.assertTrue(res_empty.is_palindrome)

        res_single = self.checker.check("a")
        self.assertTrue(res_single.is_palindrome)

    def test_step_count_and_trace(self):
        res = self.checker.check("racecar")
        self.assertGreater(res.total_step_count, 0)
        self.assertEqual(len(res.steps), 1 + 7 + 7 + 1)  # Preprocess + 7 Inserts + 7 Comparisons + 1 Verdict
        self.assertEqual(res.steps[0].phase, "PREPROCESS")
        self.assertEqual(res.steps[-1].phase, "COMPLETE")


if __name__ == "__main__":
    unittest.main()
