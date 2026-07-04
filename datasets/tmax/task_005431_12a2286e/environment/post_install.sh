apt-get update && apt-get install -y python3 python3-pip gcc redis-server nginx bubblewrap
pip3 install pytest flask redis gunicorn

mkdir -p /app /home/user

# Create the oracle binary
cat << 'EOF' > /app/oracle_decoder.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main() {
    char hex[4097];
    if (!fgets(hex, sizeof(hex), stdin)) return 1;
    hex[strcspn(hex, "\n")] = 0;

    size_t len = strlen(hex);
    if (len % 2 != 0) return 1;

    char decoded[2049];
    for(size_t i = 0; i < len; i+=2) {
        char byte_str[3] = {hex[i], hex[i+1], 0};
        decoded[i/2] = (char)strtol(byte_str, NULL, 16) ^ 0x5A;
    }
    decoded[len/2] = '\0';

    if (strstr(decoded, "MALICIOUS_DROP") != NULL) {
        fprintf(stderr, "POLICY_VIOLATION\n");
        return 42;
    }
    printf("%s", decoded);
    return 0;
}
EOF
gcc /app/oracle_decoder.c -o /app/oracle_decoder

# Stub flask app
cat << 'EOF' > /home/user/flask_app.py
from flask import Flask, request
import subprocess
import redis

app = Flask(__name__)
# Agent needs to complete this
EOF

# Stub nginx
cat << 'EOF' > /home/user/nginx.conf
events {}
http {
    server {
        listen 8080;
        # Agent needs to proxy_pass to http://127.0.0.1:5000;
    }
}
EOF

# Start script
cat << 'EOF' > /app/start_services.sh
#!/bin/bash
redis-server --requirepass SecureRedis99! --daemonize yes
nginx -c /home/user/nginx.conf
python3 -m gunicorn -b 127.0.0.1:5000 flask_app:app --daemon
EOF
chmod +x /app/start_services.sh

useradd -m -s /bin/bash user || true
chmod -R 777 /home/user