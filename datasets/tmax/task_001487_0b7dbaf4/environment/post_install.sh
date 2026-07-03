apt-get update && apt-get install -y python3 python3-pip golang redis-server nginx curl
    pip3 install pytest flask redis

    mkdir -p /app/oracle

    # Create the oracle Go program
    cat << 'EOF' > /app/oracle/spectral_dist_oracle.go
package main

import (
	"fmt"
	"math"
	"math/cmplx"
	"os"
)

func main() {
	if len(os.Args) != 2 {
		return
	}
	seq := os.Args[1]
	N := len(seq)
	if N == 0 {
		return
	}

	x := make([]float64, N)
	for i, c := range seq {
		switch c {
		case 'A':
			x[i] = 1.0
		case 'C':
			x[i] = 2.0
		case 'G':
			x[i] = -1.0
		case 'T':
			x[i] = -2.0
		}
	}

	X := make([]complex128, N)
	for k := 0; k < N; k++ {
		var sum complex128
		for n := 0; n < N; n++ {
			angle := -2.0 * math.Pi * float64(k*n) / float64(N)
			sum += complex(x[n], 0) * cmplx.Rect(1, angle)
		}
		X[k] = sum
	}

	power := make([]float64, N)
	sumPower := 0.0
	for k := 0; k < N; k++ {
		mag := cmplx.Abs(X[k])
		power[k] = mag * mag
		sumPower += power[k]
	}

	normPower := make([]float64, N)
	if sumPower == 0 {
		for k := 0; k < N; k++ {
			normPower[k] = 1.0 / float64(N)
		}
	} else {
		for k := 0; k < N; k++ {
			normPower[k] = power[k] / sumPower
		}
	}

	dist := 0.0
	uniform := 1.0 / float64(N)
	for k := 0; k < N; k++ {
		diff := normPower[k] - uniform
		dist += diff * diff
	}
	dist = math.Sqrt(dist)

	fmt.Printf("%.6f\n", dist)
}
EOF

    cd /app/oracle
    go build -o spectral_dist_oracle spectral_dist_oracle.go
    rm spectral_dist_oracle.go

    # Create Flask API
    cat << 'EOF' > /app/flask_api.py
from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/validate', methods=['GET'])
def validate():
    primer = request.args.get('primer', '')
    if primer:
        return jsonify({"status": "valid"})
    return jsonify({"status": "invalid"})

if __name__ == '__main__':
    app.run(port=5000)
EOF

    # Create Webdis-like service
    cat << 'EOF' > /app/webdis.py
from flask import Flask, request, jsonify
import redis

app = Flask(__name__)
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

@app.route('/SET/<key>/<val>', methods=['GET'])
def set_val(key, val):
    r.set(key, val)
    return jsonify({"SET": [True, "OK"]})

if __name__ == '__main__':
    app.run(port=7379)
EOF

    # Create Nginx configuration
    cat << 'EOF' > /app/nginx.conf
worker_processes 1;
daemon off;
events {
    worker_connections 1024;
}
http {
    server {
        listen 8080;

        # TODO: Add proxy rules here
    }
}
EOF

    # Create start_services.sh
    cat << 'EOF' > /app/start_services.sh
#!/bin/bash
redis-server --daemonize yes
python3 /app/webdis.py &
python3 /app/flask_api.py &
nginx -c /app/nginx.conf
EOF
    chmod +x /app/start_services.sh

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user