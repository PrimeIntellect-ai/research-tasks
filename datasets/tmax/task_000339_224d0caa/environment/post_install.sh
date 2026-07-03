apt-get update && apt-get install -y python3 python3-pip git g++ make gdb
    pip3 install pytest

    # Create user home
    useradd -m -s /bin/bash user || true

    # Create required files in /home/user
    touch /home/user/steg_decoder.cpp
    touch /home/user/crash.core
    touch /home/user/trigger_payload.bin

    # Setup /app/lib-steg-transform git repository
    mkdir -p /app/lib-steg-transform/src
    cd /app/lib-steg-transform
    git init
    git config user.email "test@example.com"
    git config user.name "Test User"
    touch src/fft_math.cpp src/payload_extract.cpp Makefile
    git add .
    git commit -m "Initial commit"

    # Create bad commit
    echo "// bad commit" >> src/fft_math.cpp
    git add src/fft_math.cpp
    git commit -m "Bad commit"

    # Setup /opt/oracle
    mkdir -p /opt/oracle
    touch /opt/oracle/steg_decoder_golden
    chmod +x /opt/oracle/steg_decoder_golden

    # Ensure permissions
    chmod -R 777 /home/user
    chmod -R 777 /app/lib-steg-transform