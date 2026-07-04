apt-get update && apt-get install -y python3 python3-pip g++ procps
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    cat << 'EOF' > /home/user/process_logs.cpp
#include <iostream>
#include <string>

int main() {
    std::string line;
    while (std::getline(std::cin, line)) {
        if (line.find("ACTION=UPDATE") != std::string::npos && line.find("PAYLOAD=") != std::string::npos) {
            size_t pos = line.find("PAYLOAD=");
            // BUG: Hardcoded offset assumes a minimum payload length. 
            // Throws std::out_of_range if line is shorter than pos + 20.
            std::string payload = line.substr(pos + 20); 
            std::cout << "Processed payload of length: " << payload.length() << "\n";
        }
    }
    return 0;
}
EOF

    g++ -O2 /home/user/process_logs.cpp -o /home/user/process_logs

    cat << 'EOF' > /home/user/generate_data.py
import random
with open("/tmp/crash_data.txt", "w") as f:
    for i in range(1, 1001):
        if i == 642:
            f.write(f"[{i}] INFO ACTION=UPDATE PAYLOAD=tiny\n") # This line causes the out_of_range exception
        else:
            f.write(f"[{i}] INFO ACTION=UPDATE PAYLOAD=this_is_a_sufficiently_long_payload_string\n")
EOF

    cat << 'EOF' > /home/user/setup_env.sh
#!/bin/bash
if ! pgrep -f "tail -f /tmp/crash_data.txt" > /dev/null; then
    python3 /home/user/generate_data.py
    tail -f /tmp/crash_data.txt > /dev/null 2>&1 &
    sleep 0.2
    rm -f /tmp/crash_data.txt
fi
EOF
    chmod +x /home/user/setup_env.sh

    echo "source /home/user/setup_env.sh" >> /etc/bash.bashrc
    echo "source /home/user/setup_env.sh" >> /home/user/.bashrc
    echo "source /home/user/setup_env.sh" >> /root/.bashrc

    # Run it once during build so files exist if tests check without triggering the script
    /home/user/setup_env.sh

    chmod -R 777 /home/user