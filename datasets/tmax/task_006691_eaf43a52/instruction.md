You are helping a researcher organize a concatenated sensor dataset. 

The dataset is currently located at `/home/user/dataset.bin.gz`. 
It contains a continuous stream of binary records. You need to decompress this file and write a C program to parse and split the uncompressed binary file into individual chunks using memory-mapped I/O (`mmap`).

The uncompressed binary file (`dataset.bin`) contains sequential records with the following binary format (Little Endian):
- **Magic Number**: 4 bytes, unsigned 32-bit integer, exactly `0x5A5A5A5A`.
- **Timestamp**: 8 bytes, unsigned 64-bit integer.
- **Payload Size**: 4 bytes, unsigned 32-bit integer.
- **Payload**: Variable length raw bytes (length is equal to the `Payload Size`).

Your task is to:
1. Decompress `/home/user/dataset.bin.gz`.
2. Write and compile a C program (save the source as `/home/user/processor.c`) that uses `mmap` to read the uncompressed `/home/user/dataset.bin` file.
3. The C program must iterate through all records in the memory-mapped file. For each valid record, it should extract the payload and save it as a new file in the directory `/home/user/chunks/` (which you must create).
4. The extracted files must be named `chunk_<timestamp>.dat` (e.g., `chunk_1630000000.dat`), containing exactly the raw bytes of the payload.
5. The C program must also generate a CSV log file at `/home/user/extraction_log.csv` containing the parsed headers in the exact format: `Timestamp,PayloadSize` (one record per line).

Constraints:
- You must use C to parse the binary format and handle the extraction.
- The C program must use `mmap` for reading the input file.
- Handle any potential struct padding issues in C carefully (the binary file is tightly packed without padding).