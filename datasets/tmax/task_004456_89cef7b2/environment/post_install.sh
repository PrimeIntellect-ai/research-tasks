apt-get update && apt-get install -y python3 python3-pip gcc make build-essential
    pip3 install pytest

    mkdir -p /app/ts_filler-1.2
    mkdir -p /home/user/data
    mkdir -p /tmp

    # Create C file
    cat << 'EOF' > /app/ts_filler-1.2/ts_filler.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main() {
    char line[256];
    int prev_time = -1;
    float prev_val = 0;

    if (fgets(line, sizeof(line), stdin)) {
        printf("%s", line);
    }

    while (fgets(line, sizeof(line), stdin)) {
        int t; float v; char m[100];
        if (sscanf(line, "%d,%f,%s", &t, &v, m) == 3) {
            if (prev_time != -1) {
                int gap = t - prev_time;
                for (int i = 1; i < gap; i++) {
                    int curr_time = prev_time + i;
                    #if INTERPOLATE_MODE == 1
                    float interp = prev_val + (v - prev_val) * i / gap;
                    printf("%d,%.2f,interp\n", curr_time, interp);
                    #else
                    printf("%d,0.00,zero\n", curr_time);
                    #endif
                }
            }
            printf("%d,%.2f,%s\n", t, v, m);
            prev_time = t;
            prev_val = v;
        }
    }
    return 0;
}
EOF

    # Create Makefile
    cat << 'EOF' > /app/ts_filler-1.2/Makefile
CFLAGS = -O2 -DINTERPOLATE_MODE=0

ts_filler: ts_filler.c
	$(CC) $(CFLAGS) -o ts_filler ts_filler.c
EOF

    # Generate raw and reference data using Python
    python3 -c "
import os
os.makedirs('/home/user/data', exist_ok=True)
os.makedirs('/tmp', exist_ok=True)

raw_data = b'timestamp,value,metadata\n1,10.0,caf\xe9\n2,12.0,caf\xe9\n\n\n4,16.0,caf\xe9\n5,18.0,caf\xe9\n'
with open('/home/user/data/raw_sensor.csv', 'wb') as f:
    f.write(raw_data)

ref_data = 'timestamp,value,metadata\n1,10.00,café\n2,12.00,café\n3,14.00,interp\n4,16.00,café\n5,18.00,café\n'
with open('/tmp/reference.csv', 'w', encoding='utf-8') as f:
    f.write(ref_data)
"

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user
    chmod -R 777 /app