apt-get update && apt-get install -y python3 python3-pip curl openssl
    pip3 install pytest flask

    useradd -m -s /bin/bash user || true

    cat << 'EOF' > /home/user/app.py
from flask import Flask, request, render_template_string

app = Flask(__name__)

@app.after_request
def apply_csp(response):
    response.headers["Content-Security-Policy"] = "default-src 'none'; script-src 'self'; connect-src https://127.0.0.1:4443;"
    return response

@app.route('/view')
def view_log():
    # Vulnerable to XSS
    user_input = request.args.get('msg', '')
    template = f'''
    <html>
    <body>
      <h1>Log Entry</h1>
      <div id="content">{user_input}</div>
    </body>
    </html>
    '''
    return render_template_string(template)

@app.route('/api/status')
def status():
    # JSONP endpoint - Gadget for CSP bypass
    callback = request.args.get('callback')
    data = '{"status": "ok", "uptime": 3600}'
    if callback:
        return f"{callback}({data});", 200, {'Content-Type': 'application/javascript'}
    return data, 200, {'Content-Type': 'application/json'}

if __name__ == '__main__':
    app.run(port=8080)
EOF

    chmod -R 777 /home/user