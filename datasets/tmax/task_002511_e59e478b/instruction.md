You are an integration developer responsible for migrating a suite of API tests. As part of this migration, we need to eliminate our dependency on a legacy, proprietary C binary used for request signing.

The binary is located at `/app/legacy_signer`. It is a stripped ELF executable. Our existing integration tests invoke this binary by passing a request payload ID (a string) as a command-line argument, and the binary outputs a signature string that is then used in the `X-Legacy-Sig` HTTP header. 

Your task is to reverse-engineer or black-box analyze the `/app/legacy_signer` binary to understand its validation and signature generation logic, and write a bit-exact equivalent Python script.

Requirements:
1. Create a Python script at `/home/user/sign_request.py`.
2. The script must accept exactly one command-line argument (the payload ID), just like the binary.
3. The script must output exactly what the binary outputs for ANY given input string. This includes matching any error messages, validation rejections (like length limits or character restrictions), and the final signature generation.
4. The output must be printed to standard output, followed by a newline, exactly matching the binary's behavior.
5. You may use any tools available in the environment (e.g., `ltrace`, `strace`, `strings`, `gdb`, or simply fuzzing the binary with various inputs) to deduce the logic.

Once you have written `/home/user/sign_request.py`, test it against the binary to ensure it produces the exact same output for various edge cases and valid payload IDs.