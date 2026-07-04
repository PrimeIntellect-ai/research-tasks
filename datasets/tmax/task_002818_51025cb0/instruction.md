I need you to write a C test fixture to analyze and execute an undocumented character encoding function provided as raw machine code. 

I am developing some utilities and received a binary blob (`/home/user/payload.bin`) containing x86_64 machine code. This code represents a function with the following C signature:
`void encode_string(char *str, unsigned long len);`

Your task:
1. Write a C program at `/home/user/test_fixture.c` that acts as a test setup.
2. The program must read the raw machine code from `/home/user/payload.bin` into an executable memory segment (you will need to use `mmap` with `PROT_READ | PROT_WRITE | PROT_EXEC`).
3. Cast the memory segment to a function pointer matching the signature above.
4. Call the function, passing in the exact string `"AgentX"` (without null terminator included in the length, so length is 6) and its length.
5. After the function returns, encode the mutated bytes of the string into uppercase hexadecimal pairs separated by a space (e.g., `1A 2B 3C ...`).
6. Write this exact hexadecimal string to a log file at `/home/user/test_output.txt`.

You must compile your C program (e.g., using `gcc`) and execute it to generate the final log file. I will verify the success of the task by checking the contents of `/home/user/test_output.txt`. 

Note: You can assume the environment is x86_64 Linux. Make sure you handle standard file I/O properly and ensure the memory is mapped correctly so the CPU doesn't throw a segmentation fault when executing the shellcode.