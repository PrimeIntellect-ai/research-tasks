I've inherited an old legacy system for a forensics project, and we have a critical bottleneck: a proprietary binary tool located at `/app/legacy_encoder` whose source code was lost years ago. We need to replace it with a modern, open-source script or compiled program.

The tool processes binary files and outputs an encoded format. It is heavily used in our data pipeline, but occasionally crashes, and we cannot fix it without the source. Your task is to analyze what `/app/legacy_encoder` is doing and write a completely independent, bit-exact equivalent replacement.

What we know:
- The binary is stripped.
- It takes two arguments: an input file path and an output file path. Example: `/app/legacy_encoder input.bin output.enc`
- You can use any tools available (like `strace`, `ltrace`, `gdb`, `objdump`, `strings`, or hex editors) to analyze its behavior, system calls, memory footprints, or intermediate states.
- The new implementation can be written in any language of your choice, but it must be executable directly from the command line as `/home/user/encoder_impl` (make sure it has execution permissions and a valid shebang if it's a script).
- It must take exactly the same arguments: `/home/user/encoder_impl <input_file> <output_file>`.
- The output file produced by your script must be bit-for-bit identical to the output produced by `/app/legacy_encoder` for any arbitrary input file.

Please analyze the binary, deduce the custom encoding algorithm it uses, and write the replacement to `/home/user/encoder_impl`. We will test your implementation by fuzzing it with hundreds of random binary files and comparing the outputs against the legacy binary.