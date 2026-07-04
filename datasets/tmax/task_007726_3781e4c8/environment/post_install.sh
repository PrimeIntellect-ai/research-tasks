apt-get update && apt-get install -y python3 python3-pip tar gzip coreutils
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    mkdir -p /home/user/artifacts

    # Create duplicate binaries
    dd if=/dev/urandom of=/tmp/base.bin bs=1K count=1 2>/dev/null
    cp /tmp/base.bin /home/user/artifacts/a_dup.bin
    cp /tmp/base.bin /home/user/artifacts/m_dup.bin
    cp /tmp/base.bin /home/user/artifacts/z_dup.bin

    # Create unique binary
    dd if=/dev/urandom of=/home/user/artifacts/unique.bin bs=1K count=1 2>/dev/null

    # Create text files
    echo "SERVER=DEV_SERVER\nDATA=123" > /home/user/artifacts/t1.txt
    echo "SERVER=PROD_SERVER\nDATA=456" > /home/user/artifacts/t2.txt
    echo "SERVER=DEV_SERVER\nDATA=789" > /home/user/artifacts/t3_archived.txt

    # Create inventory
    cat << 'EOF' > /home/user/artifacts/inventory.txt
a_dup.bin|binary|active
m_dup.bin|binary|active
z_dup.bin|binary|active
unique.bin|binary|active
t1.txt|text|active
t2.txt|text|active
t3_archived.txt|text|archived
EOF

    chown -R user:user /home/user
    chmod -R 777 /home/user