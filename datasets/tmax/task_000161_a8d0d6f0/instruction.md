You are acting as an automation assistant for a technical writer who is managing a massive, disorganized archive of legacy documentation.

We have a large archive of documentation at `/home/user/raw_docs.tar.gz`. The archive contains a deeply nested directory structure with thousands of `.txt` files. Some of these files are extremely large because they contain massive embedded base64 logs, but the crucial metadata is always located within the first 500 bytes.

Additionally, our company uses a proprietary, legacy documentation hashing algorithm. We lost the source code, but we recovered the compiled executable, which is located at `/app/doc_hasher`. 

Your goal is to organize this archive and expose it via a dual-protocol microservice.

**Step 1: Extract and Traverse**
Extract `/home/user/raw_docs.tar.gz` into `/home/user/extracted`. Recursively traverse the directory to find all `.txt` files.

**Step 2: Parse Metadata using Memory-Mapped I/O**
Because some files are gigabytes in size, do not read entire files into memory. Use Python's `mmap` module or direct streaming I/O to read only the first 500 bytes of each `.txt` file. Look for a line starting exactly with `Doc-Title: ` and extract the title. 

**Step 3: Hash and Bulk Rename**
For each `.txt` file, run the proprietary binary `/app/doc_hasher <filepath>`. It will print a 16-character hexadecimal string to standard output. 
Create a new directory at `/home/user/organized_docs`.
Move and rename every found `.txt` file into this new flat directory using the format:
`<hash>_<title>.txt`
*(Note: Replace any spaces in the extracted title with underscores `_`. For example, if the hash is `a1b2c3d4e5f60718` and the title is `System Overview`, the new filename must be `a1b2c3d4e5f60718_System_Overview.txt`)*

**Step 4: Dual-Protocol Documentation Service**
Write and run a Python script at `/home/user/serve_docs.py` that simultaneously exposes two network services:
1. **HTTP Service**: An HTTP server listening on `0.0.0.0:8080`. It must serve the static files located in `/home/user/organized_docs`. A `GET /<filename>` request should return the file's contents.
2. **TCP Metadata Service**: A raw TCP server listening on `0.0.0.0:9090`. When a client connects and sends a 16-character hash followed by a newline (`\n`), the server must respond with the exact full filename (e.g., `a1b2c3d4e5f60718_System_Overview.txt`) followed by a newline, and then close the connection.

Leave your `serve_docs.py` running in the background or in a tmux session so the verification tests can query it.