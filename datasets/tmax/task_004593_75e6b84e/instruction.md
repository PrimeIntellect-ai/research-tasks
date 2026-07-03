As a technical writer, I recently inherited a legacy documentation system. I have a large, proprietary documentation archive file located at `/home/user/legacy_docs.dcar`, and a legacy indexing tool located at `/app/doc_indexer`. I need you to extract the contents, index them, and serve them via a secure API for our new frontend to consume.

Here are the specific requirements:

**1. Extract the Archive**
The file `/home/user/legacy_docs.dcar` uses a custom binary format. You need to write a Python script to parse and extract it.
The format structure is:
*   **Header**: The first 4 bytes are the ASCII string `DCAR`.
*   **Entries**: Following the header are multiple file entries concatenated together. Each entry consists of:
    *   `File ID`: 2 bytes, Unsigned Short (Big Endian).
    *   `File Size`: 4 bytes, Unsigned Int (Big Endian).
    *   `File Path`: 128 bytes, Null-padded ASCII string. Represents the relative path (e.g., `chapter1/intro.txt`).
    *   `File Data`: The raw bytes of the file, exactly `File Size` bytes long.
Extract all files into the directory `/home/user/extracted_docs/`. You must recreate the directory structure specified in the `File Path` (e.g., create `/home/user/extracted_docs/chapter1/intro.txt`).

**2. Index the Files**
We have a legacy, compiled CLI tool at `/app/doc_indexer` (it is a stripped binary). It analyzes documentation files and generates a proprietary signature and type.
For every extracted file, run: `/app/doc_indexer <absolute_path_to_extracted_file>`.
The tool will output a string to standard output in the format: `<legacy_hash>:<doc_type>` (e.g., `b2f4c...:text`).

**3. Generate a Manifest**
Create a JSON manifest file at `/home/user/manifest.json`. It should be a dictionary where the keys are the `File ID`s (as strings, e.g., `"1"`, `"2"`), and the values are objects containing:
*   `path`: The file's relative path as stored in the archive (e.g., `"chapter1/intro.txt"`).
*   `md5`: The standard MD5 hex checksum of the extracted file.
*   `legacy_hash`: The hash produced by `/app/doc_indexer`.
*   `doc_type`: The document type produced by `/app/doc_indexer`.

**4. Serve the Documentation**
Write and start a Python HTTP server (using `Flask`, `FastAPI`, or standard `http.server`) listening on `127.0.0.1:8080`.
The server must implement the following REST API:
*   **Authentication**: All endpoints must require an `Authorization` header with the exact value: `Bearer secret-doc-token`. If missing or invalid, return a `401 Unauthorized` status.
*   **`GET /manifest`**: Returns the contents of `/home/user/manifest.json` with a `200 OK` status and `application/json` content type.
*   **`GET /doc/<file_id>`**: Returns the raw binary contents of the extracted file corresponding to the requested `<file_id>`. Set the `Content-Type` to `application/octet-stream`. If the ID doesn't exist, return `404 Not Found`.

Leave the HTTP server running in the background so it can be queried.