apt-get update && apt-get install -y python3 python3-pip wget
    pip3 install pytest pyinstaller arrow==1.2.3

    mkdir -p /app

    # Create the wrapper script
    cat << 'EOF' > /app/parse_logs.py
import sys
import os
sys.path.insert(0, '/app/arrow-1.2.3')
import arrow

if __name__ == '__main__':
    if len(sys.argv) > 1:
        print(arrow.get(sys.argv[1]).float_timestamp)
EOF

    # Create the oracle source and compile it
    cat << 'EOF' > /app/parse_logs_oracle_src.py
import sys
import arrow

if __name__ == '__main__':
    if len(sys.argv) > 1:
        print(arrow.get(sys.argv[1]).float_timestamp)
EOF

    cd /app
    pyinstaller --onefile parse_logs_oracle_src.py --distpath /app --name parse_logs_oracle
    chmod +x /app/parse_logs_oracle

    # Download and extract vendored arrow
    pip3 download arrow==1.2.3 --no-binary :all:
    tar xzf arrow-1.2.3.tar.gz

    # Apply perturbations (best-effort based on description)
    PARSER_FILE="/app/arrow-1.2.3/arrow/parser.py"
    if [ -f "$PARSER_FILE" ]; then
        sed -i 's/i += 1/if not (isinstance(token, str) and token in ["Z", "-", "+"]): i += 1/g' "$PARSER_FILE"
        sed -i 's/float(val)/float(val) * 0.1/g' "$PARSER_FILE"
    fi

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user
    chmod -R 777 /app