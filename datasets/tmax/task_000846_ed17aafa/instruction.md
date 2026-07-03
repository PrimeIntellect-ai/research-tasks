You are acting as a Release Manager preparing for a critical deployment of our new hybrid billing microservice. The core calculation logic is written in C for performance, but it needs to be served via a Python gRPC server.

Before you can certify the release, you need to patch a critical bug in the legacy C code, build the shared library, implement the gRPC server wrapper using `ctypes`, and run an end-to-end verification test.

Here is your deployment preparation checklist. Everything must be done in `/home/user/release_prep` (which has already been created and populated with the initial files).

1. **Patch the C Core**
   - The file `/home/user/release_prep/billing_core.c` contains the legacy C logic. It has a bug in the discount calculation.
   - Apply the patch file located at `/home/user/release_prep/discount_fix.patch` to `billing_core.c`.
   - Compile the patched `billing_core.c` into a shared library named `libbilling.so` in the same directory. (Use standard gcc flags for a shared library: `-shared -fPIC`).

2. **Generate gRPC Bindings**
   - We have defined the service in `/home/user/release_prep/billing.proto`.
   - Install the necessary Python gRPC tools.
   - Generate the Python gRPC and Protocol Buffer bindings in `/home/user/release_prep`.

3. **Implement the gRPC Server (`server.py`)**
   - Create `/home/user/release_prep/server.py`.
   - Implement the `BillingService` defined in the protobuf.
   - The server must use Python's `ctypes` to load `libbilling.so`.
   - You will need to design a custom ctypes `Structure` that exactly matches the C `struct LineItem`:
     `struct LineItem { int item_id; double amount; };`
   - The C function signature is `double calculate_total(struct LineItem* items, int count);`
   - Your gRPC `Calculate` RPC must extract the items from the protobuf request, convert them into a contiguous array of your custom ctypes structures, pass the array and the count to `calculate_total`, and return the result in the gRPC response.
   - Start the server on `localhost:50051`.

4. **Run the Verification Test (`verify_release.py`)**
   - Create a test script `/home/user/release_prep/verify_release.py`.
   - The script should connect to the gRPC server on `localhost:50051`.
   - It must construct a request with the following three items exactly in this order:
     - item_id: 1, amount: 100.0
     - item_id: 2, amount: 200.0
     - item_id: 3, amount: 300.0
   - Invoke the `Calculate` RPC.
   - Write the final calculated total to `/home/user/release_prep/deployment_verification.log` in the format: `FINAL_TOTAL: <value>` (e.g., `FINAL_TOTAL: 123.45`).

Please execute these steps, run the server in the background, run your verification script, and ensure the log file is created with the correct final result.