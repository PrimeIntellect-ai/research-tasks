You are acting as a backup administrator setting up a specialized real-time archiving daemon. 

We have a directory at `/home/user/live_data` that contains several files, directories, and some problematic symlinks that have previously caused our backup scripts to get stuck in infinite loops. 

Your task is to write and run a C program that acts as a TCP backup daemon listening on `127.0.0.1:9090`. 

However, the specific authentication token and the required network chunk size for this daemon were left by the previous admin in an audio memo located at `/app/directive.wav`. 

Here is what you need to do:
1. **Extract Metadata**: Transcribe the audio file at `/app/directive.wav` to find out the secret authentication token and the transmission chunk size (in bytes).
2. **Write the Daemon**: Create a C program, compile it to `/home/user/backup_daemon`, and run it. The daemon must:
   - Listen for raw TCP connections on `127.0.0.1:9090`.
   - Accept a newline-terminated authentication string from the client: `AUTH: <secret_token>\n`. If the token is incorrect, close the connection immediately.
   - If authenticated, wait for the command `BACKUP\n`.
   - Upon receiving `BACKUP\n`, traverse `/home/user/live_data`.
   - **Crucial**: You must avoid infinite symlink loops during traversal. Only process regular files and valid, non-looping symlinks (by resolving them to their target regular files). Do not archive directories themselves, only their file contents.
3. **Format and Transmission**: 
   - Before streaming, acquire an exclusive file lock (e.g., using `flock` or `fcntl`) on `/tmp/backup.lock`.
   - Stream the archived files back to the client over the TCP socket using the following custom binary format per file:
     - 2 bytes (unsigned short, little-endian): Length of the relative file path.
     - N bytes: The relative file path (e.g., `subdir/file.txt`).
     - 4 bytes (unsigned int, little-endian): Size of the file data in bytes.
     - M bytes: The actual file data.
   - The stream transmission over the socket MUST be chunked according to the chunk size specified in the audio file.
   - Once all files are sent, send a final 2-byte sequence `0x00 0x00` to indicate the end of the stream, release the file lock, and close the client connection.
   - The daemon should remain running and accept subsequent connections.

Please execute the necessary steps to transcribe the audio, write the C code, compile, and leave the daemon running in the background. Note: You may install tools like `whisper.cpp`, `ffmpeg`, or `python3` to transcribe the audio.