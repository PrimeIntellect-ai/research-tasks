apt-get update && apt-get install -y python3 python3-pip imagemagick tesseract-ocr fonts-dejavu
    pip3 install pytest

    mkdir -p /app /home/user

    cat << 'EOF' > /home/user/leaky_parser.py
import sys

def parse(data):
    state = "IDLE"
    buffer = []
    output = []

    tokens = data.replace('\n', ' ').split()
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if state == "IDLE":
            if token == "START":
                state = "RECORD"
                buffer = []
            elif token == "ERROR":
                # BUG: Infinite loop memory leak
                buffer.append("err")
                continue
        elif state == "RECORD":
            if token == "END":
                output.append(" ".join(buffer))
                state = "IDLE"
                buffer = []
            elif token == "ERROR":
                state = "IDLE"
                buffer = []
            else:
                buffer.append(token)
        i += 1
    return "\n".join(output)

if __name__ == "__main__":
    print(parse(sys.stdin.read()))
EOF

    cat << 'EOF' > /app/oracle_parser
#!/usr/bin/env python3
import sys

def parse(data):
    state = "IDLE"
    buffer = []
    output = []

    tokens = data.replace('\n', ' ').split()
    for token in tokens:
        if state == "IDLE":
            if token == "START":
                state = "RECORD"
                buffer = []
        elif state == "RECORD":
            if token == "END":
                output.append(" ".join(buffer))
                state = "IDLE"
                buffer = []
            elif token == "ERROR":
                state = "IDLE"
                buffer = []
            else:
                buffer.append(token)
    return "\n".join(output)

if __name__ == "__main__":
    print(parse(sys.stdin.read()))
EOF
    chmod +x /app/oracle_parser

    echo "START a b c END ERROR ERROR ERROR" > /home/user/payload.txt

    convert -size 400x200 xc:white -font DejaVu-Sans -pointsize 18 -fill black \
    -draw "text 10,30 'PROTOCOL RULES:'" \
    -draw "text 10,60 '1. START begins record.'" \
    -draw "text 10,90 '2. END finishes record.'" \
    -draw "text 10,120 '3. ERROR aborts record.'" \
    /app/protocol.png

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user