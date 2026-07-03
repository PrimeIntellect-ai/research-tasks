You are an artifact manager responsible for curating binary repositories. We have received a new batch of binary artifacts packaged in a custom, proprietary format called "CBND" (Custom BuNDle). These bundles are scattered throughout a directory structure.

Your task is to write a custom extraction tool in C, extract all artifacts from the repository, and generate a verified manifest.

**The CBND File Format:**
The `.cbnd` format is a simple binary archive containing zlib-compressed streams.
1. **Header:** 
   - 4 bytes: Magic string `"CBND"` (no null terminator).
   - 4 bytes: `uint32_t` (little-endian), number of entries in the bundle.
2. **Index Entries** (immediately following the header, one for each entry):
   - 64 bytes: Null-padded ASCII filename.
   - 4 bytes: `uint32_t` (little-endian), compressed size in bytes.
   - 4 bytes: `uint32_t` (little-endian), uncompressed size in bytes.
   - 4 bytes: `uint32_t` (little-endian), absolute byte offset from the beginning of the `.cbnd` file where the compressed data stream for this file begins.
3. **Data Section:**
   - Raw `zlib`-compressed data streams located at the offsets specified in the index.

**Instructions:**
1. **Develop the Extractor:** Write a C program at `/home/user/extractor.c` that takes two arguments: `<input_cbnd_file>` and `<output_directory>`. 
   - The program must parse the `.cbnd` file, seek to the offsets, decompress the streams using the `zlib` library, and write the uncompressed files into the specified output directory.
   - Ensure you compile it to `/home/user/extractor` (e.g., using `gcc`). You may assume standard zlib development headers are available (`libz-dev`).

2. **Process the Repository:**
   - The root of the repository is at `/home/user/artifact_repo`. It contains several subdirectories with `.cbnd` files.
   - Create a directory `/home/user/extracted_artifacts`.
   - Find all `.cbnd` files in the repository and use your C program to extract their contents into `/home/user/extracted_artifacts`. (If multiple bundles contain files with the same name, they can overwrite each other, though in this dataset, filenames are uniquely named across all bundles).

3. **Generate Manifest:**
   - After extracting all files, compute the SHA-256 hash of every extracted file in `/home/user/extracted_artifacts`.
   - Create a file at `/home/user/manifest.txt` with the format: `<sha256>  <filename>\n`
   - Sort the manifest alphabetically by filename. Do not include directory paths in the filename column, just the basename.

Ensure your program handles errors gracefully (e.g., if a file is malformed, skip it, though all provided files are well-formed). The final evaluation will check the contents of `/home/user/manifest.txt` against the ground truth.