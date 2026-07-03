apt-get update && apt-get install -y python3 python3-pip git g++ make strace
    pip3 install pytest

    mkdir -p /home/user/repo
    cd /home/user/repo

    git init
    git config user.email "test@example.com"
    git config user.name "Test User"

    cat << 'EOF' > event_logger.cpp
#include <iostream>
#include <fstream>

#ifndef TZ_PATH
#define TZ_PATH "/etc/localtime"
#endif

int main() {
    std::ifstream tz(TZ_PATH);
    if(!tz) {
        // Silent fallback
        return 0;
    }
    return 0;
}
EOF

    cat << 'EOF' > Makefile
all:
	g++ event_logger.cpp -o event_logger -DTZ_PATH=\"/etc/localtime\"
EOF

    git add event_logger.cpp Makefile
    git commit -m "Initial commit: Add event logger"

    for i in $(seq 1 200); do
        if [ $i -eq 137 ]; then
            sed -i 's|/etc/localtime|/etc/locatime|g' Makefile
            git commit -am "Refactor Makefile timezone path (commit $i)"
        else
            echo "// Dummy update $i" >> event_logger.cpp
            git commit -am "Update event_logger (commit $i)"
        fi
    done

    # Save the expected bad commit hash for verification
    git rev-parse HEAD~63 > /home/user/expected_bad_commit.txt

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user