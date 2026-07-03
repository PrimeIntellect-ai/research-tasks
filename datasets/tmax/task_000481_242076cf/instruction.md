You are an artifact manager responsible for curating binary repositories. We have a local multi-service stack running on this machine under `/app/`:
1. An upstream Python HTTP artifact server running on port `8081`.
2. An Nginx reverse proxy that is supposed to run on port `8080`, acting as the main gateway.

Currently, the Nginx configuration at `/home/user/nginx.conf` is broken and not routing traffic to the Python server. 

Your tasks are as follows:
1. Fix the Nginx configuration so that requests to `http://localhost:8080/artifacts/` proxy correctly to `http://localhost:8081/`.
2. Start Nginx using your fixed configuration.
3. Download the artifact bundle from `http://localhost:8080/artifacts/bundle.zip`.
4. The downloaded bundle is a nested archive containing a `.tar.gz` file, which in turn contains a directory of ELF binaries and a custom Write-Ahead Log (`journal.wal`) encoded in UTF-16LE.
5. Extract the archive.
6. Write a highly efficient C++ program at `/home/user/curator.cpp` that parses `journal.wal`. The WAL file contains raw binary records where each record starts with a 4-byte little-endian integer (record length), followed by a UTF-16LE encoded file path. 
7. Your C++ program must:
   - Read the WAL file.
   - Convert the UTF-16LE file paths to standard UTF-8.
   - Filter out paths that do not point to a valid ELF binary in the extracted directory (verify by checking the first 4 bytes for the ELF magic number `\x7F ELF`).
   - Print the valid, UTF-8 paths to standard output, one per line.
8. Compile your C++ program to `/home/user/curator`.

Efficiency is critical. Your C++ program will be evaluated against a very large benchmark WAL file by an automated metric. It must achieve a processing throughput that meets our threshold.