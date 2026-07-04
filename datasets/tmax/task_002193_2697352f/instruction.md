You are a configuration management engineer for a large distributed system. Over time, the system generates thousands of slightly modified JSON configuration files, accumulating in `/home/user/configs`. Storing these naively consumes too much disk space.

Your task is to build a high-efficiency deduplicating configuration archiver in Python.

1. Write a script `/home/user/archive.py` that takes two arguments: an input directory and an output archive file path.
   - Example: `python3 /home/user/archive.py /home/user/configs /home/user/config_archive.bin`
   - It must read all files in the input directory, compute deltas to deduplicate common data, and write a single, atomically created archive file.
   - To help you, a stripped, compiled binary is provided at `/app/bsdiff_helper`. You can invoke it via subprocess to compute highly optimized binary patches between files. Run `/app/bsdiff_helper -h` to reverse-engineer its CLI arguments.

2. Write a script `/home/user/extract.py` that takes two arguments: an archive file path and an output directory.
   - Example: `python3 /home/user/extract.py /home/user/config_archive.bin /home/user/restored_configs`
   - It must read your custom binary archive format, stream or memory-map the data for efficiency, and atomically reconstruct the exact original directory of JSON files.

The automated verification test will evaluate your solution based on the **Compression Ratio** (which translates to the final archive size). 
Your output archive must perfectly restore the original directory. If the restoration is perfectly byte-for-byte identical to the original `/home/user/configs`, the test will measure the size of your archive. 

Your objective is to achieve an archive size of **strictly less than 2,000,000 bytes (2 MB)**. The raw `/home/user/configs` directory contains roughly 50 MB of JSON data with high redundancy.