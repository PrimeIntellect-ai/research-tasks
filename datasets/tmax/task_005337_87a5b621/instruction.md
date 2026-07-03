I am migrating a legacy Python 2 video processing pipeline to Python 3. The pipeline analyzes a video file, extracts raw frames, computes the average pixel intensity of each frame, and returns the sorted indices of the top 50 brightest frames. 

Because the pure Python implementation is too slow, I decided to rewrite the computationally heavy frame analysis step in Rust and call it from Python 3 using `ctypes`. However, I am stuck on a few issues:

1. My Rust code in `/home/user/rust_ext/src/lib.rs` fails to compile due to ownership and borrow checker errors during the sorting step.
2. Even when I bypass the borrow checker by commenting code out, the FFI integration has a memory safety bug causing undefined behavior (returning dangling pointers or corrupting the array passed from Python).
3. I need to make sure the pipeline actually works on the new test video located at `/app/test_video.mp4`.

Here is your task:
1. Fix the borrow checker and ownership errors in `/home/user/rust_ext/src/lib.rs`.
2. Fix the FFI signature and C-memory safety issues so that the Rust function safely populates the provided `out_indices` C-array.
3. Build the Rust project (`cargo build --release`).
4. Update the Python 3 wrapper `/home/user/fast_pipeline.py` if necessary so it correctly loads `librust_ext.so` (or `.dylib`) and calls the function.
5. Run your modified pipeline. Ensure it outputs a file named `/home/user/output_indices.txt` containing one integer (frame index) per line for the top 50 brightest frames.

The correctness and performance will be evaluated. Your Rust-accelerated Python 3 pipeline must produce the exact same top 50 indices as the reference implementation (`/home/user/reference.py`), but it must be significantly faster.

The automated test will calculate the speedup: `(Time of reference.py) / (Time of fast_pipeline.py)`. 
Your goal is to achieve a speedup of **>= 2.5x**.