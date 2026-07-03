apt-get update && apt-get install -y python3 python3-pip redis-server ruby curl
    pip3 install pytest flask redis
    gem install redis

    mkdir -p /app/api /app/worker /app/tests/hidden_clean /app/tests/hidden_evil
    mkdir -p /home/user/data/clean /home/user/data/evil

    cat << 'EOF' > /app/start_services.sh
#!/bin/bash
redis-server --daemonize yes
python3 /app/api/app.py &
ruby /app/worker/processor.rb &
wait
EOF
    chmod +x /app/start_services.sh

    cat << 'EOF' > /app/api/app.py
from flask import Flask, request, jsonify
import redis
import json

app = Flask(__name__)
r = redis.Redis(host='localhost', port=6379, db=0)

@app.route('/ingest', methods=['POST'])
def ingest():
    data = request.json
    r.lpush('log_queue', json.dumps(data))
    return jsonify({"status": "queued"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001)
EOF

    cat << 'EOF' > /app/worker/processor.rb
require 'redis'
require 'json'

redis = Redis.new(host: "localhost", port: 6379)

def check_depth(obj, depth)
  raise "Crash" if depth > 4
  if obj.is_a?(Hash)
    obj.each { |_, v| check_depth(v, depth + 1) }
  elsif obj.is_a?(Array)
    obj.each { |v| check_depth(v, depth + 1) }
  end
end

loop do
  _, msg = redis.brpop("log_queue")
  begin
    if msg.include?('\u0000\u0000\u0000\u0000') || msg.include?("\x00\x00\x00\x00")
      raise "Crash: null bytes"
    end
    data = JSON.parse(msg)
    if data.key?('metadata')
      check_depth(data['metadata'], 1)
    end
    File.open('/tmp/processed_logs.txt', 'a') { |f| f.puts data.to_json }
  rescue => e
    exit 1
  end
end
EOF

    cat << 'EOF' > /tmp/generate_data.py
import json
import os

def write_json(path, data):
    with open(path, 'w') as f:
        json.dump(data, f)

# Clean
for i in range(50):
    write_json(f'/home/user/data/clean/clean_{i}.json', {"id": i, "metadata": {"a": {"b": {"c": "d"}}}})
for i in range(100):
    write_json(f'/app/tests/hidden_clean/clean_{i}.json', {"id": i, "metadata": {"a": {"b": {"c": "d"}}}})

# Evil
for i in range(25):
    write_json(f'/home/user/data/evil/evil_depth_{i}.json', {"id": i, "metadata": {"a": {"b": {"c": {"d": {"e": "f"}}}}}})
for i in range(25):
    write_json(f'/home/user/data/evil/evil_null_{i}.json', {"id": i, "data": "bad\x00\x00\x00\x00string"})

for i in range(50):
    write_json(f'/app/tests/hidden_evil/evil_depth_{i}.json', {"id": i, "metadata": {"a": {"b": {"c": {"d": {"e": "f"}}}}}})
for i in range(50):
    write_json(f'/app/tests/hidden_evil/evil_null_{i}.json', {"id": i, "data": "bad\x00\x00\x00\x00string"})
EOF
    python3 /tmp/generate_data.py

    useradd -m -s /bin/bash user || true
    chown -R user:user /app
    chmod -R 777 /home/user