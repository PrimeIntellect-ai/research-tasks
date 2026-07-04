I have a Python utility in `/home/user/log_processor` that parses application logs using a state machine. It works fine when I run it on a single file, but our CI test suite is failing. 

The tests pass individually, but when the entire suite runs, it fails due to state leaking between tests because the parser relies on global variables for its state machine. 

Your tasks:
1. **Refactor the Parser**: Edit `/home/user/log_processor/parser.py`. Encapsulate the global variables (`CURRENT_STATE` and `PARSED_DATA`) and the `parse_line(line)` function into a class named `LogParser`. The class should initialize `self.current_state = "IDLE"` and `self.parsed_data = []`. Modify `parse_line` to be a method of this class, using instance attributes instead of globals.
2. **Fix the Tests**: Update `/home/user/log_processor/tests/test_start.py` and `/home/user/log_processor/tests/test_stop.py` to instantiate `LogParser` and use its `parse_line` method, ensuring each test uses a fresh instance.
3. **Packaging Script**: Create a bash script at `/home/user/package.sh` that does the following in order:
   - Creates a Python virtual environment at `/home/user/venv`.
   - Activates the virtual environment.
   - Installs `pytest`.
   - Runs `pytest` on the `/home/user/log_processor/tests/` directory.
   - If the tests pass, creates a tarball named `/home/user/log_processor.tar.gz` containing the `log_processor` directory.
   - The script must exit with code 0 on success, or a non-zero code if tests fail.

Ensure `/home/user/package.sh` is executable. You can test your script to ensure the CI pipeline will pass.