You are an expert red-team operator. We have recovered a stripped, UPX-packed binary at `/app/obfuscator_oracle` which is used by an adversary to process command-line arguments and logs, redact sensitive information, mitigate injection attacks, and format the output for execution in a sandboxed environment.

Your objective is to reverse-engineer the exact behavior of this binary and implement a functionally identical replica in C++.

We need a completely standalone C++ program that is BIT-EXACT equivalent to `/app/obfuscator_oracle` for any arbitrary input provided on standard input. 

**Requirements:**
1. **Analyze the Binary:** Examine `/app/obfuscator_oracle`. You may use tools like `strace`, `ltrace`, `objdump`, `gdb`, or simply treat it as a black-box oracle and observe inputs and outputs.
2. **Replicate the Logic:** The binary reads from `stdin` until EOF. It performs specific data redactions (e.g., masking certain credential patterns), escapes characters commonly used in XSS/injection payloads, and formats the output into a custom payload format. 
3. **Implementation:** Write your solution in C++ and save the source code to `/home/user/replica.cpp`.
4. **Compilation:** Compile your code using `g++ -O2 -o /home/user/replica /home/user/replica.cpp`.

Our automated verification system will run a fuzzing campaign against both `/app/obfuscator_oracle` and your `/home/user/replica`. They will be fed thousands of random inputs (including edge cases, binary data, and various string patterns), and their standard outputs must match byte-for-byte.

Begin your analysis and provide the final replica source code.