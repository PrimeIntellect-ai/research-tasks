You are helping a developer organize a large batch of project files. Many of these files are compiled ELF binaries, but some have been corrupted, truncated, or deliberately malformed during a failing automated build process. 

We have a vendored C++ library designed to validate ELF files located at `/app/simple-elf-validator-0.1.0`. Unfortunately, the original developer left a mistake in the `Makefile` that prevents it from building successfully. 

Your tasks are:
1. Fix the build issue in `/app/simple-elf-validator-0.1.0/Makefile` so that running `make` successfully produces the static library `libelfval.a`.
2. Write a C++ command-line tool at `/home/user/classifier.cpp` that uses this library. The library provides a header `elf_validator.h` containing the function `bool is_valid_elf(const char* filepath);`.
3. Compile your tool to `/home/user/classifier`. It must link against `libelfval.a`.
4. Your tool must take a single file path as a command-line argument:
   - If the file is a valid ELF (according to `is_valid_elf`), the program should exit with status code `0`.
   - If the file is invalid, corrupted, or malformed, the program should exit with status code `1`.

You can test your classifier against the zipped corpora located at `/app/corpus.zip`. You will need to extract it to see the `clean/` and `evil/` directories containing sample ELF files. 

Ensure your final executable is exactly at `/home/user/classifier` and conforms to the exit code requirements, as an automated system will use it to grade your solution against an extensive hidden corpus of valid and malformed ELF files.