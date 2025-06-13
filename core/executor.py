# core/executor.py
import subprocess
import threading
import uuid
import os
import json

STATUS = {}

class SandboxExecutor:
    def __init__(self, agents_dir=None):
        self.agents_dir = agents_dir or os.path.join(os.path.dirname(__file__), '..', 'agents')

    def execute(self, automaton_id, config, params) -> str:
        task_id = str(uuid.uuid4())
        STATUS[task_id] = {'status': 'queued', 'result': None}
        threading.Thread(target=self._run, args=(task_id, config, params), daemon=True).start()
        return task_id

    def _run(self, task_id, config, params):
        STATUS[task_id]['status'] = 'running'
        lang = config.get('language')
        path = os.path.join(self.agents_dir, config['path'])
        cmd = []
        if lang == 'python':
            cmd = ['python', path, json.dumps(params)]
        elif lang == 'shell':
            cmd = ['bash', path] + [str(v) for v in params.values()]
        else:
            STATUS[task_id] = {'status': 'failed', 'result': f'Language {lang} not supported'}
            return
        try:
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            STATUS[task_id] = {'status': 'completed', 'result': proc.stdout}
        except Exception as e:
            STATUS[task_id] = {'status': 'failed', 'result': str(e)}

    def get_status(self, task_id: str):
        return STATUS.get(task_id)