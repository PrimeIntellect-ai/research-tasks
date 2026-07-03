You are a DevSecOps engineer responsible for enforcing policy as code. We are investigating a recent breach where an attacker bypassed file permission access controls by forging a custom-encrypted web session token.

The original developer of the session token encryption scheme left the company and took the source code. All we have is a reference oracle binary and a screen recording of the developer testing the application. 

Your task is to reverse-engineer the encryption scheme and write a bit-exact equivalent decryption tool in C++.

1. **Analyze the Video Capture:**
   There is a video file located at `/app/crypto_test.mp4`. It contains a screen recording of a terminal session where the developer tested the cipher. Use `ffmpeg` to extract frames and analyze the output to find plaintext and ciphertext pairs. 

2. **Cryptanalysis:**
   Deduce the encryption algorithm from the pairs. The algorithm operates byte-by-byte. It consists of a repeating XOR key (length 4) followed by an index-dependent arithmetic addition (wrapping around 8-bit integers). 

3. **Reimplement the Decryptor:**
   Write a C++ program at `/home/user/decryptor.cpp` and compile it to `/home/user/decryptor`. 
   - Your program must take exactly one command-line argument: a hex-encoded ciphertext string.
   - It must decode the payload, decrypt it, and print the resulting plaintext to standard output exactly, with no trailing newlines or extra text.
   - Example expected behavior: `/home/user/decryptor 237bfc8f30` should output `hello`.

Make sure your C++ tool handles standard ASCII plaintexts up to 256 characters long. An automated testing suite will fuzz your compiled binary against a hidden reference implementation with hundreds of randomized inputs to ensure bit-exact equivalence.