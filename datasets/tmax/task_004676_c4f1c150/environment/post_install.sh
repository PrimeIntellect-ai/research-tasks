apt-get update && apt-get install -y python3 python3-pip git
    pip3 install pytest scapy flask requests werkzeug

    mkdir -p /app/iot_system
    cd /app/iot_system

    cat << 'EOF' > requirements.txt
Flask
requests
EOF

    cat << 'EOF' > ingest_api.py
from flask import Flask, request
app = Flask(__name__)

@app.route('/data', methods=['POST'])
def data():
    if request.headers.get('Authorization') != 'Bearer secr3t_10t_t0k3n_8421':
        return "Unauthorized", 401
    return "OK", 200

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
EOF

    cat << 'EOF' > parser_service.py
import socket
import struct
import threading
import requests
from flask import Flask, request, jsonify

TOKEN = "REPLACE_ME"
INGEST_URL = "http://127.0.0.1:8080/data"

app = Flask(__name__)
latest_data = {}

def udp_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('127.0.0.1', 5005))
    while True:
        data, addr = sock.recvfrom(1024)
        if len(data) == 16:
            magic, sensor_id, timestamp, temp = struct.unpack('<4sIII', data)
            if magic == b'IOT\x00':
                payload = {"sensor_id": sensor_id, "timestamp": timestamp, "temperature": temp}
                headers = {"Authorization": f"Bearer {TOKEN}"}
                try:
                    resp = requests.post(INGEST_URL, json=payload, headers=headers)
                    if resp.status_code == 200:
                        latest_data[sensor_id] = temp
                except Exception as e:
                    pass

@app.route('/latest', methods=['GET'])
def latest():
    sensor_id = int(request.args.get('sensor_id'))
    return jsonify({"sensor_id": sensor_id, "temperature": latest_data.get(sensor_id)})

if __name__ == '__main__':
    t = threading.Thread(target=udp_server, daemon=True)
    t.start()
    app.run(host='127.0.0.1', port=8081)
EOF

    cat << 'EOF' > startup.sh
#!/bin/bash
python3 ingest_api.py &
python3 parser_service.py &
wait
EOF
    chmod +x startup.sh

    cat << 'EOF' > gen_pcap.py
from scapy.all import *
req = b"POST /data HTTP/1.1\r\nHost: 127.0.0.1:8080\r\nAuthorization: Bearer secr3t_10t_t0k3n_8421\r\n\r\n"
pkt = IP(dst="127.0.0.1")/TCP(dport=8080)/Raw(load=req)
wrpcap("capture.pcap", pkt)
EOF
    python3 gen_pcap.py
    rm gen_pcap.py

    git config --global init.defaultBranch main
    git config --global user.email "dev@example.com"
    git config --global user.name "Dev"

    git init
    git add ingest_api.py parser_service.py startup.sh requirements.txt
    git commit -m "Initial commit"

    git add capture.pcap
    git commit -m "Add test capture"

    git rm capture.pcap
    git commit -m "Remove capture file, oops"

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user
    chmod -R 777 /app