import os
import sys
import json
import subprocess
import time

def main(params_json=None):
    params = json.loads(params_json) if params_json else {}
    compose_path = params['compose_path']
    ngrok_token = params['ngrok_token']
    mask_domain = params['mask_domain']

    logs = []
    # 1. Iniciar Docker Compose
    logs.append(f"[Docker] Iniciando serviços em {compose_path}")
    result = subprocess.run(['docker-compose', 'up', '-d'], cwd=compose_path,
                            capture_output=True, text=True)
    logs.append(result.stdout or result.stderr)

    # 2. Login no ngrok
    logs.append("[ngrok] Autenticando token")
    subprocess.run(['ngrok', 'authtoken', ngrok_token], capture_output=True)

    # 3. Iniciar túnel HTTP no backend (porta padrão 8000)
    logs.append("[ngrok] Iniciando túnel HTTP na porta 8000")
    ngrok_proc = subprocess.Popen(['ngrok', 'http', '8000'],
                                  stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    # 4. Aguardar e capturar URL pública
    public_url = None
    start_time = time.time()
    while time.time() - start_time < 10:
        line = ngrok_proc.stdout.readline()
        logs.append(line.strip())
        if 'url=' in line:
            # exemplo: "tunnel session ... url=http://abc.ngrok.io"
            parts = line.split('url=')
            public_url = parts[-1].split()[0]
            break
    if not public_url:
        logs.append("[ngrok] Falha ao obter URL pública")
    else:
        logs.append(f"[ngrok] URL pública: {public_url}")

    # 5. Aplicar máscara (script placeholder)
    logs.append(f"[Mask] Aplicando máscara para {mask_domain} apontando para {public_url}")
    # TODO: implementar API de DNS ou redirecionamento

    # Imprimir logs no stdout
    print(json.dumps(logs))

if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else None)