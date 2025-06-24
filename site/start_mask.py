import requests
import sys
from cloudflare import Cloudflare
subdomain, target_url, api_token = sys.argv[1:]

zone_id = 'd17384fb34313df49f5878f4e8faddb8'
headers = {
    'Authorization': f'Bearer {api_token}',
    'Content-Type': 'application/json'
}

data = {
    'type': 'CNAME',
    'name': subdomain,  # ex: site.vendas
    'content': target_url,
    'ttl': 120,
    'proxied': False
}

url = f'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records'

resp = requests.post(url, headers=headers, json=data)

try:
    print(resp.json())
except requests.exceptions.JSONDecodeError:
    print("Resposta inesperada do servidor:")
    print(resp.text)

def main(subdomain, target_url, api_token, zone_id):
    cf = Cloudflare(token=api_token)
    full_name = subdomain  # ex: site.vendas.portifolio...
    data = {
        'type': 'CNAME',
        'name': full_name,
        'content': target_url.replace('https://', '').replace('http://', ''),
        'ttl': 120,
        'proxied': False
    }
    try:
        resp = cf.zones.dns_records.post(zone_id, data=data)
        print("✅ Máscara aplicada:", resp['result']['name'], "→", resp['result']['content'])
    except Exception as e:
        print("❌ Erro na criação da máscara:", e)

if __name__ == "__main__":
    sub, tgt, token, zone = sys.argv[1:]
    main(sub, tgt, token, zone)