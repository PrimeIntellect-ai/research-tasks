apt-get update && apt-get install -y python3 python3-pip gcc gdb tcpdump
    pip3 install pytest scapy

    useradd -m -s /bin/bash user || true

    mkdir -p /home/user/src

    cat << 'EOF' > /home/user/src/parser.c
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

void process(const char *input) {
    char buffer[64];
    strcpy(buffer, input); // Vulnerable function
    printf("Processed telemetry: %zu bytes\n", strlen(buffer));
}

int main(int argc, char **argv) {
    if (argc < 2) return 1;
    FILE *f = fopen(argv[1], "rb");
    if (!f) return 1;
    fseek(f, 0, SEEK_END);
    long fsize = ftell(f);
    fseek(f, 0, SEEK_SET);
    char *string = malloc(fsize + 1);
    fread(string, 1, fsize, f);
    fclose(f);
    string[fsize] = 0;
    process(string);
    return 0;
}
EOF

    gcc -fno-stack-protector -z execstack -no-pie -o /home/user/parser /home/user/src/parser.c
    chmod +x /home/user/parser

    cat << 'EOF' > /tmp/gen_pcap.py
import scapy.all as scapy

packets = []
# Packets 0 to 3: Normal payloads
for i in range(4):
    payload = b"NORMAL_DATA_" + str(i).encode() * 4
    pkt = scapy.IP(dst="192.168.1.100")/scapy.UDP(dport=8080)/scapy.Raw(load=payload)
    packets.append(pkt)

# Packet 4: Malicious payload (Buffer overflow)
# 64 bytes buffer + 8 bytes RBP = 72 bytes padding
# Next 8 bytes overwrite RIP
malicious_payload = (b"A" * 72) + b"DEADBEEF" + (b"C" * 20)
pkt_malicious = scapy.IP(dst="192.168.1.100")/scapy.UDP(dport=8080)/scapy.Raw(load=malicious_payload)
packets.append(pkt_malicious)

# Packets 5 to 7: Normal payloads
for i in range(5, 8):
    payload = b"MORE_DATA_" + str(i).encode() * 4
    pkt = scapy.IP(dst="192.168.1.100")/scapy.UDP(dport=8080)/scapy.Raw(load=payload)
    packets.append(pkt)

scapy.wrpcap("/home/user/telemetry.pcap", packets)
EOF

    python3 /tmp/gen_pcap.py
    rm /tmp/gen_pcap.py

    cat << 'EOF' > /home/user/process_telemetry.py
import subprocess
import os
import scapy.all as scapy

def main():
    packets = scapy.rdpcap("/home/user/telemetry.pcap")
    for i, pkt in enumerate(packets):
        if pkt.haslayer(scapy.Raw):
            payload = pkt[scapy.Raw].load
            tmp_file = f"/tmp/payload_{i}.dat"
            with open(tmp_file, "wb") as f:
                f.write(payload)

            print(f"Processing packet {i}...")
            # This will crash on packet 4
            subprocess.run(["/home/user/parser", tmp_file], check=True)

if __name__ == "__main__":
    main()
EOF
    chmod +x /home/user/process_telemetry.py

    chmod -R 777 /home/user