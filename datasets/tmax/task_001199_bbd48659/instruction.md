You are tasked with setting up a custom, polyglot build system from scratch in a Linux environment. You will write a Python-based build orchestrator that resolves task dependencies and executes a build pipeline, which includes generating code across multiple languages (Python and C).

You must complete the following steps:

1. **Workspace Initialization**:
   Create a directory at `/home/user/polybuild`. All your work will be done inside this directory.

2. **Code Translation Script (`translator.py`)**:
   Write a Python script at `/home/user/polybuild/translator.py`. This script must read a JSON file located at `/home/user/polybuild/schema.json` (which will contain data structure definitions) and translate it into both C and Python data structures.
   
   The `schema.json` format will strictly be a dictionary mapping a struct/class name to a dictionary of fields and their types (only `string` and `int`).
   Example `schema.json`:
   ```json
   {
     "Person": {
       "name": "string",
       "age": "int"
     }
   }
   ```
   
   Your `translator.py` must deserialize this JSON and generate two files:
   - `/home/user/polybuild/generated_schema.py`: Should contain Python `dataclasses` equivalent to the schema. A `string` becomes `str` and `int` becomes `int`.
   - `/home/user/polybuild/generated_schema.h`: Should contain C `typedef struct` definitions equivalent to the schema. A `string` becomes `char*` and `int` becomes `int`.

3. **Build Orchestrator (`builder.py`)**:
   Write a Python script at `/home/user/polybuild/builder.py`. This script must read a build definition file located at `/home/user/polybuild/build.json`. 
   
   The `build.json` file will contain a dictionary of tasks, their dependencies, and bash commands to run:
   ```json
   {
     "tasks": {
       "task_name": {
         "deps": ["dependency_task1"],
         "cmd": "echo 'running'"
       }
     }
   }
   ```
   Your orchestrator must parse this JSON, build a Directed Acyclic Graph (DAG) of the tasks, and perform a topological sort to resolve the correct execution order. 
   It must then execute the commands (`cmd`) using the `subprocess` module in the resolved order.
   As it executes each task, it must append the name of the executed task to a log file at `/home/user/polybuild/execution_log.txt` (one task name per line).
   If there is a tie in topological order, resolve it alphabetically by task name.

4. **Testing Data Setup**:
   Create the following files to test your build system:
   - `/home/user/polybuild/schema.json`: Use the `Person` example provided in Step 2.
   - `/home/user/polybuild/main.py`: A script that imports `Person` from `generated_schema`, creates an instance `Person(name="Alice", age=30)`, and prints "Python: Alice is 30".
   - `/home/user/polybuild/main.c`: A C program that includes `"generated_schema.h"`, creates a `Person` struct with `name="Bob"` and `age=25`, and prints "C: Bob is 25".
   - `/home/user/polybuild/build.json`: Create a build configuration with the following tasks:
     - `translate`: runs `python3 /home/user/polybuild/translator.py` (deps: none)
     - `compile_c`: runs `gcc /home/user/polybuild/main.c -o /home/user/polybuild/main_c` (deps: `translate`)
     - `run_c`: runs `/home/user/polybuild/main_c > /home/user/polybuild/c_out.txt` (deps: `compile_c`)
     - `run_py`: runs `python3 /home/user/polybuild/main.py > /home/user/polybuild/py_out.txt` (deps: `translate`)
     - `combine`: runs `cat /home/user/polybuild/c_out.txt /home/user/polybuild/py_out.txt > /home/user/polybuild/final_output.txt` (deps: `run_c`, `run_py`)

5. **Execution and Serving**:
   - Run your orchestrator: `python3 /home/user/polybuild/builder.py`
   - Start a background Python HTTP server on port `8080` serving the `/home/user/polybuild` directory.

The system will verify the correctness of your topological sort via `execution_log.txt`, the generated code via `generated_schema.py` and `.h`, the output in `final_output.txt`, and ensure the HTTP server is running.