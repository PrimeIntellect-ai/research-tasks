I need to organize a flat directory of unsorted project files left by a previous developer. The directory is located at `/home/user/legacy_dump/` and contains a mix of compiled ELF binaries (`.elf`) and 3D printer manufacturing instructions (`.gcode`). 

Please write a C program at `/home/user/organizer.c`, compile it to `/home/user/organizer`, and use it to process the files into a structured directory at `/home/user/structured/`. Finally, archive the organized directory.

Here are the exact requirements for your C program and the overall workflow:

1. **Input and Output**: The program must accept two command-line arguments: the input directory (`/home/user/legacy_dump/`) and the output directory (`/home/user/structured/`). It should create the output directory and any necessary subdirectories.
2. **File Processing**: Iterate over all files in the input directory.
    * **ELF Files (`.elf`)**: Parse the ELF file header to extract the machine architecture (`e_machine` field, which is a 16-bit unsigned integer at offset 0x12). Copy the file to `/home/user/structured/elf/arch_<e_machine_value>/<filename>`. (e.g., `arch_62`).
    * **GCode Files (`.gcode`)**: Read the file line by line to find the first occurrence of the extruder temperature setting command, which looks like `M104 S<temperature>` (e.g., `M104 S210`). Copy the file to `/home/user/structured/gcode/temp_<temperature>/<filename>`.
3. **Manifest Creation**: As your program processes each file, it must append a record to `/home/user/structured/manifest.txt`. 
    * Format for ELF: `<filename> - ELF - arch <e_machine_value>`
    * Format for GCode: `<filename> - GCODE - temp <temperature>`
    * **CRITICAL**: To prevent partial writes in case of a crash, you must use an **atomic write** strategy for updating the manifest. For each file processed, write the new manifest content (or appended content) to a temporary file (`/home/user/structured/manifest.tmp`) and then use the `rename()` system call to atomically replace `manifest.txt`.
4. **Archiving**: After your C program finishes executing, use standard Linux shell commands to compress the entire `/home/user/structured/` directory into a gzip-compressed tarball at `/home/user/organized_archive.tar.gz`. The tarball should contain the `structured` folder at its root.

Please write the code, compile it, run it, and create the final archive.