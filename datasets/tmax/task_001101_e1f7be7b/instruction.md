You are an artifact manager responsible for curating continuous binary streams from build servers. You need to write a C program that compresses and archives this live stream efficiently, handling log rotations seamlessly without dropping data.

Your task is to write a C program located at `/home/user/archiver.c` and compile it to `/home/user/archiver`.

The `archiver` program must fulfill the following requirements:
1. **Input Stream:** Continuously read binary data from a named pipe (FIFO) at `/home/user/stream.fifo`. (You should create this FIFO in your program or assume it exists, but create it to be safe).
2. **Custom Compression (RLE):** Compress the incoming binary data using a strict Run-Length Encoding (RLE) format. 
   - For every contiguous run of identical bytes, output a 1-byte count (from 1 to 255) followed by the 1-byte value. 
   - Example: 3 bytes of `0xAA` becomes `0x03 0xAA`. 
   - If a run exceeds 255 bytes, you must start a new RLE pair. (e.g., 260 bytes of `0xBB` becomes `0xFF 0xBB` followed by `0x05 0xBB`).
3. **Output:** Append the compressed data to an archive file named `/home/user/repo.dat`.
4. **Live Rotation (Incremental Snapshots):** The archiver must handle `SIGUSR1` to rotate the archive. 
   - When `SIGUSR1` is received, the program must immediately:
     a. Flush any pending RLE buffers.
     b. Append a special EOF marker: `0x00 0x00` to the current `repo.dat`.
     c. Close the current `repo.dat` file.
     d. Rename the closed file to `/home/user/repo.N.dat` (where N is a strictly incrementing integer starting from 1).
     e. Open a fresh `/home/user/repo.dat` to continue writing the stream.
5. **Graceful Shutdown:** On receiving `SIGTERM`, flush pending data, write the `0x00 0x00` EOF marker, close the file, and exit cleanly (do not rename on SIGTERM).

**Important Constraints:**
- The incoming stream may be slow, pause, or burst. The archiver must not block indefinitely if a run is incomplete; it should write out the current run if it has been waiting for more data, but for this task, you can buffer safely as long as `SIGUSR1` and `SIGTERM` handlers correctly flush the state.
- Compile your program using: `gcc -O2 /home/user/archiver.c -o /home/user/archiver`
- Keep the program running in the background when testing so that the evaluation scripts can interact with it.

Once you have written and compiled the program, ensure it runs correctly and can handle data written to `/home/user/stream.fifo` and handles `SIGUSR1` and `SIGTERM` as specified. Write your own test script to verify, but leave the executable `/home/user/archiver` ready for testing.