You are an AI assistant helping a technical writer recover and organize legacy documentation. The documentation is stored in a custom binary archive format, and we need a C++ tool to extract specific, fully released versions based on a configuration file.

Your task is to write a C++ program, compile it, and run it to perform the extraction.

**Background & Files:**
You have two input files in `/home/user/`:
1.  `extraction.conf`: A text-based configuration file.
2.  `archive.pak`: A custom binary archive containing multi-line logs and compressed documentation files.

**Task Requirements:**

1.  **Read the Configuration File** (`/home/user/extraction.conf`)
    It contains key-value pairs separated by a colon and a space (e.g., `Key: Value`).
    You need to extract:
    *   `Extract-Prefix`: The directory where extracted documents must be saved (you must create this directory if it doesn't exist).
    *   `Target-Categories`: A comma-separated list of document categories we care about.

2.  **Parse the Binary Archive** (`/home/user/archive.pak`)
    The archive has a 5-byte magic header: `ARCv1`.
    Following the header is a sequence of records. Each record has the following binary layout:
    *   **Record Type**: 1 byte character (`L` for Log, `C` for Compressed Document).
    *   **Category Length**: 1 byte unsigned integer (uint8_t).
    *   **Category String**: Ascii string of length specified by Category Length.
    *   **Document ID**: 4 byte unsigned integer (uint32_t, little-endian).
    *   **Payload Size**: 4 byte unsigned integer (uint32_t, little-endian).
    *   **Payload**: Binary data of length specified by Payload Size.

3.  **Process Logs and Compressed Streams**
    *   **If Record Type is `L` (Log)**: The payload is plain text containing multi-line log records about document versions. Each record looks like this:
        ```
        BEGIN_LOG
        DocID: <integer>
        Version: <integer>
        Status: <DRAFT or RELEASED>
        END_LOG
        ```
        You must parse these to find the *highest* version number for each Document ID that has the status `RELEASED`.
    *   **If Record Type is `C` (Compressed Document)**: The payload is zlib-compressed text (deflate).

4.  **Extraction Logic**
    You must extract and decompress documents from `archive.pak` ONLY IF:
    *   The document's Category string matches one of the `Target-Categories` specified in the config.
    *   The document has at least one `RELEASED` version logged in an `L` record (which may appear before or after the `C` record in the file).
    
    *Note: There is only one `C` record per Document ID in the archive. The logs (`L` records) dictate what version number it represents.*

5.  **Output Requirements**
    *   Save decompressed documents to `<Extract-Prefix>/<Category>_<DocID>_v<HighestReleasedVersion>.txt`.
    *   Generate a summary log file at `/home/user/summary.txt`. For every successfully extracted document, append a line exactly matching: `Extracted DocID <DocID> of Category <Category> at Version <Version>`. Order the lines by DocID in ascending order.

**Technical Constraints:**
*   You must write the solution in C++ (`/home/user/extract_docs.cpp`).
*   You may use standard Linux libraries (e.g., `zlib`). If you need to install libraries like `zlib1g-dev`, you may use `sudo apt-get install -y zlib1g-dev` (passwordless sudo is configured).
*   Compile your code to `/home/user/extract_docs` and execute it.