import os
import sys
import json
import subprocess
import time

def main(params_json=None):
    # 1. Carrega parâmetros
    params = json.loads(params_json) if params_json else {}
    compose_path = params['compose_path']
    ngrok_token = params['ngrok_token']
    mask_domain = params['mask_domain']
    api_token = params.get('api_token', '')

    logs = []

    # 2. Iniciar Docker Compose
    logs.append(f"[Docker] Iniciando serviços em {compose_path}")
    dc = subprocess.run(
        ["docker-compose", "up", "-d"],
        cwd=compose_path,
        capture_output=True, text=True
    )
    logs.append(dc.stdout or dc.stderr)

    # 3. Autenticar no ngrok
    logs.append("[ngrok] Autenticando token")
    ng_auth = subprocess.run(
        ["ngrok", "authtoken", ngrok_token],
        capture_output=True, text=True
    )
    logs.append(ng_auth.stdout or ng_auth.stderr)

    # 4. Iniciar túnel HTTP no backend (porta 8000)
    logs.append("[ngrok] Iniciando túnel HTTP na porta 8000")
    ng_proc = subprocess.Popen(
        ["ngrok", "http", "8000"],
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
    )

    # 5. Aguarda e captura URL pública
    public_url = None
    start_time = time.time()
    while time.time() - start_time < 15:
        line = ng_proc.stdout.readline()
        if not line:
            break
        logs.append(line.strip())
        if "url=" in line:
            # extrai algo como http://abc123.ngrok.io
            public_url = line.split("url=")[-1].split()[0]
            break

    if not public_url:
        logs.append("[ngrok] Falha ao obter URL pública")
    else:
        logs.append(f"[ngrok] URL pública: {public_url}")

        # 6. Aplicar máscara de domínio via start_mask.py
        logs.append(f"[Mask] Aplicando máscara {mask_domain} → {public_url}")
        script_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..", "site", "start_mask.py")
        )
        mask_cmd = ["python", script_path, mask_domain, public_url, api_token]
        mask_proc = subprocess.run(
            mask_cmd,
            cwd=os.path.dirname(script_path),
            capture_output=True, text=True
        )
        logs.append(mask_proc.stdout or mask_proc.stderr)
    # 6. Aplicar máscara via Cloudflare
    logs.append(f"[Mask] Aplicando máscara {mask_domain} → {public_url}")
    mask_cmd = [
        "python", script_path, mask_domain, public_url,
        params['cloudflare_token'], params['cloudflare_zone']
    ]
    mask_proc = subprocess.run(
        mask_cmd,
        cwd=os.path.dirname(script_path),
        capture_output=True, text=True
    )
    logs.append(mask_proc.stdout or mask_proc.stderr)
        # 7. Retorna todos os logs em JSON
    print(json.dumps(logs))

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)
