You are an AI assistant helping a bioinformatics researcher organize and compress a large dataset of genomic sequence chunks. 

The researcher has a raw data file located at `/home/user/raw_sequences.txt`. 
Each line in this file follows the format: `YEAR-REGION_ID:SEQUENCE`
Example:
`2019-R01:AAAAAAGGGCCCTTTT`
`2020-R02:GGGGGGGTTTAA`

Your task is to perform the following operations:
1. Write a C program at `/home/user/process.c` that parses `/home/user/raw_sequences.txt`.
2. For each line, the C program must compress the `SEQUENCE` using a custom Run-Length Encoding (RLE). The RLE should represent consecutive identical characters by their count followed by the character (e.g., `AAAAAAGGGCCCTTTT` becomes `6A3G3C4T`).
3. The C program must split and route the output based on the `YEAR`. For each line, append the resulting RLE string (followed by a newline character) to a file named `year_<YEAR>.rle` inside the directory `/home/user/processed/`. If the file does not exist, the program should create it.
4. Compile and run your C program to generate the chunked and compressed `.rle` files.
5. After the files are generated, use standard Linux shell commands to create a backup directory at `/home/user/backup/`.
6. Create **hard links** for all the generated `.rle` files from `/home/user/processed/` into `/home/user/backup/`. The hard links should have the exact same names as the original files.
7. Determine which year is the most recent (highest numerical value) among the generated files. Create a **symbolic link** at `/home/user/latest_year.sym` that points to the `.rle` file of that most recent year in the `/home/user/processed/` directory.

Constraints and Requirements:
- You must use C as the primary language for parsing, compressing, and splitting the data.
- Ensure the directories `/home/user/processed/` and `/home/user/backup/` are created before generating files or links.
- Use basic standard C libraries (`stdio.h`, `stdlib.h`, `string.h`).
- The C program should be compiled to an executable named `/home/user/process`.