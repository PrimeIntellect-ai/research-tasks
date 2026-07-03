You have just inherited an unfamiliar codebase located in `/home/user/data_parser`. 

There is a C program (`parser.c`) designed to parse a custom binary format, and it comes with a Makefile. You also have a large binary input file named `telemetry.bin` that causes the program to crash (Segmentation fault). 

Your tasks are:
1. **Analyze and Minimize:** Use delta debugging principles to isolate the absolute minimal sequence of bytes that reproduces this specific crash. Save this minimal reproducible example to `/home/user/data_parser/minimal_crash.bin`. 
2. **Diagnose and Fix:** Identify the algorithmic bug in `parser.c` that causes the segmentation fault when parsing corrupted input. 
3. **Recover Gracefully:** Modify the C code so that instead of crashing when encountering this corrupted structure, it prints exactly `ERROR: CORRUPTED INPUT` to standard error (`stderr`) and terminates cleanly with exit code `2`.
4. **Compile:** Save your fixed code as `/home/user/data_parser/fixed_parser.c` and compile it to an executable named `/home/user/data_parser/fixed_parser` using `gcc -O0 -g`.

Ensure that:
- `/home/user/data_parser/minimal_crash.bin` contains *only* the minimal bytes needed to trigger the crash (it should be 5 bytes or fewer).
- `/home/user/data_parser/fixed_parser` successfully catches the error on the original `telemetry.bin` and your `minimal_crash.bin`, outputting the correct message and exit code.