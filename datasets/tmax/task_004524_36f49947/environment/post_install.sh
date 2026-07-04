apt-get update && apt-get install -y \
        python3 \
        python3-pip \
        redis-server \
        nginx \
        gcc \
        curl

    pip3 install pytest flask redis requests

    mkdir -p /app/services/nginx
    mkdir -p /app/services/redis
    mkdir -p /app/services/registry
    mkdir -p /app/bin

    cat << 'EOF' > /app/services/nginx/nginx.conf
worker_processes 1;
pid /var/run/nginx.pid;
events { worker_connections 1024; }
http {
    server {
        listen 80;
        location / {
            root /var/www/html;
        }
    }
}
EOF

    cat << 'EOF' > /app/services/redis/redis.conf
port 6379
EOF

    cat << 'EOF' > /app/services/registry/app.py
from flask import Flask
app = Flask(__name__)

@app.route('/health')
def health():
    return "OK"

if __name__ == '__main__':
    app.run(port=5000)
EOF

    cat << 'EOF' > /app/services/start_all.sh
#!/bin/bash
redis-server /app/services/redis/redis.conf &
nginx -c /app/services/nginx/nginx.conf &
python3 /app/services/registry/app.py &
EOF
    chmod +x /app/services/start_all.sh

    cat << 'EOF' > /tmp/oracle.c
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <unistd.h>

int main(int argc, char *argv[]) {
    if (argc != 3) return 1;
    FILE *fin = fopen(argv[1], "rb");
    if (!fin) return 1;

    char temp_template[1024];
    snprintf(temp_template, sizeof(temp_template), "%s.XXXXXX", argv[2]);
    int fd = mkstemp(temp_template);
    if (fd == -1) { fclose(fin); return 1; }
    FILE *fout = fdopen(fd, "wb");
    if (!fout) { close(fd); fclose(fin); return 1; }

    uint8_t magic[4];
    uint8_t type;
    uint32_t size;

    while (fread(magic, 1, 4, fin) == 4) {
        if (memcmp(magic, "ARTF", 4) != 0) {
            fclose(fin); fclose(fout); unlink(temp_template); return 1;
        }
        if (fread(&type, 1, 1, fin) != 1) {
            fclose(fin); fclose(fout); unlink(temp_template); return 1;
        }
        if (fread(&size, 4, 1, fin) != 1) {
            fclose(fin); fclose(fout); unlink(temp_template); return 1;
        }

        uint8_t *payload = malloc(size);
        if (size > 0 && fread(payload, 1, size, fin) != size) {
            free(payload); fclose(fin); fclose(fout); unlink(temp_template); return 1;
        }

        if (type != 0x02) {
            fwrite(magic, 1, 4, fout);
            fwrite(&type, 1, 1, fout);
            fwrite(&size, 4, 1, fout);
            if (size > 0) fwrite(payload, 1, size, fout);
        }
        free(payload);
    }

    fclose(fin);
    fclose(fout);
    if (rename(temp_template, argv[2]) != 0) {
        unlink(temp_template);
        return 1;
    }
    return 0;
}
EOF
    gcc /tmp/oracle.c -o /app/bin/filter_oracle
    chmod +x /app/bin/filter_oracle
    rm /tmp/oracle.c

    useradd -m -s /bin/bash user || true
    chmod -R 777 /app
    chmod -R 777 /home/user