You are an AI assistant helping a researcher process large sensor datasets. The researcher has a large continuous log file and needs a robust Rust utility to safely chunk, compress, and archive this dataset while ensuring data integrity. 

Your task is to create a Rust project in `/home/user/archiver` that builds an executable. The executable should process a raw dataset file, split it into chunks, compress each chunk, and generate a verified manifest.

Here are the strict requirements for the Rust tool:
1. **Input/Output**: The executable must take two arguments: the input file path and the output directory path. (e.g., `cargo run -- /home/user/dataset/raw_sensor.log /home/user/dataset/archive`)
2. **Chunking**: Read the input file and split it into exactly 1 MiB (1,048,576 bytes) chunks. The final chunk will be smaller if the file size is not a multiple of 1 MiB.
3. **Compression & Atomic Writes**: 
   - Compress each chunk using gzip (`flate2`).
   - You must write the compressed data to a temporary file in the output directory first (e.g., `.tmp_chunk_0000.gz`), and then atomically rename it to the final name `chunk_0000.gz`, `chunk_0001.gz`, etc.
4. **Manifest and Checksums**:
   - For each chunk, calculate the SHA-256 hash of the **uncompressed** data.
   - After all chunks are successfully written, generate a JSON manifest file named `manifest.json` in the output directory.
   - The manifest must be a JSON array of objects. Each object must have exactly two keys: `"chunk"` (the final filename, e.g., "chunk_0000.gz") and `"original_sha256"` (the hex-encoded SHA-256 hash of the uncompressed chunk).
   - The manifest must also be written atomically (write to `.tmp_manifest.json` then rename to `manifest.json`).

Before you begin, assume the dataset is located at `/home/user/dataset/raw_sensor.log` and the output directory `/home/user/dataset/archive` exists (if not, your tool should create it). 

Write, build, and run the Rust application to process `/home/user/dataset/raw_sensor.log` and output the results to `/home/user/dataset/archive`. Leave the generated archive files and manifest in place for verification.