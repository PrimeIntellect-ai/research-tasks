You are an artifact manager tasked with curating a custom binary repository. 

A continuous build process has dumped a binary repository file at `/home/user/repo.bin`, and we need to extract specific metadata from it based on a configuration file.

The binary file `/home/user/repo.bin` has the following custom format:
1. It starts with a 4-byte magic header: `ARTF`
2. This is followed by a sequence of records. Each record consists of:
   - A Record Type (1 byte): `0x01` for JSON metadata, `0x02` for raw binary artifact data.
   - A Record Length (4 bytes, unsigned 32-bit integer, little-endian).
   - The Payload (Length bytes).

For `0x01` records, the payload is a valid JSON string containing metadata (e.g., `{"artifact_name": "alpha", "version": "2.0.0"}`). 

You also have a configuration file at `/home/user/filter.conf` with a single line specifying a target version:
`TARGET_VERSION=2.0.0`

**Your Task:**
1. Write a C program named `/home/user/parser.c` that reads the configuration file to determine the target version.
2. The C program must then parse `/home/user/repo.bin`.
3. For every `0x01` (JSON metadata) record, extract the `artifact_name` and `version` fields.
4. If the extracted `version` matches the `TARGET_VERSION` from the config file, append the information to a CSV file at `/home/user/manifest.csv`.
5. Compile and run your C program to generate the CSV.

The output CSV `/home/user/manifest.csv` must have the following format exactly (no headers):
`artifact_name,version`

Example output:
```
alpha,2.0.0
gamma,2.0.0
```

Constraints:
- You must write the solution primarily in C (`/home/user/parser.c`). Standard C library functions are sufficient. 
- You may use standard shell commands to compile and run the code.
- Ensure your C program correctly handles the binary parsing of the length field (little-endian).