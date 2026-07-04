apt-get update && apt-get install -y python3 python3-pip curl espeak sqlite3 build-essential
    pip3 install pytest

    # Install Rust
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
    export PATH="/root/.cargo/bin:$PATH"

    mkdir -p /app/corpora/evil
    mkdir -p /app/corpora/clean

    espeak "Filter out files having exactly fifty consecutive identical samples." -w /app/incident.wav

    # Setup Database
    sqlite3 /app/profiler.db "PRAGMA journal_mode=WAL; CREATE TABLE crash_logs (id INT, msg TEXT);"

    # Insert data and ensure WAL is not deleted by keeping connection open or disabling autocheckpoint
    python3 -c '
import sqlite3
conn = sqlite3.connect("/app/profiler.db")
conn.execute("PRAGMA journal_mode=WAL")
conn.execute("PRAGMA wal_autocheckpoint=0")
conn.execute("INSERT INTO crash_logs VALUES (1, \"AGC convergence failure detected. Root cause: repeated sample values. Listen to incident.wav for the exact threshold.\")")
conn.commit()
'
    # Ensure WAL exists, if not create it and put the string inside so it can be recovered
    if [ ! -f /app/profiler.db-wal ]; then
        touch /app/profiler.db-wal
        echo "AGC convergence failure detected. Root cause: repeated sample values. Listen to incident.wav for the exact threshold." >> /app/profiler.db-wal
    fi

    # Corrupt the SQLite header
    dd if=/dev/urandom of=/app/profiler.db bs=1 count=16 conv=notrunc

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user
    chmod -R 777 /app