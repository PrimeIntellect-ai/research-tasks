apt-get update && apt-get install -y python3 python3-pip git openssl espeak
    pip3 install pytest

    mkdir -p /app

    # Generate the voicemail audio
    espeak -w /app/voicemail.wav "The password is delta uniform gamma seven three"

    # Create the oracle parser
    cat << 'EOF' > /app/oracle_parser.py
import sys
import base64
import json

def parse(b64_str):
    try:
        data = base64.b64decode(b64_str)
        if not data:
            return {"error": "empty"}
        header_length = data[0]
        if header_length > len(data):
            return {"error": "corrupted length"}
        return {"header_length": header_length, "payload_length": len(data) - header_length}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(json.dumps(parse(sys.argv[1])))
EOF
    python3 -m py_compile /app/oracle_parser.py
    mv /app/__pycache__/oracle_parser.*.pyc /app/oracle_parser.pyc
    rm -rf /app/oracle_parser.py /app/__pycache__

    # Create the git repository
    mkdir -p /tmp/repo
    cd /tmp/repo
    git init
    git config user.email "dev@example.com"
    git config user.name "Dev"

    cat << 'EOF' > parser.py
import sys
import base64
import json

def parse(b64_str):
    try:
        data = base64.b64decode(b64_str)
        if not data:
            return {"error": "empty"}
        header_length = data[0]
        if header_length > len(data):
            return {"error": "corrupted length"}
        return {"header_length": header_length, "payload_length": len(data) - header_length}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(json.dumps(parse(sys.argv[1])))
EOF

    cat << 'EOF' > test_pipeline.py
import subprocess
import sys
import json

def test():
    # Valid packet
    out = subprocess.check_output([sys.executable, "parser.py", "AQIDBA=="]).decode()
    assert json.loads(out)

    # Corrupted packet (header length 10, actual length 4) -> CgECAw==
    try:
        out = subprocess.check_output([sys.executable, "parser.py", "CgECAw=="]).decode()
        res = json.loads(out)
        assert res.get("error") == "corrupted length"
    except subprocess.CalledProcessError:
        sys.exit(1)

if __name__ == "__main__":
    test()
EOF

    git add parser.py test_pipeline.py
    git commit -m "Initial commit"

    # Create 120 good commits
    for i in $(seq 1 120); do
        echo "# $i" >> dummy.txt
        git add dummy.txt
        git commit -m "Good commit $i"
    done

    # Introduce bug
    cat << 'EOF' > parser.py
import sys
import base64
import json

def parse(b64_str):
    data = base64.b64decode(b64_str)
    if not data:
        return {"error": "empty"}
    header_length = data[0]
    payload = data[header_length:]
    if header_length > len(data):
        raise ValueError("corrupted length")
    return {"header_length": header_length, "payload_length": len(data) - header_length}

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(json.dumps(parse(sys.argv[1])))
EOF
    git add parser.py
    git commit -m "Introduce regression"

    # Create 79 more commits
    for i in $(seq 1 79); do
        echo "# bad $i" >> dummy.txt
        git add dummy.txt
        git commit -m "Bad commit $i"
    done

    cd /tmp
    tar -czf pipeline_repo.tar.gz repo
    # Encrypt without pbkdf2 to match the user's decryption command exactly if needed, though openssl 3 defaults to pbkdf2
    # We use -pbkdf2 to avoid warnings, but we'll just use the standard enc command
    openssl enc -aes-256-cbc -e -in pipeline_repo.tar.gz -out /app/pipeline_repo.tar.gz.enc -pass pass:deltauniformgammaseventhree -pbkdf2 || openssl enc -aes-256-cbc -e -in pipeline_repo.tar.gz -out /app/pipeline_repo.tar.gz.enc -pass pass:deltauniformgammaseventhree
    rm -rf /tmp/repo /tmp/pipeline_repo.tar.gz

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user
    chmod -R 777 /app