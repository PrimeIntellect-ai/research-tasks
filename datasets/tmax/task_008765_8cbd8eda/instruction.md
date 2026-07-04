You are an automation specialist creating a fast data processing workflow. You need to write a C program to parse, normalize, and deduplicate a messy chat log file.

Your task is to create and execute a C program that reads a raw text file located at `/home/user/chat_logs.txt` and writes a cleaned, structured CSV file to `/home/user/clean_users.csv`.

Here are the specific requirements for your C program:

1. **Extraction**: Read `/home/user/chat_logs.txt`. Each line follows the format:
   `[{TIMESTAMP}] <{USERNAME}> {MESSAGE}`
   You must extract the Timestamp, Username, and Message. (You may use POSIX `<regex.h>` or manual string parsing).

2. **Deduplication**: If a user has sent multiple messages, you must only keep the **last** message they sent (based on the order of lines in the file).

3. **Normalization & Tokenization**:
   - For the kept message, convert all lowercase ASCII characters (`a-z`) to uppercase (`A-Z`). 
   - Leave non-ASCII characters (like UTF-8 encoded accented letters) completely untouched.
   - Replace any sequences of two or more consecutive spaces in the message with a single space.
   - Strip leading and trailing spaces from the message.

4. **Output formatting**:
   - Write the processed data to `/home/user/clean_users.csv`.
   - The format must be strictly: `Username,Timestamp,NormalizedMessage`
   - The output lines must be sorted alphabetically by Username (using standard byte-wise `strcmp`).

**Example Input:**
```
[2023-11-01T10:00:00Z] <john_doe> hello   world
[2023-11-01T10:05:00Z] <alice> Mötley   Crüe   rocks!
[2023-11-01T10:06:00Z] <john_doe> bye   world
[2023-11-01T10:07:00Z] <BØB> test    123
```

**Example Output:**
```
BØB,2023-11-01T10:07:00Z,TEST 123
alice,2023-11-01T10:05:00Z,MöTLEY CRüE ROCKS!
john_doe,2023-11-01T10:06:00Z,BYE WORLD
```

**Constraints:**
- Write your solution in a single C file, for example `/home/user/process_logs.c`.
- Compile it with standard `gcc` without requiring any external libraries outside of the standard C library (`libc`).
- Execute your compiled program to generate the required `/home/user/clean_users.csv` file.