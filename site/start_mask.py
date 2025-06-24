
import sys
from cloudflare import Cloudflare  # import correto, conforme README da biblioteca :contentReference[oaicite:3]{index=3}

def main(subdomain, target_url, cf_token, zone_id):
    cf = Cloudflare(api_token=cf_token)  # autenticação usando API Token

    hostname = subdomain
    content = target_url.replace("https://", "")
    record = {
        "type": "CNAME",
        "name": hostname,
        "content": content,
        "ttl": 120,
        "proxied": False
    }

    try:
        resp = cf.zones.dns_records.post(zone_id, data=record)
        print(f"✅ Máscara criada: {resp['result']['name']} → {resp['result']['content']}")
    except Exception as e:
        print("❌ Erro ao criar máscara CNAME:", e)

if __name__ == "__main__":
    _, sub, tgt, token, zone = sys.argv
    main(sub, tgt, token, zone)
