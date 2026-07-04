You are an artifact manager tasked with modernizing a binary curation repository. 

Our build system relies on a proprietary, legacy metadata extractor located at `/app/legacy_extractor`. This tool analyzes our compiled ELF binaries, extracts a specific embedded manifest, converts its character encoding, and prints the result. Unfortunately, the source code for this tool was lost, and the binary is stripped. We need to replace it with a maintainable script.

Your task is to reverse-engineer the behavior of `/app/legacy_extractor` and write a fully functionally equivalent program. 

Requirements:
1. Analyze `/app/legacy_extractor`. You may use tools like `gdb`, `strace`, `ltrace`, `xxd`, `strings`, `readelf`, or `objdump` to understand its logic.
2. The tool takes exactly one argument: the path to an ELF binary. 
3. It extracts a specific section from the ELF, decodes it (there is a simple obfuscation and encoding scheme applied), and prints the result to standard output.
4. Write a replacement script (you may use Python, Bash + standard utilities, C, or any other standard language available) that implements the exact same logic.
5. Save your executable script to `/home/user/extractor`. Ensure it has executable permissions (`chmod +x /home/user/extractor`).

Your program's output must be BIT-EXACT equivalent to `/app/legacy_extractor` for any given ELF file. An automated fuzzer will compile hundreds of mutated ELF binaries and test your script against the legacy oracle to ensure it handles all edge cases perfectly.