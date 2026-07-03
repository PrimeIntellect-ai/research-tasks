apt-get update && apt-get install -y python3 python3-pip curl
    pip3 install pytest

    mkdir -p /app /home/user

    cat << 'EOF' > /app/schema.json
{
  "type": "object",
  "properties": {
    "email": { "type": "string" }
  },
  "required": ["email"]
}
EOF

    cat << 'EOF' > /home/user/schema_update.patch
--- schema.json
+++ schema.json
@@ -2,7 +2,11 @@
   "type": "object",
   "properties": {
<<<<<<< HEAD
     "email": { "type": "string" }
=======
     "api_key": { "type": "string" }
>>>>>>> PR_branch
   },
   "required": ["email", "api_key"]
 }
EOF

    touch /home/user/redactor
    chmod +x /home/user/redactor

    cat << 'EOF' > /app/gateway.conf
REDACTOR_CMD="/bin/cat"
EOF

    cat << 'EOF' > /app/restart_gateway.sh
#!/bin/bash
echo "Restarting gateway..."
EOF
    chmod +x /app/restart_gateway.sh

    cat << 'EOF' > /app/oracle_redactor
#!/usr/bin/env python3
import sys
import re

def redact(line):
    return re.sub(r'(secret_token=)(?:\\ |[^\s])+', r'\1***', line)

if __name__ == '__main__':
    for line in sys.stdin:
        sys.stdout.write(redact(line))
EOF
    chmod +x /app/oracle_redactor

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user /app