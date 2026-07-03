apt-get update && apt-get install -y python3 python3-pip golang nginx
    pip3 install pytest

    mkdir -p /app
    cat << 'EOF' > /app/legacy_packer
#!/usr/bin/env python3
import json
import sys

def main():
    try:
        if len(sys.argv) > 1:
            with open(sys.argv[1], 'r') as f:
                assets = json.load(f)
        else:
            assets = json.load(sys.stdin)
    except Exception:
        sys.exit(1)

    assets.sort(key=lambda x: x['size'], reverse=True)
    bundles = []
    for a in assets:
        placed = False
        for b in bundles:
            if b['size'] + a['size'] <= 10000 and a['category'] not in b['cats']:
                b['items'].append(a['id'])
                b['size'] += a['size']
                b['cats'].add(a['category'])
                placed = True
                break
        if not placed:
            bundles.append({'items': [a['id']], 'size': a['size'], 'cats': {a['category']}})

    print(json.dumps([b['items'] for b in bundles]))

if __name__ == '__main__':
    main()
EOF
    chmod +x /app/legacy_packer

    useradd -m -s /bin/bash user || true

    cat << 'EOF' > /tmp/gen_assets.py
import json, random
random.seed(42)
assets = []
for i in range(1000):
    assets.append({
        "id": f"asset_{i:04d}",
        "size": random.randint(100, 3000),
        "category": random.randint(1, 50)
    })
with open("/home/user/assets.json", "w") as f:
    json.dump(assets, f)
EOF
    python3 /tmp/gen_assets.py

    chmod -R 777 /home/user