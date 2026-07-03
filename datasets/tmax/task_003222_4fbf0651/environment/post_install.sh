apt-get update && apt-get install -y python3 python3-pip tcpdump coreutils
    pip3 install pytest

    mkdir -p /home/user

    # Create Python script to generate the pcap file
    cat << 'EOF' > /home/user/setup.py
import struct
import time

def write_pcap(filename):
    with open(filename, 'wb') as f:
        # Global header
        f.write(struct.pack('<IHHiIII', 0xa1b2c3d4, 2, 4, 0, 0, 65535, 1)) # DLT_EN10MB = 1

        # Packet 1: TCP 192.168.1.100:1234 -> 10.0.0.5:80, len 60
        # Dummy Ethernet + IPv4 + TCP
        pkt1 = b'\x00\x11\x22\x33\x44\x55\x66\x77\x88\x99\xaa\xbb\x08\x00' # Eth
        pkt1 += b'\x45\x00\x00\x28\x00\x01\x00\x00\x40\x06\x00\x00\xc0\xa8\x01\x64\x0a\x00\x00\x05' # IP
        pkt1 += b'\x04\xd2\x00\x50\x00\x00\x00\x00\x00\x00\x00\x00\x50\x00\x00\x00\x00\x00\x00\x00' # TCP

        f.write(struct.pack('<IIII', int(time.time()), 0, len(pkt1), len(pkt1)))
        f.write(pkt1)

        # Packet 2: UDP 192.168.1.101:53 -> 8.8.8.8:53, len 50
        pkt2 = b'\x00\x11\x22\x33\x44\x55\x66\x77\x88\x99\xaa\xbb\x08\x00' # Eth
        pkt2 += b'\x45\x00\x00\x1e\x00\x01\x00\x00\x40\x11\x00\x00\xc0\xa8\x01\x65\x08\x08\x08\x08' # IP
        pkt2 += b'\x00\x35\x00\x35\x00\x0a\x00\x00\xaa\xbb' # UDP + payload

        f.write(struct.pack('<IIII', int(time.time()), 0, len(pkt2), len(pkt2)))
        f.write(pkt2)

write_pcap('/home/user/traffic.pcap')
EOF

    # Generate the pcap file
    python3 /home/user/setup.py

    # Create expected.csv
    cat << 'EOF' > /home/user/expected.csv
Source_IP,Dest_IP,Protocol,Length
192.168.1.100,10.0.0.5,TCP,40
192.168.1.101,8.8.8.8,UDP,30
EOF

    # Create transform.sh
    cat << 'EOF' > /home/user/transform.sh
#!/bin/bash
echo "Source_IP,Dest_IP,Protocol,Length"
# Buggy implementation: doesn't strip port correctly, hardcodes protocol logic poorly
tcpdump -nn -q -r "$1" 2>/dev/null | awk '{
    src = $3
    dst = $5
    gsub(/:$/, "", dst)
    proto = "UNKNOWN"
    if ($6 == "tcp") proto = "TCP"
    if ($6 == "udp") proto = "UDP"
    len = $NF
    print src "," dst "," proto "," len
}'
EOF
    chmod +x /home/user/transform.sh

    # Create user and adjust permissions
    useradd -m -s /bin/bash user || true
    chown -R user:user /home/user
    chmod -R 777 /home/user