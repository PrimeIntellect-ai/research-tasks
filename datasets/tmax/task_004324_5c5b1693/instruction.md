You are a security auditor investigating a proprietary authentication system that relies on short-lived tokens. The developers claim their tokens are secure, but you suspect they are using a weak scheme.

During your physical audit, you recorded a video of a hardware diagnostic LED on the authentication server. You suspect this LED transmits the 16-bit master secret key during boot. The video is located at `/app/key_transmission.mp4`.

**Video Specifications:**
- The video is exactly 20 seconds long, encoded at 1 Frame Per Second (fps).
- The visual is entirely black (color `#000000`) or entirely white (color `#FFFFFF`).
- The transmission protocol is:
  - Second 0: Black (Idle)
  - Second 1: White (Start bit)
  - Seconds 2 to 17: The 16 bits of the master secret key, transmitted from Most Significant Bit (MSB) to Least Significant Bit (LSB). White = 1, Black = 0.
  - Second 18: White (Stop bit)
  - Second 19: Black (Idle)

**Token Generation Algorithm:**
Through earlier reverse engineering, you discovered that the tokens are generated and logged in the format `username:token_hex`.
The `token_hex` is a 4-character lowercase hexadecimal string (e.g., `0a4f`, `b38c`).
The algorithm used is:
`token_integer = (CRC32(username) & 0xFFFF) XOR master_secret_key`
*(Note: CRC32 is the standard IEEE 802.3 polynomial, as implemented in Python's `zlib.crc32`)*

**Your Task:**
1. Analyze the video to recover the 16-bit master secret key.
2. Write a Python script at `/home/user/validator.py` that takes a single file path as its first command-line argument.
3. The input file will contain security logs with one `username:token_hex` entry per line.
4. Your script must read the file and validate every token.
5. If **ALL** tokens in the file are perfectly valid according to the algorithm and the recovered key, your script must print exactly the word `ACCEPT` to standard output (with or without a trailing newline).
6. If **ANY** token in the file is invalid, your script must print exactly the word `REJECT` to standard output.

We will test your script against two hidden corpora: a clean corpus (100% valid files) and an evil corpus (files containing forged tokens). Your solution must successfully `ACCEPT` all clean files and `REJECT` all evil files.