import sys
import subprocess
import json

def main(params_json=None):
    params = json.loads(params_json) if params_json else {}
    script = params.get('script')
    args = params.get('args', [])
    result = subprocess.run([script] + args, capture_output=True, text=True)
    print(result.stdout)

if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else None)