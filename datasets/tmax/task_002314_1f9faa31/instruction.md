You have been given access to a fragmented, polyglot monorepo located at `/home/user/monorepo`. The monorepo consists of several independent sub-projects written in C++ and Python. The build system that used to manage these projects has been lost, and your task is to write a replacement build orchestrator and data aggregator.

Inside `/home/user/monorepo`, there are several subdirectories. Every valid sub-project contains a `manifest.json` file. 

The `manifest.json` has the following schema:
```json
{
  "name": "<project_name>",
  "deps": ["<dependency_project_name>", ...],
  "build_steps": [
    "<shell_command_1>",
    "<shell_command_2>"
  ]
}
```

Your objective is to:
1. Parse all the `manifest.json` files in the monorepo.
2. Resolve the dependency graph to determine the correct build order (topological sort). A project can only be built after all of its `deps` have been successfully built.
3. Orchestrate the polyglot build by executing the `build_steps` for each project in the correct order. You must execute these commands from within the respective project's subdirectory.
4. Every successful project build will generate an `output.json` file in its subdirectory. Once all builds have completed successfully, parse every generated `output.json` file.
5. Transform and combine this data into a single file located at `/home/user/final_report.json`. The final report must be a JSON object where the keys are the project names (as defined in their manifest) and the values are the parsed JSON objects from their respective `output.json` files.

Constraints & Notes:
- Write your build orchestrator script in `/home/user/orchestrator.py` and run it.
- Do not hardcode the project names or the build order; your script must dynamically traverse the directories and calculate the dependency graph.
- All builds will succeed if executed in the correct topological order.
- The structure of `/home/user/final_report.json` must exactly match:
  ```json
  {
    "project_a": { ... },
    "project_b": { ... }
  }
  ```