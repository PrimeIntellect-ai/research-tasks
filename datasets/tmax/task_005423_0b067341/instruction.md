You are assisting a technical writer in organizing a large volume of documentation. The documentation is distributed in a proprietary custom archive format called `.darc` (DocArchive). 

We have the source code for the reference extractor tool, `doc-archiver`, located at `/app/doc-archiver-1.0`. However, the build system (Makefile) has a deliberate configuration error preventing it from compiling the `darc-extract` binary correctly. 

Your task consists of two parts:
1. **Fix the vendored package**: Identify and fix the bug in `/app/doc-archiver-1.0/Makefile` (or related configuration) so that running `make` successfully produces the `darc-extract` binary. This binary reads from `stdin` and writes the extracted, transformed markdown to `stdout`.
2. **Implement a robust equivalent**: Write your own standalone program (in any language) at `/home/user/my-darc-extract` that behaves exactly like the compiled reference `darc-extract` binary. 

The `.darc` format is a simple binary stream:
- 4-byte magic number: `DARC` (in ASCII).
- 4-byte unsigned integer (little-endian): The size of the compressed payload.
- The payload: Deflate-compressed text data.

Your implementation must read from `stdin`, validate the header, decompress the payload using streaming I/O (to handle large files without loading everything into memory), and then apply a text transformation to normalize the markdown headers: all instances of `H1:` at the start of a line must be replaced with `# `, and `H2:` with `## `. The output must be written to `stdout`. Use atomic writes/temporary files internally if you need to buffer, but the final output must stream to `stdout`.

Your implementation must be bit-for-bit equivalent to the fixed reference binary for any valid `.darc` input.