You are a QA engineer responsible for setting up and evaluating a multi-language test environment. A previous engineer wrote a test runner that executes benchmarking suites for components written in C, Python, and Go, but left before fixing a bug and completing the parsing logic.

Your tasks are:

1. **Patch the Test Runner**:
   There is a broken test runner script at `/home/user/qa/test_runner.sh` and a patch file at `/home/user/qa/fix_runner.patch`.
   Apply the patch to `test_runner.sh` so it executes properly and outputs the correct block markers.

2. **Generate Benchmark Logs**:
   Execute `/home/user/qa/test_runner.sh` and redirect its standard output to `/home/user/qa/raw_benchmark.log`. 

3. **Build an Awk State Machine Parser**:
   The generated `raw_benchmark.log` contains interleaved output, setup noise, and benchmark data. 
   Write an `awk` script at `/home/user/qa/parser.awk` that implements a state machine to parse this log. 
   
   The log format looks like this (with arbitrary noise lines between blocks):
   ```
   [NOISE] Initializing tests...
   >>> START COMPONENT: <component_name>
   [NOISE] Warming up JIT...
   Iteration: 12ms
   Iteration: 14ms
   <<< END COMPONENT
   ```
   
   Your `awk` state machine must:
   - Identify when a component block starts (`>>> START COMPONENT: <component_name>`).
   - Transition into a state to sum all the execution times (the integer value before `ms`) on lines starting with `Iteration: `.
   - Transition out of the state when it sees `<<< END COMPONENT`.
   - Ignore all lines outside of these blocks, and ignore any noise lines inside the blocks.
   
4. **Generate the Final Report**:
   Run your parser against the log file and save the output to `/home/user/qa/final_report.txt`.
   The output must have exactly one line per component in the exact order they appeared in the log, formatted as:
   `<component_name>_TOTAL:<summed_milliseconds>ms`

For example:
```
C_App_TOTAL:26ms
Python_App_TOTAL:105ms
```

Do not include any other text in `/home/user/qa/final_report.txt`. Ensure all files are placed exactly at the specified absolute paths.