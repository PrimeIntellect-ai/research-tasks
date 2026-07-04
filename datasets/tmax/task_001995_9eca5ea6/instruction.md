You are a security engineer responsible for rotating credentials across our legacy infrastructure. The old credentials were generated using a proprietary tool that we no longer have the source code for. To modernize our infrastructure and audit the generation process, we need to rewrite this tool.

Your task is to reverse-engineer the legacy credential rotator and implement a bit-exact equivalent version in C.

We have provided the legacy stripped binary at:
`/app/legacy_rotator`

Requirements:
1. Analyze `/app/legacy_rotator`. It accepts a single command-line argument (a seed string) and outputs a 32-character hexadecimal string representing the new credential.
2. Implement the exact same cryptographic hashing / transformation logic in C.
3. Save your source code to `/home/user/new_rotator.c`.
4. Compile your code to `/home/user/new_rotator`. Your compiled executable must take exactly one command-line argument (the seed) and output the exact same 32-character hex string as the legacy binary, followed by a newline (`\n`). 
5. The logic must be perfectly equivalent for any alphanumeric seed string between 8 and 64 characters in length.

You must rely on reverse engineering tools (like `objdump`, `gdb`, `ltrace`, `strace`, `strings`) to determine the custom cryptographic operations, hardcoded keys, and state mutations the binary performs.

Automated verification will aggressively fuzz your `/home/user/new_rotator` binary against the legacy oracle to ensure the outputs are strictly identical across hundreds of random seeds.