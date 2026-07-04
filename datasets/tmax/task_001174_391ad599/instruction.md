You are acting as a localization engineer for a global software team. Our legacy translation pipeline relies on a proprietary, compiled binary to generate 32-bit integer IDs for English source strings. We are migrating our entire ETL and data processing pipeline to pure Python, which requires replacing this binary.

Your task is to analyze the stripped Linux executable located at `/app/bin/key_gen` and write a Python 3 script that perfectly replicates its ID generation algorithm. 

The binary accepts a single string as a command-line argument and prints the calculated integer ID to standard output. 

Requirements:
1. Reverse-engineer or mathematically deduce the exact hashing algorithm used by `/app/bin/key_gen`. You have standard reverse-engineering tools (like `objdump`, `gdb`, `strings`) and Python available in your environment.
2. Write your solution to `/home/user/keygen.py`.
3. Your Python script must accept a single string as its first command-line argument (`sys.argv[1]`) and print the resulting integer to standard output, matching the binary's behavior exactly for any given string.
4. The script must be deterministic and handle arbitrary ASCII strings (lengths 1 to 255 characters, including spaces and punctuation).

You do not need to process our translation CSV/JSON files right now; the primary goal is building the mathematical replica of the ID generator. An automated fuzzer will test your `/home/user/keygen.py` script against the original `/app/bin/key_gen` using thousands of randomly generated strings to ensure bit-exact equivalence.