You are an AI assistant helping a researcher organize and process dataset logs. 

The researcher has received a chunked, multi-part zip archive containing binary sensor data, located in `/home/user/dataset/`. The main archive file is `/home/user/dataset/archive.zip` (along with its split parts). 

Your task is to:
1. Reassemble and extract the multi-part archive to get the inner file `measurements.bin`. You may use any command-line tools available.
2. Write a C++ program at `/home/user/process.cpp` that reads `measurements.bin` using memory-mapped I/O (`mmap`). Memory mapping is strictly required by the researcher for performance reasons on larger datasets.
3. The binary file `measurements.bin` consists of contiguous 16-byte records. Each record is tightly packed (little-endian) with the following structure:
   - `id`: unsigned 32-bit integer
   - `timestamp`: unsigned 64-bit integer
   - `value`: 32-bit float
4. The C++ program must iterate through the memory-mapped file, find all records where `value >= 80.0`, and write them out to a CSV file located at `/home/user/high_values.csv`.
5. The output CSV must have a header `id,timestamp,value` and format the float value to exactly 2 decimal places. 

Compile your C++ program and run it so that the `/home/user/high_values.csv` file is successfully generated. Ensure all paths are absolute and your C++ program cleanly handles file descriptors and memory unmapping.