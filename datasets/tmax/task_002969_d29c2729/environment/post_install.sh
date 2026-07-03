apt-get update && apt-get install -y python3 python3-pip wget tar
    pip3 install pytest

    # Create user
    useradd -m -s /bin/bash user || true

    # Download and vendor dpkt 1.9.8
    mkdir -p /app
    cd /app
    pip3 download dpkt==1.9.8 --no-binary :all:
    tar -xzf dpkt-1.9.8.tar.gz
    rm dpkt-1.9.8.tar.gz

    # Introduce the off-by-one bug in tcp.py (change length check to allow len=1)
    sed -i 's/< 2:/<= 0:/g' /app/dpkt-1.9.8/dpkt/tcp.py

    # Generate incident_capture.pcap with a malicious packet (TCP option length 1)
    cat << 'EOF' > /tmp/gen_pcap.py
import struct
import time

def write_pcap(filename):
    # pcap global header
    magic = b'\xd4\xc3\xb2\xa1'
    version_major = b'\x02\x00'
    version_minor = b'\x04\x00'
    thiszone = b'\x00\x00\x00\x00'
    sigfigs = b'\x00\x00\x00\x00'
    snaplen = b'\xff\xff\x00\x00'
    network = b'\x01\x00\x00\x00' # Ethernet

    global_hdr = magic + version_major + version_minor + thiszone + sigfigs + snaplen + network

    # Packet data
    eth_hdr = b'\x00\x01\x02\x03\x04\x05\x00\x01\x02\x03\x04\x06\x08\x00'
    ip_hdr = b'\x45\x00\x00\x2c\x00\x01\x00\x00\x40\x06\x00\x00\x7f\x00\x00\x01\x7f\x00\x00\x01'
    # TCP header with offset=6 (24 bytes, 4 bytes options)
    tcp_hdr = struct.pack('>HHIIBBHHH', 1234, 80, 1, 0, (6 << 4), 2, 8192, 0, 0)
    # TCP option: type=254, len=1 (malformed), followed by padding
    tcp_opts = b'\xfe\x01\x00\x00'
    pkt = eth_hdr + ip_hdr + tcp_hdr + tcp_opts

    ts_sec = struct.pack('<I', int(time.time()))
    ts_usec = struct.pack('<I', 0)
    incl_len = struct.pack('<I', len(pkt))
    orig_len = struct.pack('<I', len(pkt))

    pkt_hdr = ts_sec + ts_usec + incl_len + orig_len

    with open(filename, 'wb') as f:
        f.write(global_hdr)
        f.write(pkt_hdr)
        f.write(pkt)

write_pcap('/home/user/incident_capture.pcap')
EOF

    python3 /tmp/gen_pcap.py
    rm /tmp/gen_pcap.py

    # Set permissions
    chmod -R 777 /home/user