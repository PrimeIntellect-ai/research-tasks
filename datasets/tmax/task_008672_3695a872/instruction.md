I have a directory of recovered project files located at `/home/user/project_dump`. Unfortunately, the file recovery process lost the file extensions, and some files have incorrect dummy extensions. I need you to organize these files by inspecting their binary headers (magic numbers), renaming them with the correct extensions, and generating a checksum manifest.

Please write a Python script (you can name it `/home/user/organize.py`) or use shell/Python commands to do the following:

1. Scan all files in `/home/user/project_dump` (excluding any directories or files you create like the manifest).
2. Read the first few bytes of each file to determine its actual format based on these exact signatures:
   - Hex `89 50 4E 47 0D 0A 1A 0A` -> Portable Network Graphics. Set extension to `.png`.
   - Hex `1F 8B` -> GZIP archive. Set extension to `.gz`.
   - Hex `25 50 44 46 2D` -> PDF document. Set extension to `.pdf`.
   - If a file does not match any of the above signatures, treat it as a plain text file. Set extension to `.txt`.
3. Rename each file to have the correct extension. You must completely replace any existing extension (e.g., `data.dat` becomes `data.png`, `readme` becomes `readme.txt`).
4. After all files are renamed, calculate the SHA-256 checksum for each renamed file.
5. Create a manifest file at `/home/user/project_dump/manifest.sha256`. This file must follow the standard `sha256sum` output format (the checksum, followed by two spaces, followed by the filename—do not include directory paths in the filename). The entries in the manifest must be sorted alphabetically by the new filename.

Please execute your solution so that the final state of `/home/user/project_dump` contains only the correctly renamed files and the `manifest.sha256` file.