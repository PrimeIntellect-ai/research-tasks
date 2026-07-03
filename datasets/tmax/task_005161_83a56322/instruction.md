You are acting as a DevSecOps engineer. We are testing a steganographic data exfiltration policy and the sensitivity of our Intrusion Detection System (IDS). 

You have been provided with an audio carrier file at `/app/carrier.wav` (a standard 16-bit PCM mono WAV file). 

Your task is to write a C program that embeds a specific authentication token into this audio file using Least Significant Bit (LSB) steganography without triggering excessive anomaly detection thresholds.

**Instructions:**
1. Write a C program at `/home/user/stego_encoder.c` and compile it to `/home/user/stego_encoder`.
2. The program must read `/app/carrier.wav`.
3. You need to encode the exact payload token: `AUTH_TOKEN_9942_EXFIL` (including the null terminator).
4. **Encoding Scheme:** 
   - Skip the standard 44-byte WAV header.
   - For each byte of the payload token (starting from the first character and ending with the null terminator), extract its 8 bits from Least Significant Bit (bit 0) to Most Significant Bit (bit 7).
   - Embed each bit into the Least Significant Bit of the subsequent 16-bit audio samples. Note that the audio file contains little-endian 16-bit integers. Overwrite the 0th bit of the sample's 16-bit value.
   - Leave the rest of the audio file unmodified.
5. Save the resulting audio file to `/home/user/payload.wav`.
6. **Metric:** The audio quality degradation must be minimal. An automated verification suite will calculate the Peak Signal-to-Noise Ratio (PSNR) between the original `/app/carrier.wav` and your `/home/user/payload.wav`. Your goal is to achieve a PSNR of at least 85.0 dB while successfully embedding the decodable token.

Please complete the task by generating the `/home/user/payload.wav` file.