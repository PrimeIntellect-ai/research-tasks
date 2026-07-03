You are an AI assistant helping a release manager finalize a deployment preparation tool.

The release manager needs a custom validation tool written in C that parses incoming deployment manifests, enforces resource constraints, and limits the deployment rate of high-risk services.

You need to create a complete project in `/home/user/release_manager/`.

1. **Input Data**: 
Create a file named `/home/user/release_manager/input.b64` containing the following Base64-encoded JSON lines (one per line). These represent the deployment manifests:
```text
eyJzZXJ2aWNlIjogImF1dGgiLCAiY3B1IjogMiwgIm1lbSI6IDQsICJ0aWVyIjogImNyaXRpY2FsIn0=
eyJzZXJ2aWNlIjogInBheW1lbnQiLCAiY3B1IjogMiwgIm1lbSI6IDQsICJ0aWVyIjogImNyaXRpY2FsIn0=
eyJzZXJ2aWNlIjogImxvZ2dpbmciLCAiY3B1IjogMiwgIm1lbSI6IDQsICJ0aWVyIjogInN0YW5kYXJkIn0=
eyJzZXJ2aWNlIjogImJpbGxpbmciLCAiY3B1IjogMiwgIm1lbSI6IDQsICJ0aWVyIjogImNyaXRpY2FsIn0=
eyJzZXJ2aWNlIjogImNhY2hlIiwgImNwdSI6IDgsICJtZW0iOiAxNiwgInRpZXIiOiAic3RhbmRhcmQifQ==
eyJzZXJ2aWNlIjogInNlYXJjaCIsICJjcHUiOiA0LCAibWVtIjogOCwgInRpZXIiOiAic3RhbmRhcmQifQ==
```

2. **Dependency Setup**:
You must download the lightweight `cJSON` library (specifically `cJSON.h` and `cJSON.c` from its standard open-source repository) into `/home/user/release_manager/lib/`. 

3. **C Program Development (`validator.c`)**:
Write a C program named `validator.c` in `/home/user/release_manager/` that does the following:
- Reads the `input.b64` file line by line.
- Implements a custom Base64 decoding function directly in the C code to decode each line into a JSON string.
- Uses `cJSON` to parse the decoded JSON object.
- Validates each manifest against the following global constraints for the target cluster:
  - **Max Total CPU**: 16
  - **Max Total Memory**: 32
  - **Rate Limit / Risk Constraint**: A maximum of exactly 2 services with the `"tier": "critical"` attribute can be accepted in a single batch.
- Iterates sequentially through the lines. If adding a service would cause the running totals to exceed any of the constraints (CPU, Memory, or Critical Tier Count), the service must be **rejected** and its resources NOT added to the running totals. Otherwise, it is **accepted**.
- Writes the `"service"` names of all **accepted** services, in the order they were processed, to a file named `/home/user/release_manager/deploy_plan.txt` (one service name per line).

4. **Unit Testing (`test_validator.c`)**:
Write a basic unit test file `test_validator.c` that compiles against your constraint validation logic. It must run at least two test cases asserting correct constraint math (e.g., verifying a critical service is rejected if 2 criticals are already accepted). Log the test suite output to `/home/user/release_manager/test_results.log`.

5. **Build and Run**:
Create a `Makefile` or bash script to compile the project (linking `validator.c` and `lib/cJSON.c`), run the test suite, and run the main validator tool to generate `deploy_plan.txt`. Execute your build script to ensure all files are created.