apt-get update && apt-get install -y \
        python3 python3-pip ffmpeg tesseract-ocr \
        fonts-dejavu-core libsm6 libxext6 libxrender-dev

    pip3 install pytest pytesseract opencv-python-headless numpy

    mkdir -p /app/backups /app/recovered_configs /truth

    # Generate video
    ffmpeg -f lavfi -i "color=c=black:s=640x480:d=10" -vf "drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:text='FATAL\: Infinite symlink loop detected in archive backup_8492.tar.gz':fontcolor=red:fontsize=20:x=(w-text_w)/2:y=(h-text_h)/2:enable='between(t,7,8)'" -c:v libx264 -pix_fmt yuv420p /app/symlink_crash.mp4

    # Generate archives and ground truth
    python3 -c "
import os
import json
import random
import tarfile

expected_report = {}

# 39 valid archives
for i in range(1, 40):
    archive_id = 1000 + i
    lines = [f'CONFIG_SET: key_{j}=val_{random.randint(1,100)}' for j in range(5)]
    expected_report[str(archive_id)] = [line.replace('CONFIG_SET: ', '') for line in lines]

    encoding = random.choice(['shift_jis', 'cp1252'])
    filename = f'config_garbled_{archive_id}.txt'

    # 1MB of null bytes to simulate padding without making the image huge
    content = b'\x00' * 1024 * 1024 
    for line in lines:
        content += (line + '\n').encode(encoding)
    content += b'\x00' * 1024 * 1024

    with open('tmp.txt', 'wb') as f:
        f.write(content)

    with tarfile.open(f'/app/backups/backup_{archive_id}.tar.gz', 'w:gz') as tar:
        tar.add('tmp.txt', arcname=filename)

# 10 corrupted archives
for i in range(40, 50):
    archive_id = 1000 + i
    with open(f'/app/backups/backup_{archive_id}.tar.gz', 'wb') as f:
        f.write(b'this is not a valid gzip file' * 100)

# 1 symlink loop archive
os.symlink('loop_symlink', 'loop_symlink')
with tarfile.open('/app/backups/backup_8492.tar.gz', 'w:gz') as tar:
    tar.add('loop_symlink')
os.remove('loop_symlink')
if os.path.exists('tmp.txt'):
    os.remove('tmp.txt')

with open('/truth/expected_report.json', 'w') as f:
    json.dump(expected_report, f)
"

    # Create evaluator script
    cat << 'EOF' > /truth/evaluate.py
import json
import sys

def evaluate():
    try:
        with open('/truth/expected_report.json', 'r') as f:
            expected = json.load(f)
        with open('/app/recovery_report.json', 'r') as f:
            actual = json.load(f)
    except Exception as e:
        print(f"Error reading JSON: {e}")
        sys.exit(1)

    total_keys = len(expected)
    correct_keys = 0

    for key, expected_list in expected.items():
        if key in actual:
            if sorted(actual[key]) == sorted(expected_list):
                correct_keys += 1

    accuracy = correct_keys / total_keys
    print(f"Accuracy: {accuracy:.4f}")

    if accuracy >= 0.95:
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    evaluate()
EOF

    useradd -m -s /bin/bash user || true
    chmod -R 777 /app /truth /home/user