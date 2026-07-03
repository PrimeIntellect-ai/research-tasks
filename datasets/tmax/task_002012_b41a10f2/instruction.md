You are tasked with organizing a messy project repository for a developer using only Bash. The developer has an unstructured directory of asset files missing their extensions and needs them categorized, deduplicated, and logged.

**Starting State:**
You will find a directory at `/home/user/raw_project`. Inside it:
1. `/home/user/raw_project/organize.conf`: A configuration file mapping 4-byte file signatures (magic numbers) in lowercase hexadecimal to target directory paths. Format: `[4-byte-hex]:[target_relative_path]`.
2. `/home/user/raw_project/assets/`: A directory containing numerous data files without extensions. Some files are identical copies of each other.

**Your Objectives:**
You must write and execute a Bash script (e.g., `/home/user/organize.sh`) to perform the following:

1. **Binary Header Extraction & Categorization:**
   - Read the first 4 bytes of every file in `/home/user/raw_project/assets/`.
   - Match this hex signature against `/home/user/raw_project/organize.conf`.
   - Copy the file into `/home/user/organized/<target_relative_path>/`. The file should keep its original base name.
   - If a file's 4-byte signature is not in the config file, copy it to `/home/user/organized/unknown/`.

2. **Hard Link Deduplication:**
   - The developer wants to save space. After categorization, scan the entire `/home/user/organized/` directory tree.
   - Identify all files that have exactly identical content.
   - Replace duplicate files with **hard links** to a single physical file. (For any group of identical files, they must all share the same inode).

3. **Reporting:**
   - Generate a report file at `/home/user/organization_report.log`.
   - The report must list every file in `/home/user/organized/` (including subdirectories).
   - Format: `<SHA256_HASH> <RELATIVE_PATH_FROM_ORGANIZED_DIR>`
   - The output must be alphabetically sorted by the SHA256 hash, then by the relative path. Note: Do not include directory entries in the report, only files.

**Constraints:**
- You must accomplish this using Bash and standard Linux tools (e.g., `dd`, `hexdump`, `xxd`, `sha256sum`, `find`, `ln`). 
- Python, Perl, or other higher-level scripting languages are strictly forbidden.
- The working directory for relative paths in the report should be `/home/user/organized/`.