I am a researcher dealing with a batch of proprietary sensor datasets, and I need help automating my data extraction pipeline. Currently, my file lists are malformed, and I need a C++ program to safely extract binary headers and generate a verified manifest. 

Please perform the following steps:

1. **Clean the File List**: In `/home/user/dataset/files.txt`, there is a list of data files, but they were generated on a Windows machine. Use text transformation tools (like `sed` or `awk`) to modify `/home/user/dataset/files.txt` in place so that all Windows paths (e.g., `C:\dataset\`) are replaced with the correct Linux path (`/home/user/dataset/`) and all backslashes (`\`) are converted to forward slashes (`/`).

2. **C++ Parsing and Manifest Generation**: Write a C++ program at `/home/user/parser.cpp` and compile it to `/home/user/parser`. The program must:
   - Read `/home/user/dataset/config.ini` to extract the `MAGIC_BYTES` value (in the format `MAGIC_BYTES=XXXX`).
   - Iterate through each valid file path listed in the cleaned `/home/user/dataset/files.txt`.
   - Open each binary `.dat` file and read its header. The header format (little-endian) is:
     - `Offset 0-3`: 4-byte char array (Magic bytes)
     - `Offset 4-7`: 4-byte unsigned integer (Sensor ID)
     - `Offset 8-15`: 8-byte unsigned integer (Timestamp)
   - Skip any file where the extracted Magic bytes do not exactly match the `MAGIC_BYTES` from the config.
   - For valid files, compute the SHA256 checksum of the *entire* `.dat` file (you may invoke standard system utilities like `sha256sum` from within your C++ code to do this).
   - Append the extracted metadata to `/home/user/manifest.csv` in the following format:
     `[Base Filename],[Sensor ID],[Timestamp],[SHA256 Checksum]`
     *(Example: `data1.dat,42,1680000000,abc123...`)*
   - **Crucial Requirement**: Because this script will eventually be run in a multi-processing environment, your C++ program **must** use explicit file locking (e.g., `flock()` or `fcntl()`) to acquire an exclusive lock on `/home/user/manifest.csv` before writing to it, and release the lock immediately after writing each line.

Execute your compiled C++ program so that `/home/user/manifest.csv` is fully generated.

Ensure `/home/user/manifest.csv` exists and contains the correct, comma-separated data. Do not include a header row in the CSV.