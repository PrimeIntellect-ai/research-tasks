You are an artifact manager responsible for curating a large binary repository. The repository is currently packed in an uncompressed tarball at `/app/repo.tar`.

Management has provided a screenshot of the new curation rules in `/app/curation_rules.png`.

Your task is to implement an automated curation pipeline in Bash that performs the following steps:
1. Extract the repository to `/app/repo/`.
2. Extract the text from `/app/curation_rules.png` (using `tesseract` or similar tools) to understand the artifact routing rules. The image contains a list of renaming rules for file prefixes, a suffix of files to archive separately, and instructions for manifest files.
3. Perform a recursive directory traversal over `/app/repo/` to apply the bulk renaming rules to all matching files. 
4. Efficiently process all `.manifest` text files in the repository using streaming I/O (e.g., `sed` or `awk`):
   - Apply the same prefix replacements inside the text of the `.manifest` files.
   - Strip the first 5 lines (header) from every `.manifest` file.
5. Move all files matching the "archive suffix" rule into a new directory `/app/archived/` while strictly preserving their relative directory structures.
6. Create an uncompressed tarball of the archived files at `/app/archived.tar`.
7. Archive and heavily compress the remaining curated repository into `/app/curated_repo.tar.xz` using `tar` and `xz`.

Ensure your bash commands/scripts can handle files with spaces or special characters in their names. The automated verification will extract your output archives and grade your modifications against the ground truth rules. You are expected to achieve at least 98% accuracy in the curation metric.