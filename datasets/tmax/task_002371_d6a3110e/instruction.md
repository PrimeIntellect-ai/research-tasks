You are an incident responder investigating a recent breach. The attacker compromised a server and deployed a custom data exfiltration tool. We have recovered a few artifacts:
1. A surveillance video file (`/app/incident.mp4`) that was pointed at the server rack's diagnostic LED matrix during the breach.
2. The attacker's custom encryption source code (`/app/encrypt.c`), which contains a cryptographic weakness (CWE-327) by tying its key generation to a physical environmental variable.
3. A web server log (`/app/access.log`) containing the encrypted, hex-encoded exfiltration payloads in the URI parameters.

Through preliminary analysis, we know the attacker derived their 8-bit encryption key directly from the diagnostic video feed to bypass static key scanning. Specifically, the 8-bit integer key is calculated as:
`Key = (Sum of the average Red-channel pixel values across the first 10 frames of the video [Frames 0 through 9]) modulo 256`. 
(Note: Calculate the average Red channel value for each frame as an integer before summing them up).

The encryption algorithm found in `/app/encrypt.c` processes data as follows:
```c
// Pseudocode for the encryption
for (int i = 0; i < len; i++) {
    ciphertext[i] = (plaintext[i] ^ key) + (i % 256);
}
```

Your task:
1. Extract the first 10 frames from `/app/incident.mp4` using `ffmpeg` and calculate the encryption key.
2. Write a C program and compile it to exactly `/home/user/decode`.
3. The `/home/user/decode` executable must read a continuous hex-encoded string (no spaces, e.g., `4a5b6c`) from `stdin` until EOF.
4. It must decrypt the hex-encoded ciphertext back into the original raw plaintext bytes using the derived key and the inverse of the attacker's algorithm.
5. It must output the raw decrypted bytes directly to `stdout` (do not append newlines unless they are part of the plaintext).

To successfully resolve this incident, your compiled binary must be bit-exact equivalent in its input/output behavior to our internal reference decryptor when fed arbitrary hex payloads.