You are an artifact manager curating a binary repository. We have received a compressed archive of proprietary binary artifacts that need to be parsed, chunked, compressed, and indexed.

Your task is to write a Rust program that processes these files and outputs a structured repository format. 

Here are the requirements:

1. **Input Setup**:
   You will find an input archive at `/home/user/artifacts.tar.gz`. Extract it to read the `.bin` files inside.

2. **Binary Format**:
   Each `.bin` file uses a custom proprietary format:
   - Bytes [0..4]: Magic bytes `ARTF` (ASCII)
   - Byte [4]: Version (Must be `0x01`)
   - Bytes [5..7]: Length of the artifact name, `N` (16-bit unsigned integer, Little Endian)
   - Bytes [7..7+N]: Artifact Name (UTF-8 string)
   - Bytes [7+N..7+N+8]: Payload length, `P` (64-bit unsigned integer, Little Endian)
   - Bytes [7+N+8..7+N+8+P]: The actual binary payload.

3. **Processing Requirements**:
   Write and run a Rust program (e.g., in `/home/user/artifact_processor`) that reads all extracted `.bin` files.
   For each artifact:
   - Extract the payload.
   - Split the payload into chunks of exactly 1024 bytes (the final chunk may be smaller).
   - Compress each chunk using GZIP.
   - Save the compressed chunks to `/home/user/repo_out/<artifact_name>/chunk_<index>.gz` (where `<index>` starts at 0).
   
4. **Manifest Generation**:
   Your program must generate a single index file at `/home/user/repo_out/manifest.json`.
   The JSON file must have the following exact schema:
   ```json
   {
     "artifacts": {
       "<artifact_name>": [
         {
           "chunk": "chunk_0.gz",
           "sha256": "<lowercase hex sha256 of the GZIPPED chunk file>"
         },
         ...
       ]
     }
   }
   ```
   (The keys under "artifacts" should be the parsed artifact names from the `.bin` files, not the original `.bin` filenames. The list of chunks must be in order.)

Please implement the Rust program, build it (using `cargo`), and run it so that the `/home/user/repo_out` directory and `manifest.json` are populated correctly.