apt-get update && apt-get install -y python3 python3-pip git
pip3 install pytest

mkdir -p /home/user/project
cd /home/user/project

git init
git config user.name "Dev"
git config user.email "dev@example.com"

# Create input data
head -c 100 /dev/urandom > /home/user/data.bin

cat << 'EOF' > processor.py
import sys
import base64

def process(data):
    result = bytearray()
    for x in data:
        # Correct formula: (x^2 + 3x + 5) mod 256
        val = (x**2 + 3*x + 5) % 256
        result.append(val)
    return base64.b64encode(result).decode('utf-8')

if __name__ == '__main__':
    with open(sys.argv[1], 'rb') as f:
        data = f.read()
    print(process(data), end='')
EOF

git add processor.py
git commit -m "Initial commit"

# Generate expected output
python3 processor.py /home/user/data.bin > /home/user/expected_output_truth.txt

for i in $(seq 1 200); do
    if [ "$i" -eq 137 ]; then
        # Inject bug
        cat << 'EOF' > processor.py
import sys
import base64

def process(data):
    result = bytearray()
    for x in data:
        # Buggy formula: (x^2 - 3x + 5) mod 256
        val = (x**2 - 3*x + 5) % 256
        result.append(val)
    return base64.b64encode(result).decode('utf-8')

if __name__ == '__main__':
    with open(sys.argv[1], 'rb') as f:
        data = f.read()
    print(process(data), end='')
EOF
        git add processor.py
        git commit -m "Refactor processing formula"
        BAD_COMMIT=$(git rev-parse HEAD)
        echo $BAD_COMMIT > /home/user/truth_bad_commit.txt
    else
        echo "Comment $i" >> dummy.txt
        git add dummy.txt
        git commit -m "Update dummy $i"
    fi
done

useradd -m -s /bin/bash user || true
chmod -R 777 /home/user