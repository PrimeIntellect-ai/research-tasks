You are an artifact manager responsible for curating a repository of compressed binary artifacts.

In the directory `/home/user/incoming`, you will find several `.gz` files. These files are rotated artifact logs. However, due to an error in the upstream writing process, some of these gzipped files contain garbage data instead of valid Executable and Linkable Format (ELF) binaries, and some are exact duplicates of each other.

Your task is to write and execute a Python script to process these artifacts and curate a clean repository.

Specifically, your script must perform the following steps:
1. Iterate through all `.gz` files in `/home/user/incoming/`.
2. Process the compressed streams *without* extracting them fully to disk beforehand (read them directly using Python's `gzip` module).
3. Identify valid ELF binaries by checking the first 4 bytes of the uncompressed stream (the ELF magic number: `\x7fELF`). Skip any file that does not start with this magic number.
4. For valid ELF binaries, calculate the SHA256 checksum of the *uncompressed* data.
5. Extract the uncompressed data of valid ELF files into a new directory: `/home/user/curated/`. The extracted file should have the same name as the original file but without the `.gz` extension (e.g., `artifact_01.bin.gz` becomes `artifact_01.bin`).
6. **Deduplication:** If you encounter multiple valid ELF files with the exact same uncompressed SHA256 checksum, do not write a duplicate file to disk. Instead, create a **hard link** in `/home/user/curated/` pointing to the first extracted file that had that checksum.
7. Generate a manifest file at `/home/user/curated/manifest.json`. The manifest must be a JSON dictionary where the keys are the extracted filenames (e.g., `artifact_01.bin`) and the values are their corresponding uncompressed SHA256 checksums.
8. Finally, create a compressed tar archive of the entire curated directory at `/home/user/curated_archive.tar.gz`.

Ensure your Python script completely handles the pipeline, and run it to produce the final `curated_archive.tar.gz`.