I have a project backup archive located at `/home/user/project_backup.zip`. I need you to act as a developer organizing these project files, as some parts of the backup have become messy or corrupted. 

Please perform the following steps:

1. **Archive Integrity and Extraction**: Verify the integrity of `/home/user/project_backup.zip`. Extract all valid files into the directory `/home/user/project_files/`. (If any files are reported as corrupted by the archive utility, skip them and extract the intact ones).

2. **C Program Development**: Write a C program at `/home/user/organize.c` and compile it to `/home/user/organize`. Your program must perform the following tasks when executed:

    *   **Multi-line Log Parsing**: Read `/home/user/project_files/compiler_output.log`. This log contains multi-line entries separated by lines containing exactly `---`. Locate the specific block that contains the string `FATAL ERROR:`. Extract the absolute file path of the corrupted ELF binary mentioned on the same line as the fatal error (e.g., `FATAL ERROR: Corrupted binary generated: /path/to/file.elf`).
    
    *   **Domain-Specific Parsing (ELF)**: Open the extracted ELF binary file path in C. Parse its 64-bit ELF header natively to find the `e_entry` (Entry point address). Do not use external commands like `readelf` inside your C program; parse the binary header directly (`<elf.h>` is permitted). Write this entry point address in hexadecimal format (e.g., `0x401000`) to a new file at `/home/user/entry_point.txt`.

    *   **File Splitting (GCode)**: Read `/home/user/project_files/main_print.gcode`. You must split this large GCode file into smaller chunks. Create a directory `/home/user/gcode_chunks/`. Start reading the file and write to `/home/user/gcode_chunks/chunk_00.gcode`. Every time you encounter a line starting exactly with `;LAYER_CHANGE`, you must close the current chunk file and start a new one, incrementing the suffix (`chunk_01.gcode`, `chunk_02.gcode`, etc.). The `;LAYER_CHANGE` line should be the first line of the new chunk file.

3. **Execution**: Run your compiled program to generate `/home/user/entry_point.txt` and the GCode chunks in `/home/user/gcode_chunks/`.

Make sure your C code handles file paths and basic error checking properly.