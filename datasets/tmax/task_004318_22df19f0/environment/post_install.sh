apt-get update && apt-get install -y python3 python3-pip ffmpeg
    pip3 install pytest numpy Pillow

    mkdir -p /app
    mkdir -p /tmp/frames

    python3 -c "
import numpy as np
from PIL import Image
for i in range(10):
    if 5 <= i <= 7:
        arr = np.full((128, 128, 3), 128, dtype=np.uint8)
    else:
        arr = np.random.randint(0, 256, (128, 128, 3), dtype=np.uint8)
    Image.fromarray(arr).save(f'/tmp/frames/frame_{i:02d}.png')
"

    ffmpeg -y -framerate 1 -i /tmp/frames/frame_%02d.png -c:v libx264 -pix_fmt yuv420p /app/experiment_record.mp4
    rm -rf /tmp/frames

    cat << 'EOF' > /tmp/oracle_analyze_frame.py
import sys
import numpy as np
from PIL import Image

def main():
    if len(sys.argv) < 2:
        return
    img_path = sys.argv[1]
    img = Image.open(img_path).convert('L')
    arr = np.array(img, dtype=np.float64).flatten()

    N = arr.size
    mean = np.mean(arr)
    std = np.std(arr, ddof=0)
    median = np.median(arr)

    if std < 5.0:
        print("0.00,0.00,0.00,0.00,0.00")
    else:
        margin = 1.96 * (std / np.sqrt(N))
        ci_lower = mean - margin
        ci_upper = mean + margin
        print("{:.2f},{:.2f},{:.2f},{:.2f},{:.2f}".format(mean, std, median, ci_lower, ci_upper))

if __name__ == "__main__":
    main()
EOF
    chmod +x /tmp/oracle_analyze_frame.py

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user