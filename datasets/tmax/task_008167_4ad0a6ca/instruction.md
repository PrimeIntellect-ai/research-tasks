You are an AI assistant helping a technical writer recover fragmented documentation. 

The writing team uses an experimental distributed text editor that continuously syncs work by writing changes to a custom Write-Ahead Log (WAL) format. Unfortunately, the system crashed during a log rotation process, leaving behind a single interleaved WAL file at `/home/user/doc_events.wal` instead of the standard compiled documents.

Your task is to write a C++ program that parses this WAL file, reconstructs the original documents by merging their chunks in the correct sequence, and saves them to an output directory. To ensure data integrity (simulating the prevention of race conditions during concurrent log rotations), you must use atomic writes for the output files.

### WAL Format Specification
The `/home/user/doc_events.wal` file contains a continuous stream of headers and payloads:
1.  **Header Line**: Every chunk starts with a header on a single line with the format: `HEADER|<DOC_ID>|<CHUNK_SEQ>|<SIZE>`
    *   `DOC_ID`: Integer representing the document ID.
    *   `CHUNK_SEQ`: Integer representing the 0-indexed sequence number of the chunk.
    *   `SIZE`: Integer representing the exact number of bytes in the payload.
2.  **Payload**: Exactly `<SIZE>` bytes of text immediately following the newline character of the header line.
3.  The next header begins immediately after the payload's final byte.

### Requirements
1.  Create a working directory at `/home/user/output_docs/`.
2.  Write a C++ program at `/home/user/doc_parser.cpp` and compile it to `/home/user/doc_parser`.
3.  The program must read `/home/user/doc_events.wal`.
4.  For each unique `DOC_ID`, merge all chunks in ascending order of `CHUNK_SEQ`.
5.  **Atomic Writes**: The program must write the merged content for each document to a temporary file in `/home/user/output_docs/` (e.g., `/home/user/output_docs/.tmp_doc_<DOC_ID>.txt`) and then use the POSIX `rename()` function (or standard C++ filesystem equivalents) to atomically rename it to the final destination `/home/user/output_docs/doc_<DOC_ID>.txt`.
6.  Once the C++ program finishes, run a bash command to generate a SHA-256 checksum manifest of the recovered files at `/home/user/output_docs/manifest.sha256`. The format must exactly match the standard output of the `sha256sum` command (e.g., `[hash]  doc_<DOC_ID>.txt`).

Do not leave any temporary files in the output directory. Write your C++ code, compile it, run it, and generate the manifest.