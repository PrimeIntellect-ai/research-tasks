You are an artifact manager tasked with curating a repository of binary files. Your system has a directory located at `/home/user/artifacts` that contains various files, including 64-bit ELF binaries, text files, and numerous symbolic links. Due to some poor legacy curation processes, some of these symbolic links form infinite loops. 

Additionally, these files are occasionally accessed by concurrent curation services. To ensure safe parsing, you must use file locks when reading them.

Your task is to extract the Entry Point address from all unique valid 64-bit ELF binaries in the repository.

Please perform the following steps:

1. **Write a C program (`/home/user/elf_parser.c`)**
   - The program should take a single file path as a command-line argument.
   - It must open the file and attempt to acquire a shared lock using `flock(fd, LOCK_SH)`.
   - Once locked, it should read the file header to determine if it is a valid ELF file (checking the `\x7FELF` magic number).
   - If it is a 64-bit ELF file, parse the binary header natively in C to extract the 64-bit Entry Point address (`e_entry` field, which is located at offset `0x18` in the ELF header). 
   - It should print the entry point to standard output in hexadecimal format, prefixed with `0x` (e.g., `0x401000`).
   - If the file is not an ELF file, it should print `NOT_ELF`.
   - Release the lock and exit gracefully. Compile this program to `/home/user/elf_parser`.

2. **Write a Bash script (`/home/user/curate.sh`)**
   - The script must recursively traverse the `/home/user/artifacts` directory.
   - It must gracefully handle symbolic links: it should follow them to their target, but it **must avoid infinite symlink loops** without crashing or hanging.
   - To prevent redundant work, it should process each unique target file exactly once, even if multiple symlinks point to it.
   - For every unique regular file found, invoke your compiled `/home/user/elf_parser`.
   - If the parser outputs an entry point (and not `NOT_ELF`), append a line to `/home/user/curation_report.txt` in the following exact format:
     `<absolute_real_path_of_file> : <entry_point>`
     *(Example: `/home/user/artifacts/service_a : 0x401050`)*

Ensure that your `curate.sh` script is executable and run it so that the final `/home/user/curation_report.txt` is generated. Do not use external tools like `readelf` or `objdump` to parse the ELF headers; your C program must do the binary parsing directly.