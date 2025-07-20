import os
import json
import uuid

# Cada autômato tem sua pasta em /automata
BASE_DIR = os.path.dirname(__file__)
AUTOMATA_ROOT = os.path.abspath(os.path.join(BASE_DIR, '..', 'automata'))

class AutomatonManager:
    def __init__(self):
        self.configs = {}  # automatonId -> config

    def load_all(self):
        os.makedirs(AUTOMATA_ROOT, exist_ok=True)
        for module in os.listdir(AUTOMATA_ROOT):
            module_dir = os.path.join(AUTOMATA_ROOT, module)
            config_path = os.path.join(module_dir, 'config.json')
            if os.path.isdir(module_dir) and os.path.isfile(config_path):
                with open(config_path) as f:
                    config = json.load(f)
                    config['module_dir'] = module_dir
                    self.configs[config['automatonId']] = config

    def list_configs(self):
        return list(self.configs.values())

    def register(self, config: dict) -> str:
        automaton_id = config.get('automatonId') or str(uuid.uuid4())
        config['automatonId'] = automaton_id
        module_dir = os.path.join(AUTOMATA_ROOT, config['name'])
        os.makedirs(module_dir, exist_ok=True)
        config_path = os.path.join(module_dir, 'config.json')
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        config['module_dir'] = module_dir
        self.configs[automaton_id] = config
        return automaton_id

    def unregister(self, automaton_id: str):
        config = self.configs.pop(automaton_id, None)
        if not config:
            raise KeyError
        module_dir = config.get('module_dir')
        if module_dir and os.path.isdir(module_dir):
            import shutil; shutil.rmtree(module_dir)

    def get_config(self, automaton_id: str) -> dict:
        config = self.configs.get(automaton_id)
        if not config:
            raise KeyError('Automaton not found')
        return config