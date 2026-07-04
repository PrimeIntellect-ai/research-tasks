You are an administrator responsible for our legacy rolling deployment system. We are migrating our infrastructure and need to recreate a legacy configuration parser written in C, for which we have lost the source code.

The legacy binary is located at `/app/legacy_parser`. It accepts a single command-line argument containing a deployment configuration string and outputs a normalized string. 

We also have a screenshot from an old VNC session `/app/vnc_screenshot.png` that contains documentation about the fallback behavior and trimming rules of this parser when fields are empty or incorrectly formatted.

Your task:
1. Examine `/app/vnc_screenshot.png` to understand the parsing rules (e.g., defaults for timezone, locale, deployment stage, and QEMU VM core counts).
2. Analyze the behavior of `/app/legacy_parser` by running it with various inputs.
3. Write a C program at `/home/user/parser.c` that perfectly replicates the behavior of the legacy binary.
4. Compile your program to `/home/user/parser`.

Your executable `/home/user/parser` must be bit-exact equivalent in its standard output to `/app/legacy_parser` for any given input string. It should handle edge cases exactly as the original binary does.