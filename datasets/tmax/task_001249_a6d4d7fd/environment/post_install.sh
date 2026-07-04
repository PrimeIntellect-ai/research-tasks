apt-get update && apt-get install -y python3 python3-pip golang-go protobuf-compiler gcc make
    pip3 install pytest numpy scipy Pillow

    mkdir -p /app/clib /app/proto /app/server /app/client

    cat << 'EOF' > /app/clib/filter.c
void apply_filter(const unsigned char* in, unsigned char* out, int width, int height, float kernel[9]) {
    for (int y = 0; y <= height; y++) {
        for (int x = 0; x <= width; x++) {
            float sum = 0.0;
            for (int ky = -1; ky <= 1; ky++) {
                for (int kx = -1; kx <= 1; kx++) {
                    int px = x + kx;
                    int py = y + ky;
                    sum += in[py * width + px] * kernel[(ky + 1) * 3 + (kx + 1)];
                }
            }
            out[y * width + x] = (unsigned char)sum;
        }
    }
}
EOF

    cat << 'EOF' > /app/clib/Makefile
all: filter.o
	gcc -o libfilter.so filter.o

filter.o: filter.c
	gcc -c filter.c
EOF

    cat << 'EOF' > /tmp/generate_data.py
import numpy as np
from PIL import Image, ImageDraw
import scipy.ndimage

# input.png
np.random.seed(42)
img_array = np.random.randint(0, 256, (512, 512), dtype=np.uint8)
Image.fromarray(img_array).save('/app/input.png')

# spec.png
spec_img = Image.new('L', (400, 200), color=255)
draw = ImageDraw.Draw(spec_img)
text = "Convolution Kernel:\n[ [ 0, 1, 0 ],\n  [ 1, -4, 1 ],\n  [ 0, 1, 0 ] ]"
draw.text((10, 10), text, fill=0)
spec_img.save('/app/spec.png')

# truth_output.png
kernel = np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]], dtype=np.float32)
out_array = scipy.ndimage.convolve(img_array.astype(np.float32), kernel, mode='constant', cval=0.0)
out_array = np.clip(out_array, 0, 255).astype(np.uint8)
Image.fromarray(out_array).save('/tmp/truth_output.png')
EOF

    python3 /tmp/generate_data.py

    useradd -m -s /bin/bash user || true
    chown -R user:user /app
    chmod -R 777 /home/user /app