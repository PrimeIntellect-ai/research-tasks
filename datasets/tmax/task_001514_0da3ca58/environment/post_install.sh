apt-get update && apt-get install -y python3 python3-pip gcc bsdmainutils gawk coreutils
    pip3 install pytest

    mkdir -p /app
    cat << 'EOF' > /app/config_compiler.c
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

int main(int argc, char *argv[]) {
    if (argc != 3) return 1;
    FILE *in = fopen(argv[1], "r");
    if (!in) return 1;

    char line[256];
    uint32_t id = 0;
    uint64_t ts = 0;
    int valid = 0;

    while (fgets(line, sizeof(line), in)) {
        if (strstr(line, "INVALID")) {
            fclose(in);
            return 1;
        }
        if (sscanf(line, "ID=%u", &id) == 1) { valid++; }
        if (sscanf(line, "TIMESTAMP=%lu", &ts) == 1) { valid++; }
    }
    fclose(in);

    if (valid < 2) return 1;

    FILE *out = fopen(argv[2], "wb");
    if (!out) return 1;

    fwrite("CFG1", 1, 4, out);
    fwrite(&id, 4, 1, out);
    fwrite(&ts, 8, 1, out);
    fwrite("DATA", 1, 4, out);
    fclose(out);

    return 0;
}
EOF

    gcc -O2 -s /app/config_compiler.c -o /app/config_compiler
    rm /app/config_compiler.c

    cat << 'EOF' > /tmp/setup.py
import os
import json
import datetime

os.makedirs('/home/user/raw_configs', exist_ok=True)
os.makedirs('/home/user/compiled', exist_ok=True)
os.makedirs('/home/user/tracked_configs', exist_ok=True)

expected = []

configs = [
    {"name": "cfg_a", "id": 101, "ts": 1609459200, "valid": True},
    {"name": "cfg_b", "id": 102, "ts": 1612137600, "valid": True},
    {"name": "cfg_c", "id": 103, "ts": 1614556800, "valid": False},
    {"name": "cfg_d", "id": 104, "ts": 1640995200, "valid": True},
]

for c in configs:
    with open(f"/home/user/raw_configs/{c['name']}.txt", "w") as f:
        if c['valid']:
            f.write(f"ID={c['id']}\nTIMESTAMP={c['ts']}\n")
            date_str = datetime.datetime.utcfromtimestamp(c['ts']).strftime('%Y-%m-%d')
            expected.append({
                "basename": c['name'],
                "id": c['id'],
                "date": date_str
            })
        else:
            f.write("INVALID\n")

with open("/tmp/expected_mapping.json", "w") as f:
    json.dump(expected, f)
EOF

    python3 /tmp/setup.py
    rm /tmp/setup.py

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user