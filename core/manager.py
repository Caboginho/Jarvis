# core/manager.py
import os
import json
import uuid
from importlib import import_module

AGENTS_DIR = os.path.join(os.path.dirname(__file__), '..', 'agents')

class AutomatonManager:
    def __init__(self):
        self.configs = {}

    def load_all(self):
        os.makedirs(AGENTS_DIR, exist_ok=True)
        for fname in os.listdir(AGENTS_DIR):
            if fname.endswith('.json'):
                path = os.path.join(AGENTS_DIR, fname)
                with open(path) as f:
                    config = json.load(f)
                    self.configs[config['automatonId']] = config

    def list_configs(self):
        return list(self.configs.values())

    def register(self, config: dict) -> str:
        automaton_id = config.get('automatonId') or str(uuid.uuid4())
        config['automatonId'] = automaton_id
        os.makedirs(AGENTS_DIR, exist_ok=True)
        path = os.path.join(AGENTS_DIR, f"{automaton_id}.json")
        with open(path, 'w') as f:
            json.dump(config, f, indent=2)
        self.configs[automaton_id] = config
        return automaton_id

    def unregister(self, automaton_id: str):
        if automaton_id not in self.configs:
            raise KeyError
        path = os.path.join(AGENTS_DIR, f"{automaton_id}.json")
        os.remove(path)
        del self.configs[automaton_id]

    def get_config(self, automaton_id: str) -> dict:
        config = self.configs.get(automaton_id)
        if not config:
            raise KeyError("Automaton not found")
        return config