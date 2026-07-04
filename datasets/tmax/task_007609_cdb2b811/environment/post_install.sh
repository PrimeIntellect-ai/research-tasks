apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    mkdir -p /home/user/logs
    mkdir -p /home/user/bin

    cp /bin/ls /home/user/bin/backup_job

    cat << 'EOF' > /home/user/wordlist.txt
admin123
password
supersecret
opensesame
letmein99
winter2023
EOF

    cat << 'EOF' > /home/user/ps_dump.txt
UID        PID  PPID  C STIME TTY          TIME CMD
root         1     0  0 10:00 ?        00:00:01 /sbin/init
root       552     1  0 10:05 ?        00:00:00 /usr/sbin/sshd -D
user       998   552  0 10:15 pts/0    00:00:00 -bash
root      1045     1  0 10:20 ?        00:00:00 /home/user/bin/backup_job --verbose --auth-hash 43e9a4ab75570f5b1273574ed4a62174 --target /etc/shadow
user      1050   998  0 10:21 pts/0    00:00:00 ps -ef
EOF

    cat << 'EOF' > /home/user/logs/app_01.log
2023-10-01 10:00:01 INFO Starting backup
2023-10-01 10:00:02 DEBUG Auth attempted with password supersecret
2023-10-01 10:00:03 INFO Backup complete
EOF

    cat << 'EOF' > /home/user/logs/app_02.log
2023-10-02 11:00:01 WARN Failed login using supersecret
2023-10-02 11:05:00 INFO Retry success
EOF

    chown -R user:user /home/user
    chmod -R 777 /home/user
    # Restore the SUID bit that gets stripped by the recursive 777
    chmod 4755 /home/user/bin/backup_job