You are a backup administrator tasked with safely consolidating data before archiving. You need to prevent an issue similar to "Zip Slip" where malicious or poorly configured symlinks could cause an archive extraction to overwrite files outside the intended target directory.

You have a source directory located at `/home/user/source_data/`. This directory contains a complex tree of subdirectories, regular files, and symbolic links.

Your task is to prepare this data for a safe backup by mirroring it to `/home/user/archive_prep/` according to the following strict rules. You may write a script in any language you prefer (Python, Bash, etc.) to accomplish this:

1. **Mirror the Directory Structure:** Recreate the exact subdirectory structure of `/home/user/source_data/` inside `/home/user/archive_prep/`.
2. **Handle Regular Files:** For every regular file in the source directory, create a **hard link** to it in the corresponding location within `/home/user/archive_prep/`. Do not copy the file contents; you must use hard links to save disk space.
3. **Validate and Handle Symbolic Links:** 
    * For every symlink in the source directory, you must determine its absolute resolved path.
    * **Safe Links:** If the symlink resolves to a target that is strictly *inside* `/home/user/source_data/` (or any of its subdirectories), you must recreate it in `/home/user/archive_prep/`. However, the newly created symlink in `archive_prep` **must be a relative symlink** pointing to the correct target within `archive_prep`.
    * **Unsafe Links:** If the symlink resolves to a target *outside* `/home/user/source_data/` (e.g., `/etc/passwd` or `/home/user/some_other_file`), it is considered unsafe. Do not recreate it in `archive_prep`. Instead, append the absolute path of the original unsafe symlink to `/home/user/unsafe_links.log` (one path per line, sorted alphabetically at the end).
4. **Generate a Manifest:** Once the `archive_prep` directory is fully populated, generate an MD5 checksum manifest of all regular files within it. Save this manifest to `/home/user/manifest.txt`. The manifest must match the standard output format of the `md5sum` command (e.g., `<md5hash>  ./path/to/file`), where paths are relative to the `/home/user/archive_prep/` directory. Ensure the manifest lines are sorted alphabetically by the file path.

Ensure all file paths in logs and manifests are exact and the final `/home/user/manifest.txt` and `/home/user/unsafe_links.log` are present.