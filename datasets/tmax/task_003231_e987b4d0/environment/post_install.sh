apt-get update && apt-get install -y python3 python3-pip git
pip3 install pytest

mkdir -p /home/user/math_evaluator
cd /home/user/math_evaluator
git init
git config user.name "Test User"
git config user.email "test@example.com"

# Create the initial robust python script
cat << 'EOF' > evaluate.py
import sys
import json
import base64
import ast

def evaluate():
    if len(sys.argv) != 2:
        print(json.dumps({"error": "Missing argument"}))
        sys.exit(0)

    try:
        data = json.loads(sys.argv[1])
        b64_str = data.get("expr_b64", "")
        # Robust decoding
        raw_bytes = base64.b64decode(b64_str)
        expr = raw_bytes.decode('utf-8', errors='replace')

        # Dummy math evaluation (safe eval of simple math)
        node = ast.parse(expr, mode='eval')
        # Just returning success for dummy purposes
        print(json.dumps({"result": "evaluated"}))
        sys.exit(0)
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(0)

if __name__ == "__main__":
    evaluate()
EOF

git add evaluate.py
git commit -m "Initial robust mathematical parser"

# Create 200 commits. Introduce the bug at commit 142.
for i in $(seq 1 200); do
    if [ $i -eq 142 ]; then
        # Introduce regression: strict utf-8 decoding which throws UnicodeDecodeError on invalid bytes
        cat << 'EOF' > evaluate.py
import sys
import json
import base64
import ast

def evaluate():
    if len(sys.argv) != 2:
        print(json.dumps({"error": "Missing argument"}))
        sys.exit(0)

    try:
        data = json.loads(sys.argv[1])
        b64_str = data.get("expr_b64", "")
        # BUG: Removed errors='replace', will now throw UnicodeDecodeError on invalid UTF-8
        raw_bytes = base64.b64decode(b64_str)
        expr = raw_bytes.decode('utf-8')

        node = ast.parse(expr, mode='eval')
        print(json.dumps({"result": "evaluated"}))
        sys.exit(0)
    except json.JSONDecodeError as e:
        print(json.dumps({"error": "json error"}))
        sys.exit(0)
    except SyntaxError as e:
        print(json.dumps({"error": "syntax error"}))
        sys.exit(0)
    except TypeError as e:
        print(json.dumps({"error": "type error"}))
        sys.exit(0)
    # UnicodeDecodeError is no longer caught!

if __name__ == "__main__":
    evaluate()
EOF
        git add evaluate.py
        git commit -m "Update parser logic for expressions (Commit $i)"
        BAD_COMMIT=$(git rev-parse HEAD)
    else
        echo "# Comment $i" >> evaluate.py
        git add evaluate.py
        git commit -m "Minor update $i"
    fi
done

# Save the true bad commit to a hidden file for verification script
echo $BAD_COMMIT > /tmp/true_bad_commit.txt
chmod 777 /tmp/true_bad_commit.txt

useradd -m -s /bin/bash user || true
chmod -R 777 /home/user