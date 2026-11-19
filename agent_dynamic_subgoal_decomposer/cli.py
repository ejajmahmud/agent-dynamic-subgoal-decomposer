"""CLI for Subgoal Decomposer."""
import argparse
from .core import SubgoalDecomposer, Subgoal

def main():
    parser = argparse.ArgumentParser(description="Agent Dynamic Subgoal Decomposer CLI")
    parser.add_argument("--demo", action="store_true", help="Run decomposer demo")
    args = parser.parse_args()

    sd = SubgoalDecomposer()
    sd.add_subgoal(Subgoal("step1", "Init environment", lambda s: {"env": "ready"}))
    sd.add_subgoal(Subgoal("step2", "Load data", lambda s: {"data": [1, 2, 3]}))
    final = sd.execute({})
    print(f"Decomposition execution complete. Final state: {final}")

if __name__ == "__main__":
    main()
