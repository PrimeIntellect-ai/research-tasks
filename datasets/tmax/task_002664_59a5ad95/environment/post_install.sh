apt-get update && apt-get install -y python3 python3-pip git
    pip3 install pytest scapy

    mkdir -p /home/user/uptime_monitor
    cd /home/user/uptime_monitor

    # Generate pcap file
    cat << 'EOF' > gen_pcap.py
from scapy.all import IP, ICMP, wrpcap
packets = []
base_time = 1600000000.0
current_time = base_time
for i in range(1000):
    pkt = IP(dst="10.0.0.1")/ICMP()
    pkt.time = current_time
    packets.append(pkt)
    if i % 10 == 0:
        current_time += 1.0000001
    else:
        current_time += 1.0
wrpcap('heartbeats.pcap', packets)
EOF
    python3 gen_pcap.py
    rm gen_pcap.py

    # Create good version of check_uptime.py
    cat << 'EOF' > check_uptime.py
import sys
import math
from scapy.all import rdpcap

def calculate_uptime(pcap_path):
    packets = rdpcap(pcap_path)
    delays = []
    for i in range(1, len(packets)):
        diff = float(packets[i].time - packets[i-1].time)
        if diff > 1.0:
            delays.append(diff - 1.0) # outage duration

    total_time = float(packets[-1].time - packets[0].time)
    # Good version uses math.fsum for precision
    total_downtime = math.fsum(delays)

    uptime_percent = ((total_time - total_downtime) / total_time) * 100.0
    return uptime_percent

if __name__ == "__main__":
    uptime = calculate_uptime('heartbeats.pcap')
    assert uptime >= 99.999, f"Uptime assertion failed: {uptime}"
    print(f"{uptime:.5f}")
EOF

    # Initialize Git and create commit history
    git init
    git config user.email "sre@company.com"
    git config user.name "SRE"

    git add check_uptime.py
    git commit -m "Initial commit with accurate uptime calculation"
    git tag v1.0

    # 2 dummy commits
    echo "test1" > dummy.txt
    git add dummy.txt
    git commit -m "Update documentation"

    echo "test2" > dummy.txt
    git add dummy.txt
    git commit -m "Fix typo in readme"

    # Bad commit
    sed -i 's/math.fsum(delays)/sum(delays)/g' check_uptime.py
    git add check_uptime.py
    git commit -m "Simplify uptime aggregation"

    # 2 more dummy commits
    echo "test3" > dummy.txt
    git add dummy.txt
    git commit -m "Add new monitoring dashboard config"

    echo "test4" > dummy.txt
    git add dummy.txt
    git commit -m "Update dependencies"

    useradd -m -s /bin/bash user || true
    chown -R user:user /home/user
    chmod -R 777 /home/user