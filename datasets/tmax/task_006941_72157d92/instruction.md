You are a security researcher analyzing a sophisticated piece of malware. The malware exfiltrated sensitive data over the network, but it encrypted the payload using a chaotic map Pseudo-Random Number Generator (PRNG). 

We have intercepted the network traffic, captured a filesystem image of the USB drive where the malware temporarily stored its configuration, and reverse-engineered the decryption algorithm into a C program. However, the decryption is currently failing.

Your objectives are:

1. **Recover the Seed:** The malware wrote a file named `config.txt` to the USB drive, which contained the initial PRNG seed, but deleted it before the USB was seized. An image of the USB is provided at `/home/user/usb.img`. Recover the deleted `config.txt` file and read the seed value.
2. **Extract the Payload:** Analyze the packet capture at `/home/user/exfil.pcap`. The malware sent a single UDP packet to port 1337. Extract the hex-encoded data payload from this packet.
3. **Fix the Decoder:** We have provided the reverse-engineered decryption tool at `/home/user/decoder.c`. The original malware was compiled to use IEEE 754 double precision for its chaotic map generation (the Logistic Map). Our reverse-engineered C code was mistakenly written using single precision (`float`). Because the logistic map is highly sensitive to initial conditions, the precision loss over 1000 warmup iterations causes the key stream to completely diverge. Modify `/home/user/decoder.c` to use proper double precision so the key stream matches the malware's sequence.
4. **Decrypt:** Compile your fixed decoder, and run it using the recovered seed and the extracted hex payload. 

Save ONLY the final decrypted ascii string (no trailing newlines or extra text) to `/home/user/decrypted_secret.txt`.