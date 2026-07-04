You are tasked with building the core C component for a configuration management system that tracks, normalizes, and deduplicates configuration keys across multiple servers. 

Currently, raw configuration files are dropped into `/home/user/raw_configs/`. These files contain key-value pairs, but they are messy: inconsistent spacing, varying casing for keys, and comments.

Write a C program at `/home/user/config_tracker.c` and compile it to `/home/user/config_tracker`. The program must take a list of file paths as command-line arguments and process them in the order provided.

For each file, the program must:
1. **Regex Pattern Construction & Parsing**: Use POSIX regex (`<regex.h>`) to identify valid configuration lines. A valid line contains an optional leading space, a key (alphanumeric and underscores), an equals sign (`=`), and a value (any characters), with optional whitespace around the key and value. Ignore empty lines and lines where the first non-whitespace character is `#`.
2. **Tokenization & Normalization**: Extract the key and value. 
   - Normalize the key by converting all its characters to uppercase.
   - Strip all leading and trailing whitespace from both the key and the value. 
   - Construct a normalized string in the exact format: `KEY=VALUE`.
3. **Hash-Based Deduplication**: Compute the `djb2` hash of the normalized `KEY=VALUE` string. 
   - You **must** use this exact djb2 implementation for the hash:
     ```c
     unsigned long hash_djb2(const char *str) {
         unsigned long hash = 5381;
         int c;
         while ((c = *str++))
             hash = ((hash << 5) + hash) + c; /* hash * 33 + c */
         return hash;
     }
     ```
   - Maintain a record of hashes seen so far during the execution.
4. **Pipeline Logging & Output**: 
   - If the hash has **not** been seen before, print the entry to `/home/user/deduped_configs.log` in the format: `[<HASH>] <KEY>=<VALUE>\n` (e.g., `[123456789] PORT=8080`).
   - If the hash **has** been seen before (a duplicate across or within files), append a warning to a pipeline monitoring log at `/home/user/pipeline.log` in the format: `DUPLICATE: <KEY>=<VALUE>\n`.

Once compiled, run your program against the files in `/home/user/raw_configs/` in alphabetical order (e.g., `./config_tracker /home/user/raw_configs/*`).

Constraints:
- Use standard C libraries (`stdio.h`, `stdlib.h`, `string.h`, `ctype.h`, `regex.h`).
- Do not use external libraries (like PCRE).
- Process files line by line (maximum line length 1024 bytes).
- Both output files (`/home/user/deduped_configs.log` and `/home/user/pipeline.log`) must be created by your program or script and overwritten if they exist (or appended to properly as long as the final state matches the requirements).