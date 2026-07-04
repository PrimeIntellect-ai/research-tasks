apt-get update && apt-get install -y python3 python3-pip gcc binutils coreutils
pip3 install pytest

useradd -m -s /bin/bash user || true

cat << 'EOF' > /tmp/mal.c
char *c2 = "c2.evil-empire.local";
int main() { return 0; }
EOF
gcc /tmp/mal.c -o /tmp/mal.elf
export B64_ELF=$(base64 -w 0 /tmp/mal.elf)

python3 -c "
import base64, json, os

def enc(d): 
    return base64.urlsafe_b64encode(json.dumps(d).encode()).decode().rstrip('=')

tokens = []
# Token 1
tokens.append(f'{enc({\"alg\": \"HS256\"})}.{enc({\"user\": \"guest\"})}.fake_sig_1')
# Token 2
tokens.append(f'{enc({\"alg\": \"HS256\"})}.{enc({\"user\": \"user2\"})}.fake_sig_2')
# Token 3
tokens.append(f'{enc({\"alg\": \"HS256\"})}.{enc({\"user\": \"user3\"})}.fake_sig_3')
# Token 4 (Malicious)
b64_elf = os.environ.get('B64_ELF', '')
tokens.append(f'{enc({\"alg\": \"none\"})}.{enc({\"user\": \"admin\", \"malware\": b64_elf})}.')
# Token 5
tokens.append(f'{enc({\"alg\": \"HS256\"})}.{enc({\"user\": \"user4\"})}.fake_sig_4')

with open('/home/user/jwt_logs.txt', 'w') as f:
    for t in tokens:
        f.write(t + '\n')
"

chown user:user /home/user/jwt_logs.txt
chmod -R 777 /home/user