apt-get update && apt-get install -y python3 python3-pip
pip3 install pytest psycopg2-binary pymongo networkx

mkdir -p /app/corpus/clean
mkdir -p /app/corpus/evil

useradd -m -s /bin/bash user || true
chmod -R 777 /home/user