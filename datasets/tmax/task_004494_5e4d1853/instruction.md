You are an artifact manager tasked with recovering and analyzing a corrupted repository of binary artifacts. 

The backup system has scattered a split `tar.gz` archive across the directory structure in `/home/user/artifact_store/`. The archive contains several 64-bit ELF executables. 

Your task is to:
1. **Locate and Merge**: Find all files starting with `archive_part_` within `/home/user/artifact_store/` and its subdirectories. Merge them sequentially based on their alphabetical suffix (e.g., `archive_part_aa`, then `archive_part_ab`, etc.) into a single archive at `/home/user/recovered.tar.gz`.
2. **Extract**: Extract the contents of `/home/user/recovered.tar.gz` into a new directory `/home/user/binaries/`.
3. **Parse and Analyze (C Programming)**: Write a C program at `/home/user/analyze_elf.c` that:
   - Reads every file in `/home/user/binaries/`.
   - Checks if the file is a valid 64-bit ELF file by reading its binary header (using standard `<elf.h>` structs). Ignore non-ELF files or directories.
   - Extracts the Entry Point address (`e_entry`) from the ELF header.
   - Writes the extracted information to `/home/user/report.csv`.
4. **Compile and Run**: Compile your C program using `gcc` to `/home/user/analyze_elf` and execute it. 

The output file `/home/user/report.csv` must be formatted strictly as:
`filename,0x[hex_entry_point]`
(e.g., `app_alpha,0x401050`)
The entries in the CSV must be sorted alphabetically by filename. Ensure hex characters are lowercase.

Requirements:
- You must use C to parse the ELF files (do not use shell tools like `readelf` or `objdump` to generate the final CSV, though you may use them to debug).
- The C program should properly handle standard ELF64 headers.