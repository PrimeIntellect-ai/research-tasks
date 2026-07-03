I am a researcher dealing with a large batch of sensor data files, and I need a Python script to organize them efficiently without duplicating the data on disk.

In the directory `/home/user/raw_dataset/`, there are several large binary files with a `.dat` extension. Each file contains hundreds of megabytes of raw sensor readings, but the metadata we need is located in the file's header.

Here is the exact structure of the first 24 bytes (the header) of every `.dat` file:
- **Bytes 0-7:** A magic string, always `SNSR_DAT` (ASCII).
- **Bytes 8-15:** The Sensor ID (ASCII string padded with null bytes, e.g., `SENS0003`).
- **Bytes 16-23:** A UNIX timestamp representing the recording start time (64-bit unsigned integer, little-endian).

I need you to write and execute a Python script located at `/home/user/organize.py` that does the following:
1. Iterates over all `.dat` files in `/home/user/raw_dataset/`.
2. Uses Python's `mmap` module to map the file into memory and read the 24-byte header. (You must use `mmap` to avoid loading these large files into RAM).
3. Parses the Sensor ID and Timestamp from the header.
4. Creates a structured directory for the dataset at `/home/user/organized_dataset/`.
5. Creates a symbolic link for each file in the format: `/home/user/organized_dataset/{Sensor_ID}/{Timestamp}.dat`. The symlink must point to the absolute path of the original file in the raw dataset. 

For example, if a file `/home/user/raw_dataset/file_A.dat` has the sensor ID `SENS0001` and timestamp `1690000000`, your script should create the directory `/home/user/organized_dataset/SENS0001/` (if it doesn't exist) and create a symlink `/home/user/organized_dataset/SENS0001/1690000000.dat` pointing to `/home/user/raw_dataset/file_A.dat`.

Please write the script, run it, and leave the resulting symlinks in the `/home/user/organized_dataset/` directory.