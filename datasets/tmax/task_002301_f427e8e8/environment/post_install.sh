apt-get update && apt-get install -y python3 python3-pip gcc make libgl1 libglib2.0-0
    pip3 install pytest opencv-python-headless numpy

    mkdir -p /app
    cat << 'EOF' > /app/gen_video.py
import cv2
import numpy as np

secret = "PIPELINE_OK"
bits = ''.join(f"{ord(c):08b}" for c in secret)

out = cv2.VideoWriter('/app/build_signal.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 10, (200, 200))
for b in bits:
    color = 255 if b == '1' else 0
    frame = np.full((200, 200, 3), color, dtype=np.uint8)
    out.write(frame)
out.release()
EOF
    python3 /app/gen_video.py
    rm /app/gen_video.py

    useradd -m -s /bin/bash user || true

    mkdir -p /home/user/pipeline_tools
    cat << 'EOF' > /home/user/pipeline_tools/alpha.c
void beta_func();
void alpha_func() {
}
EOF

    cat << 'EOF' > /home/user/pipeline_tools/beta.c
void alpha_func();
void beta_func() {
}
EOF

    cat << 'EOF' > /home/user/pipeline_tools/main.c
void alpha_func();
void beta_func();
int main() {
    alpha_func();
    beta_func();
    return 0;
}
EOF

    cat << 'EOF' > /home/user/pipeline_tools/Makefile
all: pipeline_test

libalpha.so: alpha.c
	gcc -shared -fPIC -o libalpha.so alpha.c -L. -lbeta

libbeta.so: beta.c
	gcc -shared -fPIC -o libbeta.so beta.c -L. -lalpha

pipeline_test: main.c libalpha.so libbeta.so
	gcc -o pipeline_test main.c -L. -lalpha -lbeta
EOF

    chmod -R 777 /home/user