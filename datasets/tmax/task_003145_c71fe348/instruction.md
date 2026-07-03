You are an AI assistant helping a technical writer organize a set of legacy documentation.

The writer has received a custom archive file located at `/home/user/doc_bundle.bin`. This file is a concatenated binary format that contains:
1. A 128-byte binary header.
2. A Gzipped tarball (`.tar.gz`) containing the documentation files, starting exactly at byte offset 128.
3. A multi-line build log appended immediately after the end of the gzip stream.

Your task is to process this file with the following requirements:

1. **Safe Extraction**: Extract the `.tar.gz` stream from the binary file. The archive contains paths that attempt directory traversal (e.g., `../styles/main.css`). You must extract all files into `/home/user/docs_safe/`, neutralizing any path traversals so that no files are written outside of `/home/user/docs_safe/`. For example, `../styles/main.css` should be extracted to `/home/user/docs_safe/styles/main.css`.
2. **Encoding Conversion**: The extracted files inside the tarball are in various text encodings (some are UTF-16LE, some are ISO-8859-1). Convert all extracted files in `/home/user/docs_safe/` to UTF-8 in place.
3. **Multi-line Log Parsing**: The build log at the end of the `.bin` file (after the gzip stream) is encoded in ISO-8859-1. A log record starts with a tag like `[INFO]`, `[WARNING]`, or `[ERROR]` and may span multiple lines until the next tag. 
    - Extract the log from the binary file.
    - Convert it to UTF-8.
    - Parse out *only* the multi-line records that start with `[WARNING]`. 
    - Save these warning records (including their subsequent continuation lines) to `/home/user/warnings.log` in UTF-8.

Ensure all outputs are exactly where specified. You may use any scripting language or command-line tools available.