apt-get update && apt-get install -y python3 python3-pip
pip3 install pytest

mkdir -p /app
cat << 'EOF' > /app/legacy_archiver
#!/usr/bin/env python3
import sys
import os

if len(sys.argv) != 3:
    print("Usage: legacy_archiver <config_file> <data_directory>")
    sys.exit(1)

config_file = sys.argv[1]
data_dir = sys.argv[2]

exclude_ext = []
base_backup_dir = ""
follow_symlinks = False

if os.path.exists(config_file):
    with open(config_file, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'): continue
            if '=' in line:
                k, v = line.split('=', 1)
                k = k.strip()
                v = v.strip()
                if k == 'exclude_ext': 
                    exclude_ext = [x.strip() for x in v.split(',') if x.strip()]
                elif k == 'base_backup_dir': 
                    base_backup_dir = v
                elif k == 'follow_symlinks': 
                    follow_symlinks = (v.lower() == 'true')

results = []

for root, dirs, files in os.walk(data_dir, followlinks=follow_symlinks):
    for name in files:
        path = os.path.join(root, name)

        # Check if symlink and not following
        if os.path.islink(path) and not follow_symlinks:
            results.append(f"SKIP {path}")
            continue

        # Check exclude_ext
        ext = os.path.splitext(name)[1].lstrip('.')
        if ext in exclude_ext:
            results.append(f"SKIP {path}")
            continue

        # Check base_backup_dir
        rel_path = os.path.relpath(path, data_dir)
        dest_path = os.path.join(base_backup_dir, rel_path)

        if os.path.exists(dest_path):
            stat_src = os.stat(path)
            stat_dst = os.stat(dest_path)
            if stat_src.st_size == stat_dst.st_size and int(stat_src.st_mtime) == int(stat_dst.st_mtime):
                results.append(f"LINK {path} -> {dest_path}")
                continue

        results.append(f"COPY {path} -> {dest_path}")

results.sort()
for r in results:
    print(r)
EOF

chmod +x /app/legacy_archiver

useradd -m -s /bin/bash user || true
chmod -R 777 /home/user