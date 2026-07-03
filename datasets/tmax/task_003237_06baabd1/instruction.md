I am a data scientist working on cleaning a large text dataset. I need to filter records using a specific relevance scoring algorithm. I tried writing a C++ utility using a complex numerical library to compute cosine similarities, but due to a configuration bug, it's just outputting "0" for every input (similar to how a misconfigured matplotlib backend produces blank plots). 

I want to scrap that complex approach and build a simpler, exact integer-based similarity scorer in C++.

However, I lost the exact configuration parameters. Fortunately, I have a screenshot of the original specification message saved at `/app/scoring_rules.png`.

Your task is to:
1. Extract the `MIN_TOKEN_LENGTH` and `GLOBAL_MULTIPLIER` integer values from the image `/app/scoring_rules.png` (Tesseract is available on the system).
2. Write a C++ program at `/home/user/relevance.cpp`.
3. Compile it to an executable at `/home/user/relevance`.

The C++ program must do the following:
- Accept exactly one command-line argument: the input string (the document).
- Tokenize the string:
  - Treat ANY non-alphanumeric character as a delimiter.
  - Convert all extracted tokens to lowercase.
  - Discard any token whose length is strictly less than `MIN_TOKEN_LENGTH`.
- Compute the term frequency (count) of each remaining token in the input.
- Calculate the integer dot product between the input's term frequencies and the following target dictionary:
  `{"anomaly": 5, "dataset": 3, "clean": 4, "null": 2}`
  *(For example, if "clean" appears twice in the input, that contributes 2 * 4 = 8 to the sum).*
- Multiply the total dot product sum by `GLOBAL_MULTIPLIER`.
- Print ONLY this final integer score to standard output (followed by a newline) and exit.

Constraints:
- Only output the final integer. Do not print any debugging text.
- If the input string is empty or contains no valid tokens, the output should be `0`.

Ensure the final executable is at `/home/user/relevance` and has execute permissions.