# core/router.py
from manager import AutomatonManager
from executor import SandboxExecutor

class CommandRouter:
    def __init__(self, manager: AutomatonManager):
        self.manager = manager
        self.executor = SandboxExecutor()

    def route_run(self, payload: dict) -> str:
        automaton_id = payload.get('automatonId')
        if automaton_id is None:
            raise ValueError("automatonId is required in payload")
        params = payload.get('params', {})
        config = self.manager.get_config(automaton_id)
        return self.executor.execute(automaton_id, config, params)

    def route_status(self, task_id: str):
        return self.executor.get_status(task_id)
    