You have been given a C++ project in `/home/user/audio_processor/` that processes large sets of signal data. It currently fails to compile due to some cross-language FFI and linkage issues between the C++ core and a legacy C library (`legacy_io.c`). 

Your objectives are:
1. Fix the compilation errors. The C++ code in `main.cpp` and `processor.cpp` interacts with `legacy_io.h`, but linker errors and struct alignment issues prevent it from building. Ensure the `DataRecord` struct matches the expected memory layout of the legacy C library (which expects 8-byte alignment and a specific schema).
2. The program applies a threshold filter to the signal data. The exact numerical threshold you must use is spoken in the audio file `/app/config.wav`. You will need to transcribe or listen to this audio file to find the threshold value and hardcode it in `processor.cpp`.
3. The main data processing loop in `processor.cpp` sorts and merges the records, but it is currently implemented very naively and is far too slow. You must optimize this function (using highly optimized C++ or inline assembly) to make it extremely fast. 
4. Run your compiled program on the provided dataset: `./build/audio_processor /app/dataset.bin /home/user/output.bin`. 

Your goal is to ensure the output file is mathematically correct (using the threshold from the audio) AND that the processing time is minimized. An automated verifier will measure the execution time of your program.

Requirements:
- Ensure the project builds successfully using the provided `Makefile`.
- Produce `/home/user/output.bin` with the correct filtered and sorted data.
- The runtime of your program must be significantly reduced.