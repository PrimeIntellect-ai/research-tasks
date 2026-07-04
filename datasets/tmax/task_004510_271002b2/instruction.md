You are an artifact manager tasked with curating binary repositories and recovering corrupted artifact backups. Our system logs incremental modifications to ELF binaries using a custom Write-Ahead Log (WAL) format.

Your mission consists of two parts:

**Part 1: Recover the Repository ID from Video**
We lost the master repository ID, but we have a diagnostic video of the transmission at `/app/repo_sync.mp4`. 
The video is exactly 32 frames long (recorded at 1 frame per second, 32 seconds total). Each frame is solidly colored either completely Black or completely White. 
- Black frame = `0`
- White frame = `1`
Extract the 32-bit binary string (where Frame 0 is the Most Significant Bit) and convert it to a decimal integer. 
Write this exact decimal integer to `/home/user/repo_id.txt`. (You may use `ffmpeg` and python to analyze the frames).

**Part 2: Implement the WAL Patcher**
Write a Python script at `/home/user/apply_wal.py` that applies a custom WAL differential backup to an ELF file.
The script must have the following CLI usage:
`python3 /home/user/apply_wal.py <input_elf> <wal_file> <output_elf>`

**WAL Format Specification (ASCII Text):**
1. The first line is always: `REPO_ID <integer>`. 
   - If this `<integer>` does **not** match the repository ID you extracted in Part 1, your script must simply copy the `<input_elf>` to `<output_elf>` without any modifications and exit with code 0.
2. Subsequent lines contain sequential commands to mutate the binary:
   - `PATCH_SEC <section_name> <offset> <hex_string>`
     * You must find the precise file offset of the ELF section named `<section_name>` (e.g., `.text`, `.rodata`). You may use `readelf` via `subprocess` to parse the ELF metadata.
     * Overwrite the data in the file at `(section_file_offset + offset)` with the bytes represented by `<hex_string>`.
   - `APPEND <hex_string>`
     * Append the raw bytes represented by `<hex_string>` to the very end of the file.
   - `TRUNCATE <length>`
     * Truncate the file to exactly `<length>` bytes.

Process all WAL commands in order, keeping the mutations in a buffer or temporary file, and write the final result to `<output_elf>`. 
Your script must be robust. We will rigorously fuzz your script against an internal oracle using thousands of valid and invalid inputs to ensure it behaves exactly as specified, bit-for-bit.