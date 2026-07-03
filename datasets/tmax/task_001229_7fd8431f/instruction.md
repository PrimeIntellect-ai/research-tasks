You are tasked with writing a modern Go replacement for a legacy configuration manager tool. 

The legacy tool is a stripped binary located at `/app/conf_reader`. It reads custom configuration archive files (`.carc` format), verifies their integrity, resolves internal virtual symlinks (handling infinite loops caused by a known backup bug), converts the data to JSON, and writes the output atomically.

Your goal is to write a Go program at `/home/user/reader.go` that behaves **exactly** like `/app/conf_reader` (bit-exact output equivalence, including error cases). You can use the legacy binary to test your hypotheses about its behavior.

### Archive Format Spec (`.carc`)
The binary file format is structured as follows:
1. **Magic Bytes**: `C` `A` `R` `C` (4 bytes).
2. **Checksum**: 4 bytes, Little-Endian CRC32 (IEEE polynomial). The CRC is calculated over all bytes in the file *following* this 4-byte checksum field.
3. **Entries**: Repeating sequence of entries until EOF:
   - **Type**: 1 byte (`0x01` for File, `0x02` for Symlink).
   - **PathLength**: 1 byte (unsigned).
   - **Path**: `PathLength` bytes (UTF-8 string).
   - *If Type is File (`0x01`)*:
     - **ContentLength**: 2 bytes, Little-Endian (unsigned).
     - **Content**: `ContentLength` bytes (UTF-8 string).
   - *If Type is Symlink (`0x02`)*:
     - **TargetLength**: 1 byte (unsigned).
     - **Target**: `TargetLength` bytes (UTF-8 string).

### Processing Rules
1. **Integrity Check**:
   - If the magic bytes are not `CARC`, output exactly: `{"error": "bad_magic"}`
   - If the CRC32 does not match the computed checksum of the payload, output exactly: `{"error": "bad_crc"}`
2. **Symlink Resolution**:
   - The archive defines a virtual filesystem.
   - For *every* path defined in the archive (whether it originated as a File or a Symlink), you must output its final resolved content.
   - If a symlink points to another symlink, follow it.
   - If a symlink resolves to a missing path, its resolved content is the literal string `"<BROKEN>"`.
   - If a symlink resolution enters an infinite loop, its resolved content is the literal string `"<LOOP>"`.
3. **Format Conversion & Atomic Write**:
   - The output must be a single JSON object mapping each original `Path` to its resolved content string. (Format standard Go JSON map).
   - To prevent partial writes during concurrent backups, the program **must** write the JSON to `<output_file>.tmp` first, and then atomically rename it to `<output_file>`.

### Execution
Your program will be invoked exactly like the legacy tool:
`go run /home/user/reader.go <input_archive.carc> <output_file.json>`

You must implement `/home/user/reader.go`. Do not use any third-party libraries; standard library only.