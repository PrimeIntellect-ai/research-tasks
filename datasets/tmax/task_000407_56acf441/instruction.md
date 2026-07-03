You are a penetration tester analyzing a custom HTTP header processing utility. You have discovered a compiled C++ binary located at `/home/user/validator`. 

Through preliminary analysis, you know that this binary:
1. Reads raw HTTP headers from standard input (stdin) until it encounters an empty line (or `\r\n`).
2. Validates Content-Security-Policy (CSP) enforcement rules.
3. Inspects session cookies for authentication.

There is a hidden debug branch inside this binary that triggers when a specific CSP directive and a specific hidden debug cookie are provided simultaneously. 

Your task is to:
1. Reverse engineer or disassemble the `/home/user/validator` binary to discover the required HTTP headers (specifically the exact CSP directive and the secret Cookie value).
2. Write a C++ program at `/home/user/exploit.cpp` that acts as the exploit.
3. Your C++ program must programmatically execute `/home/user/validator`, feed it the correctly crafted HTTP headers via standard input, and read the output.
4. The output of the validator will contain a secret flag if the bypass is successful. Your C++ program must write ONLY this extracted flag to a file at `/home/user/flag.txt`.

Ensure your C++ program compiles successfully with `g++ /home/user/exploit.cpp -o /home/user/exploit`. You can use any shell commands or disassembly tools (like `strings`, `objdump`, `ltrace`, etc.) available in the environment to analyze the binary before writing your exploit.