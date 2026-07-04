apt-get update && apt-get install -y python3 python3-pip curl gnupg
    pip3 install pytest

    # Add MongoDB repository
    curl -fsSL https://pgp.mongodb.com/server-6.0.asc | gpg --dearmor -o /usr/share/keyrings/mongodb-server-6.0.gpg
    echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-6.0.gpg ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/6.0 multiverse" > /etc/apt/sources.list.d/mongodb-org-6.0.list

    # Install required packages
    apt-get update
    apt-get install -y mongodb-org redis-server sqlite3 libhiredis-dev libsqlite3-dev build-essential cmake libmongoc-dev libbson-dev

    # Create user
    useradd -m -s /bin/bash user || true

    # Create SQLite database and logs table
    sqlite3 /home/user/access_logs.db "CREATE TABLE logs (log_id TEXT, emp_id TEXT, timestamp INTEGER, action TEXT);"

    chmod -R 777 /home/user