apt-get update && apt-get install -y python3 python3-pip openssh-client procps
pip3 install pytest

useradd -m -s /bin/bash user || true

cd /home/user
PASSWORD="Evasion_Payload_Pass_9921!"
ssh-keygen -t rsa -b 2048 -m PEM -f /home/user/target_key -N "$PASSWORD" -q

cat << 'EOF' > /home/user/simulate_admin.py
import time
import subprocess
import random

PASSWORD = "Evasion_Payload_Pass_9921!"

with open("/home/user/data_backup_worker", "w") as f:
    f.write("#!/bin/bash\nsleep 0.2\n")
import os
os.chmod("/home/user/data_backup_worker", 0o755)

while True:
    time.sleep(random.uniform(2.0, 3.0))
    subprocess.Popen(["/home/user/data_backup_worker", "--ssh-pass", PASSWORD])
EOF

chmod -R 777 /home/user