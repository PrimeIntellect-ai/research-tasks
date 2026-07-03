You are acting as a release manager for a new aerospace calculation service. Your job is to prepare the deployment of a trajectory calculation REST API that relies on a backend C library. Multiple versions of the C library source code exist, and you must build them, determine which version to deploy based on a release manifest, wrap it in a Python REST API, and write mocked tests for it.

Here are the step-by-step instructions:

1. **Compilation and Shared Libraries**:
   You have two C source files provided in `/home/user/src/`:
   - `/home/user/src/mathops_v1.c` (Version 1.0.0)
   - `/home/user/src/mathops_v2.c` (Version 2.1.0)
   
   Compile both C files into shared libraries (`.so`) and place them in `/home/user/libs/` with the names `libmathops.so.1.0.0` and `libmathops.so.2.1.0` respectively. 
   *(Note: Both C files define a function `double calculate_trajectory(double velocity, double angle_radians)`).*

2. **Structured Data and Semantic Versioning**:
   Read the deployment manifest located at `/home/user/release_manifest.json`. It contains a JSON object specifying the version requirements for the "mathops" dependency. 
   Write a Python script that parses this file and uses semantic version rules to determine the highest available version of `libmathops` in `/home/user/libs/` that satisfies the requirement constraint specified in the manifest. 

3. **REST API Construction**:
   Create a Python REST API using FastAPI in `/home/user/api.py`.
   - The API must have a POST endpoint `/api/trajectory` that accepts a JSON payload: `{"v": <float>, "theta": <float>}`.
   - Using Python's `ctypes` module, dynamically load the specific shared library version determined in step 2.
   - The endpoint must call the `calculate_trajectory` function from the shared library with the provided `v` and `theta`, and return a JSON response: `{"distance": <float>, "version_used": "<the_semantic_version_string>"}`.
   - Start the FastAPI server on port `8080` in the background (e.g., using `uvicorn`).

4. **Test Fixtures and Mocks**:
   Create a test suite in `/home/user/test_api.py` using `pytest`.
   - You must test the `/api/trajectory` endpoint without actually calling the C shared library. 
   - Use `unittest.mock` to mock the `ctypes` library function call inside your FastAPI app so it always returns `999.99` for the distance.
   - Run the test suite and output the results in JUnit XML format to `/home/user/test_results.xml`.

5. **Deployment Artifact**:
   Finally, generate a deployment summary file at `/home/user/deployment_summary.json` with exactly this structure:
   ```json
   {
     "selected_version": "X.Y.Z",
     "library_path": "/home/user/libs/libmathops.so.X.Y.Z",
     "api_port": 8080
   }
   ```