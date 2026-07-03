You are acting as an artifact manager for our internal binary repository. We have been receiving custom-compressed archive submissions, some of which contain malicious embedded payloads or malformed multi-line metadata logs.

Your task is to create a Go-based sanitization and classification tool that filters these artifacts. 

First, you need to recover the internal corporate XOR key used for our proprietary compression scheme. The previous maintainer left this key in an audio memo located at `/app/reference_memo.wav`. You will need to transcribe this audio file (you may install and use any transcription tools like `whisper.cpp` or `ffmpeg` as needed) to recover the spoken numeric key.

Once you have the key, write a Go program that acts as a CLI classifier. The program must:
1. Accept a target directory of custom-compressed `.bin` files as a command-line argument.
2. Decompress each file. The files are standard `gzip` streams, but every byte of the gzip stream has been XORed with the numeric key you recovered from the audio memo.
3. Extract the uncompressed payload. Each uncompressed payload consists of a binary header (first 64 bytes), followed by a multi-line log record (text, delimited by `---END_LOG---`), and finally the artifact data.
4. Classify the artifact as "clean" or "evil". An artifact is considered "evil" if the multi-line log contains the substring `AUTHORIZATION: BYPASS` OR if the binary header's magic bytes (first 4 bytes) are `0xDE 0xAD 0xBE 0xEF`. 
5. The Go program must output the classification results to `stdout` in the exact format: `[FILENAME]: CLEAN` or `[FILENAME]: EVIL` for each file processed.
6. The program should also perform a bulk rename of the processed files in the directory, appending `.clean` or `.evil` to their original filenames based on the classification.

You must compile your Go program to `/home/user/artifact_filter`.

Ensure your tool is highly accurate. It will be tested against a hidden adversarial corpus of custom-compressed files.