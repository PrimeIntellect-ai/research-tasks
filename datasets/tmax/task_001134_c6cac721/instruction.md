I am a researcher organizing a large dataset of hierarchical sensor network readings stored in a nested JSON document format (similar to a NoSQL datastore dump). I need a C program to recursively process this data, aggregate subtree metrics, and output the high-value nodes. 

I've downloaded the source code for the `cJSON` parsing library into `/app/cJSON`, but its `Makefile` seems to be broken. When I try to compile it to a shared library, it fails with a linking error.

Please complete the following steps:
1. Fix the build issue in `/app/cJSON/Makefile` so that running `make` successfully builds the shared library (`libcjson.so`).
2. Write a C program at `/home/user/process_sensors.c` that uses the `cJSON` library to parse `/home/user/sensor_data.json`.
3. The JSON file contains a single root object representing the sensor network. Each object has:
   - `id` (string)
   - `value` (double)
   - `children` (an array of child objects, recursively following the same schema)
4. Your C program must recursively compute the "subtree sum" for every node. A node's subtree sum is its own `value` plus the subtree sums of all its children.
5. The program should identify all nodes where the computed subtree sum is strictly greater than `100.0` and output them to `/home/user/results.csv`.
6. Compile and run your C program, linking against the fixed `cJSON` shared library.

The output file `/home/user/results.csv` must contain lines in the exact format:
`id,subtree_sum`
(Format the subtree sum to 2 decimal places. The order of rows does not matter.)

Ensure your solution is robust. My automated script will evaluate the completeness and accuracy of `/home/user/results.csv` against a hidden ground-truth file.