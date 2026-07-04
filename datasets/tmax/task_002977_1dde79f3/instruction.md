You are an AI assistant helping a data researcher process a large set of simulated sensor data. The data is transferred in a custom, multi-part archived format to bypass certain firewall restrictions, and you need to build a multi-language processing pipeline to extract, analyze, and incrementally back up this data.

Your goal is to complete the following steps:

1. **Custom Decompression and Multi-part Archive Handling:**
   In `/home/user/raw_data/`, you will find three files: `sensor_dump.cst.aa`, `sensor_dump.cst.ab`, and `sensor_dump.cst.ac`. 
   These are split parts of a single custom-compressed file. The custom compression scheme is defined as follows:
   - The original file is a standard `tar` archive.
   - It was first compressed with `gzip`.
   - Then, every byte of the gzipped data was XORed with the hexadecimal value `0xAA`.
   - Finally, it was split into 5MB chunks.
   
   Write a Bash script or combine Bash with Python/C to reconstruct the file, reverse the XOR operation, decompress it, and extract the contents to a new directory: `/home/user/extracted_v1/`.

2. **Memory-Mapped I/O Analysis:**
   Inside the extracted tarball, there is a large binary file named `measurements.bin`. This file contains millions of contiguous 16-byte records.
   Each 16-byte record consists of 4 unsigned 32-bit integers (little-endian format):
   `[timestamp, sensor_id, status, value]`
   
   Write a Python script at `/home/user/analyze.py` that uses the `mmap` module to efficiently scan this binary file without loading it entirely into memory. 
   Find the maximum `value` among all records where `status` is exactly equal to `1`. 
   Write this single integer to `/home/user/max_value_report.txt`.

3. **Incremental Backups:**
   The researcher requires efficient backups using hard links to save disk space.
   - Create a full backup of `/home/user/extracted_v1/` at `/home/user/backups/v1/`.
   - Next, simulate an update by creating a new empty text file at `/home/user/extracted_v1/update.log`.
   - Now, create an incremental backup of `/home/user/extracted_v1/` at `/home/user/backups/v2/`. This backup MUST use hard links against `/home/user/backups/v1/` for any unchanged files (e.g., using `rsync --link-dest` or `cp -al`).

Ensure all scripts are executable and that the final state precisely matches the directory structures and file contents requested above. Do not delete the raw data files.