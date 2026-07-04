You are an artifact manager tasked with curating a messy directory of incoming binaries. Your goal is to write a Bash script that processes these files, identifies valid ELF binaries, extracts their metadata, organizes them into a structured repository, and generates a checksum manifest.

Write a Bash script at `/home/user/curate.sh` that performs the following operations:

1. **Search**: Scan the directory `/home/user/incoming` for all files.
2. **Filter**: Identify files that are valid ELF (Executable and Linkable Format) binaries. Ignore any non-ELF files (like text files or scripts).
3. **Parse Metadata**: For each valid ELF file, use `readelf -h` to extract:
   - **Machine architecture**: From the `Machine:` field (e.g., "Advanced Micro Devices X86-64"). Replace any spaces in this string with underscores (e.g., "Advanced_Micro_Devices_X86-64").
   - **File type**: From the `Type:` field. If the type contains "EXEC", classify it as `EXEC`. If it contains "DYN" (Shared object file or Position-Independent Executable), classify it as `DYN`.
4. **Organize**: Copy each identified ELF file into a curated repository located at `/home/user/repo/`. The directory structure must be: `/home/user/repo/<Architecture_String>/<Type_String>/<Original_Filename>`.
5. **Generate Manifest**: Create a CSV manifest at `/home/user/repo/manifest.csv`. For every ELF file processed, append a line with the following exact format (comma-separated, no spaces around commas):
   `SHA256_Checksum,Architecture_String,Type_String,Original_Filename`
   *(Use the `sha256sum` command to calculate the checksum of the original file).*

The manifest lines can be in any order.
Ensure your script creates any necessary target directories.

Run your script to complete the curation process so the results can be verified.