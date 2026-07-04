You are acting as a storage administrator for a system that is rapidly running out of disk space. You have been tasked with organizing, deduplicating, and cleaning up a large dump of backup files and logs located in `/home/user/storage_dump`. 

The dump contains two types of files:
1. **Binaries:** Located in `/home/user/storage_dump/binaries/`. These are `.dat` files.
2. **Text Logs:** Located in `/home/user/storage_dump/logs/`. These are `.log` files.

You must perform a multi-phase cleanup and organization process. You can use any combination of shell scripting, Python, or other tools available in the standard environment.

**Phase 1: Binary Header Extraction & Symlink Categorization**
Every valid `.dat` file has a specific 16-byte binary header. 
- Bytes 0-3 contain the magic ASCII string `BKUP`.
- Bytes 4-7 contain a 32-bit unsigned integer (Little Endian) representing the Category ID.
- Bytes 8-15 contain a timestamp (which you can ignore).
You must read the headers of all `.dat` files. For each valid file, extract its Category ID. Then, create a directory structure at `/home/user/organized_binaries/cat_<ID>/` (where `<ID>` is the integer ID, e.g., `cat_1`, `cat_2`). Inside the corresponding category directory, create a **symbolic link** pointing back to the original `.dat` file in the storage dump. Ignore any `.dat` file that does not start with the magic string `BKUP`.

**Phase 2: Binary Deduplication via Hard Links**
To save physical disk space, you must deduplicate the `.dat` files in `/home/user/storage_dump/binaries/`. Identify files that have the exact same SHA256 hash. For each set of identical files:
- Keep the file that comes first alphabetically.
- Replace all other identical files with a **hard link** to the alphabetically first file.

**Phase 3: Large-Scale Text Editing**
The `.log` files in `/home/user/storage_dump/logs/` are bloated with trivial debug information. 
- Create a directory `/home/user/cleaned_logs/`.
- Process every `.log` file, removing any line that exactly starts with the string `[DEBUG-TRIVIAL]`.
- Save the cleaned files into `/home/user/cleaned_logs/` keeping their original filenames.

**Phase 4: Final Report**
Generate a JSON report at `/home/user/storage_report.json` with the following structure:
```json
{
  "valid_binaries_found": <int>,
  "duplicates_replaced_with_hardlinks": <int>,
  "total_trivial_lines_removed": <int>
}
```

Ensure all paths are absolute and exactly match the instructions.