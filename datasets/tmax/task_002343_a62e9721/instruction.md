You are an artifact manager tasked with migrating our curation pipeline off a legacy, closed-source parsing utility. We need to replace it with a verifiable, open-source C implementation.

Your objectives:
1. **Find the configuration and sample data:** 
   Search the directory `/home/user/repo/archives/` for a compressed archive (`.tar.gz`) that has the "sticky bit" set in its permissions. Extract this specific archive to `/home/user/repo/extracted/`.
   Inside, you will find `schema.conf` (a large configuration file mapping record types to metadata names) and several sample `.arf` (Artifact) files.

2. **Reverse Engineer the Legacy Parser:**
   A stripped binary is located at `/app/bin/legacy_parser`. It takes exactly two arguments:
   `Usage: /app/bin/legacy_parser <path_to_schema_conf> <path_to_arf_file>`
   This utility parses the `.arf` files (which contain a custom header and compressed stream) using the schema, and outputs normalized text to `stdout`. Use the sample `.arf` files, standard Linux reverse-engineering tools (`xxd`, `strings`, `objdump`, `ltrace`, `strace`), and your analytical skills to determine the exact binary format, compression method, and output formatting logic.

3. **Develop the Replacement:**
   Write a C program at `/home/user/new_parser.c` that parses the schema and the `.arf` files exactly like the legacy parser. 
   - You must handle the compressed streams, the binary metadata structures, and the schema configuration file dynamically.
   - Compile your program to `/home/user/new_parser`.
   - Ensure you link any necessary libraries (e.g., `-lz`).

4. **Testing and Verification:**
   Your compiled binary `/home/user/new_parser` must be bit-exact equivalent in its standard output and exit codes to `/app/bin/legacy_parser` for *any* valid or invalid input. An automated verification system will extensively fuzz your executable against the legacy binary with thousands of generated inputs to ensure 100% behavioral parity, including error messages and edge cases.