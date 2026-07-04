A previous engineer left a voice memo detailing the data parsing rules for our new binary configuration tracking stream, but they left before writing the parser! 

Your task is to write a C program that implements the parsing rules described in the voice memo. 

Here is what you need to do:
1. Transcribe the audio file located at `/app/voice_memo.wav`. You can use the pre-installed `whisper` CLI tool (e.g., `whisper /app/voice_memo.wav --model base.en`) to understand the format rules.
2. Based on the rules described in the audio, write a C program at `/home/user/config_parser.c`.
3. The program must read the binary stream from `stdin` and write the parsed output to `stdout`.
4. It should process the input efficiently using streaming or memory-mapped I/O and handle the required character encoding conversions natively or via standard POSIX/C libraries (like `iconv`).
5. Compile your program to `/home/user/config_parser` (e.g., `gcc -O2 -o config_parser config_parser.c`).

The automated verifier will strictly test your compiled binary against a reference implementation using hundreds of randomly generated binary streams to ensure bit-exact equivalence. Ensure you handle EOF correctly and do not crash on truncated data (clean exit with code 1 if a chunk is truncated).