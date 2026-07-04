You are tasked with helping a developer organize and verify a set of custom project archive files. 

A previous backup job produced several large binary archive files located in `/home/user/archives/`. The backup tool also generated a configuration file at `/home/user/project_files.toml` which contains a list of these files in the following format:

```toml
[archives]
files = [
    "/home/user/archives/data_A.bin",
    "/home/user/archives/data_B.bin",
    "/home/user/archives/data_C.bin",
    "/home/user/archives/data_D.bin"
]
```

These custom archive files can be very large, so we need a highly efficient way to verify their integrity. A valid archive file must end with exactly this 17-byte string signature: `VALID_ARCHIVE_EOF`. If a file does not end with this exact string, or is smaller than 17 bytes, it is considered corrupted.

Please create a Rust project in `/home/user/verifier` and write a Rust program that does the following:
1. Parses `/home/user/project_files.toml` to extract the list of file paths.
2. Uses memory-mapped I/O (via the `memmap2` crate) to efficiently inspect the end of each file without streaming the entire contents into memory.
3. Verifies the integrity of each archive by checking if the last 17 bytes exactly match `VALID_ARCHIVE_EOF`.
4. Writes the absolute paths of any corrupted or invalid archives to `/home/user/corrupted_archives.log`. Write one path per line, and ensure the lines are sorted alphabetically.

You may use standard Rust ecosystem crates like `serde`, `toml`, and `memmap2`. Run your Rust program to generate the `/home/user/corrupted_archives.log` file.