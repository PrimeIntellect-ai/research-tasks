You are a release manager preparing the v2.0 deployment of our hybrid Go/C audio processing tool. 

The tool takes an input WAV file, processes it through a C-based audio filter, and outputs a new WAV file. The current implementation in `/home/user/src/` is extremely slow and has several structural issues that need to be fixed before release.

Your objectives:

1. **Shared Library and ABI Management**:
   The C code in `/home/user/src/filter.c` must be compiled into a shared library named `libaudiofilter.so.2.0.1` with a soname of `libaudiofilter.so.2`. Create the appropriate symlinks (`libaudiofilter.so` and `libaudiofilter.so.2`) in `/home/user/lib/`. 

2. **Go Concurrency Optimization**:
   The current Go wrapper `/home/user/src/main.go` processes audio chunks sequentially. Modify `main.go` to use Go concurrency patterns (goroutines and channels) to process the audio chunks in parallel (use at least 4 concurrent workers). 

3. **C Optimization**:
   The `apply_filter` function in `filter.c` contains a deliberately naive and artificially slow nested loop. Refactor this C function so that it correctly applies the filter but executes much faster. The output audio data must remain mathematically identical to the unoptimized version.

4. **Package and Dependency Management**:
   Once compiled and optimized, package the release. Compile the Go program into a binary named `audiotool` that dynamically links to your shared library (ensure the rpath is set to `$ORIGIN/../lib` or similar, so it finds the library when deployed). 
   Create a release tarball at `/home/user/release_v2.tar.gz` containing:
   - `bin/audiotool`
   - `lib/libaudiofilter.so.2.0.1`
   - `lib/libaudiofilter.so.2`
   - `lib/libaudiofilter.so`

5. **Testing**:
   You can test your tool on the provided audio fixture at `/app/release_sample.wav`. 
   Run: `./bin/audiotool /app/release_sample.wav /home/user/output.wav`
   
To pass, the execution time of the optimized packaged tool on the test audio must show a speedup of >= 4.0x compared to a sequential, unoptimized baseline.