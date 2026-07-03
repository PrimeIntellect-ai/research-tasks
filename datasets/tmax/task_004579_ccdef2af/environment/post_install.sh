apt-get update && apt-get install -y python3 python3-pip g++ make ffmpeg
pip3 install pytest ffmpeg-python

mkdir -p /home/user/pipeline_tool/src
mkdir -p /home/user/pipeline_tool/lib
mkdir -p /app

cat << 'EOF' > /home/user/pipeline_tool/src/evaluator.cpp
#include <stdint.h>
#include <string.h>
#include <stdlib.h>

extern "C" {
    double evaluate_frame(const uint8_t* pixels, int width, int height, const char* expr) {
        // Buggy implementation
        double total = 0;
        int num_pixels = width * height;
        for (int i = 0; i <= num_pixels; ++i) { // out of bounds
            int r = pixels[i*3];
            int g = pixels[i*3+1];
            int b = pixels[i*3+2];
            // Integer division and precedence bugs
            total += r * 0.299 + g * 0.587 + b * 0.114;
        }
        return total / num_pixels;
    }
}
EOF

cat << 'EOF' > /home/user/pipeline_tool/build.sh
#!/bin/bash
mkdir -p lib
g++ src/evaluator.cpp -o lib/libevaluator.so
EOF
chmod +x /home/user/pipeline_tool/build.sh

cat << 'EOF' > /home/user/pipeline_tool/process.py
import sys
import ctypes
import json
import ffmpeg

def main():
    video_path = sys.argv[1]
    expr = sys.argv[2]
    out_path = sys.argv[3]

    lib = ctypes.CDLL('./lib/libevaluator.so')
    lib.evaluate_frame.restype = ctypes.c_double
    lib.evaluate_frame.argtypes = [ctypes.POINTER(ctypes.c_uint8), ctypes.c_int, ctypes.c_int, ctypes.c_char_p]

    probe = ffmpeg.probe(video_path)
    video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
    width = int(video_stream['width'])
    height = int(video_stream['height'])

    out, _ = (
        ffmpeg
        .input(video_path)
        .output('pipe:', format='rawvideo', pix_fmt='rgb24')
        .run(capture_stdout=True, capture_stderr=True)
    )

    frame_size = width * height * 3
    results = []

    for i in range(0, len(out), frame_size):
        frame_bytes = out[i:i+frame_size]
        if len(frame_bytes) < frame_size:
            break

        buffer = (ctypes.c_uint8 * frame_size).from_buffer_copy(frame_bytes)
        score = lib.evaluate_frame(buffer, width, height, expr.encode('utf-8'))
        results.append({"frame": len(results), "score": score})

    with open(out_path, 'w') as f:
        json.dump(results, f)

if __name__ == "__main__":
    main()
EOF

# Generate fixture video
ffmpeg -f lavfi -i testsrc=duration=1:size=32x32:rate=10 -c:v libx264 /app/test_recording.mp4

# Generate ground truth
cat << 'EOF' > /tmp/gen_truth.py
import json
import ffmpeg

out, _ = (
    ffmpeg
    .input('/app/test_recording.mp4')
    .output('pipe:', format='rawvideo', pix_fmt='rgb24')
    .run(capture_stdout=True, capture_stderr=True)
)

width = 32
height = 32
frame_size = width * height * 3
results = []

for i in range(0, len(out), frame_size):
    frame_bytes = out[i:i+frame_size]
    if len(frame_bytes) < frame_size:
        break

    score = 0
    for p in range(0, frame_size, 3):
        r = frame_bytes[p]
        g = frame_bytes[p+1]
        b = frame_bytes[p+2]
        score += r * 0.299 + g * 0.587 + b * 0.114
    score /= (width * height)
    results.append({"frame": len(results), "score": score})

with open('/app/truth.json', 'w') as f:
    json.dump(results, f)
EOF
python3 /tmp/gen_truth.py

useradd -m -s /bin/bash user || true
chown -R user:user /home/user
chmod -R 777 /home/user
chmod -R 777 /app