You are an expert systems programmer. We have a multi-language microservice project that is failing to build and produce accurate results.

There is a C math library vendored at `/app/libfastcalc-1.2.3` which is supposed to provide high-performance math routines. We want to wrap this library in a C++ gRPC service and consume it via a Python client. 

However, we are running into several issues:
1. **Linking Issue:** The C library fails to link with our C++ gRPC server. You need to identify why the `Makefile` in `/app/libfastcalc-1.2.3` produces an archive that cannot be linked into a modern C++ gRPC application (hint: position-independent code), and fix the build.
2. **Accuracy Issue:** The `fast_sigmoid_array` function in `fastcalc.c` uses a flawed approximation. You must rewrite this function in C so that the Mean Squared Error (MSE) compared to the true mathematical sigmoid ($1 / (1 + e^{-x})$) is less than $10^{-4}$ for inputs in the range $[-10, 10]$.
3. **gRPC Service Design:** Create a protobuf file at `/home/user/service/calc.proto` defining a service `FastCalc` with two RPCs:
   - `GetVersion`: takes an empty request and returns the semantic version string of the linked C library (which is defined in `fastcalc.h`).
   - `ComputeSigmoid`: takes a message containing repeated double values and returns a message with the repeated double results.
4. **Polyglot Build & Integration:** Implement the gRPC server in C++ (`/home/user/service/server.cc`) that listens on port `50051`. It must include `fastcalc.h`, link against the fixed `libfastcalc.a`, and implement the `FastCalc` service. 
5. **Test Fixture:** Write a Python test script at `/home/user/service/test_client.py` that connects to `localhost:50051`, asserts that the semantic version returned by `GetVersion` is exactly `"1.2.3"`, and sends an array of 10,000 linearly spaced floats from -10.0 to 10.0 to `ComputeSigmoid`.

You must leave the C++ gRPC server running in the background as a process listening on port `50051` when you are finished. Automated tests will query this port to verify the metric threshold (MSE < 1e-4).