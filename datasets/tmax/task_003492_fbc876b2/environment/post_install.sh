apt-get update && apt-get install -y python3 python3-pip imagemagick tesseract-ocr fonts-dejavu
    pip3 install pytest

    mkdir -p /app
    cat << 'EOF' > /app/rules.txt
POLYGLOT BUILD REQUEST VALIDATOR RULES
Syntax: REQ <target> [RATE <limit>] [EXPR <num1> <op> <num2>]

Rules:
1. <target> must be alphanumeric. If not, return {"error":"ERR_TARGET"}
2. <limit> is an integer. Default if omitted is 100.
3. If <limit> is strictly greater than 500, return {"error":"ERR_RATELIMIT"}
4. <op> can be +, -, or *. If <op> is /, return {"error":"ERR_DIV_UNSUPPORTED"}
5. If EXPR is omitted, default result is 0.
6. If everything is valid, evaluate the math expression and output JSON:
   {"tgt":"<target>","lim":<limit>,"val":<evaluated_result>}
EOF

    # Generate the image from text
    convert -background white -fill black -font DejaVu-Sans -pointsize 18 label:"$(cat /app/rules.txt)" /app/rules.png

    # Create the oracle parser
    cat << 'EOF' > /opt/oracle_parser
#!/usr/bin/env python3
import sys
import json

def run():
    if len(sys.argv) < 2:
        return
    s = sys.argv[1]
    parts = s.split()
    if len(parts) < 2 or parts[0] != "REQ":
        return

    target = parts[1]
    if not target.isalnum():
        print('{"error":"ERR_TARGET"}')
        return

    limit = 100
    idx = 2
    if idx < len(parts) and parts[idx] == 'RATE':
        limit = int(parts[idx+1])
        idx += 2

    if limit > 500:
        print('{"error":"ERR_RATELIMIT"}')
        return

    val = 0
    if idx < len(parts) and parts[idx] == 'EXPR':
        n1 = int(parts[idx+1])
        op = parts[idx+2]
        n2 = int(parts[idx+3])
        if op == '/':
            print('{"error":"ERR_DIV_UNSUPPORTED"}')
            return
        elif op == '+': val = n1 + n2
        elif op == '-': val = n1 - n2
        elif op == '*': val = n1 * n2

    print(json.dumps({"tgt": target, "lim": limit, "val": val}, separators=(',', ':')))

if __name__ == "__main__":
    run()
EOF
    chmod +x /opt/oracle_parser

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user