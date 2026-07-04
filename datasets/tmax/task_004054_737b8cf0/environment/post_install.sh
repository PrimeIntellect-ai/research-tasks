apt-get update && apt-get install -y python3 python3-pip nginx gcc binutils
pip3 install pytest flask

mkdir -p /app/nginx
mkdir -p /app/flask

# Dummy flask app
cat << 'EOF' > /app/flask/app.py
from flask import Flask, request
app = Flask(__name__)
@app.route('/')
def hello():
    return "OK"
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
EOF

# Nginx config
cat << 'EOF' > /app/nginx/nginx.conf
events {}
http {
    server {
        listen 8080;
        location / {
            proxy_pass http://127.0.0.1:5000;
        }
    }
}
EOF

cat << 'EOF' > /app/start.sh
#!/bin/bash
python3 /app/flask/app.py &
nginx -c /app/nginx/nginx.conf &
EOF
chmod +x /app/start.sh

# Create the malicious ELF with the custom section
cat << 'EOF' > /tmp/exfiltrator.c
#include <stdio.h>
__attribute__((section(".tgt_cookie")))
const char secret_cookie[] = "X-Auth-Exfil-Token";
int main() { return 0; }
EOF
gcc /tmp/exfiltrator.c -o /app/exfiltrator_bin
strip /app/exfiltrator_bin

# Compile the Oracle
cat << 'EOF' > /tmp/oracle.c
#include <stdio.h>
#include <string.h>

void process_line(char *line) {
    if (strncmp(line, "Cookie: ", 8) == 0 || strncmp(line, "Set-Cookie: ", 12) == 0) {
        char *target = "X-Auth-Exfil-Token=";
        char *ptr = strstr(line, target);
        if (ptr) {
            char prefix[4096];
            int prefix_len = ptr - line + strlen(target);
            strncpy(prefix, line, prefix_len);
            prefix[prefix_len] = '\0';

            char *rest = ptr + strlen(target);
            char *end1 = strchr(rest, ';');
            char *end2 = strchr(rest, '\r');
            char *end3 = strchr(rest, '\n');

            char *end = NULL;
            if (end1) end = end1;
            if (end2 && (!end || end2 < end)) end = end2;
            if (end3 && (!end || end3 < end)) end = end3;

            if (!end) end = rest + strlen(rest);

            printf("%sREDACTED%s", prefix, end);
            return;
        }
    }
    printf("%s", line);
}

int main() {
    char buffer[4096];
    while (fgets(buffer, sizeof(buffer), stdin)) {
        process_line(buffer);
    }
    return 0;
}
EOF
gcc /tmp/oracle.c -o /app/oracle_redactor

useradd -m -s /bin/bash user || true
chmod -R 777 /home/user