You are helping a technical writer automate the organization of their documentation files. The writer has a large, nested repository of drafts and notes located in `/home/user/docs_raw`. 

Some files are stored as plain text (`.md`, `.txt`), while others have been individually compressed with gzip (`.md.gz`, `.txt.gz`) to save disk space. Every document contains a metadata header at the very beginning.

Your task is to write and execute a Go program at `/home/user/doc_builder.go` that performs the following operations:
1. Recursively traverse the `/home/user/docs_raw` directory.
2. Identify all files ending in `.md`, `.txt`, `.md.gz`, or `.txt.gz`.
3. Read the contents of each file. For `.gz` files, you must decompress the stream on the fly in memory (do not create temporary uncompressed files on disk).
4. Check if the file contains a line starting exactly with `Status: Publish` (case-sensitive).
5. If the file is marked for publishing, add its uncompressed contents to a new compressed archive located at `/home/user/published_docs.tar.gz`.
6. Inside the `.tar.gz` archive, the file paths must be relative to the `/home/user/docs_raw` directory. Furthermore, any `.gz` extension must be removed from the filename in the archive. For example, if a published file is at `/home/user/docs_raw/api/v1/auth.md.gz`, it must appear inside the archive as `api/v1/auth.md`.

Requirements for your Go program:
- Use standard Go libraries (`archive/tar`, `compress/gzip`, `path/filepath`, `strings`, `os`, `io`, etc.).
- Ensure the tar headers contain the correct file names, sizes, and standard file modes (e.g., 0644).
- Create the final archive `/home/user/published_docs.tar.gz`.

Once you have written the Go program, run it to generate the final archive.