apt-get update && apt-get install -y python3 python3-pip git
    pip3 install pytest scapy

    git config --global user.email "test@example.com"
    git config --global user.name "Test User"

    mkdir -p /home/user/repo
    cd /home/user/repo
    git init

    cat << 'EOF' > test_runner.py
import subprocess
import sys

try:
    output = subprocess.check_output(['python3', 'parse_pcap.py', '../test_traffic.pcap'], stderr=subprocess.STDOUT)
    if b"Precision loss detected" in output or b"Error" in output:
        sys.exit(1)
    sys.exit(0)
except subprocess.CalledProcessError:
    sys.exit(1)
EOF

    cat << 'EOF' > parse_pcap.py
import sys
import re
try:
    from scapy.all import rdpcap, Raw
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "scapy"])
    from scapy.all import rdpcap, Raw

def extract_price(payload):
    m = re.search(b"PRICE=([0-9.]+)", payload)
    if m:
        return float(m.group(1))
    return None

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 parse_pcap.py <pcap_file>")
        sys.exit(1)

    packets = rdpcap(sys.argv[1])
    for pkt in packets:
        if pkt.haslayer(Raw):
            payload = pkt[Raw].load
            price = extract_price(payload)
            if price is not None:
                # Check precision
                price_str = f"{price:.14f}"
                if price_str.endswith('000000'):
                    print(f"Precision loss detected: {price_str}")
                    sys.exit(1)
                print(f"Parsed price: {price}")

if __name__ == "__main__":
    main()
EOF

    git add test_runner.py parse_pcap.py
    git commit -m "Initial commit"
    ROOT_COMMIT=$(git rev-parse HEAD)

    for i in {1..136}; do
        echo "# dummy $i" >> test_runner.py
        git commit -am "Dummy commit $i"
    done

    # Introduce bug in commit 137
    cat << 'EOF' > parse_pcap.py
import sys
import re
try:
    from scapy.all import rdpcap, Raw
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "scapy"])
    from scapy.all import rdpcap, Raw

def extract_price(payload):
    # Fix edge case with trailing garbage
    m = re.search(b"PRICE=([0-9.]{1,8})", payload)
    if m:
        return float(m.group(1))
    return None

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 parse_pcap.py <pcap_file>")
        sys.exit(1)

    packets = rdpcap(sys.argv[1])
    for pkt in packets:
        if pkt.haslayer(Raw):
            payload = pkt[Raw].load
            price = extract_price(payload)
            if price is not None:
                # Check precision
                price_str = f"{price:.14f}"
                if price_str.endswith('000000'):
                    print(f"Precision loss detected: {price_str}")
                    sys.exit(1)
                print(f"Parsed price: {price}")

if __name__ == "__main__":
    main()
EOF

    git commit -am "Fix parsing edge case with malformed trailing chars"
    BAD_COMMIT=$(git rev-parse HEAD)

    for i in {138..200}; do
        echo "# dummy $i" >> test_runner.py
        git commit -am "Dummy commit $i"
    done

    # Generate pcap
    cd /home/user
    python3 -c "
from scapy.all import wrpcap, Ether, IP, TCP, Raw
pkts = [
    Ether()/IP(dst='1.2.3.4')/TCP(dport=80)/Raw(load=b'TRADE MSG PRICE=123.456789012345'),
    Ether()/IP(dst='1.2.3.4')/TCP(dport=80)/Raw(load=b'TRADE MSG PRICE=987.654321098765XYZ')
]
wrpcap('test_traffic.pcap', pkts)
"
    echo $BAD_COMMIT > /tmp/expected_bad_commit.txt

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user