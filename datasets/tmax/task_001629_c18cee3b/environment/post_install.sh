apt-get update && apt-get install -y python3 python3-pip bc gawk coreutils grep sed
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    mkdir -p /home/user/metrics
    mkdir -p /home/user/solution

    # The buggy bash script
    cat << 'EOF' > /home/user/metrics/process_stats.sh
#!/bin/bash
# process_stats.sh - calculates standard deviation of latencies
cat "$1" | awk '{
    sum += $1; 
    sumsq += $1 * $1;
} END {
    variance = sumsq/NR - (sum/NR)^2;
    print sqrt(variance);
}'
EOF
    chmod +x /home/user/metrics/process_stats.sh

    # The error log
    cat << 'EOF' > /home/user/metrics/error.log
awk: cmd. line:6: warning: sqrt: called with negative argument -1024
EOF

    # The memory dump (simulated with some binary garbage and the payload)
    head -c 1024 /dev/urandom > /home/user/metrics/mem.dump
    echo -n "[CRASH_CONTEXT] LAST_BUFFER: 100000000 100000001 100000002 100000003 100000004 [/CRASH_CONTEXT]" >> /home/user/metrics/mem.dump
    head -c 1024 /dev/urandom >> /home/user/metrics/mem.dump

    chmod -R 777 /home/user