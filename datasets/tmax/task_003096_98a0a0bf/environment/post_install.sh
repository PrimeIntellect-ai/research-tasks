apt-get update && apt-get install -y python3 python3-pip gcc upx-ucl
    pip3 install pytest

    # Create the archiver binary
    mkdir -p /app
    cat << 'EOF' > /app/wrapper.c
#include <stdio.h>
int main(int argc, char *argv[]) {
    return 0;
}
EOF
    gcc -O2 /app/wrapper.c -o /app/archiver
    strip /app/archiver
    upx /app/archiver || true

    # Create source data
    mkdir -p /home/user/source_data
    for i in $(seq 1 10); do
        echo "dummy_data_$i" > /home/user/source_data/file_$i.txt
    done

    # Create layout.conf
    echo "extracted/dirX/file=file_1.txt" > /home/user/layout.conf

    # Create user and set permissions
    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user