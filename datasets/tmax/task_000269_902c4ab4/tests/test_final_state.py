from flask import Flask, request, Response
import re
import hashlib
import requests

app = Flask(__name__)

# Defensive configuration
SHARED_SECRET = "secure_internal_api_key_2024"
EXPECTED_HASH = hashlib.sha256(SHARED_SECRET.encode()).hexdigest()
BACKEND_URL = "http://127.0.0.1:5000"

# Basic WAF signatures (Conceptual)
MALICIOUS_PATTERNS = [
    re.compile(r"<script.*?>", re.IGNORECASE),
    re.compile(r"UNION\s+SELECT", re.IGNORECASE),
    re.compile(r"OR\s+1=1", re.IGNORECASE)
]

# DLP Redaction pattern
CREDIT_CARD_PATTERN = re.compile(r"\b\d{4}-\d{4}-\d{4}-\d{4}\b")

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods=['GET', 'POST'])
def proxy(path):
    # 1. Authentication Check
    auth_header = request.headers.get('X-Auth-Hash')
    if not auth_header or auth_header != EXPECTED_HASH:
        return Response("Unauthorized", status=401)

    # 2. WAF Payload Filtering
    query_param = request.args.get('q', '')
    for pattern in MALICIOUS_PATTERNS:
        if pattern.search(query_param):
            # Log the blocked attempt here in a real system
            return Response("Forbidden: Malicious payload detected", status=403)

    # Forward the request to the internal backend
    try:
        resp = requests.request(
            method=request.method,
            url=f"{BACKEND_URL}/{path}",
            headers={key: value for (key, value) in request.headers if key != 'Host'},
            data=request.get_data(),
            cookies=request.cookies,
            allow_redirects=False,
            params=request.args
        )
    except requests.exceptions.RequestException:
        return Response("Bad Gateway", status=502)

    # 3. DLP Data Redaction
    response_body = resp.text
    if CREDIT_CARD_PATTERN.search(response_body):
        response_body = CREDIT_CARD_PATTERN.sub("[REDACTED]", response_body)

    headers = [(name, value) for (name, value) in resp.raw.headers.items()]

    return Response(response_body, status=resp.status_code, headers=headers)

if __name__ == '__main__':
    app.run(port=8080)