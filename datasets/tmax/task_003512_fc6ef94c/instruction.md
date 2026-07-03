You are an artifact manager tasked with curating a repository of binary artifacts. 

A legacy archiving system has dumped several important binary files into a custom text-based format called a "HexArchive". You have been provided with this archive at `/home/user/artifacts.hexar`.

The HexArchive format is structured as follows:
- A file entry begins with a header line strictly formatted as: `=== FILE: <filename> ===`
- The body consists of hexadecimal byte values separated by whitespace, spanning multiple lines.
- The file entry ends with a footer line strictly formatted as: `=== END ===`

During the archiving process, a known bug corrupted the streams: any contiguous sequence of exactly three null bytes (`00 00 00`) in the original binary was mistakenly written to the archive as three null bytes but SHOULD be restored to three `FF` bytes (`FF FF FF`). Sequences of less than or more than three `00` bytes are independent and should not be modified, but a stream of exactly three `00`s must be replaced. (For example, `01 00 00 00 02` becomes `01 FF FF FF 02`. A sequence of four nulls `00 00 00 00` remains `00 00 00 00` as it is not exactly three).

Your task:
1. Write a C program at `/home/user/extractor.c` that parses `/home/user/artifacts.hexar`.
2. The C program must extract the binary files, apply the byte sequence correction (`00 00 00` -> `FF FF FF` only when exactly 3 consecutive null bytes occur), and save the decoded binary files into the directory `/home/user/extracted/` (you will need to create this directory).
3. Compile and run your C program to perform the extraction.
4. Generate a manifest file at `/home/user/manifest.txt` containing the SHA-256 checksums of all the extracted binaries. The manifest should be formatted precisely like the output of `sha256sum`, with only the basename of the file (e.g., `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  alpha.bin`), and the lines must be sorted alphabetically by filename.

Constraints:
- You must use C to perform the parsing, logic correction, and binary file creation.
- You may use standard Bash utilities to compile your C program and generate the final checksum manifest.