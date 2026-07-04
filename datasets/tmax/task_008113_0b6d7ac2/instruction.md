You are an artifact manager tasked with migrating a legacy binary repository to a new format. The old system stored binaries using a custom Run-Length Encoding (RLE) format across a nested directory structure.

Your objective is to write a Rust utility to decompress these files, apply it across the directory tree, and construct a flat, content-addressable symlink view of the artifacts.

**Repository Structure:**
- The raw artifacts are located in `/home/user/artifacts/raw/`. They are nested in various subdirectories.
- Every legacy artifact has a `.blob` extension.

**Custom RLE Format:**
The `.blob` files are binary files encoded as a sequence of byte pairs: `[count, value]`.
- `count` (1 byte, unsigned): The number of times the `value` is repeated.
- `value` (1 byte): The actual data byte.
- The file is terminated if a `count` of `0` is encountered (the corresponding `value` byte should be ignored, and reading should stop).

**Your Tasks:**
1. **Create a Rust tool**: Initialize a Rust project at `/home/user/rle_tool` and write a program that takes an input `.blob` file path and an output `.bin` file path, and decompresses the RLE format.
2. **Process all artifacts**: Recursively traverse `/home/user/artifacts/raw/`. For every `.blob` file found, use your Rust tool to decompress it. Save the decompressed output in the same directory as the original file, but with the extension `.bin` instead of `.blob`.
3. **Create a flattened, content-addressable view**: Create a directory at `/home/user/artifacts/latest/`. For every decompressed `.bin` file, compute its SHA256 checksum. Create a symbolic link in `/home/user/artifacts/latest/` named `<sha256_hash>.bin` that points to the absolute path of the decompressed `.bin` file.

**Verification:**
An automated test will check:
- The presence and correct content of the `.bin` files in the `/home/user/artifacts/raw/` tree.
- The presence of the `/home/user/artifacts/latest/` directory.
- That `/home/user/artifacts/latest/` contains exactly the right symlinks, named using the SHA256 hashes of the decompressed contents (lowercase hex), correctly pointing to the corresponding `.bin` files.