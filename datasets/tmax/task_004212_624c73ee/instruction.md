You are a build engineer managing artifact validation for a CI/CD pipeline. 

We have a legacy, stripped binary at `/app/legacy_checker` that verifies the integrity and safety of build manifest files submitted to our artifact server. It takes a single file path as an argument (e.g., `/app/legacy_checker manifest.txt`) and exits with code `0` if the manifest is valid, and code `1` if it is rejected. 

Because it was written years ago and we lost the source code, we cannot integrate it into our new C-based shared library. We need you to reverse-engineer its logic and write a functionally identical replacement in C.

Here are your instructions:
1. **Analyze the Binary**: Use standard tools (`objdump`, `gdb`, `strings`, `ltrace`, etc.) to reverse-engineer `/app/legacy_checker`. Determine the exact validation rules it applies to an input file.
2. **Re-implement in C**: Write a C program at `/home/user/fast_checker.c` that applies the exact same validation rules. It must accept a single file path as a CLI argument and exit with `0` for valid files and `1` for invalid files.
3. **Compile**: Compile your program to `/home/user/fast_checker` using `gcc`.
4. **Adversarial Verification**: We have provided two corpora of manifests to test against:
   - `/app/corpora/clean/`: Contains manifests that must be ACCEPTED (exit 0).
   - `/app/corpora/evil/`: Contains manifests that must be REJECTED (exit 1).
   Use bash scripts and diffing tools to ensure your `/home/user/fast_checker` behaves exactly like `/app/legacy_checker` on all files in both directories.

Your final executable must be located at `/home/user/fast_checker`. Do not use external libraries besides the standard C library.