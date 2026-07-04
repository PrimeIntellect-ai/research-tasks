apt-get update && apt-get install -y python3 python3-pip git g++ make sqlite3 libsqlite3-dev
    pip3 install pytest

    mkdir -p /home/user/dispatch_service/src
    mkdir -p /home/user/dispatch_service/data
    mkdir -p /app

    # Audio fixture
    echo "The access token is ALPHA-TANGO-NINER." > "/app/dispatch call.wav"

    # Mock transcribe tool
    cat << 'EOF' > /usr/local/bin/transcribe
#!/bin/bash
if [ "$#" -ne 1 ]; then
    echo "Usage: transcribe <file>"
    exit 1
fi
if [ ! -f "$1" ]; then
    echo "File not found: $1"
    exit 1
fi
cat "$1"
EOF
    chmod +x /usr/local/bin/transcribe

    # Process audio script (with bug)
    cat << 'EOF' > /home/user/dispatch_service/process_audio.sh
#!/bin/bash
transcribe $1
EOF
    chmod +x /home/user/dispatch_service/process_audio.sh

    # C++ files
    cat << 'EOF' > /home/user/dispatch_service/src/distance.cpp
#include <cmath>
double haversine(double lat1, double lon1, double lat2, double lon2) {
    // Buggy implementation
    return std::sin(lat1) * std::sin(lat2);
}
EOF

    cat << 'EOF' > /home/user/dispatch_service/run_tests.sh
#!/bin/bash
# Mock test script
exit 1
EOF
    chmod +x /home/user/dispatch_service/run_tests.sh

    # Git repository setup
    cd /home/user/dispatch_service
    git init
    git config user.email "dev@dispatch.local"
    git config user.name "Dev"
    git add .
    git commit -m "Initial commit"

    for i in {1..20}; do
        echo "// commit $i" >> src/distance.cpp
        git commit -am "Commit $i"
    done

    # Database setup
    python3 -c "
import sqlite3
import shutil
import os

os.makedirs('/tmp/db', exist_ok=True)
conn = sqlite3.connect('/tmp/db/responders.db')
conn.execute('PRAGMA journal_mode=WAL')
conn.execute('CREATE TABLE responders(id TEXT, lat REAL, lon REAL)')
conn.execute('INSERT INTO responders VALUES (\"R-442\", 40.7128, -74.0060)')
conn.commit()

shutil.copy('/tmp/db/responders.db', '/home/user/dispatch_service/data/responders.db')
if os.path.exists('/tmp/db/responders.db-wal'):
    shutil.copy('/tmp/db/responders.db-wal', '/home/user/dispatch_service/data/responders.db-wal')
else:
    open('/home/user/dispatch_service/data/responders.db-wal', 'w').close()
"

    # Corrupt the database file
    dd if=/dev/urandom of=/home/user/dispatch_service/data/responders.db bs=16 count=1 conv=notrunc 2>/dev/null

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user
    chmod -R 777 /app