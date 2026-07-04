You are an engineer tasked with setting up a hybrid C and Python polyglot build system from scratch. Your goal is to write the code, fix an underlying memory leak, and create a build script that satisfies specific conditional build constraints and memory debugging requirements.

All files must be created in the `/home/user/polyglot` directory.

1. **The C Library (`libseq.c`)**
Create a file `/home/user/polyglot/libseq.c` based on the following buggy implementation. You must fix the memory leak present in this code:
```c
#include <stdlib.h>

// Computes a sequence: result[i] = (i * 2) + 1
int* compute_sequence(int n) {
    int* temp = malloc(n * sizeof(int));
    int* result = malloc(n * sizeof(int));
    for(int i = 0; i < n; i++) {
        temp[i] = i * 2;
    }
    for(int i = 0; i < n; i++) {
        result[i] = temp[i] + 1;
    }
    // TODO: Fix the memory leak here
    return result;
}

void free_sequence(int* seq) {
    free(seq);
}
```

2. **The C Memory Test (`test_mem.c`)**
Write a simple C program `/home/user/polyglot/test_mem.c` that includes `libseq.c` (or declares its functions), calls `compute_sequence(100)`, frees the resulting sequence, and exits cleanly. This will be used for memory profiling.

3. **The Python Verifier (`verify.py`)**
Write a Python script `/home/user/polyglot/verify.py` that uses the `ctypes` module to load `./libseq.so`. 
- It must call `compute_sequence(5)`.
- It must verify the output sequence is exactly `[1, 3, 5, 7, 9]`.
- It must call `free_sequence` to clean up the memory.
- If the output is correct, print `VERIFICATION_PASSED` to standard output. If incorrect, exit with a non-zero status.

4. **The Build Script (`build.sh`)**
Write a bash script `/home/user/polyglot/build.sh` that orchestrates the entire process. It must satisfy these constraints:
- Must have executable permissions.
- Must conditionally compile `libseq.c` into a shared library `libseq.so` based on the `BUILD_MODE` environment variable:
  - If `BUILD_MODE=PROD`, compile with `gcc -shared -fPIC -O3 -DNDEBUG libseq.c -o libseq.so`.
  - If `BUILD_MODE=DEBUG`, compile with `gcc -shared -fPIC -g -O0 libseq.c -o libseq.so`.
  - If `BUILD_MODE` is unset or any other value, default to `DEBUG`.
- Must compile `test_mem.c` into an executable called `test_mem` (link with your shared object or compile together, ensure it runs).
- Must execute `valgrind --error-exitcode=1 --leak-check=full ./test_mem`. If valgrind detects *any* memory leaks, the build script must immediately exit with code 1.
- Must run `python3 verify.py`.
- If all steps succeed, it must create a file `/home/user/polyglot/build_report.txt` containing exactly the string: `ALL_SYSTEMS_GO`.

Do not install any new packages; assume `gcc`, `valgrind`, and `python3` are already installed. You can start by creating the directory and files.