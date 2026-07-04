I am organizing a messy directory of project files created by a faulty automated build process. The directory is located at `/home/user/project_assets/`. It contains a mix of valid compiled binaries, text files, broken symlinks, and infinitely looping symlinks.

I need you to perform the following cleanup and organization task:

1. Identify and delete any infinitely looping symlinks and broken symlinks within `/home/user/project_assets/`.
2. Scan the remaining files (and the targets of valid symlinks) to find all valid ELF binaries. For this task, a valid ELF binary is strictly defined as any file whose first four bytes are `\x7fELF` (hex: `7f 45 4c 46`).
3. Create a new directory at `/home/user/organized_binaries/`.
4. For every item in `/home/user/project_assets/` that resolves to a valid ELF binary, create a **hard link** to the resolved target file inside `/home/user/organized_binaries/`. The hard link must have the exact same base name as the item in the original directory. (e.g., if `/home/user/project_assets/my_link` points to a valid ELF file, create a hard link to that target file at `/home/user/organized_binaries/my_link`).
5. Finally, generate a SHA-256 checksum manifest of all files in `/home/user/organized_binaries/` and save it to `/home/user/manifest.txt`. 

The manifest must:
- Be formatted exactly like the default output of `sha256sum` (e.g., `[hash]  [filename]`).
- Only contain the base filenames, not full paths.
- Be sorted alphabetically by filename.

You may only use Bash built-ins and standard Linux coreutils/CLI tools.