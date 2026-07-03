apt-get update && apt-get install -y python3 python3-pip tcpdump strace
    pip3 install pytest

    mkdir -p /home/user
    cd /home/user

    # Create math_worker.py
    cat << 'EOF' > math_worker.py
import sys, json, os

try:
    payload = json.load(sys.stdin)
    data = payload.get("data", [])
except Exception:
    sys.exit(0)

# The bug: A specific mathematical combination causes an abort
# It crashes if any 3 numbers in the input array multiply exactly to 1394 (which is 2 * 17 * 41)
n = len(data)
for i in range(n):
    for j in range(i+1, n):
        for k in range(j+1, n):
            if data[i] * data[j] * data[k] == 1394:
                os.system("echo 'Fatal Math Error: Unstable state detected' > /dev/stderr")
                os.abort()

print("Success")
EOF
    chmod +x math_worker.py

    # Create a python script to generate the PCAP
    cat << 'EOF' > generate_pcap.py
import struct
import json

def write_pcap(filename, packets):
    # PCAP Global Header
    # magic_number, version_major, version_minor, thiszone, sigfigs, snaplen, network (1 = Ethernet)
    global_header = struct.pack('<IHHIIII', 0xa1b2c3d4, 2, 4, 0, 0, 65535, 1)

    with open(filename, 'wb') as f:
        f.write(global_header)

        for payload in packets:
            data = payload.encode('utf-8')

            # Mock Ethernet, IP, UDP headers
            # Eth: 14 bytes, IP: 20 bytes, UDP: 8 bytes
            udp_len = 8 + len(data)
            ip_len = 20 + udp_len

            eth = b'\x00' * 14
            ip = struct.pack('!BBHHHBBH4s4s', 0x45, 0, ip_len, 0, 0, 64, 17, 0, b'\x7f\x00\x00\x01', b'\x7f\x00\x00\x01')
            udp = struct.pack('!HHHH', 12345, 8080, udp_len, 0)

            packet_data = eth + ip + udp + data

            # PCAP Packet Header
            # ts_sec, ts_usec, incl_len, orig_len
            pkt_header = struct.pack('<IIII', 1600000000, 0, len(packet_data), len(packet_data))
            f.write(pkt_header)
            f.write(packet_data)

packets = [
    json.dumps({"data": [10, 20, 30, 40, 50, 60]}),
    json.dumps({"data": [1, 5, 9, 12, 18, 24]}),
    json.dumps({"data": [5, 12, 41, 7, 88, 17, 99, 101, 2, 4]}) # Crashing payload
]

write_pcap("traffic.pcap", packets)
EOF

    python3 generate_pcap.py
    rm generate_pcap.py

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user