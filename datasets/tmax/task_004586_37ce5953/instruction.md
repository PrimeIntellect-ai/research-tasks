As a DevSecOps engineer, I am auditing a legacy web application and enforcing policy-as-code for our new infrastructure. During the audit, I discovered that the application uses a custom, undocumented stripped binary located at `/app/legacy_hasher` to hash user credentials.

We need to migrate this hashing logic to our new centralized authentication service, but the original source code has been lost. We need a bit-exact C implementation of the algorithm.

Your task is to:
1. Reverse engineer the `/app/legacy_hasher` ELF binary. It takes a single string as a command-line argument and prints a 32-character hexadecimal hash to standard output, followed by a newline.
2. Write a C program at `/home/user/hasher_rebuilt.c` that implements the exact same hashing algorithm. 
3. Your C program must accept a single command-line argument (the input string) and print the resulting hash to standard output, exactly matching the formatting of the original binary.
4. Compile your code to `/home/user/hasher_rebuilt` using `gcc -O2 /home/user/hasher_rebuilt.c -o /home/user/hasher_rebuilt`.

You have tools like `objdump`, `gdb`, `ltrace`, and `strings` available to analyze the binary. 

An automated test will verify your solution by fuzzing your compiled binary against the original `/app/legacy_hasher` oracle with thousands of random inputs.