apt-get update && apt-get install -y python3 python3-pip openssh-client
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    mkdir -p /home/user/uploads/keys
    mkdir -p /home/user/.ssh
    chmod 700 /home/user/.ssh

    cat << 'EOF' > /home/user/auth_token_gen.py
def validate_token(user, token):
    expected = ''.join([format(ord(c) ^ 0x42, '02x') for c in user])
    return token == expected
EOF

    python3 -c "import py_compile; py_compile.compile('/home/user/auth_token_gen.py', cfile='/home/user/auth_token_gen.pyc')"
    rm /home/user/auth_token_gen.py

    cat << 'EOF' > /home/user/upload_key.py
import argparse
import os
import auth_token_gen

parser = argparse.ArgumentParser()
parser.add_argument('--user', default='admin')
parser.add_argument('--token', required=True)
parser.add_argument('--filename', required=True)
parser.add_argument('--key_content', required=True)
args = parser.parse_args()

if not auth_token_gen.validate_token(args.user, args.token):
    print("Invalid token")
    exit(1)

out_path = os.path.join('/home/user/uploads/keys', args.filename)
with open(out_path, 'w') as f:
    f.write(args.key_content)
print("Key saved to", out_path)
EOF

    chmod -R 777 /home/user