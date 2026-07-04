You are a mobile build engineer maintaining an automated asset pipeline for a large-scale mobile game. To ensure asset integrity against corruption during patching, we use a custom checksum algorithm.

The exact specifications for this custom algorithm have been left in an audio memo by the senior architect. The audio file is located at `/app/build_requirements.wav`. 

Your tasks are:
1. Transcribe/listen to the audio file to understand the custom checksum algorithm parameters (you may use `ffmpeg` or install tools like `whisper` to process or transcribe it).
2. Implement this checksum algorithm in Go. 
3. Create a property-based test in Go (e.g., using `testing/quick`) in `/home/user/hasher_test.go` that verifies the algorithm is deterministic and satisfies basic checksum properties.
4. Compile your Go implementation into a standalone executable command-line tool located at `/home/user/build_hasher`.

The executable `/home/user/build_hasher` must:
- Read raw binary data from `stdin` until EOF.
- Calculate the custom checksum based on the rules dictated in the audio.
- Print the final checksum to `stdout` as a strict 8-character zero-padded lowercase hexadecimal string (e.g., `0a1b2c3d`), followed by a newline character.

Do not print any other debugging information to stdout.