You are tasked with recovering missing dependency versions from a corrupted audio transmission and using them to fix a broken C project. 

In `/app/audio/telemetry.wav`, there is a 16-bit PCM, Mono, 8000Hz audio file. It contains a digitally modulated signal. 

Your objective is to write a highly optimized Bash script at `/home/user/fast_decode.sh` that decodes this audio file into text. The decoding must be done **entirely in Bash** (using shell built-ins, `hexdump` or `od` to read binary, but no external languages like Python, C, or Awk for the algorithmic logic).

The decoding algorithm is as follows:
1. Skip the 44-byte WAV header.
2. Read the audio data as 16-bit signed little-endian integers.
3. **Numerical Algorithm (Demodulation):** Process the samples in blocks of 8. For each block, calculate the average of the absolute values of the 8 samples. If the average is greater than or equal to 8000, the block represents a binary `1`. If it is less than 8000, it represents a binary `0`.
4. **Error-Correcting Codes:** The resulting bitstream is encoded using a simple (8, 4) Hamming-like block code. For every 8 bits decoded from the audio, the first 4 bits are the data payload (Big-Endian, bit 0 is MSB, bit 3 is LSB). The next 4 bits are parity bits (P1, P2, P3, P4). 
   - P1 = Data1 XOR Data2 XOR Data3
   - P2 = Data2 XOR Data3 XOR Data4
   - P3 = Data1 XOR Data3 XOR Data4
   - P4 = Data1 XOR Data2 XOR Data4
   For this task, you do not need to implement the error *correction* part, but you MUST implement the *checksum validation*. If a block's parity bits do not match the computed parity, discard that 4-bit data payload.
5. **Character assembly:** Group the valid 4-bit payloads into 8-bit characters (first valid 4-bit block is the upper nibble, next valid 4-bit block is the lower nibble). Output the resulting ASCII string.

The decoded string will contain a list of dependencies and their semantic versions, separated by spaces (e.g., `libfoo-1.2.3 libbar-2.0.1-rc.1`).

**Performance Requirement:**
A naive implementation in Bash using subshells (e.g., `$(expr ...)`) will take over 30 seconds. Your script `/home/user/fast_decode.sh` must be optimized using native Bash arithmetic (`$(( ))`) and built-ins. 
Your script will be tested against the `telemetry.wav` file by running:
`/home/user/fast_decode.sh /app/audio/telemetry.wav`

It must output the decoded string to `stdout` and execute in **under 2.0 seconds**.

**Final Step:**
Once you have the text, you will notice it defines library versions. In `/app/src`, there is a small C project with a `Makefile`. It currently fails to build due to a linking error because it attempts to link against the wrong version paths. Use the semantic versions decoded from the audio to correct the library paths in `/app/src/Makefile` so that running `make` successfully compiles the `main` executable.