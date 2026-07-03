# test_final_state.py

import os
import re

def test_phase1_directory_structure_and_links():
    base_dir = "/home/user/deploy_pkg/app"

    # Check directories
    for d in ['bin', 'logs', 'data', 'conf']:
        dir_path = os.path.join(base_dir, d)
        assert os.path.isdir(dir_path), f"Directory {dir_path} does not exist."

    # Check symlink
    symlink_path = os.path.join(base_dir, 'current')
    assert os.path.islink(symlink_path), f"{symlink_path} is not a symbolic link."

    target = os.readlink(symlink_path)
    assert target == "bin", f"Symlink points to '{target}' instead of 'bin'."

def test_phase2_identity_script():
    script_path = "/home/user/deploy_pkg/create_identities.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."

    with open(script_path, 'r') as f:
        content = f.read()

    # Groupadd
    assert re.search(r'groupadd\s+.*-g\s+2000\s+dataproc', content) or \
           re.search(r'groupadd\s+dataproc\s+.*-g\s+2000', content), \
           "Missing or incorrect groupadd command for dataproc (GID 2000)."

    # Useradd data_ingest
    assert re.search(r'useradd\s+.*-u\s+2001\s+.*-g\s+(2000|dataproc)\s+data_ingest', content) or \
           re.search(r'useradd\s+.*-g\s+(2000|dataproc)\s+.*-u\s+2001\s+data_ingest', content), \
           "Missing or incorrect useradd command for data_ingest (UID 2001, Group dataproc)."

    # Useradd data_export
    assert re.search(r'useradd\s+.*-u\s+2002\s+.*-g\s+(2000|dataproc)\s+data_export', content) or \
           re.search(r'useradd\s+.*-g\s+(2000|dataproc)\s+.*-u\s+2002\s+data_export', content), \
           "Missing or incorrect useradd command for data_export (UID 2002, Group dataproc)."

def test_phase3_fstab_append():
    fstab_path = "/home/user/deploy_pkg/fstab.append"
    assert os.path.isfile(fstab_path), f"File {fstab_path} does not exist."

    with open(fstab_path, 'r') as f:
        content = f.read()

    # Bind mount
    assert re.search(r'/var/log/dataproc\s+/app/logs\s+(none|bind)\s+bind\s+0\s+0', content), \
           "Missing or incorrect fstab entry for bind mount."

    # NFS mount
    assert re.search(r'10\.0\.0\.5:/export/data\s+/app/data\s+nfs4\s+ro\s+0\s+0', content), \
           "Missing or incorrect fstab entry for NFS mount."

def test_phase4_firewall_script():
    script_path = "/home/user/deploy_pkg/firewall.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."

    with open(script_path, 'r') as f:
        content = f.read()

    # INPUT TCP 8080
    assert re.search(r'iptables\s+-A\s+INPUT\s+.*-p\s+tcp\s+.*--dport\s+8080\s+.*-j\s+ACCEPT', content) or \
           re.search(r'iptables\s+-A\s+INPUT\s+.*--dport\s+8080\s+.*-p\s+tcp\s+.*-j\s+ACCEPT', content), \
           "Missing or incorrect iptables rule to allow incoming TCP port 8080."

    # PREROUTING REDIRECT
    assert re.search(r'iptables\s+-t\s+nat\s+-A\s+PREROUTING\s+.*-p\s+tcp\s+.*--dport\s+80\s+.*-j\s+REDIRECT\s+--to-ports?\s+8080', content), \
           "Missing or incorrect iptables rule to redirect port 80 to 8080."

    # INPUT DROP 192.168.1.100
    assert re.search(r'iptables\s+-A\s+INPUT\s+.*-s\s+192\.168\.1\.100\s+.*-j\s+DROP', content), \
           "Missing or incorrect iptables rule to drop traffic from 192.168.1.100."