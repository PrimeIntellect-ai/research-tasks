I am currently reorganizing a massive dataset of binary files and need to recreate a missing utility. I used to have a tool that calculated the target directory "bucket" (an integer) for each file based on its `SIZE`, `MASK`, and `ID`. 

I have a stripped compiled binary of the original tool at `/app/oracle`, which takes these three values as command-line arguments and prints the bucket number. Unfortunately, I lost the source code. However, I found an old screenshot of my whiteboard at `/app/formula.png` that contains the exact mathematical formula used to calculate the bucket.

I started rewriting the tool in C at `/home/user/organizer/classifier.c`, but it's incomplete, leaks memory, and needs to be linked with a C++ helper library I wrote at `/home/user/organizer/helper.cpp` (which provides a `safe_mod(int a, int b)` function to avoid division-by-zero).

Your task:
1. Extract the mathematical formula from `/app/formula.png`.
2. Complete `/home/user/organizer/classifier.c` so that it parses the 3 command-line arguments (`SIZE`, `MASK`, `ID` as integers) and calculates the correct bucket using the formula. It must output ONLY the resulting integer to standard output.
3. Fix any memory leaks or memory corruption issues in `classifier.c` (the final binary should pass AddressSanitizer/Valgrind with zero errors).
4. Create a `Makefile` in `/home/user/organizer/` that:
   - Compiles `helper.cpp` into an object file or static library.
   - Compiles `classifier.c` and links it with the C++ helper to produce the executable `/home/user/organizer/classifier`.
5. Ensure your compiled `/home/user/organizer/classifier` behaves bit-for-bit identically to `/app/oracle` for any given positive integer inputs.

The entry point for your program must be:
`/home/user/organizer/classifier <SIZE> <MASK> <ID>`