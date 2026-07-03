You are an artifact manager tasked with curating a binary repository. We have a legacy, proprietary extraction tool located at `/app/archiver` (a stripped, UPX-packed binary). This tool extracts archives into a target directory, but we need to reconstruct a specific legacy filesystem state where some files must be written *outside* the target extraction directory (e.g., to `/home/user/system_root/`), exploiting a known directory traversal behavior in this legacy tool.

You are provided with:
1. `/app/archiver`: The stripped archive extraction tool. It takes arguments: `/app/archiver extract <archive_file> <target_dir>`.
2. `/home/user/source_data/`: A directory containing 500 binary chunks and text files. Many of these files are exact duplicates of each other.
3. `/home/user/layout.conf`: A configuration file where each line is formatted as `destination_path=source_filename`. The `destination_path` is relative to the root of the extracted environment, but some paths start with `../system_root/` to escape the extraction directory.

Your task:
1. Figure out what standard archive format `/app/archiver` expects (hint: it's a very common archive format, but the binary is obfuscated).
2. Create an archive named `/home/user/payload.archive` that packages the files from `source_data` according to `layout.conf`.
3. When `/app/archiver extract /home/user/payload.archive /home/user/extracted` is run, it must correctly place all files in their specified locations, including the escaped paths in `/home/user/system_root/`.
4. **Optimization:** The payload archive must be highly optimized in size. You must deduplicate the redundant files from `source_data`. You can achieve this by embedding the actual file data only once, and using the archive format's native support for symlinks or hardlinks for the duplicate destinations. 

The success of your task will be evaluated by an automated verifier that will check:
- All destination paths specified in `layout.conf` exist and contain the correct bytes.
- The total size of `/home/user/payload.archive` is strictly less than **25,000 bytes** (a naive archival of all files would be over 500 KB).

Write the archive to `/home/user/payload.archive`. You may use any combination of bash commands or scripting languages (e.g., Python) to manipulate the archive structure and headers to bypass standard path traversal protections during archive creation.