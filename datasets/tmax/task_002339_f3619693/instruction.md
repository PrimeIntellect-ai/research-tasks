You are a performance engineer tasked with debugging a misbehaving audio processing pipeline. The core of the pipeline is a compiled binary located at `/app/bin/audio_processor` which processes WAV files. 

Recently, the system has experienced severe performance degradation, with the processor hanging and consuming 100% CPU on certain malformed or "evil" audio files. We have captured one such file and placed it at `/app/reference.wav`.

During execution, `audio_processor` creates a temporary SQLite database to index audio metadata (chunks and headers). To save space and ensure cleanup, it unlinks (deletes) this database file from the filesystem immediately after opening it, but keeps the file descriptor open while processing. When it encounters an "evil" file, it gets stuck in an infinite loop parsing a specific malformed chunk, leaving the process hanging.

Your objectives are:
1. Run `/app/bin/audio_processor /app/reference.wav`. The process will hang.
2. Use system tracing or filesystem inspection tools (e.g., `/proc` filesystem) to recover the deleted SQLite database from the hanging process.
3. Examine the recovered SQLite database. You will need to write queries to inspect the parsed audio metadata and identify the specific anomaly (a specific chunk type and its properties) that triggers the infinite loop.
4. Write a standalone C program at `/home/user/detector.c` that parses WAV files and acts as a filter.
   - The program must take a single command-line argument: the path to a WAV file.
   - It must exit with code `1` if the file is "evil" (contains the anomaly).
   - It must exit with code `0` if the file is "clean".
   - The program must parse the WAV structure directly (do not rely on calling external binaries like `ffprobe` or the `audio_processor`).

To help you validate your detector, we have provided an adversarial corpus of audio files:
- `/app/corpus/clean/` contains valid WAV files that your detector must accept.
- `/app/corpus/evil/` contains malformed WAV files that your detector must reject.

Compile your detector to `/home/user/detector` (e.g., `gcc -o /home/user/detector /home/user/detector.c`). An automated test suite will run your compiled binary against the corpus. Your solution must accurately classify all files.