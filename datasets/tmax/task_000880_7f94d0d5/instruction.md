I am a researcher organizing a massive dataset of binary logs. I am using a custom C++ application that reads gzip-compressed Write-Ahead Logs (WAL) and serves them over an HTTP API. 

The source code for this application is vendored at `/app/wal-serve-v1.0`. However, I am running into a couple of issues preventing me from analyzing my data:

1. The build system is broken. When I try to run `make` in `/app/wal-serve-v1.0`, it fails to link the necessary compression library.
2. The application has a hardcoded path. In `server.cpp`, it is trying to read data from `/var/old_data`, but my compressed dataset is actually located at `/home/user/dataset/`.

Your task is to:
1. Fix the `Makefile` in `/app/wal-serve-v1.0` so that the program compiles successfully.
2. Modify `server.cpp` to correctly point to the `/home/user/dataset/` directory.
3. Compile the server.
4. Run the compiled server on port `9090`. The server binary accepts the port as its first argument (e.g., `./wal_server 9090`). Leave the server running in the background so it can serve requests.

Ensure the server is running on `127.0.0.1:9090` and correctly serving the parsed dataset records. Automated tests will verify your work by making HTTP GET requests to `http://127.0.0.1:9090/records`.