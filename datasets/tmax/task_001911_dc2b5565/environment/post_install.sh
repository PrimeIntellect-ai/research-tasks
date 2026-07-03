apt-get update && apt-get install -y python3 python3-pip redis-server curl
    pip3 install pytest flask requests redis

    mkdir -p /app

    # Create the reference simulation script
    cat << 'EOF' > /app/ref_sim.py
import sys
import random

def main():
    N_steps = int(sys.argv[1])
    seed = int(sys.argv[2])
    p_right = float(sys.argv[3])
    L = int(sys.argv[4])

    random.seed(seed)
    pos = 0
    steps_taken = 0

    for _ in range(N_steps):
        steps_taken += 1
        r = random.random()
        if r < p_right:
            pos += 1
        else:
            pos -= 1
        if abs(pos) == L:
            break

    print(f"RESULT: {steps_taken}, {pos}")

if __name__ == "__main__":
    main()
EOF

    # Create the Flask API
    cat << 'EOF' > /app/flask_app.py
from flask import Flask, request, jsonify
app = Flask(__name__)
results = []

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    results.append(data)
    return jsonify({"status": "ok"}), 200

@app.route('/results', methods=['GET'])
def get_results():
    return jsonify(results), 200

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
EOF

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user /app