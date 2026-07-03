You are a platform engineer optimizing a slow CI/CD pipeline. A major bottleneck is a proprietary firmware patching step. The pipeline currently uses a binary tool located at `/app/delta_apply` to apply custom binary delta updates to base firmware images. 

Unfortunately, `/app/delta_apply` is incredibly slow and consumes excessive amounts of memory, often causing pipeline runners to crash out of memory. 

Your task is to:
1. Reverse-engineer the behavior of the `/app/delta_apply` executable. It is a stripped ELF binary. It takes exactly two arguments: `/app/delta_apply <base_file> <delta_file>` and writes the patched output to `stdout`.
2. Write a highly optimized, memory-efficient replacement implementation. You can use any programming language you prefer.
3. Ensure your implementation produces the exact same output as `/app/delta_apply` for any valid base and delta inputs.
4. Your implementation must be wrapped in an executable shell script at `/home/user/fast_apply.sh` that takes the same two arguments (`<base_file> <delta_file>`) and writes the result to `stdout`.

To pass, your `/home/user/fast_apply.sh` must process a large test dataset at least 2.5x faster than the original `/app/delta_apply` while producing bit-for-bit identical output. A naive or memory-heavy implementation will likely fail the speed and memory constraints. Use profiling and memory debugging techniques to ensure your implementation processes data in a streaming or zero-copy fashion where possible.