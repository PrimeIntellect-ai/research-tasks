apt-get update && apt-get install -y python3 python3-pip curl gnupg sudo
    pip3 install pytest

    # Install PostgreSQL and MongoDB, plus Go
    curl -fsSL https://pgp.mongodb.com/server-6.0.asc | gpg -o /usr/share/keyrings/mongodb-server-6.0.gpg --dearmor
    echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-6.0.gpg ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/6.0 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-6.0.list
    apt-get update
    apt-get install -y mongodb-org postgresql golang-go

    mkdir -p /app/data

    # Generate CSV files
    python3 -c '
import csv, random
random.seed(42)

users = [{"id": i, "name": f"User_{i}", "signup_date": "2023-01-01"} for i in range(1, 1001)]
with open("/app/data/users.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["id", "name", "signup_date"])
    writer.writeheader()
    writer.writerows(users)

products = [{"id": i, "name": f"Product_{i}", "category": random.choice(["Electronics", "Books", "Clothing", "Home"])} for i in range(1, 501)]
with open("/app/data/products.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["id", "name", "category"])
    writer.writeheader()
    writer.writerows(products)

purchases = [{"id": i, "user_id": random.randint(1, 1000), "product_id": random.randint(1, 500), "amount_cents": random.randint(100, 10000)} for i in range(1, 5001)]
with open("/app/data/purchases.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["id", "user_id", "product_id", "amount_cents"])
    writer.writeheader()
    writer.writerows(purchases)

edges = [{"source_product_id": random.randint(1, 500), "target_product_id": random.randint(1, 500), "similarity_score": round(random.uniform(0.5, 1.0), 2)} for i in range(1, 2001)]
with open("/app/data/product_edges.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["source_product_id", "target_product_id", "similarity_score"])
    writer.writeheader()
    writer.writerows(edges)
'

    # Create start_services.sh
    cat << 'EOF' > /app/start_services.sh
#!/bin/bash
/etc/init.d/postgresql start
su - postgres -c "psql -tc \"SELECT 1 FROM pg_roles WHERE rolname='analyst'\" | grep -q 1 || psql -c \"CREATE USER analyst WITH PASSWORD 'data';\""
su - postgres -c "psql -tc \"SELECT 1 FROM pg_database WHERE datname='store'\" | grep -q 1 || psql -c \"CREATE DATABASE store OWNER analyst;\""
mkdir -p /data/db
mongod --fork --logpath /var/log/mongodb.log --dbpath /data/db
EOF
    chmod +x /app/start_services.sh

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user