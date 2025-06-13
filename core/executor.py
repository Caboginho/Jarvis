import subprocess
import threading
import uuid
import os
import json

STATUS = {}

class SandboxExecutor:
    def __init__(self):
        from core.manager import AUTOMATA_ROOT
        self.automata_root = AUTOMATA_ROOT

    def execute(self, automaton_id, config, params) -> str:
        task_id = str(uuid.uuid4())
        STATUS[task_id] = {'status': 'queued', 'logs': []}
        threading.Thread(target=self._run, args=(task_id, config, params), daemon=True).start()
        return task_id

    def _run(self, task_id, config, params):
        STATUS[task_id]['status'] = 'running'
        lang = config.get('language')
        module_dir = config['module_dir']
        entrypoint = config['entrypoint']
        script_path = os.path.join(module_dir, entrypoint.split('.')[0] + '.py')

        if lang == 'python':
            cmd = ['python', script_path, json.dumps(params)]
        elif lang == 'shell':
            cmd = ['bash', os.path.join(module_dir, entrypoint)] + [str(v) for v in params.values()]
        else:
            STATUS[task_id] = {'status': 'failed', 'logs': [f'Language {lang} not supported']}
            return

        try:
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            for line in proc.stdout:
                STATUS[task_id]['logs'].append(line.strip())
            proc.wait()
            STATUS[task_id]['status'] = 'completed' if proc.returncode == 0 else 'failed'
        except Exception as e:
            STATUS[task_id]['status'] = 'failed'
            STATUS[task_id]['logs'].append(str(e))

    def get_status(self, task_id: str):
        return STATUS.get(task_id)