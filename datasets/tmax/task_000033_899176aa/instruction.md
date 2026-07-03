You are an artifact manager tasked with recovering corrupted binary repositories. We have a proprietary artifact repository system that stores incremental backups of ELF binaries in a custom Write-Ahead Log (WAL) format. The blobs inside the WAL are compressed using a custom algorithm and have their string encodings obfuscated.

The original developer who designed this custom compression format left behind a voice memo detailing the exact bit-level specification of the compression and obfuscation algorithms. You can find this audio file at `/app/spec_dictation.wav`. 

Your objectives are:
1. Extract the specification from the audio file `/app/spec_dictation.wav`. (You may need to install audio processing or transcription tools to recover the spoken content).
2. Write a Rust program that implements a decompressor and decoder based EXACTLY on the dictated specification.
3. Your Rust program must read the custom compressed binary data from `stdin` and write the fully decompressed, decoded original ELF file to `stdout`. 
4. Compile your Rust program to `/home/user/decompressor`. 

To assist you, there are a few sample compressed artifacts in `/app/samples/` along with their expected decompressed ELF outputs (e.g., `/app/samples/blob1.bin` and `/app/samples/blob1.elf`). 

Your final compiled binary at `/home/user/decompressor` must perfectly match the behavior of our internal reference implementation. An automated verification suite will randomly fuzz your binary with thousands of generated inputs to ensure it is bit-for-bit equivalent to our internal oracle.