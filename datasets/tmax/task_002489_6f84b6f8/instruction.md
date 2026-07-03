You are a mobile build engineer maintaining the CI/CD pipeline for our company's flagship application. Our pipeline ingests mobile asset bundles (a custom `.mab` format) uploaded by developers, extracts their manifest files using a custom Cgo library, and validates their dependencies before packaging them into the final APK/IPA. 

Recently, the pipeline started crashing or accepting invalid bundles. Your task involves a multi-stage repair and implementation process:

**Stage 1: Fix the Vendored Extraction Library**
Our custom extraction library is vendored at `/app/libmobilemanifest`. It is a Go module that uses Cgo to parse the binary header of `.mab` files and extract the embedded JSON manifest. 
- It currently fails to build due to a misconfigured `Makefile` (it is missing the correct `CGO_CFLAGS` required for our environment) and a memory safety bug in `parser.c` (an off-by-one buffer overflow that causes a segmentation fault when parsing asset headers exactly 32 bytes long).
- Diagnose and fix the C code and the build script so the package compiles and tests pass successfully.

**Stage 2: Build the Validator REST API**
Create a new Go project at `/home/user/validator`. This must be a REST API server running on `localhost:8080` with a single endpoint:
- `POST /validate`
- The endpoint should accept a binary `.mab` file in the raw request body.
- It must use the repaired `libmobilemanifest` library to extract the JSON manifest from the binary `.mab` file.
- It must then parse the JSON manifest and run a constraint satisfaction check. The JSON contains a `provides` array (features this bundle provides) and a `requires` array (features this bundle needs). 
- **Validation Rules:**
  1. The manifest must be valid JSON.
  2. Every feature listed in `requires` MUST be present in the `provides` list of the same manifest (for standalone validation purposes).
  3. The `version` field must follow semantic versioning (`vX.Y.Z`).
- If the bundle is completely valid and satisfies all constraints, the endpoint must return HTTP status `200 OK`.
- If the bundle is invalid (malformed header, invalid JSON, or fails constraints), it must return HTTP status `400 Bad Request`.

**Stage 3: Ensure Resilience Against the Adversarial Corpus**
We have captured a set of `.mab` files from past pipeline runs. They are located at `/app/corpora/clean/` (known good bundles that MUST be accepted) and `/app/corpora/evil/` (malformed, malicious, or constraint-violating bundles that MUST be rejected).
- Ensure your API correctly classifies 100% of the clean bundles as `200 OK` and 100% of the evil bundles as `400 Bad Request`.
- Leave your server running in the background on port `8080` when you are finished. We will test it by sending requests to it.

Start the API server on port 8080 and ensure it is fully operational. Write your API start command to a script at `/home/user/start.sh` so our automated tester can restart it if needed.