You are a security auditor tasked with reverse engineering and replacing a legacy data processing utility. The system uses a proprietary tool that reads raw log entries from standard input, neutralizes potential Injection/XSS payloads, encrypts the data using a symmetric cipher to protect sensitive fields, computes an integrity checksum, and writes the resulting binary blob to standard output.

Unfortunately, the source code for the current tool has been lost. You have access to a stripped, compiled reference binary located at `/app/secure_logger_oracle`. We need you to reverse-engineer its behavior and write a bit-exact replacement in Rust.

Additionally, the encryption key used by the legacy tool was not documented in text, but was dictated in a voicemail left by the former sysadmin. This audio file is located at `/app/voicemail.wav`. You will need to process this audio file to transcribe the spoken passphrase and use it as the encryption key in your Rust implementation.

Your task:
1. Transcribe the audio file at `/app/voicemail.wav` to discover the secret encryption key.
2. Analyze the behavior of `/app/secure_logger_oracle`. You can feed it various inputs to understand its sanitization rules, encryption algorithm (it is known to be a simple cryptanalysis-friendly cipher like XOR), and file integrity verification method (a standard 32-bit checksum).
3. Write a Rust project in `/home/user/logger_src`.
4. Compile your Rust program to the exact executable path `/home/user/secure_logger`.

Your compiled executable `/home/user/secure_logger` must take input from standard input and write to standard output. It must produce exactly the same binary output as `/app/secure_logger_oracle` for any given input sequence. 

An automated verification suite will test your executable by fuzzing it with thousands of random inputs and comparing the outputs against the reference oracle.