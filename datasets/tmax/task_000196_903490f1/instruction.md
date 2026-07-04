You are a build engineer responsible for an internal artifact management tool written in Go. The project is located at `/home/user/manager`. The tool is supposed to calculate a custom mathematical signature for a set of artifact files, serve the metadata via a REST API, and provide a build script to automate the deployment. However, the current codebase is broken and incomplete.

Your task is to fix the application, build it, run it, and generate a final manifest.

Here are the requirements:

1. **Fix the Numerical Algorithm**: 
   In `/home/user/manager/algo/algo.go`, implement the `CalculateSignature(data []byte) uint32` function. The signature is defined as the sum of `uint32(byte_value) * uint32(index + 1)` for each byte in the data (where index starts at 0 for the first byte). The final sum must be modulo `1000003`.

2. **Complete the REST API & Serialization**:
   In `/home/user/manager/api/api.go`, implement the HTTP handler for the `/manifest` endpoint. It must return an HTTP 200 OK with a JSON payload representing a map of filenames (strings) to their calculated signatures (uint32). The response `Content-Type` must be `application/json`.

3. **Fix the Build Process**:
   The `/home/user/manager/build.sh` script is currently broken. Fix it so that it correctly initializes a Go module named `manager`, formats the code, and builds an executable named `artifact-server` in the `/home/user/manager` directory.

4. **Execution and Verification**:
   - Run the fixed `build.sh` script.
   - Start the compiled `artifact-server` in the background. It will automatically read the `.bin` files in `/home/user/manager/artifacts` and listen on port `8080`.
   - Make an HTTP GET request to `http://localhost:8080/manifest` and save the exact JSON response to `/home/user/final_manifest.json`.

Ensure the final JSON file is correctly formatted and contains the right calculated signatures for the provided artifacts.