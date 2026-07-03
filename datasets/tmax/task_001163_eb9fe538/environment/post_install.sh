apt-get update && apt-get install -y python3 python3-pip curl gcc make libssl-dev openssl
    pip3 install pytest

    mkdir -p /app/vendored/mongoose
    mkdir -p /app/policy-daemon

    curl -L -o /app/vendored/mongoose/mongoose.c https://raw.githubusercontent.com/cesanta/mongoose/7.11/mongoose.c
    curl -L -o /app/vendored/mongoose/mongoose.h https://raw.githubusercontent.com/cesanta/mongoose/7.11/mongoose.h

    cat << 'EOF' > /app/checksums.txt
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /app/vendored/mongoose/mongoose.h
EOF

    cat << 'EOF' > /app/policy-daemon/Makefile
policy-daemon: server.c /app/vendored/mongoose/mongoose.c
	gcc -I/app/vendored/mongoose -o policy-daemon server.c /app/vendored/mongoose/mongoose.c
EOF

    cat << 'EOF' > /app/policy-daemon/server.c
#include "mongoose.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int drop_privileges_and_init() {
    char* euid = getenv("MOCK_EUID");
    if (euid != NULL && strcmp(euid, "0") == 0) {
        return -1;
    }
    return 0;
}

static void fn(struct mg_connection *c, int ev, void *ev_data, void *fn_data) {
    if (ev == MG_EV_HTTP_MSG) {
        struct mg_http_message *hm = (struct mg_http_message *) ev_data;
        struct mg_str *auth = mg_http_get_header(hm, "Authorization");
        if (auth && mg_vcasecmp(auth, "Bearer devsecops-token-99") == 0) {
            mg_http_reply(c, 200, "Content-Type: application/json\r\n", "{\"status\": \"policy_enforced\", \"version\": \"1.0\"}");
        } else {
            mg_http_reply(c, 401, "", "Unauthorized");
        }
    }
}

int main(void) {
    if (drop_privileges_and_init() < 0) {
        // VULNERABILITY: Does not terminate! 
        // Agent needs to add a termination call.
    }

    struct mg_mgr mgr;
    mg_mgr_init(&mgr);
    mg_http_listen(&mgr, "https://0.0.0.0:8443?cert=certs/server.crt&key=certs/server.key", fn, NULL);
    for (;;) mg_mgr_poll(&mgr, 1000);
    mg_mgr_free(&mgr);
    return 0;
}
EOF

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user
    chmod -R 777 /app