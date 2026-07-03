apt-get update && apt-get install -y python3 python3-pip bc
    pip3 install pytest

    mkdir -p /home/user

    cat << 'EOF' > /home/user/simulate.sh
#!/bin/bash
if [ -z "$1" ]; then
    echo "Usage: $0 <k>"
    exit 1
fi
k=$1
echo "Initializing graph..."
echo "Running diffusion steps..."
# Energy = 10k^2 - 5k + 20. Target 50 is reached at k=2.00
energy=$(echo "scale=2; 10 * $k * $k - 5 * $k + 20" | bc -l)
printf "Node A: %0.2f\n" $(echo "$k * 1.5" | bc -l)
printf "Node B: %0.2f\n" $(echo "$k * 2.5" | bc -l)
printf "System Energy: %0.2f\n" "$energy"
EOF
    chmod +x /home/user/simulate.sh

    cat << 'EOF' > /home/user/golden.txt
Initializing graph...
Running diffusion steps...
Node A: 3.00
Node B: 5.00
System Energy: 50.00
EOF

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user