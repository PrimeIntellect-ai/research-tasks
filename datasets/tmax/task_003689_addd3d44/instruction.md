You are tasked with building a core component of our new Artifact Manager, which curates binary repositories and prevents data corruption during log rotation races. 

Our system needs a Rust-based tool that takes incoming binary streams, chunks them into multi-part archive segments, calculates integrity checksums, and ensures exclusive access using file locks. 

First, analyze the provided video artifact located at `/app/rotation_capture.mp4`. This video is a screen capture of our old system's logging dashboard. Somewhere in the video (around the 2 to 3-second mark), a terminal window flashes a critical configuration string in the format `PARAMS: CHUNK=<size>, ALGO=<algo>`. You must extract this frame, read the configuration, and hardcode these exact parameters into your Rust application.

**Application Requirements:**
1. Create a Rust binary project in `/home/user/archiver`.
2. The executable must read binary data from standard input (`stdin`) until EOF.
3. Before processing, the application MUST acquire an exclusive filesystem lock (`flock`) on `/tmp/artifact.lock`. This simulates protecting the archiving process against our log rotation script.
4. Process the input stream by dividing it into chunks of exactly `<size>` bytes (as found in the video), except for the final chunk which may be smaller.
5. For each chunk, calculate the checksum using the `<algo>` algorithm found in the video.
6. Write the resulting custom multi-part archive format to standard output (`stdout`) exactly as follows:
   - **Header**: The ASCII string `ARTM` (4 bytes).
   - **Segments** (for each chunk, in order):
     - Segment Index: 2 bytes, Unsigned 16-bit integer, Little-Endian (starts at 0).
     - Data Length: 2 bytes, Unsigned 16-bit integer, Little-Endian.
     - Checksum: 4 bytes, Unsigned 32-bit integer, Little-Endian (using the algorithm from the video).
     - Data: The actual bytes of the chunk.
   - **Footer**: The ASCII string `ENDM` (4 bytes), followed immediately by the Total Bytes processed across all chunks (4 bytes, Unsigned 32-bit integer, Little-Endian).
7. Release the lock on `/tmp/artifact.lock` and exit gracefully.

**Constraints:**
- You may use external crates like `adler` or `crc32fast` (depending on what the video requires) and `fs4` or `fd-lock` for file locking.
- Build the project using `cargo build --release`. 
- The final executable must be located at `/home/user/archiver/target/release/archiver`.
- Your executable will be rigorously fuzzed against a reference implementation to ensure bit-exact equivalence on `stdout` given random `stdin` binary inputs.