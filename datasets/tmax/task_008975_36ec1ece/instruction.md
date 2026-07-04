I need you to help me organize some messy project backups. I have a master archive located at `/home/user/project_dump/master.zip` that contains a mixture of files and nested archives (`.zip` and `.tar.gz`), some of which are nested up to 2 levels deep. 

I need you to write and run a Rust program that deeply traverses these archives, extracts their contents, and searches for two specific types of binary files based strictly on their magic numbers (file signatures), regardless of their current file extensions:
1. **ELF Executables**: Files starting with the bytes `0x7F 0x45 0x4C 0x46` (`\x7fELF`).
2. **SQLite WAL (Write-Ahead Log) files**: Files starting with the bytes `0x37 0x7F 0x06 0x82` OR `0x37 0x7F 0x06 0x83`.

Your Rust program should:
1. Be created in a new Cargo project at `/home/user/archive_organizer`.
2. Recursively extract `master.zip` and any `.zip` or `.tar.gz` files found inside it to a temporary directory.
3. Scan every extracted file to check its magic number against the ELF and WAL signatures.
4. For every ELF and WAL file found, calculate its SHA-256 hash.
5. Create a new, flat gzipped tarball archive at `/home/user/extracted_artifacts.tar.gz`.
6. Add all the identified files into the root of this new `extracted_artifacts.tar.gz` archive. The files must be named using their SHA-256 hash in lowercase hex, followed by the appropriate extension: `<sha256>.elf` for ELF files, and `<sha256>.wal` for WAL files. Do not preserve the original filenames or directory structures inside the new archive.

You may use standard Rust crates from crates.io (such as `tar`, `flate2`, `zip`, `sha2`, `walkdir`) by adding them to your `Cargo.toml`. The final output must be precisely located at `/home/user/extracted_artifacts.tar.gz`. Let me know once the script has finished executing and the archive is generated.