You are a developer tasked with debugging a failing data processing build. The project is located in `/home/user/data_processor`. 

The project reads a CSV file containing records (`id`, `name`, `score`), filters for records with a score greater than 50, and calculates the average score of those filtered records. The final average should be written to `/home/user/result.txt`.

However, the current state of the project has several issues:
1. The build is failing. You must fix the `Makefile` so that the code compiles successfully. It is recommended to enable debug symbols.
2. Once compiled, running the executable fails an internal intermediate validation (assertion). You will need to inspect the code and/or use an interactive debugger (`gdb`) to understand why the query results parsed from the CSV do not match expectations, and correct the C++ source code.
3. After fixing the assertion failure, there is another hidden memory/logic bug that causes a crash. Diagnose and fix this bug so the program completes successfully.

Your final goal is to fix the build, fix the C++ code, and successfully run the executable so that it creates the output file `/home/user/result.txt` containing the exact text:
`Average: <calculated_average>`

Requirements:
- Do not modify the data file `/home/user/data_processor/data.csv`.
- The final output file must be located exactly at `/home/user/result.txt`.
- Make sure to clean up any memory if necessary, though the primary success metric is the correct output file.