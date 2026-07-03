You are a platform engineer responsible for maintaining your company's custom CI/CD pipeline orchestrator. Recently, several pipeline builds have been failing before they even start because of cyclic dependencies in the pipeline definitions and mismatched tool version requirements. 

Your task is to build an analysis tool to parse the pipeline definitions, detect cycles, and validate semantic versions using a mocked API.

The pipeline definitions are stored as JSON files in `/home/user/pipeline_defs/`. Each JSON file represents a CI task and has the following schema:
```json
{
  "name": "task_name",
  "depends_on": ["other_task_name"],
  "requires": {
    "tool_name": ">=1.0.0, <2.0.0"
  }
}
```

Write a Python script at `/home/user/pipeline_analyzer.py` that does the following:
1. **Dependency Analysis:** Parses all `.json` files in `/home/user/pipeline_defs/`. It must build a dependency graph and detect if there is a cycle (e.g., A depends on B, B depends on C, C depends on A).
2. **Cycle Reporting:** If a cycle is detected, write the exact cycle path to `/home/user/cycle_report.txt`. Format the output as a string of names separated by ` -> `. The cycle should start with the lexicographically smallest task name in the cycle and end with the same task name. (e.g., `task_A -> task_B -> task_C -> task_A`). If no cycle exists, create the file and leave it empty.
3. **Semantic Version Validation:** The script should extract all tool requirements from the `requires` block across all tasks. For each required tool, it must fetch available versions by making an HTTP GET request to `http://registry.internal/api/tools/{tool_name}`. This endpoint returns JSON in the format `{"versions": ["1.0.0", "2.1.0"]}`.
4. **Validation Logic:** A requirement is met ONLY if the *highest available version* returned by the registry satisfies all the version constraints specified in the task using standard semantic versioning rules (PEP 440). Output a newline-separated, alphabetically sorted list of tools that FAIL to meet their requirements into `/home/user/invalid_versions.txt`.
5. **Testing & Mocking:** Because `registry.internal` does not exist in this environment, you must write a test suite at `/home/user/test_analyzer.py` using `pytest`. The test suite must:
    - Mock the `requests.get` function to simulate the registry API.
    - Run the analyzer logic against the files in `/home/user/pipeline_defs/`.
    - Verify that the correct invalid tools are identified.

You may install any required Python packages (such as `pytest`, `requests`, `packaging`) using `pip`.

To complete the task:
1. Ensure the JSON files are properly analyzed.
2. Ensure `/home/user/cycle_report.txt` and `/home/user/invalid_versions.txt` are created with the correct outputs.
3. Ensure `/home/user/test_analyzer.py` exists, contains the mocked tests, and passes when run with `pytest`.