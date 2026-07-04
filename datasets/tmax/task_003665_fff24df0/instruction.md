You are an AI assistant helping a technical writer build a robust documentation processing system. The technical writer has left an audio dictation for you at `/app/dictation.wav` detailing the exact custom binary format required for archiving the documentation.

Your task is to create a Python script at `/home/user/doc_builder.py` that processes a directory of documentation files, applies the custom archiving format specified in the audio file, and outputs a compressed archive.

Requirements:
1. **Transcribe the Dictation:** First, listen to (transcribe) `/app/dictation.wav` to understand the precise custom binary format and processing rules required by the documentation team. You may install and use any tools (like `ffmpeg`, `whisper`, etc.) to transcribe this file.
2. **Directory Traversal & Symlink Safety:** The script must recursively traverse a given input directory. The documentation directories are known to contain complex symlinks (some of which are infinite recursive loops, similar to a rogue backup script). Your script MUST safely avoid infinite loops by tracking visited directory real paths. Only process files with a `.md` extension.
3. **Format Conversion & Compression:** For each valid `.md` file discovered, read its contents and stream it into the custom binary format detailed in the dictation. The overall output stream must be compressed using `gzip`. Process the files in alphabetical order of their relative paths to ensure deterministic output.
4. **Atomic Writes:** The system must never leave a partially written archive if it crashes. Your script must stream the compressed data to a temporary file in the same output directory and use an atomic rename to move it to the final output destination once complete.
5. **Command Line Interface:** Your script must accept exactly two arguments:
   `python3 /home/user/doc_builder.py <input_directory> <output_archive.gz>`

The output archive will be strictly tested against a reference implementation using hundreds of randomly generated complex directory structures with adversarial symlinks. Your script must produce bit-for-bit identical, deterministic output.