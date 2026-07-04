You are tasked with creating a C++ utility that acts as a configuration manager tracking changes to system binaries. 

A set of system updates has been dropped into the directory `/home/user/configs/`. This directory contains several JSON metadata files and corresponding ELF64 executable binaries. 

You must write a C++ program at `/home/user/config_tracker.cpp`, compile it to `/home/user/config_tracker`, and execute it against the `/home/user/configs/` directory.

Your program must perform the following steps:

1. **Parse Metadata**: Scan `/home/user/configs/` for all `.json` files. Each JSON file contains metadata strictly in this single-line format: 
   `{"config_id": "<string>", "binary": "<filename>", "timestamp": <integer>}`
   *Process the updates in strictly ascending order of their `timestamp` values.*

2. **Binary Header Extraction**: For each update, read the target ELF64 executable file (located in the same directory). Your C++ code must directly read the binary file's ELF header (do not shell out to tools like `readelf`) to extract the 64-bit Entry Point address (`e_entry`). Standard Linux headers like `<elf.h>` are available on the system.

3. **File Locking & WAL Append**: Open a Write-Ahead Log (WAL) file located at `/home/user/tracker.wal`. You must acquire an exclusive file lock on this log file (using `flock` or `fcntl`) before writing to it, and release it afterward, simulating a concurrent environment. 
   Append a new line to the log file in the following CSV format:
   `config_id,binary_filename,0x<entry_point_in_lowercase_hex>`
   *(Example: `cfg_alpha,app_v1.elf,0x401050`)*

4. **Link Management**: After logging an update, force-update a symbolic link at `/home/user/latest.elf` so that it points to the absolute path of the ELF binary that was just processed.

Constraints:
- You do not have root access; do not attempt to use `apt` or `sudo`. You can parse the simple JSON format using standard C++ libraries (e.g., `<regex>` or string manipulation).
- Ensure your output hex address does not have leading zeros after the `0x`.
- Compile your program using standard C++17: `g++ -std=c++17 -o /home/user/config_tracker /home/user/config_tracker.cpp`
- Once compiled, run it to generate the final `/home/user/tracker.wal` file and `/home/user/latest.elf` symlink.