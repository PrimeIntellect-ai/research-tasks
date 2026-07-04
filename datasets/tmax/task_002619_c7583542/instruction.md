You are acting as a security researcher investigating a suspicious, partially corrupted C++ server left behind by a threat actor.

We have recovered the server's source code at `/app/src/server.cpp` and a custom write-ahead log (WAL) file at `/app/db.wal`. However, the server has a few issues:

1. **Deadlock**: The server frequently deadlocks under high contention when handling concurrent requests. You need to analyze `/app/src/server.cpp`, identify the race condition/deadlock (likely a lock inversion), and fix the source code.
2. **Corrupted WAL**: The `/app/db.wal` file contains a corrupted entry that causes the server to crash when loading it on startup. You must find and remove the single corrupted line. You may want to use a delta debugging approach to isolate the line that triggers the crash.
3. **Authentication**: The threat actor left behind a screenshot of their terminal containing the admin token at `/app/token.png`. You need to extract this token (e.g., using `tesseract`). 

Your final goal is to:
1. Fix the C++ code to prevent deadlocks.
2. Clean the `/app/db.wal` file so the server starts successfully.
3. Compile the server using `g++ -O2 -pthread /app/src/server.cpp -o /app/server`.
4. Start the server so it listens on `127.0.0.1:8080`.

Leave the server running in the background. An automated verification script will send concurrent HTTP requests to `127.0.0.1:8080/query` and `127.0.0.1:8080/update`, passing the token you extracted from the image in the `Authorization: Bearer <TOKEN>` header. If the server deadlocks or rejects the token, the verification will fail.