I am a researcher organizing a custom dataset and I need your help extracting data payloads from a custom binary archive format. 

I have a configuration file located at `/home/user/dataset.conf` which contains a list of valid 4-byte ASCII "Magic Headers", one per line.
My dataset files are scattered throughout the `/home/user/datasets/` directory and its subdirectories. 

The valid dataset files have the `.dat` extension. However, not all `.dat` files are valid. A valid dataset file follows this exact binary structure:
1. **Magic Header** (4 bytes): Must exactly match one of the 4-byte strings listed in `/home/user/dataset.conf`.
2. **Payload Length** (4 bytes): An unsigned 32-bit integer (little-endian) representing the length of the data payload `N`.
3. **Data Payload** (`N` bytes): The actual raw data.

Your task is to write and execute a C program that:
1. Reads `/home/user/dataset.conf` to load the valid magic headers.
2. Recursively traverses the `/home/user/datasets/` directory looking for `.dat` files.
3. Opens each `.dat` file and checks its 4-byte header.
4. If the header matches a valid magic header from the config, read the payload length, extract the data payload, and append it to a single binary file located at `/home/user/extracted_payloads.bin`.
5. For every valid file processed, append a line to `/home/user/extraction.log` in the exact format: `<relative_path_from_datasets_dir>: <4_byte_magic>` (e.g., `group_A/sample1.dat: RSCH`). Sort the final `/home/user/extraction.log` alphabetically by the relative path and save it.

Please write the C code (e.g., `extractor.c`), compile it, and run it to produce `/home/user/extracted_payloads.bin` and `/home/user/extraction.log`.