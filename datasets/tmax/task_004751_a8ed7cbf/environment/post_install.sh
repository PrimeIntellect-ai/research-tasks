apt-get update && apt-get install -y python3 python3-pip g++ libhiredis-dev docker.io docker-compose
    pip3 install pytest

    mkdir -p /home/user/pipeline/nginx
    mkdir -p /home/user/pipeline/flask
    mkdir -p /home/user/worker
    mkdir -p /home/user/data
    mkdir -p /home/user/tests/corpus

    cat << 'EOF' > /home/user/pipeline/docker-compose.yml
version: '3'
services:
  nginx:
    image: nginx:latest
    ports:
      - "8080:8080"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - flask
  flask:
    build: ./flask
    ports:
      - "5000:5000"
    depends_on:
      - redis
  redis:
    image: redis:latest
    ports:
      - "6379:6379"
EOF

    cat << 'EOF' > /home/user/pipeline/nginx/nginx.conf
events {}
http {
    server {
        listen 8080;
        location /api/ingest {
            # Missing proxy_pass
        }
    }
}
EOF

    cat << 'EOF' > /home/user/pipeline/flask/Dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app.py .
CMD ["python", "app.py"]
EOF

    cat << 'EOF' > /home/user/pipeline/flask/requirements.txt
flask
redis
EOF

    cat << 'EOF' > /home/user/pipeline/flask/app.py
from flask import Flask, request
import redis

app = Flask(__name__)
# Buggy redis connection
r = redis.Redis(host='dummy_host', port=9999)

@app.route('/api/ingest', methods=['POST'])
def ingest():
    data = request.get_data(as_text=True)
    r.lpush('raw_csv_queue', data)
    return "OK", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
EOF

    cat << 'EOF' > /home/user/data/reference_stats.csv
feature_id,mean,stddev
F1,10.0,2.0
F2,50.0,5.0
EOF

    cat << 'EOF' > /home/user/tests/corpus/clean.csv
batch_id,feature_id,val1,val2,val3,val4,val5,val6,val7,val8,val9,val10
B1,F1,10.1,9.9,10.0,10.2,9.8,10.0,10.1,9.9,10.0,10.0
EOF

    cat << 'EOF' > /home/user/tests/corpus/evil.csv
batch_id,feature_id,val1,val2,val3,val4,val5,val6,val7,val8,val9,val10
B2,F1,20.0,20.0,20.0,20.0,20.0,20.0,20.0,20.0,20.0,20.0
EOF

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user