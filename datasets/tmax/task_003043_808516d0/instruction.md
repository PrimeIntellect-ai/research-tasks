You are acting as a release manager preparing a deployment for our legacy data processing pipeline. As part of this, we need to rebuild a custom C-based bytecode emulator that has been unmaintained.

We have a broken CMake project located in `/home/user/emulator_project`. 
Currently, it fails to build because it cannot find the shared library `libvmlog.so` at link time. The library is located in `/home/user/emulator_project/lib`, but the `CMakeLists.txt` is configured incorrectly.

Your tasks:
1. Fix the `CMakeLists.txt` so the project compiles and links successfully.
2. Implement the missing emulator logic in `vm.c`. The original documentation was lost, but an old engineer's voice memo describing the specification was recovered and is located at `/app/spec_memo.wav`. You will need to transcribe this audio file to understand how to implement the emulator.
3. The executable should be built at `/home/user/emulator_project/build/vm_emulator`. 
4. The executable takes exactly one command-line argument: a string of characters (the bytecode). It must process the string according to the rules in the audio memo and print the final state to standard output, followed by a newline.

Ensure your C code is robust and does not crash on arbitrary input strings. The final binary will be rigorously tested against millions of random input sequences to ensure it behaves exactly like our historical reference binary.