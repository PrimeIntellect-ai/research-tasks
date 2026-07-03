You are an AI assistant helping a technical writer organize and serve a large corpus of documentation. The writer has provided a raw archive of text files and an index mapping document IDs to their file paths. Your task is to set up a local web server to serve these documents using a provided, partially complete C++ server application.

Here is the setup information:
1. **Raw Data:** 
   - An archive is located at `/home/user/data/raw_docs.tar.gz`. 
   - An index file is located at `/home/user/data/index.csv`. It has no header, and each line is formatted as `doc_id,relative_path`.

2. **Provided Server Package:**
   - A vendored C++ server package `docserve` (version 1.0) is located at `/app/docserve-1.0`. 
   - It contains a `Makefile`, a `server.cpp` source file, and a header-only HTTP library `httplib.h`.
   - The package is supposed to compile a binary named `server`. However, the provided `Makefile` is slightly broken and fails to compile the application out-of-the-box. You will need to debug and fix the compilation issue.

Your concrete tasks are:
1. **Prepare the Filesystem:**
   - Extract the contents of `/home/user/data/raw_docs.tar.gz` into the directory `/home/user/data/extracted/`.
   - Create a directory at `/home/user/www/docs/`.

2. **Fix and Complete the C++ Server:**
   - Fix the `Makefile` in `/app/docserve-1.0` so that `make` successfully builds the `server` binary.
   - Edit `/app/docserve-1.0/server.cpp` and implement the empty `setup_docs(const std::string& csv_path)` function.
   - Your implementation in `setup_docs` must read and parse the CSV file at `/home/user/data/index.csv` using standard C++ streaming (e.g., `std::ifstream`) or memory-mapped I/O.
   - For every row in the CSV (`doc_id,relative_path`), the function must programmatically create a **symbolic link** at `/home/user/www/docs/<doc_id>.txt` that points to the absolute path of the corresponding extracted file (`/home/user/data/extracted/<relative_path>`). Use the appropriate POSIX C++ headers (e.g., `<unistd.h>`) to create the symlink.

3. **Run the Server:**
   - Once compiled successfully, execute the server binary in the background from within `/app/docserve-1.0`. 
   - The server is hardcoded to listen on `127.0.0.1:8080` and serve static files from `/home/user/www`.
   - Ensure the server is running and remains active so that an automated verifier can query the documentation over HTTP.

Note: The automated test will verify your success by issuing HTTP GET requests directly to the web server to fetch specific documents via their symlinked `doc_id` paths (e.g., `http://127.0.0.1:8080/docs/101.txt`). Make sure the symlinks resolve correctly.