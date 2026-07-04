You are a web developer building a high-performance data processing service in Go. We are using a vendored C library for run-length encoding (RLE) to process incoming payloads fast. However, we are running into several issues that prevent our CI pipeline from passing. 

Here is what you need to do:

1. **Fix the Vendored C Library:**
   There is a vendored C package located at `/app/rle-c-1.0.0`. 
   - Its `Makefile` is broken (it fails to produce a static library `librle.a` due to missing flags and commands). Fix it so that running `make` outputs `librle.a`.
   - The C code has a memory safety / undefined behavior issue. When encoding certain strings (e.g., long sequences of the same character), it writes out of bounds or crashes. Debug and fix the memory safety issue in `rle.c`.

2. **Property-Based Testing:**
   In `/home/user/service/`, create a Go package that wraps this C library using `cgo`. Write a property-based test in `rle_test.go` using the `testing/quick` package to verify that your wrapper doesn't crash on random string inputs. You must ensure `go test` passes reliably.

3. **Schema Migration & Service Implementation:**
   Implement the main Go service in `/home/user/service/main.go`. 
   - On startup, it must connect to a SQLite database at `/home/user/service/data.db` and apply a schema migration to create a table: `CREATE TABLE IF NOT EXISTS processed_data (id INTEGER PRIMARY KEY AUTOINCREMENT, original TEXT, encoded TEXT);`
   - It must start an HTTP server listening on `127.0.0.1:8080`.
     - `POST /encode`: Accepts a JSON body `{"text": "..."}`. It should encode the text using the C library, save the original and encoded text to the SQLite database, and return JSON `{"encoded": "..."}`.
   - It must simultaneously run a raw TCP server listening on `127.0.0.1:9090`. Whenever a client connects and sends a raw string (terminated by `\n`), the server should encode it, insert it into the database, and send back the encoded string followed by `\n`.

Start the Go service in the background once you are done, so it is actively listening on both ports.

Ensure the C code is fixed correctly so the service doesn't crash under load or edge-case inputs!