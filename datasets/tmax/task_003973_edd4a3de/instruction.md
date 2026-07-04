You are an open-source maintainer reviewing a broken Pull Request. A contributor submitted a PR to your Python project that parses a custom configuration format and transforms it into structured data. They added a feature to interpolate environment variables but broke the core parsing logic and failed to include property-based tests.

Your task is to fix the code, implement dependency management, write property-based tests, and output a final parsed JSON file.

Here is the situation:
The repository is located at `/home/user/sysconf_parser`. 
Inside, there is a broken parser script at `/home/user/sysconf_parser/parser.py` and a sample configuration at `/home/user/sysconf_parser/example.conf`.

The configuration format is simple:
- One key-value pair per line separated by `=`.
- The first `=` on a line separates the key from the value (values can contain `=` characters).
- Lines starting with `#` are comments and should be ignored.
- Empty lines should be ignored.
- Values can contain environment variables in the format `${VAR_NAME}`. These must be interpolated using an environment dictionary passed to the parser. If a variable is not found in the dictionary, it should be replaced with an empty string.
- Keys and values should have leading/trailing whitespace stripped.

Your goals:
1. Initialize a Python environment and manage dependencies. Create a `requirements.txt` in `/home/user/sysconf_parser` that includes `pytest` and `hypothesis` (for property-based testing), and install them.
2. Fix the `parse_config(text: str, env: dict) -> dict` function in `/home/user/sysconf_parser/parser.py` to meet the specifications above.
3. Write property-based tests in `/home/user/sysconf_parser/test_parser.py` using `hypothesis`. Test that generating a dictionary of random alphanumeric keys and alphanumeric values (which represent an environment), formatting them into a config string, and parsing them back with an empty environment dictionary yields the original dictionary. Ensure your tests pass when running `pytest /home/user/sysconf_parser/test_parser.py`.
4. Create a script `/home/user/sysconf_parser/run_example.py` that imports your fixed `parse_config`, reads `/home/user/sysconf_parser/example.conf`, and parses it using the following environment dictionary: `{"SYSTEM_ROOT": "/var/lib", "USER": "admin"}`.
5. The script must write the resulting dictionary as a formatted JSON file to `/home/user/sysconf_parser/output.json` (with 4 spaces indentation).

Please complete these steps. The automated verification will check if `pytest` passes your property-based tests and will verify the exact contents of `/home/user/sysconf_parser/output.json`.