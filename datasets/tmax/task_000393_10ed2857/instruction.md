You are acting as a technical assistant for a technical writer who is organizing a large archive of dictated audio notes. The writer needs an automated way to index the audio formats while ensuring safe concurrent access (since an automated background backup service periodically reads these files).

Your task has two parts:

**Part 1: Transcribe the Dictation**
There is a dictation audio file located at `/app/dictation.wav`. Recover the spoken English content from this file using any available audio processing or transcription tools in your environment (e.g., Python libraries, ffmpeg, etc.). 
Save the transcribed text into a file at `/home/user/transcript.txt`.

**Part 2: Build a Safe Audio Indexer in C**
The writer needs a tool to safely extract metadata from the binary headers of these WAV files. 
Write a C program at `/home/user/indexer.c` and compile it to `/home/user/indexer`.

Requirements for `/home/user/indexer`:
1. It must accept exactly one argument: the path to a WAV file (e.g., `./indexer /app/dictation.wav`).
2. Before reading, it must acquire a shared POSIX read lock on the file using `fcntl` (`F_RDLCK`) to prevent backup processes from modifying it while being read. If the file cannot be opened or locked, exit with code 1.
3. Parse the standard 44-byte RIFF WAV binary header.
4. Extract the RIFF chunk size, the number of channels, and the sample rate.
5. Print the extracted metadata to `stdout` in this exact format (followed by a newline):
   `SIZE: <TotalFileSize> | CH: <Channels> | SR: <SampleRate>`
   *(Note: TotalFileSize is the RIFF Chunk Size + 8 bytes)*
6. Unlock and close the file before exiting cleanly with code 0.

Ensure your C code properly handles the binary format extraction according to the standard WAV specification.