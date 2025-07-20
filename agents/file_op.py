# agents/file_op.py
import sys
import os
import json

def main(params_json=None):
    params = {}
    if params_json:
        params = json.loads(params_json)
    path = params.get('path', os.getcwd())
    files = os.listdir(path)
    print(json.dumps(files))

if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else None)