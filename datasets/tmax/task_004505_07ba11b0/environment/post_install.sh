apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest

    mkdir -p /home/user/logs
    mkdir -p /home/user/scripts

    cat << 'EOF' > /home/user/logs/access.log
192.168.1.15 - - [10/Oct/2023:13:55:36 -0700] "GET /index.html HTTP/1.1" 200 2326
10.0.5.22 - - [10/Oct/2023:13:56:01 -0700] "GET /search?q=<script>alert('XSS')</script> HTTP/1.1" 403 400
192.168.1.15 - - [10/Oct/2023:13:57:11 -0700] "GET /about.html HTTP/1.1" 200 1102
172.16.0.45 - - [10/Oct/2023:13:58:20 -0700] "POST /login HTTP/1.1" 200 532
10.0.5.22 - - [10/Oct/2023:13:59:05 -0700] "GET /search?q=<script>fetch('http://evil.com')</script> HTTP/1.1" 403 400
198.51.100.3 - - [10/Oct/2023:14:01:12 -0700] "GET /contact?msg=hello<script> HTTP/1.1" 403 400
172.16.0.45 - - [10/Oct/2023:14:02:10 -0700] "GET /dashboard HTTP/1.1" 200 1520
EOF

    cat << 'EOF' > /home/user/scripts/clean_temp.py
import os
import shutil

def clean():
    tmp_dir = "/tmp/app_cache"
    if os.path.exists(tmp_dir):
        shutil.rmtree(tmp_dir)
        print("Cache cleaned.")

if __name__ == "__main__":
    clean()
EOF

    cat << 'EOF' > /home/user/scripts/backup_manager.py
import os
import sys

def run_backup():
    if len(sys.argv) < 2:
        print("Usage: backup_manager.py <target_directory>")
        sys.exit(1)

    target = sys.argv[1]
    # VULNERABILITY: Unsanitized user input passed to os.system
    os.system("tar -czf /var/backups/archive.tar.gz " + target)

if __name__ == "__main__":
    run_backup()
EOF

    cat << 'EOF' > /home/user/scripts/log_rotate.py
import subprocess

def rotate():
    # Safe usage with subprocess.run and list arguments
    subprocess.run(["logrotate", "-f", "/etc/logrotate.conf"])

if __name__ == "__main__":
    rotate()
EOF

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user