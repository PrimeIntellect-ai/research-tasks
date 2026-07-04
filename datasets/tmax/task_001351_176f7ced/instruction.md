You are a systems programmer debugging a local environment issue that causes a CI pipeline to fail due to dynamic library versioning conflicts. 

You have an incoming data file at `/home/user/data/requests.csv` with the old schema format: `timestamp,user_id,value`.
You need to process this file using a C program, but the CI environment has multiple versions of a shared math library, and linking against the wrong one causes runtime errors or incorrect mathematical outputs.

Write a bash script at `/home/user/run.sh` and a C program at `/home/user/process.c` that accomplish the following:

1. **Semantic Version Comparison (Bash)**: 
   In `/home/user/run.sh`, inspect the directory `/home/user/libs/`. It contains several shared libraries named `libmathops-<X>.<Y>.<Z>.so`. Find the library with the highest semantic version that is strictly less than `2.0.0` (i.e., the highest `1.x.x` version).

2. **Compilation**: 
   Your script must compile `/home/user/process.c` into an executable named `/home/user/process`. 

3. **Execution & Dynamic Loading (C)**:
   The script should execute `./process`, passing the absolute path to the selected shared library as the first argument, and the path to the data file (`/home/user/data/requests.csv`) as the second argument.
   Inside `/home/user/process.c`, use `dlopen` to load the library and `dlsym` to extract the function pointer for `int process_value(int)`.

4. **Request Validation & Rate Limiting (C)**:
   Read the CSV file line by line. 
   - *Validation*: Only accept lines where `value` is a strictly positive integer (`> 0`).
   - *Rate Limiting*: Process a maximum of 2 valid requests per `user_id`. Discard any further valid or invalid requests from a user once they have had 2 valid requests processed. Assume `user_id` is an integer between 1 and 100.

5. **Schema Migration (C)**:
   For each accepted request, pass the `value` to the `process_value` function. 
   Write the result to `/home/user/output.jsonl`. Each processed request must be written as a JSON object on a new line in the exact format:
   `{"uid": <user_id>, "result": <computed_value>}`

Ensure your script `/home/user/run.sh` is executable and can be run without arguments to produce the final `output.jsonl` file.