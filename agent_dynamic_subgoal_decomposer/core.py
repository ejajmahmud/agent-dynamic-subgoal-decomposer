"""Core Dynamic Subgoal Decomposer with Checkpoint Rollbacks."""
from typing import Dict, List, Optional, Any, Callable
import copy

class Subgoal:
    def __init__(self, goal_id: str, description: str, action: Callable[[Dict[str, Any]], Dict[str, Any]]):
        self.goal_id = goal_id
        self.description = description
        self.action = action
        self.status = "pending"

class Checkpoint:
    def __init__(self, step_idx: int, state: Dict[str, Any]):
        self.step_idx = step_idx
        self.state = copy.deepcopy(state)

class SubgoalDecomposer:
    def __init__(self):
        self.subgoals: List[Subgoal] = []
        self.checkpoints: List[Checkpoint] = []
        self.current_state: Dict[str, Any] = {}

    def add_subgoal(self, subgoal: Subgoal):
        self.subgoals.append(subgoal)

    def execute(self, initial_state: Dict[str, Any]) -> Dict[str, Any]:
        self.current_state = copy.deepcopy(initial_state)
        idx = 0
        while idx < len(self.subgoals):
            sg = self.subgoals[idx]
            # Save checkpoint before execution
            self.checkpoints.append(Checkpoint(idx, self.current_state))
            try:
                result = sg.action(self.current_state)
                self.current_state.update(result)
                sg.status = "completed"
                idx += 1
            except Exception as e:
                sg.status = "failed"
                # Rollback to prior checkpoint
                if self.checkpoints:
                    last_cp = self.checkpoints.pop()
                    self.current_state = last_cp.state
                raise RuntimeError(f"Subgoal {sg.goal_id} failed: {e}. State rolled back.")
        return self.current_state
