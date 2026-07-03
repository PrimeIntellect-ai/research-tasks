We are migrating our dependency resolution tool from Go to C++ to squeeze out more performance, and we need your help to extract the latest test dataset from a corrupted archive visualization and build the optimized C++ version.

Here is what you need to do:
1. **Extract the Dataset**: There is a video file at `/app/signal.mp4`. This video encodes a binary stream via its frames (a completely black frame represents `0`, and a completely white frame represents `1`). The video runs at 30 FPS. Extract the binary sequence from the frames in order, and decode every 8 bits into an ASCII character. Save the decoded text to `/home/user/dataset.txt`. This file contains a list of semantic version constraints (e.g., `pkgA>=1.2.0,<2.0.0`).

2. **Translate and Optimize**: 
   In `/home/user/resolver.go`, there is a Go program that parses `dataset.txt`, uses goroutines and channels to concurrently process the constraints, compares the semantic versions, and uses a custom graph data structure to find the highest valid version for each package.
   Translate this logic into a highly optimized C++ program at `/home/user/resolver.cpp`. 
   You must implement a custom concurrent data structure in C++ to handle the version interval merging and graph resolution. Your C++ implementation should produce the exact same final resolution output as the Go program.

3. **Output Format**:
   Your C++ program must output the resolved versions to standard output in the format `Package: Version` (one per line, sorted alphabetically by package name).

4. **Performance Goal**:
   Your C++ program will be compiled with `g++ -O3 -pthread -std=c++20 resolver.cpp -o resolver`. It must execute in less than 0.5 seconds on a scaled-up internal dataset (the verification step will test this runtime metric). Ensure your concurrency model and custom data structure are efficient!