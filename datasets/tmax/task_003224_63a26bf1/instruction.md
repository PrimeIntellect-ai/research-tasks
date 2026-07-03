You are a DevOps engineer debugging a critical Rust-based logging service that recently crashed and corrupted its Write-Ahead Log (WAL).

There are three main objectives to resolve this incident:

1. **Extract the Encryption Key from the Video Fixture**:
   The hardware watchdog captured a diagnostic video during the crash, located at `/app/error_signal.mp4`. The video is exactly 16 frames long (encoded at 1 fps). The top-left 50x50 pixel region of each frame flashes either pure white (representing binary `1`) or pure black (representing binary `0`).
   Decode this sequence (Frame 0 is the Most Significant Bit, Frame 15 is the Least Significant Bit) to recover a 16-bit integer. This is the `magic_seed` needed to decrypt the WAL entries.

2. **Recover the Database (WAL)**:
   The Rust service source code is located at `/home/user/logd`. The corrupted database file is at `/home/user/data/store.wal`. 
   The service currently panics when trying to read the WAL due to a partially written record (dropped future/cancellation issue). 
   Modify `/home/user/logd/src/wal.rs` to:
   - Gracefully skip any WAL entries where the payload length does not match the header, or where the simple XOR checksum fails.
   - Use the `magic_seed` you extracted from the video to XOR the raw bytes of the valid payloads to recover the plaintext data.

3. **Fix the Service and Serve the Data**:
   The HTTP server in `/home/user/logd/src/main.rs` has a bug where it leaks Tokio tasks on client disconnects, eventually leading to OOM or file descriptor exhaustion. Fix this connection handling leak.
   Finally, compile and run the fixed Rust service so it listens on `127.0.0.1:8888`. It must successfully load the recovered WAL and serve HTTP `GET` requests at the endpoint `/record/<id>` (where `<id>` is a u32), returning the recovered plaintext string for that ID with a `200 OK` status, or `404 Not Found` if the ID doesn't exist.

Leave the service running in the background when you are finished.