apt-get update && apt-get install -y python3 python3-pip golang docker.io docker-compose
pip3 install pytest redis psycopg2-binary numpy

mkdir -p /app

cat << 'EOF' > /app/docker-compose.yml
version: '3.8'
services:
  redis:
    image: redis:alpine
    ports:
      - "6379:6379"
  postgres:
    image: postgres:14-alpine
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: secret
      POSTGRES_DB: sensors
    ports:
      - "5432:5432"
EOF

cat << 'EOF' > /app/slow_processor.py
# Slow python processor implementation
EOF

cat << 'EOF' > /app/producer.py
# Producer implementation
EOF

useradd -m -s /bin/bash user || true
chmod -R 777 /home/user
chmod -R 777 /app