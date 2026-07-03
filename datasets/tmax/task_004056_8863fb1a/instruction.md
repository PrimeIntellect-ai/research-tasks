You are acting as a technical writer tasked with organizing and serving a complex repository of system documentation. 

Your task consists of three main phases:

**Phase 1: Archive Extraction and Integrity**
You will find a nested archive at `/home/user/docs_backup.tar.gz`. This archive contains several split zip files and a compressed GCode log. 
1. Extract the nested archives. 
2. Verify the integrity of the extracted files (one of the split zip parts is slightly corrupted and needs manual repair using standard stream editors to remove a trailing garbage string "BADEOF" appended to it before unzipping).
3. Combine and extract the final text files into `/home/user/raw_docs/`.

**Phase 2: Proprietary WAL Parsing**
Some critical documentation is stored in a proprietary Write-Ahead Log (WAL) format located at `/home/user/raw_docs/syslog.wal`. 
We do not have the source code for the parser, but there is a stripped, legacy binary utility provided at `/app/bin/wal_parser`. 
1. Use standard Linux reverse-engineering or black-box testing tools to figure out how to pass the `syslog.wal` file into this binary to extract the hidden Markdown documentation blocks.
2. The binary outputs heavily obfuscated text. You must figure out the transformation it applies (it is a simple symmetric cipher) and write a Go script at `/home/user/decoder.go` to process the binary's output into plain text Markdown.
3. Use Bash text-processing macros to append a standard documentation header to all extracted Markdown files in `/home/user/processed_docs/`.

**Phase 3: Multi-Protocol Serving**
Write a Go server in `/home/user/doc_server/` that serves the files from `/home/user/processed_docs/`.
1. The server must expose an HTTP REST endpoint on port 8080: `GET /api/v1/docs/{filename}`
2. The server must also expose a gRPC service on port 9090 with a method `GetDocument(DocumentRequest) returns (DocumentResponse)`.
3. Both endpoints must enforce an authorization header/metadata check requiring the token: `Bearer TECH-WRITE-2024`.

Leave your server running in the background when you are finished.