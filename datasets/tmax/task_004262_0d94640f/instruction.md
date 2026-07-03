You have inherited an unfamiliar, undocumented financial forensics codebase. We have a known-good legacy executable located at `/app/legacy_calc`. This is a stripped binary that processes input from `stdin` and outputs a specific hash/checksum.

Recently, the team tried to rewrite this tool in C. The git repository for the rewrite is located at `/home/user/hash_repo`. It is a simple C project that reads `stdin` and prints the calculated hex value. 

Unfortunately, the `main` branch of `/home/user/hash_repo` currently produces incorrect outputs compared to `/app/legacy_calc`. We suspect two issues:
1. A regression was introduced somewhere in the git history that causes precision loss during the calculation. 
2. The legacy binary utilizes a hidden magic string for its calculation that is currently missing or incorrect in the C rewrite. 

Your objectives are:
1. Construct a regression test and use Git bisection in `/home/user/hash_repo` to find the exact commit that introduced the precision loss. Revert or fix the code changes introduced by that bad commit.
2. Analyze the stripped binary `/app/legacy_calc` (e.g., using `strings`, `gdb`, or memory dumping) to extract the correct magic string constant it uses.
3. Update the C code in the repository to use the correct magic string.
4. Compile your fixed C code into a final standalone binary at `/home/user/solution_bin`.

To succeed, `/home/user/solution_bin` must behave EXACTLY like `/app/legacy_calc` for any arbitrary `stdin` input. An automated fuzzing suite will run hundreds of random inputs through both binaries to verify absolute bit-for-bit equivalence in their standard output.