You are an artifact manager tasked with curating legacy binary repositories. We recently discovered a large cache of old binaries packed in a proprietary archive format. 

The previous maintainer left behind a screenshot of the format specification, located at `/app/archive_spec.png`. Your first step is to extract the text from this image to understand the binary layout of this proprietary archive format.

Your objective is to write a Rust command-line utility that streams this proprietary archive format from Standard Input (`stdin`), converts it on-the-fly, and writes a standard uncompressed GNU Tar archive to Standard Output (`stdout`). 

Requirements:
1. Create a new Rust project at `/home/user/barc2tar`.
2. The utility must read from `stdin` and write to `stdout` to support standard stream redirection and piping. Do not buffer the entire archive in memory, as the real files might be gigabytes in size. Use streaming I/O.
3. Parse the custom archive header and entries according to the exact rules (magic bytes, endianness, field sizes) recovered from `/app/archive_spec.png`.
4. Pack the extracted files into standard GNU tar format and write it directly to `stdout`. You may use the `tar` crate.
5. If the magic bytes do not match, or if the archive is corrupted/truncated, the program should exit with code 1 and write a descriptive error to `stderr`.
6. Compile your final binary in release mode. The automated verification system will run your compiled binary at `/home/user/barc2tar/target/release/barc2tar` and compare its output bit-for-bit against a reference implementation using thousands of randomly generated inputs.

Please begin by inspecting `/app/archive_spec.png` to learn the archive structure, then implement and build your Rust converter.