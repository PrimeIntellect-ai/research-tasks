You are tasked with implementing the core engine for a novel configuration management tracker in Go. This tool tracks changes to system configuration files and streams them into a custom append-only archive format. 

You must write a Go program at `/home/user/archiver.go` and compile it to `/home/user/archiver`.

**Step 1: Retrieve the Protocol Specification**
There is an audio recording left by the lead architect at `/app/archiver_spec.wav`. You must transcribe this audio file (you may install and use Python packages like `SpeechRecognition`, `pydub`, or `whisper` to do this, or any other method available in the container). The audio reveals the secret Magic Bytes that must start the archive, as well as the exact padding requirements for the binary headers.

**Step 2: Implement the Archiver**
Write the Go program `/home/user/archiver.go` with the following requirements:
1. **Invocation**: The program will be invoked as `./archiver <lock_file_path>`.
2. **File Locking**: Before reading any input, the program must acquire an exclusive POSIX lock (using `syscall.Flock`) on the file specified by `<lock_file_path>`. If the lock cannot be acquired immediately, it should block until it can. The file should be created if it doesn't exist.
3. **I/O**: Read a stream of configuration change events from `stdin` and write the compiled binary archive to `stdout`. Use buffered I/O for efficiency.
4. **Input Format** (Plaintext commands):
   - `WRITE <path> <size>\n<data>` (where `<data>` is exactly `<size>` bytes of raw data, followed immediately by the next command, no implicit newlines).
   - `HLINK <target_path> <link_path>\n` (simulates creating a hard link to save space in the archive).
5. **Output Format** (Binary):
   - The file must start with the Magic Bytes specified in the audio recording.
   - For a `WRITE` command: 
     - 1-byte ASCII 'W'
     - The `<path>` string, exactly encoded as specified in the audio (including length limitations and padding).
     - 8-byte little-endian unsigned integer representing the `<size>`.
     - The raw `<data>` bytes.
   - For an `HLINK` command:
     - 1-byte ASCII 'H'
     - The `<link_path>` string (encoded with the same padding rules as `WRITE` paths).
     - The `<target_path>` string (encoded with the same padding rules).
6. **Graceful Exit**: When `stdin` reaches EOF, flush the stdout buffer, release the file lock, and exit with status code 0.

Ensure your compiled binary behaves exactly as expected, as it will be rigorously tested against thousands of random command sequences by an automated fuzzing suite.