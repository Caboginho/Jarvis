import sys, os, json

def main(params_json=None):
    params = json.loads(params_json) if params_json else {}
    path = params.get('path', os.getcwd())
    files = os.listdir(path)
    print(json.dumps(files))

if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else None)