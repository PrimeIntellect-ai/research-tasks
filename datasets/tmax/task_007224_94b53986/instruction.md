You are tasked with writing a C program to act as a configuration manager that processes custom Write-Ahead Log (WAL) files. A system generates binary `.wal` files representing configuration changes over time. Your goal is to parse these files, merge the configuration states, and output the final active configuration.

**Requirements:**
1. Create a C program at `/home/user/wal_compiler.c` and compile it to `/home/user/wal_compiler`.
2. The program must search the directory `/home/user/wals/` for all files ending in `.wal`.
3. Parse each valid `.wal` file. The binary format of a `.wal` file is:
   - **Header:** 8-byte magic string exactly matching `CFGWAL01` (ASCII).
   - **Records:** Followed immediately by zero or more records. Each record consists of:
     - `timestamp` (uint32_t, little-endian)
     - `key_len` (uint8_t)
     - `val_len` (uint16_t, little-endian)
     - `key` (ASCII string of length `key_len`, not null-terminated in the file)
     - `value` (ASCII string of length `val_len`, not null-terminated in the file)
4. Merge the configuration data across all files:
   - Keep track of the most recent value for each key based on the `timestamp`. Higher timestamps take precedence, regardless of which file the record was found in.
   - If a record has a `val_len` of `0`, this indicates the key was **deleted** at that timestamp.
5. Generate the final configuration file at `/home/user/compiled_config.txt`.
   - The file should contain `key=value` pairs, one per line.
   - Do not include deleted keys.
   - The output lines must be sorted alphabetically by the `key`.

**Execution:**
You should write the code, compile it with standard GCC (`gcc /home/user/wal_compiler.c -o /home/user/wal_compiler`), and execute it to produce the final `/home/user/compiled_config.txt` file. Standard C library functions are sufficient for this task.