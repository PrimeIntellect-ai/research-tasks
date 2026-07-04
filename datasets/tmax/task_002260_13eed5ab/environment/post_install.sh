apt-get update && apt-get install -y \
        python3 \
        python3-pip \
        ffmpeg \
        tesseract-ocr \
        extundelete \
        e2fsprogs \
        gawk \
        libglib2.0-0 \
        libsm6 \
        libxext6 \
        libxrender-dev

    pip3 install pytest opencv-python-headless numpy

    mkdir -p /app/.truth

    # Create expected CSV
    cat << 'EOF' > /app/.truth/expected.csv
Timestamp,Level,Metric,Value
2023-10-12T14:00:01,ERROR,MEM,98
2023-10-12T14:00:02,WARN,CPU,85
2023-10-12T14:00:03,INFO,IO,20
2023-10-12T14:00:04,INFO,NET,15
2023-10-12T14:00:05,ERROR,DISK,99
2023-10-12T14:00:06,WARN,MEM,88
2023-10-12T14:00:07,INFO,CPU,45
2023-10-12T14:00:08,ERROR,IO,95
2023-10-12T14:00:09,WARN,NET,60
2023-10-12T14:00:10,INFO,DISK,50
2023-10-12T14:00:11,ERROR,MEM,97
2023-10-12T14:00:12,WARN,CPU,82
2023-10-12T14:00:13,INFO,IO,25
2023-10-12T14:00:14,INFO,NET,18
2023-10-12T14:00:15,ERROR,DISK,96
EOF

    # Generate video
    cat << 'EOF' > /tmp/gen_vid.py
import cv2
import numpy as np

lines = [
    "[2023-10-12T14:00:01] [ERROR] MEM=98",
    "[2023-10-12T14:00:02] [WARN] CPU=85",
    "[2023-10-12T14:00:03] [INFO] IO=20",
    "[2023-10-12T14:00:04] [INFO] NET=15",
    "[2023-10-12T14:00:05] [ERROR] DISK=99",
    "[2023-10-12T14:00:06] [WARN] MEM=88",
    "[2023-10-12T14:00:07] [INFO] CPU=45",
    "[2023-10-12T14:00:08] [ERROR] IO=95",
    "[2023-10-12T14:00:09] [WARN] NET=60",
    "[2023-10-12T14:00:10] [INFO] DISK=50",
    "[2023-10-12T14:00:11] [ERROR] MEM=97",
    "[2023-10-12T14:00:12] [WARN] CPU=82",
    "[2023-10-12T14:00:13] [INFO] IO=25",
    "[2023-10-12T14:00:14] [INFO] NET=18",
    "[2023-10-12T14:00:15] [ERROR] DISK=96",
]

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('/app/crash_vid.mp4', fourcc, 1.0, (800, 200))

for i in range(0, 15, 3):
    img = np.zeros((200, 800, 3), dtype=np.uint8)
    for j in range(3):
        if i + j < 15:
            cv2.putText(img, lines[i+j], (10, 50 + j*50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
    out.write(img)

out.release()
EOF
    python3 /tmp/gen_vid.py

    # Create backup.img
    mkdir -p /tmp/img_content
    cat << 'EOF' > /tmp/img_content/parser.sh
#!/bin/bash
echo "Timestamp,Level,Metric,Value"
while read -r line; do
  if [[ -z "$line" ]]; then continue; fi
  while [[ "$line" == *" "* ]]; do
      ts=$(echo $line | awk '{print $1}')
      lvl=$(echo $line | awk '{print $2}')
      rest=$(echo $line | awk '{print $3}')
      if [[ "$rest" != *"="* ]]; then continue; fi
      metric=$(echo $rest | cut -d= -f1)
      val=$(echo $rest | cut -d= -f2)
      echo "$ts,$lvl,$metric,$val" | tr -d '[]'
      break
  done
done < "$1"
EOF
    chmod +x /tmp/img_content/parser.sh

    dd if=/dev/zero of=/app/backup.img bs=1M count=20
    mkfs.ext4 -d /tmp/img_content /app/backup.img
    debugfs -w -R "rm parser.sh" /app/backup.img

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user
    chmod -R 777 /app