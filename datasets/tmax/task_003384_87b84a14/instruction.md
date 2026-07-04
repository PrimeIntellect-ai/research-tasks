**Ticket ID:** #INC-8482
**Reporter:** Dev Team
**Subject:** `logchunker` tool fails to compile and crashes on our log files

**Description:**
Hi IT Support,

One of our junior developers tried to update our internal `logchunker` utility located in `/home/user/logchunker/`. They pushed a broken version and left for the day. 

Right now, the Go code doesn't even compile. Even if you fix the compiler error, we know there is an algorithmic bug in the `ChunkData` function: it panics with a "slice bounds out of range" error when the input data length isn't perfectly divisible by the chunk size. The tool is trying to process `/home/user/server_logs.txt`.

Please fix this for us:
1. Fix the compiler/build error in `/home/user/logchunker/main.go`.
2. Debug the `ChunkData` function and fix the off-by-one algorithmic bug that causes the slice bounds panic.
3. Create a minimal reproducible regression test in `/home/user/logchunker/main_test.go`. The test must include a test function named `TestChunkData` that calls `ChunkData([]string{"A", "B", "C", "D"}, 3)` and asserts the output is correctly chunked without panicking.
4. Once fixed and tested, compile the binary to exactly: `/home/user/logchunker/chunker`.

I need the binary built and the `go test` passing so we can resume our pipeline. Thanks!