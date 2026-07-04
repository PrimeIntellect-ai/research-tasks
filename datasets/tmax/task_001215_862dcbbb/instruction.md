You are an AI assistant helping a technical writer organize and process a complex documentation system.

The workspace is located at `/home/user/docs_system/`. Inside, you will find:
1. A `drafts/` directory containing several markdown (`.md`) files.
2. A monolithic documentation file named `monolith.md`.

You must perform the following operations:

1. **Metadata Search & Text Transformation**: 
   Find all `.md` files in `/home/user/docs_system/drafts/` that contain the exact string `[SECRET]`. In those specific files, replace all occurrences of `[SECRET]` with `[REDACTED]` in-place. Leave files that do not contain `[SECRET]` untouched.

2. **File Merging**:
   Merge the contents of *only* the modified files (the ones where you replaced `[SECRET]`) into a new file `/home/user/docs_system/merged_drafts.md`. Concatenate them in alphabetical order of their original filenames.

3. **Custom Splitting and Compression (C++)**:
   Write a C++ program at `/home/user/docs_system/processor.cpp` and compile it to `/home/user/docs_system/processor`.
   The program must read `/home/user/docs_system/monolith.md` and split it into multiple chunks based on the delimiter line: `---SPLIT---`
   - Every time this exact line is encountered, it marks the boundary between chunks. Do not include the delimiter line in the chunks.
   - For each chunk, save it to a directory `/home/user/docs_system/chunks/` as `chunk_1.rle`, `chunk_2.rle`, etc. (1-indexed). You must create the `chunks/` directory if it does not exist.
   - **Custom Compression**: Before writing a chunk to disk, apply a strict Run-Length Encoding (RLE) to its contents. The RLE format must encode *every* character (including newlines and spaces) as its count followed by the character itself. For example, the string `"AABBB\n\nC"` must be written to the `.rle` file exactly as `"2A3B2\n1C"`. When accumulating text for a chunk, include the newline characters at the end of each line (except for the delimiter lines).

4. **Manifest and Checksum Generation**:
   Generate a manifest file at `/home/user/docs_system/manifest.txt` containing the SHA-1 checksums of all the generated `.rle` files.
   - Format each line exactly as the default output of `sha1sum`: `<checksum>  <filename>`
   - The filenames in the manifest must be just the base filenames (e.g., `chunk_1.rle`), NOT the full paths.
   - Sort the lines in the manifest alphabetically by filename.

Ensure all file paths and outputs match the specifications exactly.