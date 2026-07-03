apt-get update && apt-get install -y python3 python3-pip gcc netcat-openbsd curl systemd
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    # Create oracle parser
    mkdir -p /opt/oracle
    cat << 'EOF' > /opt/oracle/parser_oracle.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main() {
    char line[512];
    if (!fgets(line, sizeof(line), stdin)) return 0;

    char *newline = strchr(line, '\n');
    if (newline) *newline = '\0';

    char metric_name[256] = {0};
    float value = 0;
    char type[256] = {0};

    char *colon1 = strchr(line, ':');
    if (!colon1) goto invalid;

    char *pipe1 = strchr(colon1, '|');
    if (!pipe1) goto invalid;

    char *pipe2 = strchr(pipe1 + 1, '|');
    if (!pipe2) goto invalid;

    if (pipe2[1] != '#') goto invalid;

    strncpy(metric_name, line, colon1 - line);
    metric_name[colon1 - line] = '\0';
    if (strlen(metric_name) == 0) goto invalid;

    char value_str[256];
    strncpy(value_str, colon1 + 1, pipe1 - colon1 - 1);
    value_str[pipe1 - colon1 - 1] = '\0';
    if (sscanf(value_str, "%f", &value) != 1) goto invalid;

    strncpy(type, pipe1 + 1, pipe2 - pipe1 - 1);
    type[pipe2 - pipe1 - 1] = '\0';
    if (strlen(type) == 0) goto invalid;

    char tags_str[256];
    strcpy(tags_str, pipe2 + 2);
    if (strlen(tags_str) == 0) goto invalid;

    char tags_out[1024] = {0};
    char *token = strtok(tags_str, ",");
    while (token) {
        char *colon2 = strchr(token, ':');
        if (!colon2 || colon2 == token || strlen(colon2+1) == 0) goto invalid;
        *colon2 = '\0';
        strcat(tags_out, token);
        strcat(tags_out, "=");
        strcat(tags_out, colon2 + 1);
        strcat(tags_out, ";");
        token = strtok(NULL, ",");
    }

    printf("NAME=[%s] TYPE=[%s] VALUE=[%.4f] TAGS=[%s]\n", metric_name, type, value, tags_out);
    return 0;

invalid:
    printf("INVALID_METRIC\n");
    return 0;
}
EOF
    gcc -o /opt/oracle/parser_oracle /opt/oracle/parser_oracle.c
    rm /opt/oracle/parser_oracle.c

    # Create mock services
    mkdir -p /usr/local/bin
    cat << 'EOF' > /usr/local/bin/app_mock.sh
#!/bin/bash
while true; do
    echo "cpu_load:2.45|gauge|#host:server1,env:prod" | nc -u -w0 localhost 8125 || true
    sleep 5
done
EOF
    chmod +x /usr/local/bin/app_mock.sh

    cat << 'EOF' > /usr/local/bin/dashboard.py
from http.server import BaseHTTPRequestHandler, HTTPServer

latest_data = ""

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        global latest_data
        if self.path == '/ingest':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            latest_data = post_data.decode('utf-8').strip()
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK")
    def do_GET(self):
        if self.path == '/latest':
            self.send_response(200)
            self.end_headers()
            self.wfile.write(latest_data.encode('utf-8'))

if __name__ == '__main__':
    server = HTTPServer(('localhost', 9090), Handler)
    server.serve_forever()
EOF

    mkdir -p /home/user/.config/systemd/user

    cat << 'EOF' > /home/user/.config/systemd/user/app_mock.service
[Unit]
Description=App Mock Service

[Service]
ExecStart=/usr/local/bin/app_mock.sh
Restart=always

[Install]
WantedBy=default.target
EOF

    cat << 'EOF' > /home/user/.config/systemd/user/dashboard.service
[Unit]
Description=Dashboard Service

[Service]
ExecStart=/usr/bin/python3 /usr/local/bin/dashboard.py
Restart=always

[Install]
WantedBy=default.target
EOF

    chown -R user:user /home/user
    chmod -R 777 /home/user