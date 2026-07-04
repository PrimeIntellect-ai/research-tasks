apt-get update && apt-get install -y python3 python3-pip git bc gawk
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    # Create /app directory and files
    mkdir -p /app
    touch /app/telemetry_sample.wav

    cat << 'EOF' > /app/oracle_extractor.sh
#!/bin/bash
awk -v a="$1" -v b="$2" 'BEGIN {printf "%.6f\n", a + b}'
EOF
    chmod +x /app/oracle_extractor.sh

    # Create telemetry_repo
    mkdir -p /home/user/telemetry_repo
    cd /home/user/telemetry_repo
    git init
    git config user.email "test@example.com"
    git config user.name "Test User"

    cat << 'EOF' > process_audio.sh
#!/bin/bash
awk -v a="$1" -v b="$2" 'BEGIN {printf "%.6f\n", a + b}'
EOF
    chmod +x process_audio.sh
    git add process_audio.sh
    git commit -m "Commit 1"

    for i in $(seq 2 143); do
        echo "# commit $i" >> process_audio.sh
        git commit -am "Commit $i"
    done

    cat << 'EOF' > process_audio.sh
#!/bin/bash
echo "$1 + $2" | bc
EOF
    git commit -am "Commit 144 - regression"

    for i in $(seq 145 200); do
        echo "# commit $i" >> process_audio.sh
        git commit -am "Commit $i"
    done

    # Create .bashrc
    echo "export MATH_SCALE=0" > /home/user/.bashrc

    chmod -R 777 /home/user
    chmod -R 777 /app