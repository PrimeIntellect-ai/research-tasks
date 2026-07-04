apt-get update && apt-get install -y python3 python3-pip gcc redis-server curl
    pip3 install pytest flask redis

    mkdir -p /app/services /app/bin

    cat << 'EOF' > /tmp/oracle.c
#include <stdio.h>
#include <stdlib.h>
int main() {
    int V, E;
    if (scanf("%d %d", &V, &E) != 2) return 1;
    int *deg = calloc(V, sizeof(int));
    for(int i=0; i<E; i++) {
        int u, v;
        scanf("%d %d", &u, &v);
        deg[u]++; deg[v]++;
    }
    int *w = malloc(V * sizeof(int));
    for(int i=0; i<V; i++) {
        scanf("%d", &w[i]);
    }
    long long sum = 0;
    int count = 0;
    for(int i=0; i<V; i++) {
        if (deg[i] >= 2) {
            sum += w[i];
            count++;
        }
    }
    if (count == 0) printf("0\n");
    else printf("%lld\n", sum / count);
    free(deg); free(w);
    return 0;
}
EOF
    gcc -O3 /tmp/oracle.c -o /app/oracle_mol_analyze
    strip /app/oracle_mol_analyze

    cat << 'EOF' > /app/services/config.json
{
    "redis_host": "localhost",
    "redis_port": 6380
}
EOF

    cat << 'EOF' > /app/services/api.py
from flask import Flask, jsonify
import json, redis, subprocess, os
app = Flask(__name__)

with open('/app/services/config.json') as f:
    config = json.load(f)

r = redis.Redis(host=config['redis_host'], port=config['redis_port'])

@app.route('/trigger_test', methods=['POST'])
def trigger():
    try:
        r.ping() # test connection
        # Run the binary with a static test
        res = subprocess.run(['/app/bin/mol_analyze'], input=b"4 3 0 1 1 2 1 3 10 20 30 40", capture_output=True)
        with open('/home/user/integration_output.txt', 'w') as out:
            out.write(res.stdout.decode('utf-8'))
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000)
EOF

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user