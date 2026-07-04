You are a security researcher investigating a novel piece of malware. The malware authors communicated via a voice channel, and a snippet of their conversation was intercepted. 

Your goals are to extract an encrypted binary, reverse engineer its core payload decoding algorithm, and write a clean, equivalent implementation in C++.

Here are your instructions:
1. An intercepted audio file is located at `/app/intercepted_audio.wav`. It contains a spoken passphrase. Transcribe this audio (you may use Python libraries, `ffmpeg`, or any other tool you can install in the container to extract or transcribe it).
2. Use the transcribed passphrase (all lowercase, spaces removed) to decrypt the archive located at `/app/evidence.zip`. Use the standard `unzip -P <passphrase>` command.
3. Inside the extracted contents, you will find a stripped ELF executable named `payload_decoder` and a core dump `core.payload`. 
4. The `payload_decoder` binary accepts a single command-line argument (a string) and prints a transformed hexadecimal representation to stdout. 
5. Reverse engineer `payload_decoder`. Analyze its stack trace from the core dump if it helps you understand its internal structures.
6. Write a C++ program at `/home/user/clean_decoder.cpp` that perfectly mimics the transformation logic of the original `payload_decoder` for any given input string. 
7. Compile your code to produce an executable at `/home/user/clean_decoder`. 

Your implementation must be functionally bit-exact to the original binary on all valid string inputs. An automated fuzzing suite will invoke your `/home/user/clean_decoder` with hundreds of random inputs and compare its output directly against the original binary.