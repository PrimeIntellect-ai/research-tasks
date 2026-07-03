You are assisting a developer in organizing and processing legacy project files. The developer has left an audio memo containing specific parameters for a custom log transformation utility that needs to be written.

Your tasks are:

1. **Listen to / transcribe the audio memo** located at `/app/project_memo.wav`. 
   The memo contains three critical configuration parameters dictated by the lead developer:
   - A `MAGIC_OFFSET` (number of bytes)
   - A `BLOCK_SIZE` (number of bytes)
   - An `XOR_KEY` (a hexadecimal value)

2. **Develop a C program** at `/home/user/transformer.c` and compile it to an executable named `/home/user/transformer`.
   The program must perform the following streaming format conversion:
   - Read binary data from `stdin` until EOF.
   - Discard the first `MAGIC_OFFSET` bytes of the input stream entirely.
   - For all remaining data, read it in chunks of `BLOCK_SIZE` bytes.
   - Apply a byte-wise XOR operation using the `XOR_KEY` to every byte in these chunks. If the final chunk is smaller than `BLOCK_SIZE`, apply the XOR operation to the remaining bytes normally.
   - Write the transformed binary data to `stdout`.

Constraints:
- The program must handle streaming input efficiently (e.g., using `fread`/`fwrite` or memory-mapped I/O where appropriate, though stdin is typically a stream).
- The program must not crash if the input is smaller than `MAGIC_OFFSET` (it should output nothing).
- You can use standard command-line tools like `whisper`, `ffmpeg`, or Python scripts to transcribe or listen to the audio file to obtain the parameters.