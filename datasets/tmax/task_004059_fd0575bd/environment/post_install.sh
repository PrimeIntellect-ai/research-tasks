apt-get update && apt-get install -y python3 python3-pip procps coreutils
    pip3 install pytest

    mkdir -p /home/user/app /home/user/dumps /home/user/logs
    mkfifo /home/user/app/sensor_pipe

    cat << 'EOF' > /home/user/app/sensor_aggregator.sh
#!/bin/bash
declare -a ORPHANED_PAYLOADS # This is the leaking variable

cleanup() {
    rm -f /home/user/app/sensor_pipe
    exit 0
}
trap cleanup SIGINT SIGTERM

while read -r line; do
    if [[ $line == *"TYPE:ORPHAN"* ]]; then
        # BUG: Keeps appending to an array forever
        ORPHANED_PAYLOADS+=("$line")
    fi
    echo "Processed: $line" > /dev/null
done < /home/user/app/sensor_pipe
EOF
    chmod +x /home/user/app/sensor_aggregator.sh

    dd if=/dev/urandom of=/home/user/dumps/mem_core.dump bs=1M count=2
    for i in $(seq 1 5000); do
        echo "TYPE:ORPHAN TRACE_ID:TRC-88392 PAYLOAD:DROPPED_PRECISION_DATA_POINT_$(printf '%05d' $i)" >> /home/user/dumps/mem_core.dump
    done
    dd if=/dev/urandom of=/home/user/dumps/mem_core.dump bs=1M count=1 oflag=append conv=notrunc

    cat << 'EOF' > /home/user/logs/sensor.log
2023-10-12T10:00:01 INFO TRACE_ID:TRC-11223 TYPE:NORMAL
2023-10-12T10:05:22 WARN TRACE_ID:TRC-88392 TYPE:ORPHAN PAYLOAD:DROPPED_PRECISION_DATA_POINT_00001
2023-10-12T10:05:23 WARN TRACE_ID:TRC-88393 TYPE:ORPHAN PAYLOAD:DROPPED_PRECISION_DATA_POINT_00002
EOF

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user