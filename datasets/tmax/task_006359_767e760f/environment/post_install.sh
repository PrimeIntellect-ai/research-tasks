apt-get update && apt-get install -y python3 python3-pip golang
    pip3 install pytest

    mkdir -p /home/user/incoming
    mkdir -p /home/user/output

    cat << 'EOF' > /home/user/setup.py
import tarfile
import zipfile
import os
import io

# Create valid and malicious contents
db_valid = b'{"service":"db", "version":"1.0", "settings":{"port":5432}}'
db_malicious = b'{"service":"hack", "version":"9.9", "settings":{"root":true}}'

web_valid = b'{"service":"web", "version":"2.1", "settings":{"host":"localhost", "tls":true}}'
web_malicious = b'{"service":"hack2", "version":"9.9", "settings":{"root":true}}'

# Create db.zip
with zipfile.ZipFile('/home/user/incoming/db.zip', 'w') as z:
    z.writestr('../db_secret.json', db_malicious)
    z.writestr('db.json', db_valid)
    z.writestr('folder/../../etc/passwd', db_malicious)

# Create web.tar.gz
with tarfile.open('/home/user/incoming/web.tar.gz', 'w:gz') as t:
    # Malicious 1
    ti = tarfile.TarInfo('../../web_secret.json')
    ti.size = len(web_malicious)
    t.addfile(ti, io.BytesIO(web_malicious))

    # Malicious 2 (absolute path)
    ti_abs = tarfile.TarInfo('/etc/shadow')
    ti_abs.size = len(web_malicious)
    t.addfile(ti_abs, io.BytesIO(web_malicious))

    # Valid
    ti2 = tarfile.TarInfo('web_config.json')
    ti2.size = len(web_valid)
    t.addfile(ti2, io.BytesIO(web_valid))

# Pack both into backups.tar
with tarfile.open('/home/user/incoming/backups.tar', 'w') as t:
    t.add('/home/user/incoming/db.zip', arcname='db.zip')
    t.add('/home/user/incoming/web.tar.gz', arcname='web.tar.gz')

# Cleanup intermediate nested files
os.remove('/home/user/incoming/db.zip')
os.remove('/home/user/incoming/web.tar.gz')
EOF

    python3 /home/user/setup.py
    rm /home/user/setup.py

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user