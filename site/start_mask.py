import requests
import sys
# Parâmetros: subdomain, target_url, api_token
subdomain, target_url, api_token = sys.argv[1:]
# Exemplo DNS provider API
resp = requests.post('https://api.dnsprovider.com/v1/records', json={
    'type': 'CNAME', 'name': subdomain, 'content': target_url
}, headers={'Authorization': f'Bearer {api_token}'})
print(resp.json())