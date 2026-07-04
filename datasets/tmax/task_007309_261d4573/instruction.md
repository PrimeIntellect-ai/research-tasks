You are a developer taking over a mathematical parser project. The project files are currently dumped in the home directory (`/home/user`), and there are a few issues to resolve:

1. **Fix a state bug:** `/home/user/parser.py` contains a Reverse Polish Notation (RPN) parser class (`RPNParser`). There is a bug where state is improperly shared across instances, causing sequential parses or multiple instances to fail. Fix the parser so that each instance manages its state independently.

2. **Implement test with mock:** `/home/user/test_parser.py` contains a test suite. Implement the `test_file_read` method. You must use `unittest.mock.patch` with `mock_open` to mock `builtins.open`. The mock should simulate reading a file named `data.txt` which contains the string `"2 3 + 4 *"`. The test should read this mock file, pass the contents to a new `RPNParser` instance, and assert that the result is `20`.

3. **Organize project files:** Create a proper project structure. 
   - Create the directory `/home/user/math_project`.
   - Move `parser.py` to `/home/user/math_project/src/parser.py`.
   - Move `test_parser.py` to `/home/user/math_project/tests/test_parser.py`.
   - Create empty `__init__.py` files in both the `src` and `tests` directories.

4. **Test execution:** Create a bash script at `/home/user/run_tests.sh` that does the following:
   - Changes the current directory to `/home/user/math_project`.
   - Exports `PYTHONPATH=src`.
   - Runs the tests using `python3 -m unittest discover -s tests`.
   - Redirects both standard output and standard error to `/home/user/test_results.log`.

Make sure `/home/user/run_tests.sh` is executable and run it to produce the log file.