You are acting as an artifact manager curating a messy binary repository. A previous automated build system dumped multiple compressed binary artifacts into a single directory and left behind a massive, outdated manifest file. 

Your task is to organize these artifacts and update the manifest using Python.

Here is the current state of the system:
1. **Raw Artifacts**: Located in `/home/user/raw_artifacts/`. There are several `.bin.gz` files. These files are gzip-compressed. If you read the uncompressed stream of each file, the first 8 bytes consist of an ASCII string representing the architecture type (e.g., `ARCH_X86`, `ARCH_ARM`).
2. **Manifest**: Located at `/home/user/metadata/manifest.txt`. It contains build logs and paths.

Please write and execute a Python script (or multiple scripts) to perform the following operations:

**Part 1: Artifact Curation (Header Extraction & Symlinking)**
1. Iterate through all `.bin.gz` files in `/home/user/raw_artifacts/`.
2. Open each compressed file and read *only* the first 8 bytes of the uncompressed data to extract the architecture header. Do not decompress the entire file to disk.
3. Create a structured repository in `/home/user/curated/`. For each unique architecture header found, create a subdirectory (e.g., `/home/user/curated/ARCH_X86/`).
4. Inside the appropriate subdirectory, create a **symbolic link** pointing to the original `.bin.gz` file. The symlink must use absolute paths and have the same name as the target file (e.g., `/home/user/curated/ARCH_X86/artifact_01.bin.gz` -> `/home/user/raw_artifacts/artifact_01.bin.gz`).

**Part 2: Large-Scale Text Editing & Merging**
1. The file `/home/user/metadata/manifest.txt` is large. Read it and replace every instance of the string `SERVER_A_DEPRECATED` with `SERVER_B_ACTIVE`.
2. Save the updated content to `/home/user/metadata/manifest_updated.txt`.

**Part 3: Reporting**
1. Generate a JSON report at `/home/user/report.json` with the following structure:
```json
{
  "artifact_01.bin.gz": "ARCH_X86",
  "artifact_02.bin.gz": "ARCH_ARM"
}
```
(Include all artifacts in the actual output, mapped to their extracted 8-byte header).

Ensure all scripts are run and the final files and directories are in place before you complete the task.