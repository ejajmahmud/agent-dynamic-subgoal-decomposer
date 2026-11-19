"""Tests for Subgoal Decomposer."""
import unittest
from agent_dynamic_subgoal_decomposer.core import SubgoalDecomposer, Subgoal

class TestSubgoalDecomposer(unittest.TestCase):
    def test_successful_execution(self):
        sd = SubgoalDecomposer()
        sd.add_subgoal(Subgoal("1", "add a", lambda s: {"a": 1}))
        sd.add_subgoal(Subgoal("2", "add b", lambda s: {"b": s["a"] + 2}))
        res = sd.execute({})
        self.assertEqual(res, {"a": 1, "b": 3})

    def test_rollback_on_failure(self):
        sd = SubgoalDecomposer()
        sd.add_subgoal(Subgoal("1", "add a", lambda s: {"a": 10}))
        def failing_action(s):
            raise ValueError("Unexpected network error")
        sd.add_subgoal(Subgoal("2", "fail", failing_action))
        
        with self.assertRaises(RuntimeError):
            sd.execute({})
        # State should be rolled back to state before step 2
        self.assertEqual(sd.current_state, {"a": 10})
