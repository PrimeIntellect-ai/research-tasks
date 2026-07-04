apt-get update && apt-get install -y python3 python3-pip coreutils tar gzip
pip3 install pytest

mkdir -p /home/user/data
mkdir -p /home/user/backup_out

# Create random files with specified approximate sizes
dd if=/dev/urandom of=/home/user/data/file1.txt bs=1024 count=100
dd if=/dev/urandom of=/home/user/data/file2.txt bs=1024 count=120
dd if=/dev/urandom of=/home/user/data/file3.txt bs=1024 count=80

# Compute SHA256 of file1.txt
hash1=$(sha256sum /home/user/data/file1.txt | cut -d' ' -f1)

# Fake SHA256 for file2.txt
hash2_fake="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"

# Create baseline.txt
echo "$hash1  file1.txt" > /home/user/baseline.txt
echo "$hash2_fake  file2.txt" >> /home/user/baseline.txt

useradd -m -s /bin/bash user || true
chmod -R 777 /home/user