I need you to help me organize a messy collection of project build artifacts. 

I have a nested archive located at `/home/user/project_artifacts.tar.gz`. This archive contains several `.zip` files which in turn contain a mix of different project files (text, GCode, and compiled ELF binaries). 

Please perform the following operations:

1. **Extract and Verify**: Extract the `project_artifacts.tar.gz` archive into `/home/user/extracted/`. Inside, you will find several `.zip` files. First, verify the integrity of these zip files. Then, extract their contents into the same `/home/user/extracted/` directory.

2. **Parse and Filter**: I need you to write a Python script (`/home/user/organize_elfs.py`) to scan through all the extracted files and identify only the ELF binaries. An ELF file can be identified by the magic number `\x7fELF` at the very beginning of the file. 

3. **Format Parsing (ELF Architecture)**: For each ELF file, your script must read the ELF header to determine the target architecture. Specifically, read the 16-bit `e_machine` field located at byte offset 18 (0x12) in the file. 
   - If the value is `0x28` (40 in decimal), it is an ARM binary.
   - If the value is `0x3E` (62 in decimal), it is an x86_64 binary.

4. **Symlink Organization**: For every identified ELF file, your script should create a symbolic link in `/home/user/organized_elfs/{architecture}/` pointing to the **absolute path** of the extracted file. 
   - Replace `{architecture}` with either `ARM` or `x86_64` based on the parsed header.
   - The symlink should have the same base name as the original file.
   - Create the target directories if they don't exist.

5. **Log File**: Finally, the script should create a log file at `/home/user/elf_inventory.log` containing a list of all created symlink paths, one per line, sorted alphabetically.

Execute your script to complete the task. You are restricted to using standard Python libraries and standard bash utilities.