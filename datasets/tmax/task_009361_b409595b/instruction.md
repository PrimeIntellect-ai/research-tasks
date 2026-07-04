You are an open-source maintainer for a custom C-based WebSocket Virtual Machine server. A contributor has recently submitted a pull request in the form of a patch file, but their submission broke the build and introduced critical bugs.

The codebase is located in `/home/user/repo/`.
The contributor's patch is located at `/home/user/pr.patch`.

The patch attempts to:
1. Update the HTTP/WebSocket handshake routing logic to extract query parameters.
2. Add a new `OP_JMP` (relative jump) instruction to the VM emulator.
3. Update the `Makefile` to include new compiler flags.

However, the PR has three major issues:
1. **Broken Build**: The contributor broke the `Makefile` structure. `make` no longer works.
2. **Web Security Vulnerability**: The URL routing update in `http_parser.c` introduces a classic buffer overflow vulnerability when handling unusually long routes.
3. **VM Emulator Bug**: The new `OP_JMP` implementation in `vm.c` lacks bounds checking. A maliciously crafted relative jump can move the program counter (PC) outside the allocated bytecode buffer, causing a segmentation fault.

Your task:
1. Apply the patch `/home/user/pr.patch` to the repository in `/home/user/repo/`.
2. Fix the `Makefile` so that running `make` successfully compiles the `ws_vm` binary.
3. Fix the vulnerability in `http_parser.c` by ensuring the route extraction safely truncates to the size of the destination buffer (15 readable characters + null terminator) rather than blindly copying.
4. Fix the `OP_JMP` logic in `vm.c` to include bounds checking. If a jump target would move the PC outside the valid range of the bytecode (`0` to `code_length - 1`), the VM should immediately halt and return `-1`.
5. Compile the fixed binary by running `make` in `/home/user/repo/`.
6. Run the integration test suite by executing `/home/user/run_tests.sh`.

If all your fixes are correct, the test script will successfully execute and create a verification log at `/home/user/final_result.txt` containing the text `ALL_PASSED`.