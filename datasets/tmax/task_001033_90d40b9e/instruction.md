You are acting as a Release Manager preparing for a new deployment. You have received a binary manifest file containing the configuration of several microservices, but the tooling to process this specific legacy format is broken. 

You need to write a C++ program to parse the manifest, verify its integrity, evaluate semantic version constraints, and determine the final valid set of services to deploy.

The binary manifest is located at `/home/user/deploy.bin`.

### 1. File Format specification
The binary file uses Little-Endian byte order for all multi-byte integers.
*   **Header (4 bytes):** Magic bytes `DPLY` (ASCII).
*   **Record Count (2 bytes):** Unsigned 16-bit integer representing the number of service records.
*   **Records (variable length):**
    *   **Service ID (1 byte):** Unsigned 8-bit integer.
    *   **Version Length (1 byte):** Unsigned 8-bit integer ($L_1$).
    *   **Version String ($L_1$ bytes):** ASCII string (Semantic Versioning format `MAJOR.MINOR.PATCH`).
    *   **Dependency ID (1 byte):** Unsigned 8-bit integer of the required service. `0xFF` means no dependency.
    *   **Min Required Version Length (1 byte):** Unsigned 8-bit integer ($L_2$). (If Dependency ID is `0xFF`, this is `0`).
    *   **Min Required Version String ($L_2$ bytes):** ASCII string (Semantic Version format).
*   **Checksum (4 bytes):** An Adler-32 checksum (unsigned 32-bit integer) covering all preceding bytes in the file (from the magic bytes up to the end of the last record).

### 2. Integrity Verification (Checksum)
Implement the standard Adler-32 checksum algorithm. The initial Adler-32 value is `1`. Verify the calculated checksum against the last 4 bytes of the file. If they do not match, your program should exit with code `1`.

### 3. Constraint Satisfaction & Semantic Versioning
A service can only be deployed if its dependency is satisfied.
*   If a service has a Dependency ID of `0xFF`, it has no dependencies and is initially considered **valid**.
*   If a service depends on another service, it is **valid** ONLY IF:
    1. The required service is present in the manifest.
    2. The required service's version is `>=` the Min Required Version.
    3. The required service itself is also **valid**.
*   Semantic Version comparison should follow standard rules (e.g., `2.0.0` > `1.9.9`, `1.2.1` > `1.2.0`).

*Note:* Constraint resolution must be exhaustive. If Service A depends on Service B, and Service B depends on Service C, if C is removed, B becomes invalid, which means A also becomes invalid.

### 4. Output
Once you have determined the final set of valid services, write their Service IDs in **ascending numerical order**, separated by commas, to `/home/user/valid_deployments.txt` (e.g., `1,2,4`).

Write your code in `/home/user/parser.cpp`, compile it (using `g++ -std=c++17`), and run it. Do not hardcode the expected output; your C++ program must implement the logic.