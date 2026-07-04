You are helping a developer organize and normalize legacy project files. The developer needs a utility to parse various file headers (ELF binaries, SQLite WAL files, and raw text) to extract metadata and normalize it using a specific hardware calibration factor.

Your task is to write a C program at `/home/user/normalize.c` and compile it to `/home/user/normalize`.

### Phase 1: Recover the Calibration Factor
We have a recording of the hardware diagnostic LED from the original server: `/app/diagnostic.mp4`. 
You must analyze this video to find the calibration factor `N`. 
`N` is defined as the exact number of frames in the video where the mean color of the frame is predominantly green (specifically: mean Green channel > 200, mean Red channel < 50, and mean Blue channel < 50). 
You may use `ffmpeg` and any scripting languages (e.g., Python, Bash) to extract this number. Do not hardcode a guess; compute it.

### Phase 2: Build the Normalization Utility
Write a C program that reads exactly 64 bytes from `stdin` and writes a single newline-terminated string to `stdout`.

The program must inspect the 64 bytes and behave as follows:

1. **ELF Binary Detection:**
   If the first 4 bytes are `\x7FELF`, treat the 64 bytes as a standard 64-bit Little-Endian ELF header.
   - Extract the 16-bit `e_type` (offset 0x10), 16-bit `e_machine` (offset 0x12), and 64-bit `e_entry` (offset 0x18).
   - Add `N` to the `e_entry` value.
   - Print `ELF %04x %04x %016lx\n` substituting the extracted/calculated values.

2. **WAL File Detection:**
   If the first 4 bytes are `WAL\x00`, treat it as a mock Write-Ahead Log header.
   - Extract the 32-bit Little-Endian integer at offset 8 (the "salt").
   - Compute the bitwise XOR of the salt and `N`.
   - Print `WAL %08x\n` with the result.

3. **Text Fallback:**
   If neither of the above signatures match, treat the 64 bytes as a sequence of 32 UTF-16LE encoded characters.
   - Convert this UTF-16LE sequence into a UTF-8 byte array.
   - Take exactly the first `N` bytes of the resulting UTF-8 array (if the UTF-8 array is shorter than `N` bytes, take the whole array).
   - Replace any unprintable ASCII characters (any byte not in the range `0x20` to `0x7E` inclusive) with a period (`.`).
   - Print the resulting string followed by a newline.

**Requirements:**
- Your C code must compile cleanly using `gcc /home/user/normalize.c -o /home/user/normalize`.
- The program must not output anything else to stdout.
- The program must be robust to arbitrary 64-byte inputs (it will be heavily fuzzed against a reference implementation).