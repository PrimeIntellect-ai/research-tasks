apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest

    useradd -m -s /bin/bash user || true
    mkdir -p /home/user/incident

    # 1. Create a valid PCAP file with python
    cat << 'EOF' > /home/user/incident/make_pcap.py
import struct

def create_pcap(filename):
    # PCAP Global Header
    magic_number = 0xa1b2c3d4
    version_major = 2
    version_minor = 4
    thiszone = 0
    sigfigs = 0
    snaplen = 65535
    network = 1 # Ethernet

    global_header = struct.pack('<IHHIIII', magic_number, version_major, version_minor, thiszone, sigfigs, snaplen, network)

    with open(filename, 'wb') as f:
        f.write(global_header)

        # Fake Packet: Ethernet + IPv4 + UDP + Payload
        # Src IP: 192.168.100.42 (c0 a8 64 2a)
        # Dst IP: 10.0.0.5 (0a 00 00 05)
        payload = b'Some random text FATAL_POISON and more'

        # Mocking headers (simplistic)
        eth_hdr = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\x00'
        ip_hdr = b'\x45\x00\x00\x00\x00\x00\x40\x00\x40\x11\x00\x00\xc0\xa8\x64\x2a\x0a\x00\x00\x05'
        udp_hdr = b'\x12\x34\x12\x34\x00\x00\x00\x00'

        packet_data = eth_hdr + ip_hdr + udp_hdr + payload

        # PCAP Packet Header
        ts_sec = 1600000000
        ts_usec = 0
        incl_len = len(packet_data)
        orig_len = len(packet_data)

        pkt_header = struct.pack('<IIII', ts_sec, ts_usec, incl_len, orig_len)
        f.write(pkt_header)
        f.write(packet_data)

create_pcap('/home/user/incident/traffic.pcap')
EOF
    python3 /home/user/incident/make_pcap.py
    rm /home/user/incident/make_pcap.py

    # 2. Create the core dump with random data and the token
    dd if=/dev/urandom of=/home/user/incident/core.dmp bs=1K count=10 2>/dev/null
    echo "Some junk data TOKEN-a1b2c3d4e5f67890a1b2c3d4e5f67890 more junk" >> /home/user/incident/core.dmp
    dd if=/dev/urandom bs=1K count=10 >> /home/user/incident/core.dmp 2>/dev/null

    # 3. Create parser.py with bug and dependency check
    cat << 'EOF' > /home/user/incident/parser.py
import sys
try:
    import urllib3
    if urllib3.__version__ != "1.26.15":
        print(f"Dependency Error: urllib3 version must be 1.26.15, found {urllib3.__version__}")
        sys.exit(1)
except ImportError:
    print("Dependency Error: urllib3 is not installed.")
    sys.exit(1)

def compute_checksum(n):
    # Missing base case causes recursion error
    return n + compute_checksum(n - 1)

if __name__ == "__main__":
    # When fixed, compute_checksum(10) should return 55
    print(compute_checksum(10))
EOF

    # Install conflicting version of urllib3
    pip3 install urllib3==2.0.7

    chmod -R 777 /home/user