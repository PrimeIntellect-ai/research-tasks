apt-get update && apt-get install -y python3 python3-pip gcc binutils
pip3 install pytest pyelftools

useradd -m -s /bin/bash user || true

mkdir -p /home/user/incoming /home/user/scripts /home/user/docs_target /home/user/system_conf
mkdir -p /tmp/build

# Create vulnerable extract script
cat << 'EOF' > /home/user/scripts/extract.py
import tarfile
import sys
import os

def extract_archive(tar_path, dest_dir):
    with tarfile.open(tar_path, 'r') as tar:
        tar.extractall(path=dest_dir)

if __name__ == "__main__":
    extract_archive(sys.argv[1], sys.argv[2])
EOF

# Create malicious file
echo "hacked" > /tmp/malicious.txt

# Create firmware.elf and pad it to > 5KB
echo "int main(){return 0;}" > /tmp/build/dummy.c
gcc -o /tmp/build/firmware.elf /tmp/build/dummy.c
dd if=/dev/zero bs=1024 count=6 >> /tmp/build/firmware.elf

# Create calibration.gcode
cat << 'EOF' > /tmp/build/calibration.gcode
G28
G1 X10 Y10 F1000
G1 X20 Y20 E2.5
G1 X30 Y30 E4.2
G1 X40 Y40 E6.8
G0 Z10
EOF

# Create compile.log
cat << 'EOF' > /tmp/build/compile.log
[2023-10-24] INFO Starting build...
[2023-10-24] WARNING Skipping missing optional header
[2023-10-24] FATAL Linker error: out of memory
  at module hardware_init.c:120
  memory map exhausted
[2023-10-24] INFO Cleaning up
EOF

# Create the malicious tarball
cat << 'EOF' > /tmp/make_tar.py
import tarfile

with tarfile.open('/home/user/incoming/release_data.tar', 'w') as tar:
    # Malicious file attempting directory traversal
    tar.add('/tmp/malicious.txt', arcname='../../home/user/system_conf/hacked.txt')

    # Valid files
    tar.add('/tmp/build/firmware.elf', arcname='firmware.elf')
    tar.add('/tmp/build/calibration.gcode', arcname='calibration.gcode')
    tar.add('/tmp/build/compile.log', arcname='compile.log')
EOF

python3 /tmp/make_tar.py

# Cleanup tmp build files
rm -rf /tmp/build /tmp/malicious.txt /tmp/make_tar.py

chmod -R 777 /home/user