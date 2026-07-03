You are tasked with helping a developer organize and migrate a chaotic directory of legacy project files. 

You have a set of legacy binary files in `/home/user/legacy_projects/`. 
Each file contains a custom binary header followed by arbitrary project data. Over the years, the header schema has changed, and the developer wants to organize these files into a new directory while simultaneously migrating all headers to the latest schema version.

Your task is to write a Rust program that acts as a binary parser, schema migrator, and file organizer.

**Header Format Specifications:**
*   **Magic Number:** 4 bytes at offset 0. Must be `0x4C 0x45 0x47 0x41` (ASCII "LEGA").
*   **Schema Version:** 1 byte at offset 4. Can be `0x01` (Version 1) or `0x02` (Version 2).
*   **Filename Length (L):** 2 bytes at offset 5. Unsigned 16-bit integer, **Little-Endian**. Represents the length of the filename in bytes.
*   **Filename:** `L` bytes at offset 7.
    *   If Version 1: The filename is encoded in standard ASCII.
    *   If Version 2: The filename is encoded in **UTF-16LE** (Little-Endian).
*   **Payload:** All remaining bytes after the filename constitute the actual file content.

**Requirements:**
1.  Write a Rust program (you can create a Cargo project in `/home/user/organizer`) that reads every file in `/home/user/legacy_projects/`.
2.  For each file, parse the binary header using a state-machine or cursor-based approach. Extract the original filename and the payload.
3.  **Schema Migration:** If a file is Version 1, you must upgrade it to Version 2 in memory. This requires converting the ASCII filename to UTF-16LE, updating the Filename Length field to reflect the new byte length, and changing the Schema Version byte to `0x02`.
4.  **Organizing:** Write the finalized file (migrated V2 header + original payload) into the directory `/home/user/organized_projects/`. The name of the file on disk should be the decoded filename. (Create this directory if it doesn't exist).
5.  **Logging:** Append a line to `/home/user/migration.log` for each successfully processed file. The log file must be exactly in this format:
    *   For upgraded V1 files: `<source_filename> -> <decoded_filename> [V1_UPGRADED]`
    *   For V2 files (which just need to be copied with their headers intact): `<source_filename> -> <decoded_filename> [V2_UNCHANGED]`
    *(Example log line: `file_001.dat -> project_alpha.txt [V1_UPGRADED]`)*
    Sort the processing order of the files alphabetically by their source filename (e.g., `file_001.dat` before `file_002.dat`) so the log is deterministic.

Use standard Rust (`std::fs`, `std::io`) to complete this task. Once your program is written, compile and run it to process the files, ensuring the `/home/user/organized_projects/` directory is fully populated and `/home/user/migration.log` is created.