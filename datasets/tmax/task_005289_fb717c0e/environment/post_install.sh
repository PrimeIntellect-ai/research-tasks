apt-get update && apt-get install -y python3 python3-pip gawk curl
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    mkdir -p /app/services/sensor_stream
    mkdir -p /app/services/aggregator_api

    cat << 'EOF' > /app/oracle_aggregate
#!/bin/bash
sort -n -k1,1 "$1" | awk '
NR==1 {x0=$1; y0=$2; sum=0}
NR>1 {
    x=$1; y=$2;
    sum += (x - x0) * (y + y0) / 2.0;
    x0=x; y0=y;
}
END {printf "%.6f\n", sum}'
EOF
    chmod +x /app/oracle_aggregate

    cat << 'EOF' > /app/start_services.sh
#!/bin/bash
echo "Starting services..."
EOF
    chmod +x /app/start_services.sh

    touch /home/user/config.env

    chmod -R 777 /home/user
    chmod -R 777 /app