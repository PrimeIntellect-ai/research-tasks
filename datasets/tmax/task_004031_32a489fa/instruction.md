You are tasked with fixing a data cleaning pipeline for a dataset containing heavily escaped JSON-lines text. The original developer left a voice memo detailing the exact parsing rules, but the Python implementation was too slow. You need to rewrite the core parser in C++.

Here are your steps:
1. An audio file containing the developer's instructions is located at `/app/voicemail.wav`. Transcribe this audio (you may use `whisper` or similar tools available in your environment) to understand the exact processing rules.
2. The rules will describe how to:
   - Validate the input string.
   - Decode specific unicode escape sequences.
   - Extract tokens using a specific regular expression.
   - Apply a windowed aggregation and deduplication strategy using a custom hash.
3. Write a C++ program at `/home/user/cleaner.cpp` that implements these exact instructions.
4. Compile your program to an executable located at `/home/user/cleaner`.
5. Ensure your compiled program behaves EXACTLY identically to the compiled oracle binary provided at `/app/oracle_cleaner`. Your program must read a single line from standard input and output the result to standard output.

We will verify your solution by running an automated fuzzing tool that feeds thousands of random string permutations (including valid and invalid JSON strings, various unicode escapes, and random characters) to both your `/home/user/cleaner` executable and the `/app/oracle_cleaner` binary, asserting that the standard output is bit-for-bit identical for every input.