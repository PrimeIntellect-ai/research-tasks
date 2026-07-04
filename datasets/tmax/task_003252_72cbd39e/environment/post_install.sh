apt-get update && apt-get install -y python3 python3-pip ffmpeg fonts-dejavu-core
    pip3 install pytest

    # Create oracle directory and script
    mkdir -p /opt/oracle
    cat << 'EOF' > /opt/oracle/evasion_encoder.py
import sys
import json
import hashlib

def generate_payload(target_path, content):
    # To escape /var/www/uploads/, we need to go up 3 directories.
    if target_path.startswith('/'):
        target_path = target_path[1:]

    # Construct the conceptual traversal path
    traversal_path = "../../../" + target_path

    # Apply evasion substitutions in reverse to bypass IDS but resolve correctly post-normalization
    evaded_path = traversal_path.replace("../", "!-!")
    evaded_path = evaded_path.replace("root", "@_@")
    evaded_path = evaded_path.replace("etc", "~_~")

    # Generate signature
    salt = "SALT_81726354"
    signature = hashlib.sha256((evaded_path + salt).encode()).hexdigest()

    payload = {
        "filename": evaded_path,
        "content": content,
        "signature": signature
    }

    # Print deterministic JSON (sorted keys, no spaces)
    print(json.dumps(payload, separators=(',', ':'), sort_keys=True))

if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(1)
    generate_payload(sys.argv[1], sys.argv[2])
EOF
    chmod +x /opt/oracle/evasion_encoder.py

    # Create the task directory and the simulated WAF debug video
    mkdir -p /app
    cat << 'EOF' > /tmp/logic.txt
def handle_upload(filepath_header, content, signature):
    # 1. Signature Validation
    expected_sig = hashlib.sha256((filepath_header + "SALT_81726354").encode()).hexdigest()
    if signature != expected_sig: raise AuthError()

    # 2. IDS Pattern Matching
    if re.search(r'\.\./', filepath_header): raise IDS_Alert()
    if "root" in filepath_header: raise IDS_Alert()
    if "etc" in filepath_header: raise IDS_Alert()

    # 3. Normalization (Evasion markers replaced by backend)
    filepath_header = filepath_header.replace("!-!", "../")
    filepath_header = filepath_header.replace("@_@", "root")
    filepath_header = filepath_header.replace("~_~", "etc")

    # 4. File Write
    full_path = "/var/www/uploads/" + filepath_header
    write_file(full_path, content)
EOF

    # Generate a 1-second video displaying the backend logic
    ffmpeg -f lavfi -i color=c=black:s=1280x720:d=1 \
        -vf "drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:textfile=/tmp/logic.txt:fontcolor=white:fontsize=18:x=10:y=10" \
        -c:v libx264 /app/waf_debug.mp4
    rm /tmp/logic.txt

    # Create user and set permissions
    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user