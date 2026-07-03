You are tasked with porting a legacy Linux data archiving tool into a minimal container environment. The legacy tool processes massive amounts of telemetry data, but it is too slow for our new high-throughput requirements. 

Your objective is to fix the environment's C-based validator, analyze the custom archive format, and write a high-performance, concurrent replacement in Go.

**Step 1: Fix the Archive Validator**
There is a C-based archive validation tool located in `/workspace/validator_src/`. However, the build configuration is broken.
1. Inspect and repair the `Makefile` in `/workspace/validator_src/`. It currently fails to compile due to syntax and linking errors.
2. Build the validator. The final executable must be located at `/workspace/validator_src/validator`.
3. This tool can be used to verify if a given `.pak` file is structurally sound by running: `./validator <archive.pak>`

**Step 2: Understand the Custom Archive Format**
We have provided the legacy, stripped binary at `/app/packer_oracle`. This tool packs a directory of files into our custom "PAK1" format.
Usage: `/app/packer_oracle <input_directory> <output_file.pak>`

The PAK1 binary format is structured as follows:
- **Header:** 4 bytes representing the ASCII string `PAK1` (0x50, 0x41, 0x4B, 0x31).
- **File Count:** 1 unsigned 32-bit integer (Little-Endian) representing the number of files in the archive.
- **File Records:** The entries **must be sorted alphabetically** by their relative file path. For each file:
  - **Path Length:** 1 unsigned 16-bit integer (Little-Endian).
  - **Path:** The relative path of the file (e.g., `subdir/file.txt`), exactly `Path Length` bytes long.
  - **File Size:** 1 unsigned 32-bit integer (Little-Endian).
  - **Checksum:** 1 unsigned 32-bit integer (Little-Endian). This must be the **Fletcher-32** checksum of the file's uncompressed data.
  - **Data:** The raw bytes of the file.

*Note on Fletcher-32:* 
- Sum1 and Sum2 are initialized to 0xFFFF. 
- Process the data stream in 16-bit words (Little-Endian). If the data length is odd, pad the final word with a 0x00 byte for the calculation.
- Modulo used is 65535.
- The final 32-bit checksum is `(Sum2 << 16) | Sum1`.

**Step 3: Implement the Fast Go Packer**
Write a Go program at `/workspace/fast_packer.go` that takes an input directory and an output file path as arguments, exactly like the oracle.
- It must produce a completely valid PAK1 archive that is **bit-for-bit identical** to the output of `/app/packer_oracle`.
- You **must** utilize Go's concurrency features (goroutines, channels, or WaitGroups) to read files and compute their Fletcher-32 checksums in parallel. The legacy oracle is strictly sequential and slow.
- Your Go implementation will be tested against a massive dataset. To pass the evaluation, your program must execute at least **2.5x faster** than `/app/packer_oracle`.

Leave your completed, working Go source code at `/workspace/fast_packer.go`.