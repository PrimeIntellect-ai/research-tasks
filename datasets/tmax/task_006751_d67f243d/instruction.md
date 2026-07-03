You are a build engineer responsible for an automated artifact promotion pipeline. The pipeline evaluates the quality of build artifacts using a custom mathematical scoring formula.

Your task is to fix and complete the artifact scoring pipeline located in `/home/user/artifact_pipeline`.

Here is the current state of your workspace:
You have a directory `/home/user/artifact_pipeline` containing:
1. `artifacts.json`: A JSON file containing metrics for several recent build artifacts.
2. `update.patch`: A unified diff file containing recent metric corrections that need to be applied to `artifacts.json`.
3. `formula.txt`: A text file containing a single mathematical expression used to score the artifacts.

Your objectives:
1. **Diff and Patch Processing:** Apply `update.patch` to `artifacts.json` to correct the underlying artifact metrics.
2. **Expression Parsing and Evaluation:** Write a Python script `/home/user/artifact_pipeline/scorer.py`. This script must:
    - Read `formula.txt`. The formula contains basic arithmetic operators (`+`, `-`, `*`, `/`), the exponentiation operator (`^`), parentheses, and variable names that correspond to keys in `artifacts.json`. Note that Python's default `eval` does not natively treat `^` as exponentiation; you must handle the parsing/evaluation of this mathematical expression correctly following standard order of operations.
    - Read the patched `artifacts.json`.
    - Evaluate the formula for each artifact using its metrics.
    - Write the IDs of all artifacts with a calculated score strictly greater than `50.0` to `/home/user/artifact_pipeline/approved.txt`. Each ID should be on a new line.
3. **CI/CD Pipeline Setup:** Create a `Makefile` in `/home/user/artifact_pipeline` with a target named `ci-run`. When `make ci-run` is executed, it must:
    - Apply the patch to `artifacts.json` (if it hasn't been applied yet; ensure this is idempotent or properly sequenced).
    - Run the `scorer.py` script to generate `approved.txt`.

Ensure your Python script works cleanly and relies on standard libraries or explicitly manages its dependencies. The final verification step will run `make ci-run` inside `/home/user/artifact_pipeline` and verify the contents of `approved.txt`.