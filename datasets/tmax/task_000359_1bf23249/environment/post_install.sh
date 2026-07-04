apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest

    # Create the user
    useradd -m -s /bin/bash user || true

    # Create the application directory
    mkdir -p /home/user/app

    # Create the vulnerable authentication backend
    cat << 'EOF' > /home/user/app/auth_backend.py
import base64
import json

SECRET_DATA = "COMPLIANCE_FLAG_{7h3_4ud17_15_c0mpl373}"

def authenticate(username, password):
    """Authenticates a user and returns a token."""
    if username == "guest" and password == "guest":
        token_data = {"user": username, "role": "user"}
        return base64.b64encode(json.dumps(token_data).encode()).decode()
    return None

def get_admin_data(token):
    """Returns sensitive data if the token belongs to an admin."""
    try:
        decoded = json.loads(base64.b64decode(token).decode())
    except Exception:
        return "Invalid token"

    if decoded.get("role") == "admin":
        return SECRET_DATA
    else:
        return "Access Denied: Admin role required."
EOF

    # Set permissions
    chmod -R 777 /home/user