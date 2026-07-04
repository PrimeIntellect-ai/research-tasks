You are a penetration tester analyzing a proprietary authentication mechanism. During an audit of a target system, you extracted a stripped binary located at `/app/token_validator`. This binary acts as a local oracle, verifying authentication tokens passed to it via standard input and outputting either the decoded payload or specific error messages.

To proceed with an offline vulnerability scan and cryptanalysis, you need an exact source-code replica of this token validator. Your objective is to reverse-engineer the binary and write a C program that perfectly mimics its behavior for any given input.

Requirements:
1. Analyze `/app/token_validator` using tools like `objdump`, `gdb`, `strings`, `ltrace`, or `strace` (all standard tools are available).
2. The binary reads a token (encoded as a hexadecimal string) from standard input.
3. You must deduce the decoding mechanism, the custom checksum/hash algorithm it uses to validate the payload, and all error-handling paths.
4. Write a functionally equivalent C program at `/home/user/validator.c`.
5. Compile your program to `/home/user/validator` using `gcc /home/user/validator.c -o /home/user/validator`.
6. Your program's output to standard output and standard error, as well as its exit code, must be BIT-EXACT equivalent to the original `/app/token_validator` for all possible inputs (both valid and invalid).

Constraints:
- Do not use any external libraries other than the standard C library.
- The compiled program must reside exactly at `/home/user/validator`.
- Your code must handle arbitrary length inputs gracefully, just as the original binary does.

Once you have successfully reverse-engineered the binary, created the C program, and compiled it, you have completed the task. Our automated verification system will extensively fuzz both the original binary and your compiled program with identical inputs and assert that the outputs perfectly match.