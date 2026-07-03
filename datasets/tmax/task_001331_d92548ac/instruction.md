As a data scientist, I need to clean a dirty dataset of product names. I have a raw text file located at `/home/user/products.txt` containing one product name per line. The data is messy: it has inconsistent casing, erratic spacing, and some slight typos.

Please write a C program at `/home/user/dedup.c` that reads `/home/user/products.txt`, processes the data, and writes the cleaned, deduplicated list to `/home/user/cleaned_products.txt`. 

Your C program must perform the following pipeline for each line:
1. **Normalization & Tokenization**: 
   - Trim all leading and trailing whitespace.
   - Replace any sequence of multiple spaces inside the string with a single space.
   - Convert all uppercase ASCII characters to lowercase.
2. **Deduplication using Distance**:
   - Maintain a list of "accepted" product names.
   - For each normalized string, compute its Levenshtein (edit) distance against all currently accepted strings.
   - If the Levenshtein distance between the current normalized string and ANY already-accepted string is less than or equal to 1, consider it a duplicate and discard it. 
   - Otherwise, append it to the accepted list.
3. **Output**: Write the accepted strings to `/home/user/cleaned_products.txt`, one per line, in the order they were first added.

Compile your program (e.g., using `gcc -O2 /home/user/dedup.c -o /home/user/dedup`) and run it to produce the output file.