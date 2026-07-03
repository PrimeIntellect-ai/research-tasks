You have been assigned to finish reorganizing the file structure of our team's custom text processing utility. A previous developer started migrating our old tool to a modular C++ architecture, but left the project in a broken state. 

Here is what you need to do:
1. **Fix the Build Environment:** The source code is located in `/home/user/project/`. The developer tried to separate utility functions and core logic, but accidentally introduced a circular inclusion issue between `encoder.h` and `utils.h` that prevents compilation. Furthermore, the `Makefile` in the directory is corrupted and fails to build the `rle_encoder` target. Repair the header files and the Makefile so the project compiles successfully using `make`.
2. **Apply the Benchmarking Patch:** There is a patch file located at `/home/user/benchmarking.patch`. This patch adds performance benchmarking measurements to `main.cpp`. Apply this patch to the project.
3. **Replicate the Legacy Utility:** The actual string encoding logic in `encoder.cpp` is currently a stub. We lost the original source code for our legacy encoder, but we have a stripped, compiled binary located at `/app/legacy_encoder`. 
   - Analyze the behavior of `/app/legacy_encoder` by passing it various strings as command-line arguments (e.g., `/app/legacy_encoder "AAABBB"`).
   - Implement the exact same encoding algorithm in `encoder.cpp` so that your compiled `/home/user/project/rle_encoder` produces the exact same standard output as the legacy binary for any given string.

Your final executable must be located at `/home/user/project/rle_encoder` and must identically match the output of `/app/legacy_encoder` for any arbitrary alphanumeric input string.