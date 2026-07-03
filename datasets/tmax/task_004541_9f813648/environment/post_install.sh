apt-get update && apt-get install -y python3 python3-pip gcc redis-server nginx jq curl
    pip3 install pytest flask redis jupyter nbconvert

    mkdir -p /app/oracle
    mkdir -p /app/flask_service
    mkdir -p /app/services
    mkdir -p /home/user/validation

    # /app/oracle/integrator.c
    cat << 'EOF' > /app/oracle/integrator.c
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {
    if (argc < 6) return 1;
    printf("{\"t\": [\"%f\"], \"y\": [[\"%f\", \"%f\"]]}\n", atof(argv[1]), atof(argv[3]), atof(argv[4]));
    return 0;
}
EOF

    # /app/flask_service/integrator.py
    cat << 'EOF' > /app/flask_service/integrator.py
def calculate_error():
    pass

def adapt_step():
    pass

def integrate(t0, tf, y0, tol):
    return {"t": [f"{t0:.6f}"], "y": [[f"{y0[0]:.6f}", f"{y0[1]:.6f}"]]}
EOF

    # /app/flask_service/app.py
    cat << 'EOF' > /app/flask_service/app.py
from flask import Flask, request, jsonify
from integrator import integrate
import redis
import config

app = Flask(__name__)
cache = redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT)

@app.route('/simulate', methods=['POST'])
def simulate():
    data = request.json
    res = integrate(data['t0'], data['tf'], data['y0'], data['tol'])
    return jsonify(res)

if __name__ == '__main__':
    app.run(port=5000)
EOF

    # /app/flask_service/config.py
    cat << 'EOF' > /app/flask_service/config.py
REDIS_HOST = "localhost"
REDIS_PORT = 6380 # Wrong port
EOF

    # /app/services/nginx.conf
    cat << 'EOF' > /app/services/nginx.conf
events {}
http {
    server {
        listen 8080;
        location /simulate {
            # proxy_pass missing
        }
    }
}
EOF

    # /app/services/start_services.sh
    cat << 'EOF' > /app/services/start_services.sh
#!/bin/bash
redis-server --daemonize yes
nginx -c /app/services/nginx.conf
cd /app/flask_service && python3 app.py &
EOF
    chmod +x /app/services/start_services.sh

    # /home/user/validation/check_analytical.ipynb
    cat << 'EOF' > /home/user/validation/check_analytical.ipynb
{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "print('Validation passed')"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
EOF

    useradd -m -s /bin/bash user || true
    chown -R user:user /home/user
    chmod -R 777 /home/user