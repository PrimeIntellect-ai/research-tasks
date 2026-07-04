You are a data engineer building a high-performance ETL component. You need to write a C++ program that processes a raw text data feed, normalizes it, calculates rolling statistics on the text properties, and creates a stratified sample of the output. 

Write a C++ program at `/home/user/processor.cpp` and compile it to `/home/user/processor`.

**Input Data:**
A tab-separated file at `/home/user/raw_chat.tsv` with three columns:
`MsgID` \t `Encoding` \t `Message`

- `Encoding` will be either `UTF-8` or `LATIN1` (ISO-8859-1).
- `Message` contains the raw text of the message.

**Processing Requirements:**
Your C++ program must read the input file and perform the following operations:
1. **Character Encoding Handling:** Read the message. If the `Encoding` is `LATIN1`, convert it to valid `UTF-8`. If it is `UTF-8`, leave it as is.
2. **Tokenization and Normalization:** 
   - Tokenize the UTF-8 string by splitting on spaces (` `) and standard ASCII punctuation marks: period (`.`), comma (`,`), exclamation (`!`), and question mark (`?`).
   - Discard empty tokens.
   - Normalize the tokens by converting any uppercase ASCII letters (`A-Z`) to lowercase (`a-z`). Leave multi-byte UTF-8 characters as they are.
3. **Rolling Statistics:**
   - Maintain a global sliding window of the lengths (in **bytes**) of the last `100` valid tokens processed across the entire stream.
   - For each message, after processing all its tokens and updating the global window, compute the average token length in the window. If no tokens have been processed yet, the average is `0.00`.
4. **Stratification:**
   - Classify the message into a length stratum based on its `TokenCount` (number of valid tokens in the message):
     - `S` (Short): 0 to 5 tokens.
     - `M` (Medium): 6 to 15 tokens.
     - `L` (Long): 16 or more tokens.

**Outputs:**
Your program should produce two TSV files:

1. `/home/user/processed_chat.tsv`
   Columns: `MsgID` \t `TokenCount` \t `RollingAvg` \t `Stratum`
   - `RollingAvg` must be formatted to exactly 2 decimal places (e.g., `4.50`).
   - Example row: `msg_123 \t 4 \t 4.25 \t S`

2. `/home/user/sampled_chat.tsv`
   - Implement data sampling and stratification by extracting exactly the **first 2 messages** encountered for each stratum (`S`, `M`, and `L`) from the processed results.
   - The file should contain at most 6 rows (2 of each stratum), preserving the exact same columns and format as `processed_chat.tsv`. The rows should be ordered by their appearance in the input file.

**Constraints:**
- Use standard C++17 (`g++ -std=c++17 /home/user/processor.cpp -o /home/user/processor`). 
- Do not use heavy external libraries (like ICU or Boost); standard library features are sufficient for basic LATIN1 to UTF-8 conversion and ASCII normalization.
- Ensure your program runs efficiently and closes files properly. Execute your program after building it to generate the outputs.