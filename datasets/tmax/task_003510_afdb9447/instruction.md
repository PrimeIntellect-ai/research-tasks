You are a Data Scientist tasked with building a high-performance C++ real-time inference and data cleaning microservice for a sensor network. 

The system receives raw sensor data that frequently contains missing values and outliers. Your task is to clean this data, process it through a small mathematical model, and serve the results via an HTTP API.

Part 1: Fix the Vendored Math Library
We have a proprietary linear algebra library vendored at `/app/tinyml`. Unfortunately, the provided `Makefile` contains an intentional configuration error that prevents it from building on our current system, throwing compilation errors related to unsupported modern C++ features.
1. Navigate to `/app/tinyml`.
2. Diagnose and fix the build configuration issue in the `Makefile`.
3. Compile the library so that `libtinyml.a` is successfully built.

Part 2: Build the Inference API Service
You need to write a C++ HTTP service. You may use the single-header libraries provided at `/app/httplib/httplib.h` and `/app/json/json.hpp`.

Create your server application at `/home/user/server.cpp`. It must implement the following specification:
1. Listen on `127.0.0.1:8080`.
2. Expose a `POST` endpoint at `/infer`.
3. Protect the endpoint by requiring the exact HTTP header: `Authorization: Bearer super-secret-ds-token`. Reject unauthorized requests with a `401 Unauthorized` status.
4. Accept a JSON payload containing an array of exactly 5 floats under the key `"features"`. Example: `{"features": [2.0, 4.0, -9999.0, 100.0, 6.0]}`.

Part 3: Data Cleaning & Inference Logic
Inside your `/infer` handler, implement the following pipeline:
1. **Missing Value Imputation**: Missing values are hardcoded as `-9999.0`. Calculate the mean of the *valid* features (excluding `-9999.0`). Replace any `-9999.0` with this mean.
2. **Outlier Clipping**: Compute the standard deviation of the original *valid* features. Define boundaries as `mean ± (2 * stddev)`. Clamp all features (including the newly imputed ones) to these boundaries. If a value exceeds the upper bound, set it to the upper bound; if below the lower bound, set it to the lower bound.
3. **Inference**: Use the `tinyml::dot_product` function from the fixed `/app/tinyml` library to calculate the dot product of your cleaned 5-element feature vector and the fixed weight vector: `[0.2, 0.8, -0.5, 1.0, 0.1]`.
4. Return a JSON response with status `200 OK` containing the cleaned vector and the prediction. Format: `{"cleaned": [f1, f2, f3, f4, f5], "prediction": p}`.

Part 4: Deployment
Write a bash script at `/home/user/run_server.sh` that compiles your `server.cpp` (statically linking `libtinyml.a` and including the necessary paths) and runs the server in the background. Execute this script so the server is listening when you finish.