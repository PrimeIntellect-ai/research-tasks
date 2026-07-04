You are tasked with building a configuration tracking utility for a custom firmware deployment system. The system tracks configurations embedded within ELF binaries and converts their metadata into a Write-Ahead Log (WAL) format.

Your objective has two parts:

Part 1: Fix the Vendored Test Environment
There is a test data generator package located at `/app/vendored-tracker-1.2`. 
1. The `Makefile` in this package contains a bug: it uses a macOS-style `sed` command (`sed -i '' ...`) which fails on our Linux environment.
2. Fix the `Makefile` to use standard GNU `sed` syntax.
3. Run `make setup` inside `/app/vendored-tracker-1.2`. This will compile several test ELF binaries and place them into `/home/user/test_elfs/`.

Part 2: Write the Extraction Script
Write a pure Bash script at `/home/user/elf_to_wal.sh` that does the following:
1. Accepts exactly one argument: the path to an ELF file.
2. Uses standard system utilities (like `readelf -S`) to parse the section headers of the provided ELF file.
3. Identifies all sections whose names begin with `.cfg_`.
4. For each matching section, extracts the section's Name, Size, and Offset. Note that `readelf` outputs Size and Offset in hexadecimal without a `0x` prefix.
5. Performs a format conversion on the extracted values:
   - Convert the Size from hexadecimal to a decimal integer.
   - Keep the Offset in hexadecimal, but prepend it with `0x` and make sure the hex characters are lowercase (e.g., `0x01a4`).
6. Prints a formatted log entry to Standard Output (stdout) for each matched section, strictly in the order they appear in the `readelf` output.

The output format for each matched section must be exactly:
`WAL_RECORD: name=<NAME> size=<SIZE_DECIMAL> offset=<OFFSET_HEX>`

Example output:
`WAL_RECORD: name=.cfg_network size=1024 offset=0x04b0`
`WAL_RECORD: name=.cfg_auth size=256 offset=0x08c0`

Requirements:
- Your script must be written in Bash (using standard CLI tools like `awk`, `grep`, `sed`, `readelf` is permitted).
- Do not output anything else to stdout (no debugging information, no headers).
- If no `.cfg_` sections are found, the script should output nothing and exit with status 0.