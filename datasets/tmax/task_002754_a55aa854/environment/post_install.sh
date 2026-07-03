apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest

    # Create /app directory and start_services.sh
    mkdir -p /app
    cat << 'EOF' > /app/start_services.sh
#!/bin/bash
# Mock script to start services
echo "Starting PostgreSQL..."
echo "Starting Neo4j..."
EOF
    chmod +x /app/start_services.sh

    # Create user
    useradd -m -s /bin/bash user || true

    # Create config.env with dummy values
    cat << 'EOF' > /home/user/config.env
PGUSER=dummy
PGPASSWORD=dummy
NEO4J_USERNAME=dummy
NEO4J_PASSWORD=dummy
EOF

    # Create initial naive etl.sh
    cat << 'EOF' > /home/user/etl.sh
#!/bin/bash
source /home/user/config.env
# Naive ETL implementation
echo "Extracting and loading data naively..."
EOF
    chmod +x /home/user/etl.sh

    # Set permissions
    chmod -R 777 /home/user