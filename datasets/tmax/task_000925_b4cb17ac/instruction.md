You are a QA engineer tasked with modernizing the end-to-end test orchestration for a legacy Python project. 

The project is located in `/home/user/qa_project`. It currently has a broken build configuration (`pyproject.toml` has syntax errors and incorrect metadata) that prevents it from installing locally. 

Additionally, the test orchestrator relies on a proprietary, notoriously slow, stripped binary located at `/app/legacy_resolver`. This binary takes two arguments: a custom semantic version constraint expression and a target version string. It exits with code 0 if the version satisfies the expression, and code 1 otherwise.

Your tasks are:
1. **Fix the Package Setup**: Repair `/home/user/qa_project/pyproject.toml` so the package can be installed in a virtual environment (`python -m pip install .`).
2. **Reverse Engineer the Resolver**: Probe `/app/legacy_resolver` to figure out its custom expression syntax. It supports standard SemVer comparators (e.g., `>=`, `<=`, `=`, `<`, `>`), combined with specific boolean operators (`&&`, `||`) and parentheses for grouping.
3. **Write a Bash Replacement**: Create a highly performant Bash script at `/home/user/semver_match.sh` that implements the same expression parsing and semantic version comparison logic as the binary. It must accept the same arguments (`<expression>` `<version>`) and return the same exit codes. Note: You must write this evaluation logic primarily in Bash, though you can use standard coreutils (awk, sed, etc.).
4. **Update the Orchestrator**: Refactor the end-to-end test script at `/home/user/qa_project/run_e2e_tests.sh` to use your new `semver_match.sh` instead of `/app/legacy_resolver`. 

Your goal is to ensure `semver_match.sh` perfectly mimics the behavior of `/app/legacy_resolver`. An automated suite will test your script against a hidden dataset of complex expressions and versions to calculate its accuracy.