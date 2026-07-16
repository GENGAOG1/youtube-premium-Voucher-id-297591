from flask import Flask, request
import os

app = Flask(__name__)

@app.before_request
def block_internal():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    if ip and ip.startswith(('127.', '10.', '172.16.', '192.168.', '34.82.')):  # Render-Bereich blocken
        if '/health' not in request.path:  # Falls du Health-Check hast
            return "OK", 200  # Silent für interne

# Dann deine normale Route
@app.route('/')
def log_ip():
    # Nur echte externe IPs loggen
    forwarded = request.headers.get('X-Forwarded-For')
    ip = forwarded.split(',')[0].strip() if forwarded else request.remote_addr
    
    # Filtere Render-IPs raus
    if ip.startswith(('34.82.', '127.')):
        return "URL NOT FOUND PLEASE VISIT: https://gengaog/github.io/-/", 200  # Kein Log für interne Requests
    
    # ... dein Payload hier mit dem gefilterten ip ...

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
