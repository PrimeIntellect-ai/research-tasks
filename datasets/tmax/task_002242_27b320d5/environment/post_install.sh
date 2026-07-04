apt-get update && apt-get install -y python3 python3-pip nginx gcc make curl
    pip3 install pytest aiosmtpd

    useradd -m -s /bin/bash user || true

    mkdir -p /home/user/nginx /home/user/restore_out /home/user/src /home/user/data /home/user/bin
    mkdir -p /home/user/nginx/client_body /home/user/nginx/fastcgi_temp /home/user/nginx/proxy_temp /home/user/nginx/scgi_temp /home/user/nginx/uwsgi_temp

    cat << 'EOF' > /home/user/nginx/nginx.conf
pid /home/user/nginx/nginx.pid;
events {}
http {
    access_log /home/user/nginx/access.log;
    error_log /home/user/nginx/error.log;
    client_body_temp_path /home/user/nginx/client_body;
    fastcgi_temp_path /home/user/nginx/fastcgi_temp;
    proxy_temp_path /home/user/nginx/proxy_temp;
    scgi_temp_path /home/user/nginx/scgi_temp;
    uwsgi_temp_path /home/user/nginx/uwsgi_temp;
    server {
        listen 8080;
        location / {
            root /home/user/restore_out;
        }
    }
}
EOF

    cat << 'EOF' > /home/user/src/restore_tool.c
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {
    // TODO: Implement fast restore tool and email notification
    return 0;
}
EOF

    cat << 'EOF' > /tmp/gen_backup.py
import os, struct, random
with open('/home/user/data/backup.dat', 'wb') as f:
    written = 0
    target = 50 * 1024 * 1024
    while written < target:
        chunk = random.randint(1024, 65536)
        if written + chunk > target:
            chunk = target - written
        f.write(struct.pack('<I', chunk))
        f.write(os.urandom(chunk))
        written += chunk
EOF
    python3 /tmp/gen_backup.py
    rm /tmp/gen_backup.py

    chown -R user:user /home/user
    chmod -R 777 /home/user