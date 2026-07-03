You are a platform engineer maintaining a CI/CD pipeline for a high-performance data processing service. The pipeline is currently failing because the primary analytics microservice, written in C, has broken builds, missing protocol definitions, and memory corruption issues (Undefined Behavior).

Your task is to fix the service, make it compile, ensure it is memory-safe, and process a batch of test data.

The workspace is located at `/home/user/analytics_service`. 

Here is what you need to do:

1. **Protobuf Service Design**:
   Create a protobuf definition file at `/home/user/analytics_service/schema.proto`.
   It must use `proto3` syntax.
   Define a message named `DataBatch`.
   It must contain a single field: a repeated list of `double` values named `samples` with field number 1.

2. **Fix the C Code (`compute.c`)**:
   The file `/home/user/analytics_service/compute.c` contains the logic to read a binary serialized `DataBatch` file, deserialize it using `protobuf-c`, and compute the sample mean and sample variance using Welford's online algorithm.
   However, the code currently has several issues:
   - It contains memory safety bugs (Undefined Behavior like out-of-bounds access and memory leaks). 
   - It lacks proper error handling for empty batches or batches with only 1 sample (which makes sample variance undefined; in such cases, variance should be printed as `0.000000`).
   Fix the C code so that it is strictly memory safe (no leaks, no UB) and correctly implements the mathematical algorithm. The program takes the binary file path as `argv[1]`.

3. **Fix the Build System (`Makefile`)**:
   The `/home/user/analytics_service/Makefile` is incomplete and broken. 
   Modify it so that running `make` will:
   - Compile `schema.proto` into C source files using `protoc-c`.
   - Compile `compute.c` and the generated protobuf-c files into an executable named `analytics_engine`.
   - Link the necessary libraries (`-lprotobuf-c` and the math library).

4. **Run the Pipeline**:
   There is a test data generator script at `/home/user/analytics_service/generate_test_data.py`. Run it to produce `test_batch.bin` (this script uses the standard python `protobuf` library, which requires you to compile the `schema.proto` for Python as well: `protoc --python_out=. schema.proto`).
   Then, run your fixed compiled C program: `./analytics_engine test_batch.bin > /home/user/result.txt`.

The output written to `/home/user/result.txt` must strictly follow this exact format:
```
Mean: <mean_value_formatted_to_6_decimal_places>
Variance: <variance_value_formatted_to_6_decimal_places>
```