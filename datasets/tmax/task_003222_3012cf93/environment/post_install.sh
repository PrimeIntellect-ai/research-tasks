apt-get update && apt-get install -y python3 python3-pip nginx
pip3 install pytest flask

mkdir -p /home/user/services

cat << 'EOF' > /home/user/services/user_service.py
from flask import Flask, jsonify
import hashlib
import random
app = Flask(__name__)

@app.route('/user/<user_id>')
def get_user(user_id):
    random.seed(user_id)
    return jsonify({"embedding": [random.uniform(-1, 1) for _ in range(5)]})

if __name__ == '__main__':
    app.run(port=8081)
EOF

cat << 'EOF' > /home/user/services/item_service.py
from flask import Flask, jsonify
import random
app = Flask(__name__)

@app.route('/item/<item_id>')
def get_item(item_id):
    random.seed(item_id)
    cats = ['book', 'clothing', 'electronics', 'home', 'toys', 'beauty']
    return jsonify({
        "category": random.choice(cats),
        "price": round(random.uniform(1.0, 500.0), 2)
    })

if __name__ == '__main__':
    app.run(port=8082)
EOF

cat << 'EOF' > /home/user/nginx.conf
events {}
http {
    server {
        listen 8000;
        # TODO: route /user/ to 127.0.0.1:8081
        # TODO: route /item/ to 127.0.0.1:8082
    }
}
EOF

cat << 'EOF' > /home/user/projection_matrix.csv
0.1,0.2,-0.1
-0.2,0.1,0.5
0.3,-0.3,0.1
0.0,0.4,-0.2
-0.1,-0.1,-0.1
0.5,0.0,0.0
0.0,0.5,0.0
0.0,0.0,0.5
-0.5,-0.5,-0.5
0.2,0.2,0.2
EOF

cat << 'EOF' > /tmp/oracle.py
import sys, json, math
import urllib.request

def run():
    data = json.loads(sys.argv[1])
    uid = data['user_id']
    iid = data['item_id']

    u_req = urllib.request.urlopen(f"http://127.0.0.1:8000/user/{uid}")
    u_data = json.loads(u_req.read())
    emb = u_data['embedding']

    i_req = urllib.request.urlopen(f"http://127.0.0.1:8000/item/{iid}")
    i_data = json.loads(i_req.read())
    cat = i_data['category']
    price = i_data['price']

    cats = ['book', 'clothing', 'electronics', 'home']
    onehot = [1.0 if cat == c else 0.0 for c in cats]

    price_feat = math.log10(price + 1.0)

    v = emb + onehot + [price_feat]

    with open('/home/user/projection_matrix.csv', 'r') as f:
        mat = [[float(x) for x in line.strip().split(',')] for line in f if line.strip()]

    out = [0.0, 0.0, 0.0]
    for i in range(10):
        for j in range(3):
            out[j] += v[i] * mat[i][j]

    print(f"{out[0]:.4f} {out[1]:.4f} {out[2]:.4f}")

if __name__ == '__main__':
    run()
EOF

useradd -m -s /bin/bash user || true
chmod -R 777 /home/user