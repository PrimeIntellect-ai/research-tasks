You are an artifact manager building a secure parser for a custom binary repository.

Your task is to write a Go program that parses a custom binary artifact format, decodes its payload, and outputs the raw payload to `stdout`.

### The Master Key
You have been provided with a video file at `/app/artifact_scan.mp4`. This video transmits a 1-byte Global Master Key visually. 
- The video consists of exactly 8 frames.
- Each frame is completely black or completely white.
- A black frame represents the bit `0`, and a white frame represents the bit `1`.
- The 8 frames chronologically form an 8-bit integer, where the first frame is the Most Significant Bit (MSB) and the 8th frame is the Least Significant Bit (LSB).
Extract this byte; you will need it as your `MasterKey`.

### The Binary Format
Your Go program must parse files adhering to the following structure:
- **Offset 0** (4 bytes): Magic signature, must be exactly `ARTF`.
- **Offset 4** (1 byte): Version, must be exactly `0x02`.
- **Offset 5** (1 byte): Flags (bitmask).
  - Bit 0 (`0x01`): If set, the payload is XOR-masked with the Embedded Key.
  - Bit 1 (`0x02`): If set, the payload is XOR-masked with the Global Master Key.
- **Offset 6** (1 byte): Embedded Key Length (`K`).
- **Offset 7** (`K` bytes): Embedded Key.
- **Offset 7+K** (4 bytes): Payload Length (`P`), unsigned 32-bit integer in Little-Endian.
- **Offset 11+K** (`P` bytes): The encrypted Payload.

### Decoding Logic
1. Your program must accept a single file path as a command-line argument (`os.Args[1]`).
2. Before reading, your program **must** acquire a shared POSIX file lock (`LOCK_SH`) on the file to prevent concurrent writers from mutating the file while you read it.
3. Validate the file. If the file is too short, the magic signature is incorrect, the version is not `0x02`, or the file does not have enough bytes for the claimed Payload Length, your program must print `INVALID` to `stdout` and exit with status `1`.
4. If valid, extract the payload.
5. If Bit 0 of Flags is set, decrypt the payload by XORing each byte of the payload with the Embedded Key cyclically. For example, `payload[i] ^= embedded_key[i % K]`. (If `K=0`, skip this step).
6. If Bit 1 of Flags is set, decrypt the payload by XORing every byte with the `MasterKey` you extracted from the video. (Both bit 0 and bit 1 can be set; apply Embedded Key XOR first, then Master Key XOR).
7. Print the final decrypted raw payload bytes to `stdout` (do not add trailing newlines unless they are part of the payload) and exit with status `0`.

### Requirements
- Write your code in `/home/user/parser.go`.
- Compile it to `/home/user/parser`.
- Your program must strictly output only the specified bytes or `INVALID`. Any extraneous output will cause verification to fail.