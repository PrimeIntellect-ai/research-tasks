apt-get update && apt-get install -y python3 python3-pip gcc procps
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    cat << 'EOF' > /home/user/log_generator.sh
#!/bin/bash
exec 3> /home/user/.hidden_log.txt
rm /home/user/.hidden_log.txt
echo "2023-10-10 10:00:00 [INFO] User login successful" >&3
echo "2023-10-10 10:00:01 [ERROR] Failed to load \"config.json\" - retrying" >&3
echo "2023-10-10 10:00:02 [WARN] Empty" >&3
while true; do
    sleep 3600
done
EOF
    chmod +x /home/user/log_generator.sh

    cat << 'EOF' > /home/user/filter_tool.c
#include <stdio.h>
#include <math.h>
#include <string.h>

int main(int argc, char **argv) {
    if (argc < 2) return 0;
    double score = sqrt(strlen(argv[1]));
    printf("%.2f\n", score);
    return 0;
}
EOF

    cat << 'EOF' > /home/user/build_tool.sh
#!/bin/bash
gcc filter_tool.c -o filter_tool
EOF
    chmod +x /home/user/build_tool.sh

    cat << 'EOF' > /home/user/process_logs.sh
#!/bin/bash
if [ -z "$1" ]; then echo "Usage: $0 <file>"; exit 1; fi

exec 4< "$1"
while :; do
    read -r line <&4
    status=$?
    if [ $status -ne 0 ] && [ -z "$line" ]; then
        # Reached EOF
        continue
    fi

    level=$(echo "$line" | cut -d' ' -f3)
    msg=$(echo "$line" | cut -d' ' -f4-)

    if [ "$level" == "[ERROR]" ]; then
        score=$(./filter_tool $msg)
        echo "Error score: $score"
    fi
done
EOF
    chmod +x /home/user/process_logs.sh

    chmod -R 777 /home/user