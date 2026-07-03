You are a developer tasked with organizing a legacy project's file registry. The old system tracks files using a messy CSV format, and we need to migrate this into a highly optimized, custom binary index format using C. You must write the C program, compile it, and write a test script to orchestrate the end-to-end process.

Here is the setup:
You will work in `/home/user/workspace`. 

1. **Schema Migration & Custom Data Structure**:
You need to write a C program, `/home/user/workspace/migrator.c`, that reads `/home/user/workspace/registry.csv`.
The CSV has lines formatted as: `filename,owner,permissions` (e.g., `data.txt,admin,0644`).
You must ignore `owner` and `permissions`, and instead inspect the actual file referenced by `filename` in the `/home/user/workspace/` directory to gather its size and checksum.

Your C program must create a custom binary file `/home/user/workspace/index.bin` with the following little-endian structure:
- **Header (8 bytes)**:
  - Magic bytes (4 bytes): `0x49 0x44 0x58 0x31` (ASCII "IDX1")
  - Version (2 bytes): `0x0002`
  - File count (2 bytes): Number of entries in the registry.
- **Entries (70 bytes per file)**:
  - Filename (64 bytes): Null-padded string of the filename.
  - File Size (4 bytes): Unsigned 32-bit integer.
  - Checksum (2 bytes): Unsigned 16-bit integer (details below).

2. **Checksum and Error-Correcting Code**:
For each file, calculate a custom 16-bit XOR checksum.
- Initialize the checksum to `0x0000`.
- Read the file byte-by-byte.
- For the *i*-th byte (0-indexed), left-shift the byte value by `(i % 2) * 8` and XOR it into the checksum. (Effectively reading 16-bit little-endian words and XORing them).
- If the file has an odd number of bytes, treat the missing final byte as `0x00`.

3. **End-to-End Test Orchestration**:
Write a bash script `/home/user/workspace/test_runner.sh` that does the following:
- Creates three dummy files in `/home/user/workspace`:
  - `fileA.dat` containing exactly the string: `HELLO`
  - `fileB.dat` containing exactly the string: `WORLD!`
  - `fileC.dat` containing exactly the string: `TESTING123`
- Creates `/home/user/workspace/registry.csv` with the following content:
  ```
  fileA.dat,alice,0644
  fileB.dat,bob,0600
  fileC.dat,charlie,0755
  ```
- Compiles `migrator.c` into an executable named `migrator` (using `gcc`).
- Runs `./migrator`.
- Verifies that `index.bin` is generated.
- If successful, writes the text `TEST_PASSED` to `/home/user/workspace/test_report.log`.

Your objective is to write `migrator.c` and `test_runner.sh`, and then execute `bash test_runner.sh` so that `index.bin` and `test_report.log` are correctly generated.