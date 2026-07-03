You are acting as a forensics analyst recovering evidence from a compromised host. We have discovered a suspicious encryption utility left behind by the attacker, along with intercepted audio of a voicemail and a set of digital certificates.

Your objective is to build a decryption tool that perfectly reverses the attacker's custom encryption scheme, allowing us to recover further intercepted files. 

Here are the artifacts provided to you:
1. `/app/voicemail.wav`: An audio recording intercepted from the attacker's communications. It contains a spoken sequence of words that acts as the initial seed or password for the encryption routine.
2. `/app/encryptor.c`: The source code of the custom encryption utility found on the system. You need to perform a code audit to identify the cryptographic weaknesses (e.g., predictable initialization, weak block cipher, or linear cryptanalysis vulnerabilities) and understand how it uses the spoken sequence from the audio file.
3. `/app/certs/`: A directory containing a certificate chain (`root.crt`, `intermediate.crt`, `leaf.crt`). The attacker's encryption routine relies on the public key of the valid leaf certificate to further derive its state. You must validate this chain; if valid, extract the RSA public exponent to use as a multiplier in the cipher's state machine.

Your final goal is to write a standalone decryption program.
Create an executable file at `/home/user/decryptor`. It can be a compiled binary or a script (e.g., Python, Node.js, C++). 
It must read encrypted binary data from standard input (`stdin`), decrypt it using the recovered seed from the audio and the extracted parameters from the validated certificate chain, and write the strictly decrypted, unpadded plaintext to standard output (`stdout`).

Requirements:
- Transcribe the audio in `/app/voicemail.wav` to find the passcode.
- Validate the certificate chain in `/app/certs/`. If invalid, use a default multiplier of 1. If valid, use the RSA public exponent.
- Identify the CWEs in `/app/encryptor.c` to reverse its logic.
- Your `/home/user/decryptor` must be bit-exact in its output, as it will be heavily tested against a reference implementation with thousands of randomized inputs.