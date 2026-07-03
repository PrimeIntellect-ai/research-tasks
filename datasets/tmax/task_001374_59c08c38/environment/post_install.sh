apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest h5py numpy

    mkdir -p /app/data
    mkdir -p /app/protein-model-server

    # Create FASTA file
    cat << 'EOF' > /app/data/proteins.fasta
>P12345
MVLSPADKTNVKAAWGKVGAHAGEYGAEALERMFLSFPTTKTYFPHFDLSHGSAQVKGHG
KKVADALTNAVAHVDDMPNALSALSDLHAHKLRVDPVNFKLLSHCLLVTLAAHLPAEFTP
AVHASLDKFLASVSTVLTSKYR
>P67890
MTEYKLVVVGAGGVGKSALTIQLIQNHFVDEYDPTIEDSYRKQVVIDGETCLLDILDTAG
QEEYSAMRDQYMRTGEGFLCVFAINNTKSFEDIHQYREQIKRVKDSDDVPMVLVGNKCDL
EOF

    # Generate HDF5 file
    cat << 'EOF' > /tmp/gen_h5.py
import h5py
import numpy as np
import math

L = 142
N = 10
exp_curve_P12345 = [L * (1 - math.exp(-0.05 * t)) + 1.0 for t in range(N)]

with h5py.File('/app/data/experiments.h5', 'w') as f:
    grp = f.create_group('experiments')
    p1 = grp.create_group('P12345')
    p1.create_dataset('curve', data=np.array(exp_curve_P12345, dtype=np.float64))
EOF
    python3 /tmp/gen_h5.py
    rm /tmp/gen_h5.py

    # Create server.py
    cat << 'EOF' > /app/protein-model-server/server.py
import http.server
import socketserver
import json
import subprocess
import re

class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.headers.get('Authorization') != 'Bearer wrong-token':
            self.send_response(401)
            self.end_headers()
            return

        match = re.match(r'^/api/protein/([A-Z0-9]+)/validate$', self.path)
        if match:
            prot_id = match.group(1)
            # Call compute.sh
            res = subprocess.run(['./compute.sh', prot_id], capture_output=True, text=True, cwd='/app/protein-model-server')
            try:
                data = json.loads(res.stdout)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(data).encode())
            except:
                self.send_response(500)
                self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()

with socketserver.TCPServer(("127.0.0.1", 9090), Handler) as httpd:
    httpd.serve_forever()
EOF

    # Create compute.sh
    cat << 'EOF' > /app/protein-model-server/compute.sh
#!/bin/bash
# Broken compute script
PROT_ID=$1
# Bug 1: Only gets one line of sequence
SEQ=$(grep -A 1 "^>${PROT_ID}" /app/data/proteins.fasta | tail -n 1)
L=${#SEQ}

# Agent will likely replace this entirely with a Python script since h5dump parsing is tedious in bash,
# or write a fixed python script for the math.
# Output expected format: {"id": "P12345", "length": 142, "mse": 1.0}
echo '{"id": "'$PROT_ID'", "length": '$L', "mse": 999.99}'
EOF
    chmod +x /app/protein-model-server/compute.sh

    # Set permissions for /app
    chmod -R 777 /app

    # Create user
    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user