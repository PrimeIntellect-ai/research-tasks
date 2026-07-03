You are a QA engineer responsible for setting up a test environment evaluation tool. You have been given a partially complete Go project that evaluates feature configurations dynamically using a shared C library.

However, the project is currently broken. Your goal is to fix the build system, complete the Go application logic, and generate the final configuration report.

Here are the details of your workspace:

1. **The Build Error**: 
   Inside `/home/user/project/`, there is a `Makefile` intended to compile a small C library (`evaluator.c` into `libeval.so`) and then build the Go application. The compilation of the C shared library currently fails due to a linking error (it uses math functions but fails to link the math library properly). You must fix the `Makefile` so that `make` successfully builds `libeval.so` and compiles `main.go` into an executable named `eval_tool`.

2. **The Go Application Logic** (`/home/user/project/main.go`):
   The Go program is missing its core algorithmic logic. You need to implement the following pipeline in Go:
   
   * **Semantic Versioning**: Read the file `/home/user/data/versions.txt`. Parse the semantic versions (which follow SemVer 2.0.0 format) and sort them. Find the **highest** version `V` that satisfies the condition: `V >= 1.2.0` AND `V < 2.0.0`. Note that pre-release versions (e.g., `-alpha`) have lower precedence than their corresponding normal versions.
   
   * **Configuration Merging**: Read `/home/user/data/base.txt` and `/home/user/data/diff_<V>.txt` (where `<V>` is the version string you found). Both files contain configuration rules in the format `KEY=base_value,exponent_value` (e.g., `ALPHA=2.0,3.0`), one per line.
   Merge the configurations: any key present in the `diff` file should override the corresponding key in the `base` file. Any keys unique to either file should be kept.

   * **Expression Evaluation**: For each merged key-value pair, use the provided C library function (via Cgo) `evaluate_power(double base, double exp)` to calculate the result. 

   * **Output**: Produce a JSON file at `/home/user/report.json` containing a single JSON object mapping the string keys to their evaluated numeric results. Use Go's `json.MarshalIndent` with a two-space indent. The keys must be sorted alphabetically.

Ensure your Go program runs without errors. You may need to set `LD_LIBRARY_PATH` appropriately so the Go binary can locate `libeval.so` at runtime. Run your fixed project to generate `/home/user/report.json`.