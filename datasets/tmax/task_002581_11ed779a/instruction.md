You are an MLOps engineer responsible for tracking text-based experiment artifacts before they are ingested into our main training pipeline. We need a fast validation step to count the basic vocabulary size (total whitespace-separated tokens) across our raw dataset artifacts.

The raw dataset text files are located in `/home/user/artifacts/raw_data/`. 

Your task is to:
1. Write a C++ program located at `/home/user/tokenizer_check.cpp`.
2. The program must read all `.txt` files within the `/home/user/artifacts/raw_data/` directory.
3. For each file, tokenize the text by whitespace and count the total number of tokens.
4. The program must aggregate the total token count and the total number of processed `.txt` files.
5. Finally, the program must output the results to a JSON file at `/home/user/artifacts/token_summary.json` with the exact following structure:
   `{"total_tokens": X, "num_files": Y}`
   (where X is the integer sum of tokens, and Y is the integer count of text files).
6. Compile your C++ program using g++ with C++17 support and run it to produce the output JSON.

Requirements:
- Only consider `.txt` files in the directory.
- Use basic whitespace separation for tokenization.
- Do not use external C++ libraries beyond the standard library (e.g., `<iostream>`, `<fstream>`, `<filesystem>`, `<sstream>`, etc.).
- Ensure your compiled binary is executed so the JSON file is generated.