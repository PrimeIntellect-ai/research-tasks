You are helping me debug a failing test in a Rust project located at `/home/user/wal_parser`. 

This library parses a simple Write-Ahead Log (WAL) format for a custom database. Recently, a corrupted journal file was introduced to the test suite, causing `cargo test` to panic. The test reads from `/home/user/wal_parser/test_data/journal.wal`.

The WAL format consists of consecutive records:
- `[1 byte]` Record Type
- `[4 bytes]` Payload Length (Little Endian `u32`, let's call it `N`)
- `[N bytes]` Payload

Your task is to:
1. Diagnose the failing build (`cargo test` panics due to out-of-bounds slice access).
2. Fix the edge-case in `src/lib.rs` so that the `parse_wal` function gracefully returns `Err(Error::UnexpectedEof)` whenever a record's length exceeds the remaining buffer size, instead of panicking. 
3. Locate the exact 0-indexed byte offset of the beginning of the corrupted record (the 1-byte record type) inside `test_data/journal.wal`.
4. Write this integer byte offset to a file named `/home/user/corrupt_offset.txt`.
5. Ensure that `cargo test` passes after your modifications.

Do not change the function signatures or the `Error` enum in `src/lib.rs`. Only modify the logic inside `parse_wal` to fix the panic and return the correct error.