You are a storage administrator managing an archive for a massive audio dataset. Your disk arrays are reaching capacity due to millions of small, fragmented audio chunk files containing significant amounts of digital silence (zeroes). Furthermore, users upload automated "tar" archives of their chunks, and security has flagged several archives attempting path traversal and symlink attacks to overwrite system files.

Your task has two independent parts:

**Part 1: Transcribe the Reference Audio**
We received a highly important voice memo from the lead engineer regarding the storage failure, located at `/app/reference.wav`. 
You must transcribe the spoken English content of this file and save it exactly as plain text to `/home/user/audio_secret.txt` (all lowercase, no punctuation). You may install any tools necessary (e.g., python packages, ffmpeg) to perform this transcription.

**Part 2: The `audio_sanitizer` Utility**
You must write a C++ program and compile it to `/home/user/audio_sanitizer`.
This utility must act as both an adversarial filter and a storage optimizer. It must accept a command-line interface exactly as follows:

`./audio_sanitizer validate <path_to_tar_file>`
When run in `validate` mode, your program must scan the specified uncompressed `.tar` archive file. It must exit with code `0` (Safe) ONLY IF all file and directory paths specified in the tar headers are safe. It must exit with code `1` (Evil) if the archive contains any of the following:
- Paths containing `../` or `..\\`
- Absolute paths (starting with `/`)
- Any symbolic links (Tar typeflag `2`)

`./audio_sanitizer optimize <input_dir> <output_dir>`
When run in `optimize` mode, your program must read all `.chunk` files in `<input_dir>`, apply a custom zero-byte Run-Length Encoding (RLE) compression, and write the compressed files to `<output_dir>`. 
- **Custom Zero-Byte RLE**: Non-zero bytes are written as-is. Whenever a sequence of one or more `0x00` bytes occurs, it must be replaced by exactly two bytes: `0x00` followed by an 8-bit unsigned integer representing the count of zeroes (e.g., a single zero becomes `0x00 0x01`, 255 zeroes become `0x00 0xFF`). If there are more than 255 consecutive zeroes, split them into multiple blocks (e.g., 256 zeroes becomes `0x00 0xFF 0x00 0x01`).
- **Hard Linking**: To save inodes and disk space, if two or more compressed `.chunk` files have the exact same compressed binary payload, only the first one should be written as a regular file. Subsequent identical chunks must be created as **hard links** to the first file in the `<output_dir>`.

Ensure your C++ code is robust. Our automated verification suite will test your compiled `/home/user/audio_sanitizer` against a hidden corpus of clean and malicious tar files using the `validate` command, and will test your `optimize` command on a set of generated `.chunk` files.