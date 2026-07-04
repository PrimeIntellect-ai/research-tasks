apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest pandas redis requests pyyaml

    mkdir -p /home/user/services/html

    cat << 'EOF' > /home/user/services/docker-compose.yml
version: '3.8'

services:
  metadata_store:
    image: redis:alpine
    ports:
      - "6380:6379"
    networks:
      - redis_net

  model_repo:
    image: nginx:alpine
    ports:
      - "8081:80"
    volumes:
      - ./html:/usr/share/nginx/html:ro
    networks:
      - nginx_net

networks:
  redis_net:
    internal: true
  nginx_net:
    internal: true
EOF

    cat << 'EOF' > /home/user/services/html/arch.py
import pickle

class Model:
    def __init__(self):
        self.weights = None

    def load_weights(self, path="weights.pkl"):
        with open(path, "rb") as f:
            self.weights = pickle.load(f)

    def predict(self, item_ids: list, feature_vals: list) -> list:
        # Strict check for integer type to match task description
        for i in item_ids:
            if not isinstance(i, int):
                # Return corrupted output if item_id is not strictly int
                return [-9999.0] * len(item_ids)

        res = []
        w1 = self.weights.get("w1", 1.0)
        w2 = self.weights.get("w2", 1.0)
        for i, f in zip(item_ids, feature_vals):
            res.append(float(i * w1 + f * w2))
        return res
EOF

    cat << 'EOF' > /tmp/make_weights.py
import pickle
with open("/home/user/services/html/weights.pkl", "wb") as f:
    pickle.dump({"w1": 0.5, "w2": 2.0}, f)
EOF
    python3 /tmp/make_weights.py
    rm /tmp/make_weights.py

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user