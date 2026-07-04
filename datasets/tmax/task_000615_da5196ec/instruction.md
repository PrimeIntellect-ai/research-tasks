I am a technical writer tasked with reorganizing our legacy documentation archives. I have a monolithic directory of old documentation files, and I need you to write a C tool to process them safely.

Here is the setup:
- A configuration file is located at `/home/user/doc_rules.conf`. It contains three lines:
  ```
  SEARCH=LegacySys
  REPLACE=QuantumFlow
  DELIMITER=@@@PAGE_BREAK@@@
  ```
- The directory `/home/user/legacy_docs/` contains several large `.txt` files.
- We only want to process files in `/home/user/legacy_docs/` that have the metadata tag `Status: ReadyForArchive` on their very first line.

Your task:
1. Write a C program at `/home/user/processor.c` and compile it to `/home/user/processor`.
2. The program should read `/home/user/doc_rules.conf` to dynamically extract the `SEARCH`, `REPLACE`, and `DELIMITER` strings.
3. Use shell commands to find the valid `.txt` files in `/home/user/legacy_docs/` (checking the metadata tag on the first line) and pass them to your C program.
4. For each valid file, the C program must:
   - Split the file into multiple smaller files wherever the `DELIMITER` appears on a line by itself.
   - The delimiter line itself should NOT be included in the output chunks.
   - Strip the `Status: ReadyForArchive` line from the output.
   - Perform a global text replacement, replacing all instances of the `SEARCH` string with the `REPLACE` string.
   - Write the output chunks to `/home/user/processed_docs/` using the naming format `<original_filename>_part<N>.txt` (where N starts at 1 for each file).
   - **Crucial**: To ensure data integrity, the C program must perform atomic writes for the output files. Write the chunk to a temporary file (e.g., `<original_filename>_part<N>.tmp`) and then atomically rename it to the final `.txt` extension.
5. Once all valid files are processed, create a compressed gzip archive of the `/home/user/processed_docs/` directory at `/home/user/final_docs.tar.gz`.

Ensure your C program handles potential edge cases like consecutive delimiters or files without delimiters (which would just be one part). The final archive `final_docs.tar.gz` must contain only the correctly replaced and split `.txt` files.