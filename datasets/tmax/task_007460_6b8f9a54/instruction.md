You are an open-source maintainer reviewing a broken Pull Request for a web security tool named "GoC-Scanner". The tool is designed to quickly analyze incoming web payloads for known attack signatures. 

To achieve maximum performance, the tool uses a hybrid architecture:
1. A Go frontend (`main.go`) handles concurrent log parsing using goroutines and channels.
2. A C++ backend (`detector.cpp`) handles the heavy lifting of sorting, diffing, and matching payload tokens against known threat signatures via FFI (C bindings / cgo).

The PR author left the repository in a broken state in `/home/user/pr_review`. 
Here is what you need to do:

1. **Fix the C++ FFI code (`detector.cpp`):**
   The PR author attempted to write a function `int detect_threat(const char* payload, const char* signatures)` that takes a space-separated payload string and a newline-separated list of signature strings (where each signature is a space-separated list of tokens). 
   A payload is considered a "threat" if it contains *all* tokens of at least *one* signature. 
   The current implementation in `detector.cpp` has segmentation faults, incorrect sorting/diffing logic, and doesn't properly export the C ABI for Go. Fix it so it correctly identifies threats.

2. **Fix the Build System:**
   Create a `Makefile` in `/home/user/pr_review` that:
   - Compiles `detector.cpp` into a shared library `libdetector.so` (ensure position-independent code).
   - Compiles the Go code into an executable named `scanner` that links against `libdetector.so`. Ensure the build sets the CGO_LDFLAGS properly so it finds the library in the current directory.

3. **Run the tool:**
   The `main.go` reads `payloads.csv` (format: `ID,payload_string`) and `signatures.txt`. It feeds them to the C++ detector concurrently. 
   You must run `./scanner` and pipe its standard output to `/home/user/alerts.txt`.
   The Go program already outputs the IDs of the malicious payloads, but due to concurrency, they are printed out of order. Ensure the final `/home/user/alerts.txt` contains the malicious IDs **sorted numerically** in ascending order, one ID per line.

Do not modify `main.go`, `payloads.csv`, or `signatures.txt`. Your job is to fix the C++ code, write the Makefile, and produce the sorted `/home/user/alerts.txt`.