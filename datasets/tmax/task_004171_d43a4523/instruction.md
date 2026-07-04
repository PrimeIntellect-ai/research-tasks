You are a data analyst setting up a fast C++ pipeline for tabular data processing. We have a third-party CSV parser library vendored on our system, but the previous engineer left it in a broken state. You need to fix the library, write a data processing tool, and ensure it perfectly matches our specification.

Here are the steps to complete this task:

1. **Fix the Vendored Library**:
   The source for `fastcsv` (version 1.0) is located at `/app/fastcsv-1.0/`.
   If you try to run `make` in that directory, it will fail to compile. Identify the configuration error in its `Makefile`, fix it, and build the static library (`libfastcsv.a`).

2. **Implement the Data Processor**:
   Write a C++ program at `/home/user/process.cpp` and compile it to `/home/user/process`.
   Your program must read a CSV file from standard input (`stdin`). 
   The CSV will always have the following header: `id,group,feature_x,feature_y`.
   
   Using the `fastcsv` library, process the incoming data:
   * Read each row (skipping the header).
   * Perform dimensionality reduction on the features by computing a projected score `Z` for each row using the formula: 
     `Z = (0.8 * feature_x) + (0.2 * feature_y)`
   * Aggregate the data by calculating the mean `Z` score for each `group`.

3. **Output Formatting**:
   Print the aggregated results to standard output (`stdout`) in CSV format.
   The output must have a header: `group,mean_z`.
   The rows must be sorted alphabetically by the `group` name.
   The `mean_z` values must be formatted to exactly 3 decimal places (e.g., `12.340`, `-0.005`).

Compile your program so it links against the fixed `/app/fastcsv-1.0/libfastcsv.a` and includes the header `/app/fastcsv-1.0/fastcsv.h`. 
Once compiled to `/home/user/process`, our automated testing framework will fuzz-test your executable against an oracle to ensure identical behavior across random datasets.