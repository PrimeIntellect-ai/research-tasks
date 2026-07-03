I am a researcher working with a massive collection of proprietary sensor data from a recent neuroimaging study. The datasets are delivered in a custom binary format (`.pdat` archives). I have a proprietary pre-compiled tool located at `/app/header_parser` that validates these archives and extracts their metadata. 

However, this tool is a closed-source binary, and my university's high-performance computing cluster uses an architecture that cannot run it. I need to transition to an open implementation. 

Your objective is to reverse-engineer the behavior of `/app/header_parser` and write a 100% equivalent Bash script, then use it to organize my chaotic raw data directory.

**Step 1: Reverse Engineer and Replicate the Parser**
Analyze `/app/header_parser`. It takes a single file path as an argument and prints out metadata about the file's header and payload integrity.
You must create a Bash script at `/home/user/parse_header.sh` that perfectly replicates the standard output and error handling of `/app/header_parser` for any arbitrary input file. My automated systems will fuzz your script against the original binary with thousands of random inputs to ensure exact bit-for-bit behavioral equivalence.
Your script must natively perform the binary format extraction and archive integrity verification (the binary computes a checksum of the payload data starting immediately after the header). 

**Step 2: Bulk Renaming & Organization**
I have a directory of raw, unsorted sensor files at `/home/user/raw_data/`. 
Create a second script, `/home/user/organize_data.sh`, that uses your `parse_header.sh` script to process all `.dat` files in `raw_data`. For each file:
1. Parse the header.
2. If the integrity is invalid, or if there is an error (e.g., bad magic number), log the filename to `/home/user/corrupt_files.log` and skip it.
3. If valid, copy the file into `/home/user/organized_data/` using the directory structure `DEV_<device_id>/EXP_<exp_id>/<timestamp>.dat`.
4. The move must be done safely: copy the file to a temporary file in `/home/user/organized_data/.tmp/` first, and once the copy is complete, atomically rename it to its final destination to prevent partial file writes during a potential crash.

Ensure `/home/user/parse_header.sh` is robust, executable, and relies primarily on standard Bash and Linux utilities (like `od`, `hexdump`, `crc32`, `dd`, etc.).