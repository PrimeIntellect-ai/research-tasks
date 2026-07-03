I am a researcher dealing with a massive amount of legacy dataset files. Years ago, my lab used a custom archiving tool to pack and chunk experimental data streams before compressing them. We still have the compiled binary for this tool located at `/app/legacy_archiver`, but we have completely lost the original source code. 

To future-proof our pipeline and process newly generated datasets natively, I need you to reverse-engineer the behavior of this binary and write a C++ replacement. 

Here is what you need to do:
1. Analyze the `/app/legacy_archiver` binary. It is a command-line filter that reads raw binary data from `stdin` and writes a custom chunked archive format to `stdout`.
2. Write a C++ program that exactly replicates this archiving behavior bit-for-bit.
3. Save your source code at `/home/user/archiver.cpp` and compile it to create the executable `/home/user/archiver`.

The new C++ tool must process standard stream redirections exactly like the original. It should handle arbitrary binary data and efficiently split/chunk the stream into the custom archive format used by the legacy tool. You can use standard tools like `xxd`, `strace`, `objdump`, or `gdb` to inspect the legacy binary's output given various inputs.

Please ensure your compiled binary is at `/home/user/archiver`. I will be testing it against the original binary using thousands of random binary inputs to ensure perfect equivalence.