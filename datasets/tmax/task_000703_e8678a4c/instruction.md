As a security engineer, you have been assigned to rotate the credentials for our legacy verification system and recreate its core hashing utility, as we have lost its source code. 

First, we received an audio dictation from the head of security containing the new cryptographic salt to be used for the rotation. You can find this recording at `/app/salt_dictation.wav`. Transcribe this audio to recover the new salt.

Second, we have the legacy stripped binary at `/app/oracle_verifier`. This binary was used to sanitize inputs against basic injection/XSS payloads and then hash them, but it uses the *old* salt. You need to analyze this ELF binary to understand its exact behavior, specifically:
1. What exact string sanitization rules it applies (it filters out specific injection/XSS patterns).
2. How it computes the hash (it appends the salt to the sanitized input and outputs the checksum).

Your objective is to write a new executable program at `/home/user/verifier` that behaves *exactly* like the `/app/oracle_verifier`, but uses the **new** salt from the audio recording instead of the old one. 

Your program must:
1. Be an executable file at `/home/user/verifier`.
2. Accept exactly one command-line argument (the input string).
3. Print the resulting hex checksum to standard output, followed by a newline.
4. Exactly match the sanitization logic of the original binary.

You may write this program in any language, but it must run natively or via standard interpreters available in the terminal.