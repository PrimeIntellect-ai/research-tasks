You are a DevSecOps engineer responsible for enforcing "Policy as Code" in our execution pipeline. We have a requirement to run untrusted third-party binaries in a restricted sandbox. The execution constraints (system calls allowed) are embedded directly inside the binaries as encoded payloads.

You need to write a C++ sandbox wrapper called `secure_runner` that will execute these binaries.

However, the sandboxing library we use, `libseccomp` (vendored at `/app/vendored/libseccomp-2.5.4`), has a configuration issue preventing it from building correctly in our environment.

Your objectives:

1. **Fix the Vendored Package**: 
   Navigate to `/app/vendored/libseccomp-2.5.4`. The `./configure` script or Makefile contains a deliberate flaw injected during our last repository migration that prevents it from linking correctly (specifically, an invalid compiler flag is hardcoded). Find and fix this perturbation, then build and install the package locally to `/app/libs`.

2. **Develop the C++ Wrapper**:
   Write a C++ program at `/home/user/secure_runner.cpp`. 
   Compile it to `/home/user/secure_runner`.
   The program must accept exactly two arguments: the path to an untrusted ELF binary, and a single string argument to pass to that binary.
   Usage: `/home/user/secure_runner <path_to_elf> <input_arg>`

3. **ELF Analysis and Payload Decoding**:
   Your `secure_runner` must parse the target ELF binary to find a custom section named `.secpolicy`.
   This section contains a payload string formatted as a Base64 encoded string, which, when decoded, is XOR-encrypted with the single-byte key `0x5A`.
   The decrypted payload is a comma-separated list of system call names (e.g., `read,write,exit_group,execve`).

4. **Process Isolation (Sandboxing)**:
   Using the fixed `libseccomp` library, your wrapper must:
   - Initialize a seccomp filter that defaults to KILL (killing the process on violation).
   - Parse the decrypted policy list and add rules to ALLOW only the specified system calls.
   - Load the filter.
   - Execute the target ELF binary using `execve`, passing the binary path as `argv[0]` and the `<input_arg>` as `argv[1]`. `argv[2]` must be NULL. Environment variables should be cleared.

Your final executable must perfectly match the behavior of our reference implementation for any given valid ELF file and input. It should exit with code 255 if the `.secpolicy` section is missing or decoding fails, and otherwise yield the exact output and exit code of the constrained binary.