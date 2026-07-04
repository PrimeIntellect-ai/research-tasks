apt-get update && apt-get install -y python3 python3-pip ffmpeg
    pip3 install pytest

    mkdir -p /app

    # Generate the video
    cat << 'EOF' > /tmp/gen_video.py
import sys
width, height = 640, 480
num_frames = 300
explosion_frame = 142

black_frame = b'\x00' * (width * height * 3)
white_pixels = int(width * height * 0.1) + 10 # slightly more than 10%
white_bytes = b'\xff' * (white_pixels * 3)
exploded_frame = white_bytes + b'\x00' * ((width * height - white_pixels) * 3)

for i in range(num_frames):
    if i < explosion_frame:
        sys.stdout.buffer.write(black_frame)
    else:
        sys.stdout.buffer.write(exploded_frame)
EOF

    python3 /tmp/gen_video.py | ffmpeg -y -f rawvideo -pixel_format rgb24 -video_size 640x480 -framerate 30 -i pipe:0 -c:v libx264rgb -crf 0 /app/particle_sim.mp4

    # Create the oracle program
    cat << 'EOF' > /app/oracle_stable_var
#!/usr/bin/env python3
import sys

def welford_var(values):
    n = 0
    mean = 0.0
    M2 = 0.0
    for x in values:
        n += 1
        delta = x - mean
        mean += delta / n
        delta2 = x - mean
        M2 += delta * delta
    if n < 2:
        return 0.0
    return M2 / (n - 1)

if __name__ == '__main__':
    args = sys.argv[1:]
    try:
        vals = [float(x) for x in args]
    except ValueError:
        vals = []
    print(f"{welford_var(vals):.6f}")
EOF
    chmod +x /app/oracle_stable_var

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user