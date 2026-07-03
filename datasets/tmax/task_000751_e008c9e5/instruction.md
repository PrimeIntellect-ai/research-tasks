You are a data analyst building a high-performance C++ engine that translates NoSQL JSON aggregation pipelines into SQL operations to query a massive dataset of CSV files. Before executing any user-provided pipelines, you need to build a robust security filter.

Your task consists of two parts:

Part 1: Fix the Vendored CSV Query Package
We have vendored a third-party C++ package, `libcsvquery` (version 1.2.0), located at `/app/vendor/libcsvquery`. It is required to parse our CSV schemas. However, the package currently fails to build due to a configuration error introduced during vendoring.
1. Inspect the source and build files in `/app/vendor/libcsvquery`.
2. Fix the perturbation so that running `make` successfully produces the static library `libcsvquery.a`.

Part 2: Build the NoSQL Pipeline Sanitizer
Once the library builds, implement a C++ program that validates NoSQL JSON aggregation pipelines to prevent data exfiltration.
Write your program in `/home/user/sanitizer.cpp` and compile it to `/home/user/sanitizer`. 

Your program must accept a single command-line argument: the path to a JSON file containing the pipeline.
It must output exactly `CLEAN` to standard output if the pipeline is safe, and `EVIL` if it violates any of the following security rules:
1. **Path Traversal**: Any `collection` name or `$lookup` target containing `.` or `/`.
2. **Restricted Schemas**: Any `$lookup` or `$match` targeting collections that start with the prefix `private_` or `system_`.
3. **Arbitrary Code Execution**: The presence of any `$where` or `$javascript` keys anywhere in the JSON pipeline.

Compile your program linking against `/app/vendor/libcsvquery/libcsvquery.a`. You may use standard Linux command-line tools to aid your development and testing.

Ensure your binary is executable and outputs *only* `CLEAN` or `EVIL` followed by a newline.