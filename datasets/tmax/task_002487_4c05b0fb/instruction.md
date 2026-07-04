You are a security auditor tasked with containing a proprietary, potentially vulnerable data processing tool. 

We have a stripped binary located at `/app/bin/data_parser`. This binary parses custom log formats, but we suspect it has undocumented behaviors (potential backdoors or directory traversal vulnerabilities) when given maliciously crafted input.

Your task is to write a secure C wrapper around this binary to sandbox its execution, enforce path policies, and verify file integrity before processing.

Create your wrapper source code at `/home/user/secure_wrapper.c` and compile it to `/home/user/secure_wrapper`.

The wrapper must implement the following security controls:
1. **Command Line Arguments:** The wrapper must accept exactly two arguments: `<input_file>` and `<output_file>`.
2. **Content Security Policy (Path Enforcement):** 
   - The `<input_file>` path must strictly start with `/app/data/in/`.
   - The `<output_file>` path must strictly start with `/app/data/out/`.
   - If either path violates this policy, print "POLICY_VIOLATION" to standard error and exit with code 1.
3. **File Integrity Verification:**
   - Before doing anything else, the wrapper must compute the SHA-256 hash of the `<input_file>`.
   - It must read the expected hash from a sidecar file named `<input_file>.sha256` (which contains the 64-character hex hash followed by a newline).
   - If the sidecar file is missing or the hashes do not match exactly, print "INTEGRITY_ERROR" to standard error and exit with code 2.
4. **Process Isolation (Sandboxing):**
   - The wrapper must use `seccomp` (Strict or BPF) to drop privileges before executing the `/app/bin/data_parser` binary.
   - At a minimum, you MUST explicitly block the following system calls to prevent network exfiltration and arbitrary code execution: `execve` (after the initial binary is loaded, so use `fork` and apply seccomp in the child right before or just after `execve` - wait, seccomp BPF allows blocking `execve` but you need it to run the parser. Better approach: use `fork()`, inside the child use `execve()`, but wait, we want to restrict the *parser*. Since it's an external binary, you should compile a shared library that uses `__attribute__((constructor))` to apply seccomp and inject it via `LD_PRELOAD`, OR just block network calls like `socket`, `connect`, `bind` using seccomp BPF in the child right before `execve` (though `execve` resets seccomp strict, seccomp BPF persists across `execve` if `NO_NEW_PRIVS` is set!).
   - *Requirement:* In the child process, call `prctl(PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0)`, load a seccomp BPF filter that specifically denies `socket`, `connect`, `bind`, `listen`, `accept`, and `clone`, and then `execve` the `/app/bin/data_parser` binary. 
   - Wait for the child to exit and return its exit status.

Your solution will be tested against a suite of 20 test cases evaluating valid inputs, corrupted inputs, policy bypass attempts, and malicious files triggering network/system behaviors in the parser. 

Compile your code with `gcc -o /home/user/secure_wrapper /home/user/secure_wrapper.c -lseccomp -lcrypto` (you may need to install `libseccomp-dev` and `libssl-dev` first). Ensure the executable is placed at `/home/user/secure_wrapper`.