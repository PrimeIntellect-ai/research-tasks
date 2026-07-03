apt-get update && apt-get install -y python3 python3-pip rsync
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    cat << 'EOF' > /tmp/setup.py
import os
import struct
import gzip
import tarfile
import subprocess
import random

# Create directories
os.makedirs('/home/user/raw_data', exist_ok=True)
os.makedirs('/home/user/backups', exist_ok=True)

# Generate measurements.bin
bin_path = '/tmp/measurements.bin'
max_val_status_1 = 0

with open(bin_path, 'wb') as f:
    # Write 100,000 records
    for i in range(100000):
        timestamp = 1600000000 + i
        sensor_id = random.randint(1, 10)
        status = random.choice([0, 1, 2, 3])
        value = random.randint(0, 1000000)

        # Ensure we have a predictable max value to verify
        if i == 50000:
            status = 1
            value = 9999999

        if status == 1 and value > max_val_status_1:
            max_val_status_1 = value

        f.write(struct.pack('<IIII', timestamp, sensor_id, status, value))

# Create a notes.txt to make the tar interesting
notes_path = '/tmp/notes.txt'
with open(notes_path, 'w') as f:
    f.write("Sensor data collected from station Alpha.\n")

# Tar it up
tar_path = '/tmp/data.tar'
with tarfile.open(tar_path, 'w') as tar:
    tar.add(bin_path, arcname='measurements.bin')
    tar.add(notes_path, arcname='notes.txt')

# Gzip it
gz_path = '/tmp/data.tar.gz'
with open(tar_path, 'rb') as f_in, gzip.open(gz_path, 'wb') as f_out:
    f_out.writelines(f_in)

# XOR it with 0xAA
cst_path = '/tmp/data.cst'
with open(gz_path, 'rb') as f_in, open(cst_path, 'wb') as f_out:
    data = f_in.read()
    xored = bytearray(b ^ 0xAA for b in data)
    f_out.write(xored)

# Split into 500KB chunks (instead of 5MB so it actually splits for this small dataset)
subprocess.run(['split', '-b', '500k', cst_path, '/home/user/raw_data/sensor_dump.cst.'])

# Clean up tmp files
os.remove(bin_path)
os.remove(notes_path)
os.remove(tar_path)
os.remove(gz_path)
os.remove(cst_path)

# Write out ground truth metadata for validation script internally
with open('/tmp/ground_truth.txt', 'w') as f:
    f.write(str(max_val_status_1))
EOF

    python3 /tmp/setup.py
    rm /tmp/setup.py

    chmod -R 777 /home/user