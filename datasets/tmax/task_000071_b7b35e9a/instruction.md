You are an artifact manager tasked with curating a local binary repository. 

A set of scientific artifact files are stored in the directory `/home/user/artifacts`. Some of these files are actively being rotated or written to by background processes (indicated by a `.tmp` extension), while others might be corrupted due to race conditions during past writes.

Your task is to write a C++ program at `/home/user/process_artifacts.cpp` that performs the following tasks:
1. Recursively traverse the directory `/home/user/artifacts`.
2. Find all files ending in `.bin`. You must strictly ignore any files ending in `.tmp` (even if they have `.bin` in the name, like `.bin.tmp`), as they are currently being written.
3. For each `.bin` file, open it using streaming or memory-mapped I/O and parse its binary contents. 
   - The file format strictly consists of a 4-byte little-endian magic number `0xDEADC0DE` at the very beginning.
   - This is followed by a sequence of 64-bit IEEE 754 double-precision floating-point numbers (little-endian).
4. Validate each `.bin` file:
   - If the file does not start with the exact magic number `0xDEADC0DE`, or if the remaining file size is not an exact multiple of 8 bytes (meaning a float was partially written), the file is considered corrupted.
   - If a file is corrupted, do not extract any numbers from it. Instead, append its absolute path (one per line) to `/home/user/corrupt.log`.
5. For valid `.bin` files, perform a format conversion:
   - Read all the double-precision floats.
   - Create a text file in the exact same directory, with the exact same base name, but with a `.txt` extension (e.g., `data.bin` becomes `data.txt`).
   - Write each float to this text file on a new line, formatted to exactly 4 decimal places (e.g., `3.1416`).

Once you have written the code, compile it using `g++ -std=c++17 -o /home/user/processor /home/user/process_artifacts.cpp` and execute the binary. 

Ensure that `/home/user/corrupt.log` and all resulting `.txt` files are correctly generated according to the specifications.