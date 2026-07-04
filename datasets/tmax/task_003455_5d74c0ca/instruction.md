You are helping a developer organize and test a polyglot project. The project currently contains a legacy data processing worker written in Go, and we are migrating some parts to Python while keeping the Go binaries for specific target environments.

You need to perform the following steps:

1. **Code Translation (Go to Python)**
   In `/home/user/project/src/`, there is a file named `worker.go`. It implements a concurrent file word-counter using Go's concurrency patterns (a worker pool using goroutines and channels). 
   Write a Python equivalent named `/home/user/project/py_worker.py` that replicates this logic exactly. It must take a directory path as a command-line argument, process all `.txt` files in that directory concurrently using a thread pool and queues (mimicking the worker pool and channels), and print the total word count in the exact same format as the Go script: `Total words: <count>`.

2. **Polyglot Build Orchestration & Cross-Compilation**
   Write a Python script named `/home/user/project/test_orchestrator.py` that automates the build and testing process. This script must:
   - Compile `worker.go` for Linux (`GOOS=linux`, `GOARCH=amd64`).
   - Compile `worker.go` for Windows (`GOOS=windows`, `GOARCH=amd64`).
   - Organize the resulting binaries into a newly created build directory structure:
     - The Linux binary must be moved to `/home/user/project/build/linux/worker`
     - The Windows binary must be moved to `/home/user/project/build/windows/worker.exe`
   
3. **Automated Testing**
   Extend `/home/user/project/test_orchestrator.py` to test both implementations. It should:
   - Run the compiled Linux Go binary on the directory `/home/user/project/data/`.
   - Run your `py_worker.py` on the directory `/home/user/project/data/`.
   - Compare the standard outputs of both executions.
   - If both outputs match exactly, the script must create a file at `/home/user/project/test_result.log` containing the exact line: `TEST PASSED: <output>` (e.g., `TEST PASSED: Total words: 42`). If they do not match, write `TEST FAILED`.

Once you have written `py_worker.py` and `test_orchestrator.py`, execute your orchestrator script so that the directories are organized, binaries are compiled, and the final `test_result.log` is generated.