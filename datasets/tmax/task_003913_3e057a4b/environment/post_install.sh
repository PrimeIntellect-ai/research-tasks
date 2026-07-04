apt-get update && apt-get install -y python3 python3-pip git build-essential
    pip3 install pytest

    # Create directories
    mkdir -p /app/corpora/evil
    mkdir -p /app/corpora/clean
    mkdir -p /home/user

    # Create dummy video and pcap files
    touch /app/crash_demo.mp4
    touch /app/traffic.pcap

    # Create dummy corpora
    echo -ne "\x42\x00\x05hello" > /app/corpora/clean/1.bin
    echo -ne "\x42\x00\xffevil" > /app/corpora/evil/1.bin

    # Setup the git repository
    mkdir -p /home/user/packetd_repo
    cd /home/user/packetd_repo
    git init
    git config user.email "test@example.com"
    git config user.name "Test User"
    git config init.defaultBranch master

    echo "#include <string.h>" > packetd.c
    echo "int main() { return 0; }" >> packetd.c
    git add packetd.c
    git commit -m "Initial commit"
    git tag v1.0

    # Add commits
    for i in $(seq 1 140); do
        echo "// commit $i" >> packetd.c
        git commit -am "Commit $i"
    done

    # The bad commit (removes bounds check)
    echo "void process_tlv(char *data, int len) { char buf[10]; memcpy(buf, data, len); }" >> packetd.c
    git commit -am "Refactor TLV processing"

    # More commits
    for i in $(seq 142 200); do
        echo "// commit $i" >> packetd.c
        git commit -am "Commit $i"
    done

    # Create user and set permissions
    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user /app