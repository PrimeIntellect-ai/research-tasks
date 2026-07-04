You are an AI assistant helping a localization engineer prepare a sample of user interface strings for a translation smoke test. 

We have a raw dump of UI strings extracted from a legacy application in `/home/user/raw_strings.txt`. The file contains lines formatted like this:
`MSG_ID_001: "Welcome to the App, User!"`
`MSG_ID_002: "Please log-in..."`

Your task is to write a C program at `/home/user/process_strings.c` that performs normalization, deduplication, and sampling on these strings, and then saves the sorted output.

Follow these specific rules for the C program:
1. **Extraction & Normalization**: For each line, extract only the text inside the double quotes. Convert all alphabetical characters to lowercase. Remove all characters except lowercase letters (`a-z`), digits (`0-9`), and spaces (` `). For example, `"Welcome to the App, User!"` becomes `welcome to the app user`.
2. **Hash-Based Deduplication**: Implement the standard DJB2 string hashing algorithm. 
   *(DJB2 algorithm: initialize hash to 5381, then for each character `c`, `hash = ((hash << 5) + hash) + c;`)*
   Keep track of the hashes of the normalized strings. If you encounter a normalized string whose hash has already been seen, ignore it.
3. **Sampling**: We only want a subset of the unique strings for our smoke test. Only output a normalized string if its DJB2 hash modulo 10 equals 0 (`hash % 10 == 0`).
4. **Output**: The C program should print the sampled, normalized strings to standard output (one per line).

Once your C program is complete:
1. Compile it using `gcc -o /home/user/process_strings /home/user/process_strings.c`.
2. Run it and redirect the output to `/home/user/sampled_strings.txt`.
3. Use the bash `sort` command to alphabetically sort `/home/user/sampled_strings.txt` and save the final result to `/home/user/final_sample.txt`.

Ensure your C program is robust enough to handle lines up to 1024 characters long.