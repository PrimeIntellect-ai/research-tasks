I am a technical writer organizing the documentation for our project's new developer portal. The portal consists of Markdown files, API references extracted directly from our backend binaries, and transaction histories from our custom Write-Ahead Log (WAL).

I need you to perform a series of cleanup and generation tasks to get the documentation ready for publishing.

Here is what you need to do:

1. **Text Transformation**: We recently changed our terminology. Recursively find all `.md` files in `/home/user/docs/` and use standard CLI tools (like `sed`) to replace every occurrence of the exact word `DEPRECATED` with `OBSOLETE`.

2. **Go Automation Script**: Write a Go program at `/home/user/build_nav.go` that performs the following tasks:
   
   a) **Domain-Specific Format Parsing (ELF)**: 
   The program must read the ELF binary located at `/home/user/bin/backend_srv`. Use Go's standard `debug/elf` package to extract all exported dynamic symbols (functions/variables). Filter this list to include ONLY symbols that begin with the exact prefix `Api` (e.g., `ApiGetUser`). Write these symbol names, one per line, sorted alphabetically, into a new file at `/home/user/docs/api_reference.md`.

   b) **Multi-line Log Record Parsing**:
   Our system writes a custom text-based WAL to `/home/user/logs/system.wal`. The format consists of multi-line records like this:
   ```
   BEGIN TX
   TX_ID: 9482
   AUTHOR: jsmith
   AFFECTED_DOC: setup.md
   END TX
   ```
   Your Go program must use streaming/buffered I/O (e.g., `bufio.Scanner`) to parse this file. Extract the mapping between `AFFECTED_DOC` and `TX_ID`. If a document is affected by multiple transactions, record only the *most recent* (the last one appearing in the file). 
   
   c) **Directory Traversal and Output Generation**:
   Traverse the `/home/user/docs/` directory recursively. For every `.md` file found (ignoring `api_reference.md`), print a navigation index entry to `/home/user/docs/nav_index.txt`. Each line in `nav_index.txt` must be formatted exactly as:
   `[Filename] - LastTX: [TX_ID]`
   (e.g., `setup.md - LastTX: 9482`). If a file has no transactions in the WAL, use `LastTX: NONE`. Sort the lines alphabetically by filename.

3. **Execution**: Build and run your Go program to generate `api_reference.md` and `nav_index.txt`. 

Please execute all of these steps. I will verify the contents of `/home/user/docs/`, `/home/user/docs/api_reference.md`, and `/home/user/docs/nav_index.txt` when you are finished.