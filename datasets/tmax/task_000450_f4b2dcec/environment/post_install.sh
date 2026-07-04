apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest Pillow

    mkdir -p /app/build_logs
    mkdir -p /home/user/build

    # Create the image
    cat << 'EOF' > /tmp/make_image.py
from PIL import Image, ImageDraw
img = Image.new('RGB', (800, 100), color = (255, 255, 255))
d = ImageDraw.Draw(img)
d.text((10,10), "Hey, to fix the NaN issue, make sure to use CLIP=3.14 and EPS=1e-7 in the denominator.", fill=(0,0,0))
img.save('/app/slack_snippet.png')
EOF
    python3 /tmp/make_image.py
    rm /tmp/make_image.py

    # Create logs
    echo "2023-10-01T12:00:00Z [INFO] Compute node started." > /app/build_logs/compute_node.log
    echo "2023-10-01T12:00:01Z [INFO] Loading parameters." > /app/build_logs/param_server.log
    echo "2023-10-01T12:00:02Z [DEV NOTE] Update rule must be changed to: new_w = old_w - lr * (clipped_g / (abs(old_g) + EPS)). Clipping must bound gradients between -CLIP and CLIP." >> /app/build_logs/param_server.log
    echo "2023-10-01T12:00:03Z [ERROR] ZeroDivisionError detected." > /app/build_logs/validator.log

    # Create buggy script
    cat << 'EOF' > /home/user/build/optimizer.py
import argparse
import json

def update_weights(weights, gradients):
    lr = 0.01
    new_weights = []
    for w, g in zip(weights, gradients):
        # BUG: unstable update
        new_weights.append(w - lr * (g / abs(g))) 
    return new_weights

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--weights", type=str)
    parser.add_argument("--gradients", type=str)
    args = parser.parse_args()

    w = json.loads(args.weights)
    g = json.loads(args.gradients)
    print(json.dumps(update_weights(w, g)))
EOF

    # Create oracle
    cat << 'EOF' > /app/oracle_optimizer
#!/usr/bin/env python3
import argparse
import json

def update_weights(weights, gradients):
    lr = 0.01
    clip_val = 3.14
    eps = 1e-7
    new_weights = []
    for w, g in zip(weights, gradients):
        clipped_g = max(-clip_val, min(clip_val, g))
        new_w = w - lr * (clipped_g / (abs(g) + eps))
        new_weights.append(new_w)
    return new_weights

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--weights", type=str)
    parser.add_argument("--gradients", type=str)
    args = parser.parse_args()

    w = json.loads(args.weights)
    g = json.loads(args.gradients)
    print(json.dumps(update_weights(w, g)))
EOF
    chmod +x /app/oracle_optimizer

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user