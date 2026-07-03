You are an AI assistant helping a technical writer finalize a documentation draft for an embedded robotics system. The writer has a large Markdown draft with placeholders that need to be populated with metadata extracted from domain-specific files (GCode and ELF binaries). 

Your task is to write a C++ program to perform this transformation, compile it, run it, and then use shell commands to append a file manifest.

Here is the step-by-step requirement:

1. **Write a C++ program** (save it as `/home/user/doc_builder.cpp`) that reads `/home/user/draft.md`.
2. The program must scan the text for two types of placeholders and replace them:
   - `{{GCODE_STATS:<filepath>}}`: Parse the referenced GCode file, find the maximum X, Y, and Z coordinate values (from lines like `G1 X10.5 Y20.0 Z5.0`), and replace the placeholder with the exact string: `Max X: <val>, Max Y: <val>, Max Z: <val>` (formatted to 1 decimal place).
   - `{{ELF_ENTRY:<filepath>}}`: Parse the referenced 64-bit ELF binary using standard structures (e.g., `<elf.h>`), extract the entry point address (`e_entry`), and replace the placeholder with the exact string: `Entry Point: 0x<hex_value>` (lowercase hex).
3. The C++ program should output the transformed markdown to `/home/user/final_doc.md`.
4. Compile your program using `g++ -std=c++17 -O2 doc_builder.cpp -o doc_builder`.
5. Run your program.
6. **Generate a Manifest:** Use bash commands to calculate the SHA256 checksums of all GCode and ELF files present in the `/home/user/assets/` directory. Append the exact text `\n## Manifest\n` to `/home/user/final_doc.md`, followed by the output of `sha256sum /home/user/assets/*`.

**Constraints & Details:**
- The paths in the placeholders are relative to `/home/user/`.
- The GCode parser only needs to look for `X`, `Y`, and `Z` characters followed immediately by floating-point numbers on lines starting with `G0` or `G1`.
- The C++ program must not use any external libraries other than the standard library and standard Linux headers like `<elf.h>`.