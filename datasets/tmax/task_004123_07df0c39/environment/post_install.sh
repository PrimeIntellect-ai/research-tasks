apt-get update && apt-get install -y python3 python3-pip curl postgresql cargo build-essential
    pip3 install pytest

    # Install MongoDB binaries to avoid repo issues and save time
    curl -O https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-ubuntu2204-6.0.8.tgz
    tar -zxvf mongodb-linux-x86_64-ubuntu2204-6.0.8.tgz
    cp mongodb-linux-x86_64-ubuntu2204-6.0.8/bin/* /usr/local/bin/
    rm -rf mongodb-linux-x86_64-ubuntu2204-6.0.8*

    useradd -m -s /bin/bash user || true

    mkdir -p /app
    cat << 'EOF' > /app/start_services.sh
#!/bin/bash
service postgresql start
mkdir -p /data/db
mongod --fork --logpath /var/log/mongodb.log
EOF
    chmod +x /app/start_services.sh

    cat << 'EOF' > /app/oracle_auditor
#!/bin/bash
echo '{"path_exists": false, "shortest_path_length": null, "roles_involved": []}'
EOF
    chmod +x /app/oracle_auditor

    cat << 'EOF' > /home/user/db_config.env
PG_URL=postgres://postgres:postgres@localhost:5432/compliance_iam
MONGO_URL=mongodb://localhost:27017
EOF

    chmod -R 777 /home/user
    chmod -R 777 /app