You are managing a configuration tracking system for a hardware manufacturing lab. We need a Python script to automate the processing, parsing, and bulk-renaming of machine files (GCode) and firmware files (ELF binaries) based on a central configuration file.

Your task is to write and execute a Python script (save it as `/home/user/tracker.py`) that does the following:

1. **Parse Configuration**: Read the configuration file located at `/home/user/rules.ini`. It uses a standard INI format and contains the desired naming conventions and the path for the output log.
2. **Process GCode Files**: In the `/home/user/files/` directory, there are several `.gcode` files. You must read them as text to extract metadata from the comments at the top of the file. Specifically, look for lines exactly matching `; MATERIAL:<material_name>` and `; TIME:<seconds>`.
3. **Process ELF Files**: In the same directory, there are `.elf` files. You must read them as binary to determine if they are 32-bit or 64-bit. The 5th byte (index 4) of an ELF file header (EI_CLASS) dictates this: a value of `1` means 32-bit, and `2` means 64-bit.
4. **Bulk Rename**: Rename all `.gcode` and `.elf` files in `/home/user/files/` using the formats specified in `/home/user/rules.ini`.
5. **Write a Tracking Log (WAL)**: As you rename the files, append a record to the Write-Ahead Log (WAL) file specified in the configuration. Each line in the WAL must be strictly formatted as: `[RENAME] <original_filename> -> <new_filename>`.

Here are the specific details of the files you will work with:
- Configuration file: `/home/user/rules.ini`
- Target directory: `/home/user/files/`

The Python script must handle the file I/O carefully and accurately. Once you have written the script, run it to perform the bulk renaming and log generation.