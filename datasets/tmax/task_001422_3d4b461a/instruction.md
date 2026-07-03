You are an infrastructure developer maintaining a legacy patching system. We have an old, stripped, and UPX-packed utility located at `/app/legacy_patcher`. This binary processes "MathPatches"—a custom data structure used to apply mathematical transformations to data streams. 

MathPatches are provided as Base64-encoded strings. When decoded, they contain a sequence of custom bytecode instructions representing mathematical operations and offset calculations.

Recently, we discovered that `/app/legacy_patcher` crashes or corrupts data when fed mathematically malformed patches (e.g., operations that result in a division by zero or a negative data offset during runtime evaluation). 

Your task is to:
1. Analyze the `/app/legacy_patcher` binary to understand how it decodes the Base64 input and evaluates the custom mathematical bytecode (opcodes, operands, and offset state).
2. Design and implement a standalone classifier utility at `/home/user/patch_classifier.py` (or a shell script invoking other languages if you prefer, ensuring it's executable as `python3 /home/user/patch_classifier.py <input_file>`).
3. Your utility must read a file containing a single Base64-encoded MathPatch, decode it, and mathematically evaluate the operations to determine if it is "safe" or "malicious" (would trigger the binary's faults).
4. The script must exit with code 0 and print exactly "CLEAN" to stdout if the patch is mathematically valid and safe.
5. The script must exit with code 1 and print exactly "EVIL" to stdout if the patch evaluates to an invalid mathematical state (e.g., negative offset or div-by-zero).
6. Provide a comprehensive unit test suite in `/home/user/tests/` that proves your classifier works on various crafted edge cases (you will need to encode your own custom test data structures based on your assembly analysis).

Do not attempt to patch the binary itself. You must write the pre-execution classifier.