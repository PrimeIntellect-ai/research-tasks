I am a researcher organizing legacy dataset files, and I need your help to decompress and catalog them safely. The datasets are scattered in the directory `/home/user/datasets` and are encoded using a custom Run-Length Encoding (RLE) format with the `.rle` extension. 

Here is what you need to do:

1. **Write a Custom Decompressor in C:**
   Create a C program at `/home/user/decoder.c` and compile it to `/home/user/decoder`. 
   The RLE format is a simple binary format: every 2 bytes represent a chunk. The first byte is an unsigned 8-bit integer representing the character count, and the second byte is the ASCII character itself. For example, the bytes `0x03 0x41` should decompress to the string "AAA".
   
   The program must accept exactly two command-line arguments: the input file path and the output file path.
   Usage: `./decoder <input_file.rle> <output_file.txt>`

2. **Implement Atomic Writes:**
   To prevent corrupting datasets if the system crashes, your C program MUST use atomic writes. It should open a temporary file, write all the decompressed data into it, close it, and then use the `rename()` system call to atomically move it to the final output file path. 

3. **Metadata-Based Search and Processing:**
   Search the directory `/home/user/datasets` for all `.rle` files that were modified **within the last 7 days**. 
   For each file you find matching this criteria, use your compiled `decoder` program to decompress it into the `/home/user/processed/` directory. The output file should have the exact same base name but with a `.txt` extension (e.g., `data1.rle` becomes `/home/user/processed/data1.txt`).

4. **Logging via Redirection:**
   As you process the files, capture the base names of the newly created text files (e.g., `data1.txt`) and save them to `/home/user/processed_log.txt`. The list in `processed_log.txt` must be sorted alphabetically, with one filename per line.

Ensure that the final text files contain the correct decompressed ASCII data. Do not process files older than 7 days.