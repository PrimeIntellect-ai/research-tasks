You are an Artifact Manager curating a repository of binary assets for a legacy system. An automated backup dump has placed thousands of files in `/home/user/incoming_artifacts`. Your goal is to write a Rust tool to traverse this directory tree, identify specific custom binary files, validate their headers, and package the valid ones into a curated release archive with a manifest.

**The Custom Binary Format (`.bx`)**
Valid artifacts are files with the `.bx` extension that conform exactly to this binary structure:
1. **Magic Bytes (4 bytes):** ASCII characters `B`, `X`, `0`, `1` (Hex: `42 58 30 31`).
2. **Version (2 bytes):** Unsigned 16-bit integer, Little Endian. We only support version `2` or higher (i.e., >= 2).
3. **Payload Length (4 bytes):** Unsigned 32-bit integer, Little Endian.
4. **Payload (Variable):** Raw bytes. The length of this section must match *exactly* the Payload Length field. Any file with trailing bytes or truncated payloads is considered corrupted.

**Your Tasks:**
1. Write a Rust project in `/home/user/curator` (you can initialize it with `cargo new`) that performs the curation.
2. Recursively traverse `/home/user/incoming_artifacts`.
3. Handle archives: If you encounter a `.zip` or `.tar.gz` file, you must inspect its contents (in memory or extracted to a temp folder) for `.bx` files. Nested archives (e.g., a zip inside a tar) do not need to be processed; just check one level deep inside archives for `.bx` files.
4. Parse every `.bx` file (standalone or inside archives) and validate it against the `.bx` binary format rules.
5. For every **valid** `.bx` file, compute its SHA-256 hash.
6. Copy valid `.bx` files into a new flat directory `/home/user/curated_artifacts/`. Rename each copied file to its SHA-256 hash with the `.bx` extension (e.g., `a1b2c3...d4.bx`).
7. Create a JSON manifest file at `/home/user/curated_artifacts/manifest.json`. The manifest must be a JSON object mapping the new SHA-256 filename to the original basename of the file. If two valid files have the same original basename but different contents, both should be processed. If they have identical contents (same hash), only one copy needs to exist in the curated folder, but the manifest should map the hash to the original basename. Format:
```json
{
  "1234567890abcdef...1234.bx": "original_name1.bx",
  "abcdef1234567890...5678.bx": "extracted_file.bx"
}
```
8. Compress the `/home/user/curated_artifacts/` directory into a standard zip archive at `/home/user/curated_release.zip`. The zip should contain the files directly or within a `curated_artifacts` folder, as long as the manifest and `.bx` files are present.

You may use standard Cargo crates like `walkdir`, `zip`, `tar`, `flate2`, `sha2`, and `serde_json`. You will need to write the Rust code, build it (`cargo run --release`), and ensure the final `curated_release.zip` is created perfectly.