You are an operations engineer triaging an incident. A critical system component, `/home/user/legacy_service`, has started crashing with a segmentation fault during startup. The source code for this binary has been lost.

Through initial triage, you know the following:
1. The binary requires exactly one command-line argument: an 8-character initialization key.
2. If the correct key is provided, the binary initializes successfully and exits with code 0.
3. If an incorrect key is provided, the binary jumps to a deliberate crash handler and segfaults.
4. The key validation involves some simple bitwise obfuscation (not standard plain text), meaning standard `strings` or `ltrace` commands might not immediately reveal the plaintext key.

Your task:
1. Use interactive debuggers (`gdb`), reverse engineering tools (`objdump`), or memory inspection to analyze `/home/user/legacy_service` and determine the correct 8-character initialization key.
2. Save the correct 8-character key to a file named `/home/user/key.txt` (with no trailing newlines).
3. Write a Python script at `/home/user/verify.py` that reads the key from `/home/user/key.txt`, executes `/home/user/legacy_service` with the key as its argument, and uses a Python `assert` statement to validate that the binary's exit code is exactly 0. 

The task is complete when `/home/user/key.txt` contains the correct key and `/home/user/verify.py` runs successfully without any assertion errors.