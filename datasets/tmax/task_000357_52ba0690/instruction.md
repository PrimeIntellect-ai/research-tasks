You are tasked with creating a custom Python-based build system for a multi-target project. You need to write a master build script at `/home/user/project/build.py` that handles dependency resolution (constraint satisfaction), conditional cross-compilation, and integrity verification via checksums and parity codes.

Here is the setup:
1. First, create the directory `/home/user/project/src` and `/home/user/project/build`.
2. Inside `/home/user/project`, create a file named `deps.json` with the following content:
```json
{
  "components": {
    "core": [
      {"version": "1.0", "cost": 40},
      {"version": "2.0", "cost": 60}
    ],
    "net": [
      {"version": "1.0", "cost": 30},
      {"version": "2.0", "cost": 20}
    ],
    "ui": [
      {"version": "1.0", "cost": 20},
      {"version": "1.1", "cost": 25}
    ]
  },
  "conflicts": [
    {"core": "2.0", "net": "1.0"}
  ]
}
```
3. Create a C source file at `/home/user/project/src/main.c` with the following content:
```c
#include <stdio.h>
int main() {
#ifdef TARGET_ARM
    printf("Architecture: ARM\n");
#else
    printf("Architecture: x86\n");
#endif

#ifdef CORE_V2
    printf("Core: v2\n");
#else
    printf("Core: v1\n");
#endif
    return 0;
}
```

Your script `/home/user/project/build.py` must perform the following three phases sequentially when executed:

**Phase 1: Constraint Satisfaction (Dependency Resolution)**
The script must read `deps.json` and select exactly one version for each of the three components (`core`, `net`, `ui`). 
The selection must satisfy the following constraints:
- The total `cost` of the selected versions must be strictly less than 90.
- It must not violate any rules in the `conflicts` list (e.g., if `core` 2.0 is selected, `net` cannot be 1.0).
- If multiple valid combinations exist, choose the one with the highest total cost that is still strictly less than 90.
Write the selected versions to `/home/user/project/build/resolution.txt` in the format: `component:version` (one per line, sorted alphabetically by component name).

**Phase 2: Conditional Compilation**
Using the `subprocess` module, your Python script must compile `/home/user/project/src/main.c` using `gcc` into two separate binaries in the `/home/user/project/build/` directory:
1. `app_x86`: Compiled with no special target flags.
2. `app_arm`: Compiled with the `-DTARGET_ARM` flag (simulating a cross-build).

Additionally, if the resolved version of the `core` component is `2.0`, you must pass the `-DCORE_V2` flag to GCC for BOTH binaries.

**Phase 3: Integrity and Error-Correcting Parity**
Your script must calculate the SHA-256 hash of both generated binaries (`app_x86` and `app_arm`). 
Then, it must calculate a "Parity Checksum" to ensure manifest integrity. The Parity Checksum is a single byte (represented as a 2-character hex string) calculated by taking the XOR sum of all the individual bytes of the raw binary SHA-256 digests of both files combined (i.e., XORing all 64 bytes together - 32 bytes from the first hash and 32 bytes from the second).

Write a manifest file to `/home/user/project/build/manifest.txt` with exactly this format:
```
app_arm:<sha256_hex_of_app_arm>
app_x86:<sha256_hex_of_app_x86>
PARITY:<2_char_hex_of_xor_sum>
```

Run your `build.py` script so that all outputs are generated.