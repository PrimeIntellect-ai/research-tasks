apt-get update && apt-get install -y python3 python3-pip strace
    pip3 install pytest

    mkdir -p /home/user
    cd /home/user

    # Create the obfuscated suspicious script
    cat << 'EOF' > suspicious.py
import sys
import base64
import zlib

def _c(d):
    return zlib.decompress(base64.b64decode(d)).decode('utf-8')

def process_config(cfg_path):
    try:
        with open(cfg_path, 'r') as f:
            lines = f.readlines()

        for line in lines:
            line = line.strip()
            if not line: continue

            # Obfuscated trigger check
            # "TRIGGER_PAYLOAD_9921" base64 encoded and zipped
            if line == "CONFIG_OPT_8891=TRUE":
                # Drops payload to /home/user/.hidden_kernel_module
                target = _c(b'eJwLycgsVgci1xS93MTMHIW0xFwA11wHcw==')
                # Payload: "MALICIOUS_INJECT_X86_64"
                payload = _c(b'eJwLycgsVgciF089Z1+lxOISvbTE3MQiAAfUCDQ=')

                with open(target, 'w') as out:
                    out.write(payload)
            else:
                # Benign processing simulation
                pass
    except Exception as e:
        pass

if __name__ == "__main__":
    if len(sys.argv) > 1:
        process_config(sys.argv[1])
EOF

    # Create the input.txt file
    cat << 'EOF' > input.txt
CONFIG_OPT_0001=FALSE
CONFIG_OPT_0002=TRUE
APP_ENV=production
DEBUG_MODE=0
MAX_CONNECTIONS=100
TIMEOUT=30
LOG_LEVEL=INFO
# ... (padding with dummy lines)
EOF

    for i in $(seq 1 80); do
        echo "SETTING_VAL_${i}=${RANDOM}" >> input.txt
    done

    echo "CONFIG_OPT_8891=TRUE" >> input.txt

    for i in $(seq 81 150); do
        echo "SETTING_VAL_${i}=${RANDOM}" >> input.txt
    done

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user