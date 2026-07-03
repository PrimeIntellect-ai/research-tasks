You are a build engineer managing artifact configurations. We define our build metadata using a custom functional expression language. Recently, misconfigured and potentially malicious expressions have been causing our build system to crash or run out of memory. 

You need to write a C++ sanitization tool that parses these expressions and flags them as either safe or dangerous based on our security policy.

We have a legacy C++ parser skeleton located at `/home/user/parser.cpp`. However, it has two major issues:
1. It lacks policy enforcement. The security rules for expressions are documented in an image artifact left by the previous security engineer at `/app/policy.png`. You will need to extract the text from this image (e.g., using `tesseract`) to learn the specific constraints (such as maximum allowed AST depth and forbidden function names).
2. The current implementation of `/home/user/parser.cpp` has a memory leak. You must fix the memory leak using standard C++ memory management (e.g., `std::unique_ptr` or proper destructors).

Your task is to:
1. Read the policy rules from `/app/policy.png`.
2. Modify `/home/user/parser.cpp` to parse the expressions, enforce the extracted rules, and run without memory leaks.
3. Compile the program to `/home/user/sanitizer` (e.g., `g++ -O2 -std=c++17 /home/user/parser.cpp -o /home/user/sanitizer`).

**Program Interface Requirement:**
The compiled program `/home/user/sanitizer` must accept a single command-line argument: the path to a text file containing one expression.
- If the expression is completely valid and complies with the policy in the image, the program must print `CLEAN` to standard output and exit with code `0`.
- If the expression violates the policy (e.g., exceeds the maximum depth, uses forbidden functions, or is syntactically invalid), it must print `EVIL` to standard output and exit with code `1`.

We have provided two directories containing test cases to help you test your program:
- `/home/user/corpora/clean/`: Contains safe expressions.
- `/home/user/corpora/evil/`: Contains malicious/violating expressions.

Ensure your compiled program strictly adheres to these input/output requirements, as it will be integrated into our automated build pipeline.