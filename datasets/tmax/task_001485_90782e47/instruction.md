We are migrating our backend services from Python 2 to Python 3. As part of this migration, we have updated our core C-based serialization and parsing shared library (`libparser.so`) to handle the new Python 3 ABI data format. However, the migration is stuck due to a few issues.

First, the `Makefile` in `/app/libparser` has a linking error preventing the shared library from building correctly. You need to fix it so that `make` succeeds and produces `libparser.so`.

Second, we need a validation utility. During the migration, our API is receiving a mix of valid new payloads, old legacy (Python 2) payloads, and completely malformed data. We have prepared two test corpora:
- `/app/corpus/clean/`: Contains strictly valid, new-format payloads.
- `/app/corpus/evil/`: Contains legacy payloads, malformed data, and intentionally corrupted files.

You must create a CLI tool at `/app/validator` written in C. This tool must:
1. Accept a single file path as a command-line argument (e.g., `./validator /path/to/payload.bin`).
2. Read the file.
3. Check the file against the new magic header. The exact required magic string for the new protocol is documented in a diagram image located at `/app/protocol_spec.png`. You will need to inspect or OCR this image to find the correct magic header.
4. If the magic header is correct, pass the remaining payload (after the header) to the `parse_data(const char* buffer, int len)` function provided by `libparser.so`.
5. Exit with code `0` if the payload has the correct magic header AND `parse_data` returns `0` (success).
6. Exit with a non-zero code (e.g., `1`) if the file is missing, the magic header is incorrect, or `parse_data` fails.

Requirements:
- Your `validator.c` source code should be saved in `/app/`.
- Compile it to an executable named `/app/validator`, correctly linking against the fixed `/app/libparser/libparser.so`.
- Make sure `libparser.so` is discoverable at runtime by the validator.
- Your validator must accept 100% of the files in `/app/corpus/clean/` (exit 0) and reject 100% of the files in `/app/corpus/evil/` (exit non-zero).