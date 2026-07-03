You are an open-source maintainer reviewing a pull request for a mathematical C utility called `fast-det`, located in `/home/user/fast-det`. This tool calculates the determinant of square matrices. 

The contributor's PR introduced a new recursive determinant algorithm, but it completely broke the build and test pipeline. It's reminiscent of a messy dependency conflict, but here it's due to broken linking, missing header imports, and a broken Bash test orchestrator.

Your task is to fix the repository so that the build succeeds and all tests pass.

Here is what you need to do:
1. **Fix the Makefile:** The `Makefile` in `/home/user/fast-det/Makefile` is failing to compile and link the project. It is missing the necessary flags to link the standard math library, and it has a broken rule for generating the executable `./fast-det`.
2. **Fix the C Code:** The compiler will complain about implicit function declarations in `/home/user/fast-det/src/determinant.c`. Find the missing standard header and add it.
3. **Repair the Test Orchestrator:** The bash script `/home/user/fast-det/tests/test_runner.sh` is supposed to parse the structured test data in `/home/user/fast-det/tests/cases.csv`. The CSV format is `id,size,flattened_matrix_elements,expected_determinant` (elements are space-separated). The script has a bug in how it parses the CSV using `awk`/`cut` and handles the loop. Fix the Bash script so it correctly extracts the size and elements, passes them to `./fast-det <size> <elements...>`, and compares the integer output to the expected determinant.
4. **Generate the Report:** The bash script must output a final report to `/home/user/pr_summary.json` exactly in this format once it finishes running all test cases:
```json
{
  "passed": <number_of_passed_tests>,
  "failed": <number_of_failed_tests>,
  "total": <total_tests>
}
```

Constraints:
- Do not change the logic of the determinant calculation itself, only fix the compilation errors.
- Ensure the `Makefile` builds the target `fast-det` in the root of the project directory.
- The `test_runner.sh` script must be written primarily in Bash and correctly handle the CSV parsing.