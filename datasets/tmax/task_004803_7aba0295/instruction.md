You are a backup administrator tasked with optimizing the storage of historical access logs. The current system relies on text logs scattered across nested archives, and metadata (user mappings) stored in a fast Redis cache. Your goal is to consolidate this data into a highly efficient custom binary format using C, enabling faster downstream analytics and reducing storage footprint.

Your environment includes multiple cooperating services, which you must start by running `/app/start_services.sh`.
1. **Nginx (Port 8080):** Hosts a master archive of the logs at `http://127.0.0.1:8080/backup_pool.tar`.
2. **Redis (Port 6379):** Contains user mappings in a hash named `user_map`. Keys are integer User IDs, and values are alphanumeric usernames.

**Step 1: Data Preparation**
- Download the master archive from the Nginx server and unpack it. Inside, you will find multiple daily `.tar.gz` files. Extract all nested log files (which end in `.log`) into a directory `/home/user/raw_logs`.
- Query the Redis server to dump the `user_map` hash. Use standard text transformation tools (`sed`, `awk`) to format this dump into a clean, comma-separated lookup file at `/home/user/user_dict.csv` with the format: `UID,USERNAME`.

**Step 2: C Implementation (Memory-Mapped Parser)**
Write a C program at `/home/user/archiver.c`. This program must:
- Take two arguments: the path to the directory containing the text logs (`/home/user/raw_logs`) and the output binary file path (`/home/user/archive.bin`).
- Read `/home/user/user_dict.csv` into memory to build a lookup table.
- Iterate through all `.log` files in the provided directory. To ensure maximum performance, you *must* use `mmap` (memory-mapped I/O) to read these log files.
- Parse each line of the logs. The text logs have the format: `[TIMESTAMP] UID ACTION_STRING` (e.g., `[1700000000] 105 LOGIN`).
- Write the records to the output file in a tightly packed binary format:
  - **Timestamp:** 4 bytes, unsigned 32-bit integer (Epoch time).
  - **Username:** 16 bytes, ASCII string. Look up the UID in your dictionary to get the username. Pad the string with null bytes (`\0`) if it's shorter than 16 bytes. If a UID is missing from the dictionary, use the string `UNKNOWN`.
  - **Action Code:** 1 byte, unsigned 8-bit integer. Map the `ACTION_STRING` as follows: `LOGIN` = 0x01, `LOGOUT` = 0x02, `DOWNLOAD` = 0x03, `UPLOAD` = 0x04. Any other action should be mapped to `0xFF`.

**Step 3: Execution and Verification**
Compile your C program to `/home/user/archiver` and run it against the extracted logs to produce `/home/user/archive.bin`.

The final success of this task will be evaluated by an automated script that tests the performance and compression ratio of your binary output. Your output binary file size must be rigorously minimized, conforming precisely to the 21-byte per record specification.