You are a storage administrator tasked with reclaiming disk space on a legacy system while preserving critical compliance data. Your workflow consists of two main objectives: extracting text from a legacy audio recording and implementing a custom bulk-archiving script in Bash.

Part 1: Audio Transcription
You have discovered a legacy compliance recording located at `/app/voicemail.wav`. To save space, we need to extract the spoken content and ultimately delete the large audio file.
1. Install any necessary tools (e.g., `ffmpeg`, `whisper`, or Python-based transcription libraries) in your environment.
2. Transcribe the audio file.
3. Save the resulting text to `/home/user/transcripts/voicemail.txt`. Ensure the text is clean and contains only the transcribed words (no timestamps or extra metadata).

Part 2: Log Archival and Streaming Compression
There is a heavily bloated directory at `/home/user/syslogs/` containing uncompressed, poorly named log files. You must write a Bash script at `/home/user/archive.sh` that performs the following operations:
1. **Bulk Renaming:** Find all `.log` files in `/home/user/syslogs/` and rename them so that any spaces in their filenames are replaced with underscores (`_`).
2. **Streaming Text Editing:** Read each renamed log file using streaming I/O (e.g., `sed` or `awk`) and filter out any line containing the exact string `[DEBUG]`.
3. **Custom Compression Pipeline:** Pipe the filtered output directly into `gzip` (do not create intermediate uncompressed files on disk, to save I/O and space).
4. **Relocation:** Save the resulting compressed files to `/home/user/archive_dir/` keeping their original base names but adding the `.gz` extension.

Before starting, create some dummy log files with spaces in their names and `[DEBUG]` lines in `/home/user/syslogs/` to test your script. Once your script is written and tested, execute it so the final state is present in `/home/user/archive_dir/`.

Your work will be evaluated based on the accuracy of the transcribed text (evaluated via a quantitative string distance metric) and the successful execution of your streaming compression script.