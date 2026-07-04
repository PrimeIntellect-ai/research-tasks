You are a security researcher analyzing a suspicious binary. You have discovered a C source file `/home/user/vuln_parser.c` and an input payload `/home/user/payload.bin`. 

The binary `vuln_parser` crashes intermittently when processing `payload.bin`. Your investigation suggests this is due to uninitialized memory on the heap. 

Your tasks are to:
1. **Reproduce the intermittent failure reliably:** Identify the standard glibc environment variable used to poison/initialize `malloc` allocations with a specific byte pattern. Figure out which byte value forces the crash to happen 100% of the time. Write the name of this environment variable (just the variable name, e.g., `SOME_ENV_VAR`) into `/home/user/env_var.txt`.
2. **Trace the intermediate state:** Determine the exact integer value of the `state_counter` variable on the precise line and moment where the null-pointer dereference (the crash) is triggered. Write this integer value into `/home/user/trace.txt`.
3. **Construct a regression test:** Create a bash script at `/home/user/regression.sh` that reliably reproduces the crash. The script must execute `./vuln_parser payload.bin` with the correct environment variable set to the correct value to force the crash. The script should exit with `0` if the program correctly terminates with a Segmentation Fault (exit code 139), and exit with `1` if it does not crash or exits with any other code.

**Setup Instructions:**
Assume the following files exist in `/home/user/`:

`vuln_parser.c`:
```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int process_data(const char *filename) {
    FILE *f = fopen(filename, "rb");
    if (!f) return -1;

    int state_counter = 0;
    char *buf = malloc(32); // Uninitialized heap allocation
    fread(buf, 1, 16, f);

    for (int i = 0; i < 16; i++) {
        if (buf[i] == 'A') {
            state_counter++;
        }
        if (buf[i] == 'X') {
            // Suspicious logic: uses uninitialized memory past index 16
            if (buf[i + 16] == (char)0xFF) {
                // Trigger artificial crash
                char *crash = NULL;
                *crash = 1;
            }
        }
        state_counter += 2;
    }

    free(buf);
    fclose(f);
    return state_counter;
}

int main(int argc, char **argv) {
    if (argc < 2) return 1;
    process_data(argv[1]);
    return 0;
}
```

The `payload.bin` file contains exactly 16 bytes. The first 5 bytes are `AAA_X`, followed by 11 null bytes (`\x00`).

Compile the binary using:
`gcc -g -o vuln_parser vuln_parser.c`

Ensure all your output files (`env_var.txt`, `trace.txt`, `regression.sh`) are created in `/home/user/` and that `regression.sh` is executable.