I need you to write a robust archiving and project organization tool in Python. I'm a developer trying to clean up my old project directories, but my previous backup script keeps getting stuck in infinite loops because of complex symlink structures I used for local package linking. 

Additionally, the project directories contain a mix of different file types that need special handling before archiving:
1. **Legacy Text Files:** Some old project logs are encoded in ISO-8859-1. Your script must read any `.txt` file, convert its contents to UTF-8, and store the UTF-8 version.
2. **Database WAL Files:** There are SQLite Write-Ahead Log (`.wal`) files. Your script needs to parse the WAL header to extract the 32-bit Magic Number (the first 4 bytes) and include it in the metadata manifest.
3. **Nested Archives:** There are existing `.zip` files. You must verify their integrity (e.g., using `zipfile.is_zipfile` and a test read). If a zip is corrupted, skip it entirely.
4. **Symlink Loops:** You must implement a safe traversal mechanism that detects and breaks infinite symlink loops, restricting traversal to a maximum depth of 10.

Before you build the archiver, there is a dictation audio file left by the previous lead developer at `/app/project_dictation.wav`. You need to transcribe this audio (you can install and use `ffmpeg` and `whisper` or `whisper.cpp` in the environment). Save the transcription text to `/home/user/dictation_transcript.txt`.

Your final Python program should be saved at `/home/user/archiver.py`. It must accept a target directory as an argument and output a deterministic JSON manifest to `stdout` containing the processed files, resolved paths, extracted WAL magic numbers, and UTF-8 converted text content (for txt files). 

The output JSON manifest must be a list of dictionaries, sorted alphabetically by the relative file path, with the following structure:
`[{"path": "relative/path", "type": "file|symlink|zip|wal", "content": "utf8_text_if_txt", "wal_magic": "hex_string_if_wal", "target": "symlink_target_if_symlink"}]`