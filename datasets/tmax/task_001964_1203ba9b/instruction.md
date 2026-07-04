You are an artifact manager responsible for curating and maintaining a legacy binary repository located at `/home/user/repo`. Over time, the repository has accumulated out-of-date binaries and obsolete configuration files that need to be reorganized and updated.

Please perform the following curation tasks:

1. **Metadata-based identification and bulk renaming:**
   Find all binary artifact files (ending in `.bin`) anywhere within `/home/user/repo` that meet *both* of the following conditions:
   - The file size is strictly greater than 100 KB (102,400 bytes).
   - The file's last modified timestamp is strictly before January 1, 2023.
   
   Once identified, bulk-rename these specific files by prepending `legacy_` to their original filename. For example, if you find an old, large file named `app_build.bin` inside a subdirectory, it should be renamed to `legacy_app_build.bin` in the exact same directory. Do not alter `.bin` files that do not meet both criteria.

2. **Text transformation of configurations:**
   Find all configuration files (ending in `.conf`) anywhere within `/home/user/repo`. 
   Update their contents in-place to migrate the storage backend pointing: replace every instance of the exact string `backend: legacy-storage` with `backend: cloud-storage`.

3. **Manifest generation:**
   Extract the artifact IDs from all the `.conf` files you just processed. Every `.conf` file contains a line formatted exactly as `id: <value>`. 
   Extract just the `<value>` portion (ignoring the "id: " prefix and any leading/trailing whitespace), and write these extracted values into a new manifest file at `/home/user/extracted_ids.txt`. 
   The values in `/home/user/extracted_ids.txt` must be sorted alphabetically, with exactly one ID per line. Do not process files that do not end in `.conf`.

Use any combination of scripting languages (like Python or Bash) and shell utilities (like find, sed, awk) to accomplish this.