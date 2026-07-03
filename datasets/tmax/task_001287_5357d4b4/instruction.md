You are an artifact manager for our internal binary repository. We are implementing a custom C++ archiver to append incoming compiled binaries into a single continuous repository file using the Snappy compression algorithm. 

We have vendored the `snappy-1.1.10` source code at `/app/vendor/snappy-1.1.10`. However, the build is currently failing because someone accidentally modified its `CMakeLists.txt` to enforce C++98, which is incompatible with the library's required C++11 standard. 

Here is what you need to do:
1. Fix the `CMakeLists.txt` in the vendored snappy package using standard text utilities so that it uses `C++11` instead of `C++98`, then build and install the library locally to `/home/user/local/`.
2. Write a C++ program at `/home/user/archiver.cpp` that implements an artifact watcher and compressor. It must:
   - Continuously poll the `/home/user/incoming/` directory for new files.
   - When a file appears, read it, and compress it using the snappy library.
   - Acquire an exclusive file lock (`flock`) on the target archive file `/home/user/repo.bin` to ensure concurrent safety (as other processes might be reading it).
   - Append a header consisting of the original filename (null-terminated) followed by an 8-byte unsigned integer representing the compressed data size, and finally append the snappy compressed binary stream.
   - Remove the processed file from the incoming directory.
3. Compile your program and run it in the background. 
4. We have a test script at `/home/user/trigger_incoming.sh` that will dump 50 large uncompressed binaries into `/home/user/incoming/` simulating concurrent artifact uploads. Run this script.
5. Wait for your archiver to process all 50 files (the incoming directory becomes empty). 

Your success will be measured by the final size of the `/home/user/repo.bin` archive. It must achieve our required compression baseline. Leave the final `repo.bin` on disk for automated verification.