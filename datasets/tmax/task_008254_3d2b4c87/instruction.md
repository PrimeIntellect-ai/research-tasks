You are helping a developer secure and organize project backups stored in a custom archive format called `.parc` (Project Archive).

The `.parc` format structure is as follows:
- Magic bytes: `PARC` (4 bytes, ASCII)
- A sequence of file records. Each record consists of:
  - Path Length: `uint16_t` (little endian)
  - Path: ASCII String of the specified length
  - Compressed Data Length: `uint32_t` (little endian)
  - Compressed Data: A custom Run-Length Encoding (RLE) format where each pair consists of `[uint8_t count][char value]`. E.g., `0x03 'A'` means "AAA".

You have been provided with a buggy, incomplete C++ extractor in `/home/user/tools/parc_extractor.cpp`. Currently, it is vulnerable to a "Zip Slip" attack: it blindly trusts the `Path` specified in the archive, which could lead to files being written outside the extraction directory if the path contains `../` or starts with `/`.

Here is what you need to do:

1. **Fix the C++ Extractor**: 
   - Edit `/home/user/tools/parc_extractor.cpp`.
   - Add path sanitization: If a file path in the archive starts with `/` or contains `../`, the extractor must **skip** extracting that file.
   - For every skipped file, append its exact malicious path (followed by a newline) to `/home/user/rejected_paths.log`.
   - Ensure the RLE decompressor works correctly (the boilerplate might need minor adjustments).
   - The compiled binary should take two arguments: `./parc_extractor <archive_file> <output_dir>`.

2. **Compile the Extractor**:
   - Compile your fixed code to `/home/user/tools/parc_extractor` using `g++`.

3. **Filter and Extract**:
   - There are multiple `.parc` files in `/home/user/raw_data/`. Only extract the ones that have the **user executable permission bit** set (`u+x`).
   - Use your compiled `parc_extractor` to extract the contents of these specific `.parc` files into `/home/user/safe_extract/`. 

4. **Organize via Hard Links**:
   - Create a directory at `/home/user/cpp_links/`.
   - Find all `.cpp` files that were successfully extracted into `/home/user/safe_extract/` (including those in subdirectories).
   - Create **hard links** for each of these `.cpp` files in `/home/user/cpp_links/`. The link names should match the original file names (assume no name collisions).

Ensure all paths are absolute and exactly match the instructions.