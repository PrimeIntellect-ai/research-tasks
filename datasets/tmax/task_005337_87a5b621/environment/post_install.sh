apt-get update && apt-get install -y python3 python3-pip ffmpeg cargo rustc
    pip3 install pytest

    mkdir -p /app
    # Generate a sample 10-second 30fps 640x360 h264 video
    ffmpeg -f lavfi -i testsrc=duration=10:size=640x360:rate=30 -c:v libx264 -pix_fmt yuv420p /app/test_video.mp4

    mkdir -p /home/user/rust_ext/src

    cat << 'EOF' > /home/user/reference.py
import subprocess
import sys
import time

def process_video(video_path):
    width, height = 640, 360
    cmd = ['ffmpeg', '-i', video_path, '-f', 'image2pipe', '-pix_fmt', 'gray', '-vcodec', 'rawvideo', '-']
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

    frame_size = width * height
    frame_idx = 0
    intensities = []

    while True:
        raw_frame = process.stdout.read(frame_size)
        if len(raw_frame) != frame_size:
            break

        # Inefficient sum in python
        total = sum(raw_frame)
        intensities.append((total, frame_idx))
        frame_idx += 1

    intensities.sort(key=lambda x: x[0], reverse=True)
    top_50 = [idx for total, idx in intensities[:50]]

    with open('/home/user/output_indices.txt', 'w') as f:
        for idx in top_50:
            f.write(f"{idx}\n")

if __name__ == "__main__":
    start = time.time()
    process_video('/app/test_video.mp4')
    print(f"Time: {time.time() - start}")
EOF

    cat << 'EOF' > /home/user/rust_ext/Cargo.toml
[package]
name = "rust_ext"
version = "0.1.0"
edition = "2021"

[lib]
crate-type = ["cdylib"]
EOF

    cat << 'EOF' > /home/user/rust_ext/src/lib.rs
#[no_mangle]
pub extern "C" fn process_frames(buffer: *const u8, num_frames: usize, frame_size: usize, out_indices: *mut u32) {
    if buffer.is_null() || out_indices.is_null() { return; }

    let data_slice = unsafe { std::slice::from_raw_parts(buffer, num_frames * frame_size) };

    let mut intensities = Vec::new();
    for i in 0..num_frames {
        let start = i * frame_size;
        let end = start + frame_size;
        let frame = &data_slice[start..end];

        let mut sum: u64 = 0;
        for &pixel in frame {
            sum += pixel as u64;
        }
        intensities.push((sum, i as u32));
    }

    // Borrow checker error: sorting by a closure that moves or borrows incorrectly, 
    // or just a naive implementation bug
    let mut sorted = intensities;
    sorted.sort_by(|a, b| b.0.cmp(&a.0));

    // Memory UB bug: passing back a dangling pointer or not writing to the out_indices correctly
    // The user needs to write:
    // let out_slice = unsafe { std::slice::from_raw_parts_mut(out_indices, 50) };
    // for i in 0..50 { out_slice[i] = sorted[i].1; }
}
EOF

    cat << 'EOF' > /home/user/fast_pipeline.py
import subprocess
import sys
import ctypes
import time

def process_video(video_path):
    width, height = 640, 360
    cmd = ['ffmpeg', '-i', video_path, '-f', 'image2pipe', '-pix_fmt', 'gray', '-vcodec', 'rawvideo', '-']
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

    raw_data = process.stdout.read()
    frame_size = width * height
    num_frames = len(raw_data) // frame_size

    # Load rust library
    lib = ctypes.CDLL('./rust_ext/target/release/librust_ext.so')
    lib.process_frames.argtypes = [ctypes.c_char_p, ctypes.c_size_t, ctypes.c_size_t, ctypes.POINTER(ctypes.c_uint32)]

    out_indices = (ctypes.c_uint32 * 50)()

    lib.process_frames(raw_data, num_frames, frame_size, out_indices)

    with open('/home/user/output_indices.txt', 'w') as f:
        for i in range(50):
            f.write(f"{out_indices[i]}\n")

if __name__ == "__main__":
    start = time.time()
    process_video('/app/test_video.mp4')
    print(f"Time: {time.time() - start}")
EOF

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user
    chmod -R 777 /app