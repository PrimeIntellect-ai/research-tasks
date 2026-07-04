You are an AI assistant helping a data researcher safely organize active data streams. 

The researcher has an automated data collection process that continuously writes large binary files to the `/home/user/dataset/incoming/` directory. To avoid race conditions and safely archive the data without interrupting the collection, the collection script creates a `.ready` file when a dataset is complete.

Your task is to write a C++ program (at `/home/user/dataset/processor.cpp`) that watches this directory, safely processes the finalized datasets, and archives them.

Here are the exact requirements for your C++ program:
1. **Directory Watching**: The program must monitor the `/home/user/dataset/incoming/` directory. 
2. **Trigger**: Whenever a file named `<filename>.ready` appears, the program must process the corresponding `<filename>.dat` file.
3. **Chunking**: Read the `<filename>.dat` file and split it into chunks of exactly 100,000 bytes. Name the chunks `<filename>_part0.bin`, `<filename>_part1.bin`, etc., and save them to `/home/user/dataset/chunks/`. The last chunk may be smaller than 100,000 bytes.
4. **Manifest & Checksum**: For each chunk created, compute its SHA-256 checksum. Append the result to `/home/user/dataset/manifest.txt` in the exact format: `<checksum>  <chunk_filename>\n`. You may invoke standard coreutils (like `sha256sum`) from within your C++ code to compute the hashes.
5. **Hard Linking**: To maintain a fast, zero-copy archive of the original finalized files, create a hard link of the original `<filename>.dat` in the `/home/user/dataset/archive/` directory.
6. **Termination**: When the program detects a file named `DONE.ready`, it should gracefully exit.

**Setup Instructions:**
1. Create the necessary directories: `/home/user/dataset/incoming/`, `/home/user/dataset/chunks/`, and `/home/user/dataset/archive/`.
2. Write your C++ program to `/home/user/dataset/processor.cpp`.
3. Compile your program (e.g., using `g++ -std=c++17 -o /home/user/dataset/processor /home/user/dataset/processor.cpp`).
4. We have provided a test script at `/home/user/simulate_stream.sh` (you will need to create a dummy one for testing, but assume the real one exists during verification). Run your compiled `processor` in the background, then run the simulation script. Your program should automatically process the files and exit.

**Verification:**
An automated test suite will examine `/home/user/dataset/manifest.txt`, verify the exact chunk files in `/home/user/dataset/chunks/`, and ensure the hard links in `/home/user/dataset/archive/` point to the correct inodes.