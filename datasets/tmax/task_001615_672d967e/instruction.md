You are tasked with building a secure configuration manager that tracks changes and persists them using a custom obscured file format. 

**Step 1: Extract the Encryption Key**
We have recorded a video of a legacy terminal's boot sequence, located at `/app/server_logs.mp4`. During this sequence, the screen occasionally flashes completely black (`#000000` or RGB 0,0,0). 
Extract the video frames and count the exact number of completely black frames. Let this number be `B`. This integer `B` is your shift key for the configuration manager.

**Step 2: Implement the Configuration Manager**
Write a C++ program `/home/user/solution.cpp` and compile it to `/home/user/config_manager`. 

Your program must accept the shift key `B` as its first command-line argument:
`./config_manager <B>`

It must then read a sequence of commands from standard input (`stdin`), one per line, and execute them. The state is a simple key-value map (both keys and values are strings with no spaces).

**Commands to support:**
1. `SET <key> <value>`: Updates the in-memory configuration map. If the key exists, overwrite the value. Does not output anything.
2. `DEL <key>`: Removes the key from the in-memory map. Does not output anything.
3. `COMMIT <filepath>`: Writes the entire current in-memory configuration to the specified file. 
   - The data must be written as `key=value\n`, sorted alphabetically by key.
   - **Obfuscation**: Before writing to the file, every character in the output string (including the `=` and `\n`) must have its ASCII value increased by `B`. (Assume standard ASCII, overflow beyond 255 can wrap via standard 8-bit unsigned integer logic).
   - Does not output anything to `stdout`.
4. `LOAD <filepath>`: Clears the current in-memory map, reads the specified file, applies the reverse obfuscation (subtracting `B` from each byte), and populates the in-memory map with the parsed `key=value\n` pairs. Does not output anything.
5. `DUMP`: Prints the current in-memory configuration to `stdout`. The output must be one `key=value` pair per line, sorted alphabetically by key.

**Requirements:**
- Handle concurrent/rapid successive `COMMIT` and `LOAD` operations cleanly using standard C++ file streams (e.g., `std::ifstream`, `std::ofstream`).
- Write robust parsing to handle the exact specification without crashing on empty files or simple invalid inputs (ignore malformed lines quietly).
- When you are finished, ensure the compiled binary is located exactly at `/home/user/config_manager`.

*Note: An automated verification system will run your binary against thousands of random command sequences to ensure it behaves completely identically to our reference implementation, producing the exact same standard output and file artifacts.*