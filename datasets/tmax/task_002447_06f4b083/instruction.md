You are acting as a penetration tester analyzing a compromised system. We have intercepted a suspicious audio file and a binary, along with a dataset of authentication tokens used by the adversary.

Your task has three parts:

1. **Audio Analysis**: We have an audio file located at `/app/intercepted_comms.wav`. It contains a sequence of DTMF (Dual-tone multi-frequency) tones. Decode these tones. The decoded sequence represents the "Master PIN". Write this Master PIN to `/home/user/master_pin.txt`.

2. **ELF Analysis**: There is a binary file located at `/app/auth_service_dump`. Analyze this ELF binary to find the hardcoded salt string used for token hashing. It is stored in the `.rodata` section and is exactly 16 alphanumeric characters long, prefixed with `SALT_`. Write the 16-character salt (without the `SALT_` prefix) to `/home/user/salt.txt`.

3. **Token Validator Implementation**: The adversary uses a custom token format. You must write a C program located at `/home/user/validator.c` and compile it to `/home/user/validator`.
The program must take a single command-line argument: the path to a file containing a token.
It must exit with status `0` if the token is valid, and exit with status `1` if the token is invalid.

Token Validation Rules:
- The token must be exactly 32 bytes long.
- The first 4 bytes must match the first 4 digits of the Master PIN.
- The next 16 bytes must be an exact match of the extracted salt.
- The remaining 12 bytes must contain only valid hexadecimal characters (0-9, a-f, A-F).
- The program must not crash on malformed inputs or binary data.

To help you develop this, we have provided two directories containing sample tokens:
- `/app/corpus/clean/`: Contains valid tokens.
- `/app/corpus/evil/`: Contains malformed, malicious, or invalid tokens.

Your compiled `/home/user/validator` must correctly accept all tokens in the `clean` corpus and reject all tokens in the `evil` corpus.