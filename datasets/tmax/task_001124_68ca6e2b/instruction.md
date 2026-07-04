You are an automation specialist creating an ETL pipeline for video analytics. During a previous run, the pipeline encountered a retry error and generated duplicate records (frames). Your task is to extract features, compute similarities, and build a C-based tool to identify these near-duplicates.

Step 1: Frame Extraction
We have a video file located at `/app/input_video.mp4`.
Extract frames from this video at exactly 1 frame per second using `ffmpeg`. 
Scale the frames to 64x64 pixels, convert them to grayscale, and output them as raw 8-bit unsigned integer binaries (`.bin` files).
Save them in `/home/user/frames/` with names like `frame_001.bin`, `frame_002.bin`, etc. Each file should be exactly 4096 bytes.

Step 2: Feature Extraction and Similarity Tool
Write a C program at `/home/user/frame_hasher.c` and compile it to `/home/user/frame_hasher`.
This program must accept exactly two command-line arguments (paths to two raw `.bin` frame files) and compute a spatial average hash for each, then compute the Hamming distance between the hashes.

The hashing algorithm must strictly follow these steps to ensure bit-exact equivalence with our system:
1. Read the 4096-byte frame (64x64 pixels, row-major order).
2. Divide the image into an 8x8 grid of blocks. Each block is 8x8 pixels.
3. For each block `b` from 0 to 63 (where block 0 is top-left, block 1 is to its right, up to block 63 at bottom-right), compute the sum of its 64 pixels.
4. Calculate the block average `A_b = sum / 64` using standard integer division (truncation).
5. Calculate the global sum `G` of all 64 block averages (`A_b`).
6. Calculate the global average `A_g = G / 64` using integer division.
7. Construct a 64-bit unsigned integer hash. For each block `b` (from 0 to 63), if `A_b > A_g`, set the `b`-th bit of the hash to 1. Otherwise, set it to 0. (The 0-th bit corresponds to block 0, which is the least significant bit `1ULL << 0`).
8. Calculate the Hamming distance between the two 64-bit hashes (the number of bits that differ).

The program must print exactly the following to standard output:
```
Hash1: <16-character zero-padded lowercase hex string for file 1>
Hash2: <16-character zero-padded lowercase hex string for file 2>
Distance: <integer>
```

Step 3: Execution
Run your `/home/user/frame_hasher` tool to compare `frame_001.bin` and `frame_002.bin`. Save the standard output of this specific comparison to `/home/user/sample_output.txt`.