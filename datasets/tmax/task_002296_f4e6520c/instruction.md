You are a support engineer tasked with recovering diagnostic telemetry data from a corrupted binary file. 

The customer provided a binary dump file at `/home/user/telemetry.bin` and a Go script `/home/user/reader.go` that they use to parse the file. However, the script crashes when trying to read this specific dump.

The customer mentioned two issues:
1. **Corrupted Input**: The telemetry device sometimes writes arbitrary garbage bytes to the file during a brownout. The parser needs to recover from this and find the next valid record in the stream. Valid records always end with a specific 4-byte magic marker (which you can find by reading `reader.go`).
2. **Floating-Point Precision Loss**: Due to a known firmware bug, the device sometimes writes the `Value` field as a 32-bit float (`float32`) instead of the standard 64-bit float (`float64`). When this happens, the first 4 bytes of the 8-byte value field contain the `float32` (in little-endian), and the remaining 4 bytes are padded with `0xFFFFFFFF`.

Your task:
1. Analyze `/home/user/reader.go` to understand the expected binary format and identify why it crashes.
2. Write a repaired Go script at `/home/user/recover.go` that reads `/home/user/telemetry.bin`.
3. Your script must scan through the file, skipping over any garbage bytes, and extract all valid records.
4. For each valid record, correctly parse the `Value` field. If it was written as a padded `float32`, convert it correctly so that the actual value is recovered rather than interpreting the padding as part of a `float64` mantissa/exponent.
5. Write the recovered data to `/home/user/recovered.csv`.

**Requirements for `/home/user/recovered.csv`**:
- The file must contain one line per recovered record.
- The format must be strictly: `ID,Value`
- The `Value` must be formatted to exactly 4 decimal places (e.g., `10.5000`).
- Example output line: `1,10.5000`

Use your Go programming and binary debugging skills to recover all records.