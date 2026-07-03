You are assisting a researcher in organizing a large dataset of experimental recordings and sensor data. The task consists of two parts: building a robust C tool to filter corrupted sensor data files, and analyzing an experimental video recording to extract synchronization pulses.

**Part 1: Adversarial Dataset Filter (C Programming)**
The researcher's sensor data files are mixed with corrupted, malformed, and potentially malicious files. You need to write a C program that filters out the bad files.

Create a C program at `/home/user/dataset_filter.c` and compile it to `/home/user/dataset_filter`. 
The program must take exactly three arguments:
`./dataset_filter <input_dir> <output_dir> <manifest_file>`

Requirements for the C program:
1. **Recursive Traversal**: Recursively scan `<input_dir>` for all regular files.
2. **Memory-Mapped I/O**: Read each file using `mmap`.
3. **Validation**: A valid dataset file MUST meet all of the following structural conditions:
   - Starts with the magic bytes `DSF2` (4 bytes).
   - Followed by a 32-bit unsigned integer (little-endian) representing the `payload_length` (4 bytes).
   - The payload starts immediately after (at offset 8).
   - A 1-byte checksum located exactly at offset `8 + payload_length`. The checksum is the simple 8-bit XOR sum of all bytes in the payload.
   - The total file size must be exactly `9 + payload_length`.
4. **Atomic Writes**: For each valid file, copy it to `<output_dir>` (flattening the directory structure, just use the original filename). To ensure data integrity, write the data to a temporary file in `<output_dir>` first, then atomically rename it to the final filename. 
5. **Manifest Generation**: As valid files are successfully copied, append a line to `<manifest_file>` with the format: `<filename> <file_size>`.

We have provided a sample corpus containing both valid and corrupted files at `/app/corpus/clean/` and `/app/corpus/evil/`. Your program should accept 100% of the clean files and reject 100% of the evil files.

**Part 2: Video Synchronization Analysis**
The researcher also has a video recording of the experiment at `/app/experiment_video.mp4`. The video occasionally flashes a bright square in the center to indicate a synchronization pulse.

1. Extract the frames from `/app/experiment_video.mp4` (you can use `ffmpeg`, which is preinstalled).
2. Count the number of frames where the center 10x10 pixel region has an average grayscale brightness greater than 200 (on a 0-255 scale).
3. Write the integer count of these synchronization pulses to `/home/user/pulse_count.txt`.

Ensure your C code is efficient and handles file descriptors and memory mapping securely without leaks.