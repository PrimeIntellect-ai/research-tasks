apt-get update && apt-get install -y python3 python3-pip espeak
    pip3 install pytest

    mkdir -p /app

    cat << 'EOF' > /app/legacy_router_oracle
#!/usr/bin/env python3
import sys
import json
import urllib.parse

def route(url_str):
    parsed = urllib.parse.urlparse(url_str)
    path = parsed.path
    params = urllib.parse.parse_qsl(parsed.query, keep_blank_values=True)
    param_dict = {k: v for k, v in params}

    if path.endswith(".php"):
        return {"path": path, "params": {}, "status": 403}

    if path.startswith("/secure"):
        try:
            token = int(param_dict.get("token", ""))
            if token % 17 == 3:
                return {"path": path, "params": param_dict, "status": 200}
            else:
                return {"path": path, "params": param_dict, "status": 403}
        except ValueError:
            return {"path": path, "params": param_dict, "status": 403}

    return {"path": path, "params": param_dict, "status": 200}

if __name__ == "__main__":
    input_url = sys.argv[1] if len(sys.argv) > 1 else ""
    print(json.dumps(route(input_url)))
EOF
    chmod +x /app/legacy_router_oracle

    espeak -w /app/dev_notes.wav "Hey, just a quick note on the router migration. For security reasons, if the path starts with /secure, the 'token' parameter must be an integer where token modulo 17 equals 3. If the token is missing or fails this constraint, the status should be 403. Also, any path ending in .php should immediately return status 403 and empty parameters. Everything else defaults to status 200."

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user