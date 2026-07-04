You have recently inherited an unfamiliar C codebase located at `/home/user/sensor_processor`. It is a data processing daemon that reads sensor data from a CSV file, applies a transformation algorithm, and outputs a new CSV file. 

The previous developer left behind a partially working pipeline. However, there are two major issues you need to debug and fix:
1. **Segmentation Fault:** When running the compiled program on the full production dataset (`/home/user/data/input.csv`), it crashes and produces a core dump.
2. **Precision Loss:** When tested on a smaller dataset before the crash occurs, the output slightly differs from the gold-standard reference data (`/home/user/data/expected_output.csv`). The business logic is conceptually correct, but there is a data-type or mathematical precision issue during the transformation phase.

Your tasks are:
1. Navigate to `/home/user/sensor_processor` and compile the code using the provided `Makefile`. You may need to modify the Makefile to include debugging symbols (`-g`) to analyze the core dump.
2. Run the program with `/home/user/data/input.csv` and analyze the resulting core dump/stack trace to identify and fix the root cause of the crash in `main.c`.
3. Once the crash is fixed, run the program again. Compare its output (`/home/user/data/output.csv`) against `/home/user/data/expected_output.csv`. Use diffing tools to spot the discrepancies.
4. Identify the precision loss bug in the data transformation logic within `main.c` and fix it.
5. Recompile and run the tool to generate the completely correct output. Rename the final, perfect output to `/home/user/data/final_output.csv`.
6. Create a file named `/home/user/debug_report.txt` with exactly two lines:
   - Line 1: The name of the variable or array that caused the segmentation fault.
   - Line 2: The exact C type (e.g., `int`, `float`, `double`) that was improperly used and caused the precision loss.

Execution Details:
- The executable is expected to take two arguments: `./sensor_processor <input_file> <output_file>`
- You have access to `gdb`, `valgrind`, and standard Linux diff utilities.