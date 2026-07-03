apt-get update && apt-get install -y python3 python3-pip g++ make redis-server
    pip3 install pytest redis

    mkdir -p /home/user/services/generator
    mkdir -p /home/user/services/processor
    mkdir -p /app

    # Create the oracle processor
    cat << 'EOF' > /tmp/oracle.cpp
#include <iostream>
#include <cstdint>
#include <cstring>

using namespace std;

int main() {
    char buf[4];
    while (cin.read(buf, 4)) {
        if (memcmp(buf, "WAL\x01", 4) == 0) {
            char crc[4];
            if (!cin.read(crc, 4)) break;
            if (!cin.read(buf, 4)) break;
        }
        if (memcmp(buf, "LOG1", 4) == 0) {
            uint64_t ts;
            if (!cin.read(reinterpret_cast<char*>(&ts), 8)) break;
            float metric;
            if (!cin.read(reinterpret_cast<char*>(&metric), 4)) break;
            uint16_t len;
            if (!cin.read(reinterpret_cast<char*>(&len), 2)) break;
            char* str = new char[len + 1];
            if (!cin.read(str, len)) {
                delete[] str;
                break;
            }
            str[len] = '\0';
            printf("{\"timestamp\": %lu, \"metric\": %.6f, \"message\": \"%s\"}\n", ts, metric, str);
            delete[] str;
        } else {
            break;
        }
    }
    return 0;
}
EOF
    g++ -O3 /tmp/oracle.cpp -o /app/oracle_processor
    strip /app/oracle_processor
    rm /tmp/oracle.cpp

    # Create the buggy main.cpp
    cat << 'EOF' > /home/user/services/processor/main.cpp
#include <iostream>
#include <cstdint>
#include <cstring>

using namespace std;

int main() {
    char buf[4];
    while (cin.read(buf, 4)) {
        if (memcmp(buf, "WAL\x01", 4) == 0) {
            cerr << "Error: WAL frame not supported" << endl;
            return 1;
        }
        if (memcmp(buf, "LOG1", 4) == 0) {
            uint64_t ts;
            cin.read(reinterpret_cast<char*>(&ts), 8);

            uint32_t metric_raw;
            cin.read(reinterpret_cast<char*>(&metric_raw), 4);
            float metric = (float)metric_raw;

            uint16_t len;
            cin.read(reinterpret_cast<char*>(&len), 2);
            len = (len >> 8) | (len << 8); 

            char* str = new char[len + 1];
            cin.read(str, len);
            str[len] = '\0';

            printf("{\"timestamp\": %lu, \"metric\": %f, \"message\": \"%s\"}\n", ts, metric, str);
            delete[] str;
        } else {
            break;
        }
    }
    return 0;
}
EOF

    # Create generator mock
    cat << 'EOF' > /home/user/services/generator/gen.py
import sys
import time

if __name__ == "__main__":
    while True:
        time.sleep(1)
EOF

    # Create buggy config files
    cat << 'EOF' > /home/user/services/processor/config.env
REDIS_PORT=6380
LISTEN_PORT=8081
EOF

    cat << 'EOF' > /home/user/start_services.sh
#!/bin/bash
redis-server --port 6380 &
/home/user/services/processor/processor &
python3 /home/user/services/generator/gen.py --port 8081 &
wait
EOF
    chmod +x /home/user/start_services.sh

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user
    chmod -R 777 /app