You are an AI assistant helping a developer migrate a legacy web security tool from Python 2 to Python 3. 

The tool relies on a custom binary token format for authentication. To ensure high-speed parsing, the token deserialization is implemented as a state machine in a C shared library, which is called from Python using `ctypes`. The project is located in `/home/user/workspace/`.

When the developer attempts to run the test suite using Python 3, they encounter multiple issues: type errors, segmentation faults, and failing mock tests. Your goal is to fix the code, compile the C library, and make the test suite pass.

The workspace contains three files:
1. `/home/user/workspace/token_parser.c`: The C implementation of the token parser state machine.
2. `/home/user/workspace/security_tool.py`: The Python module providing the `SecurityTokenManager` class. It manages serialization and FFI integration.
3. `/home/user/workspace/test_security_tool.py`: A `unittest` suite that relies on mock setups to verify the module.

Here is what you need to do:
1. **Build the C library**: Compile `token_parser.c` into a shared library named `libtoken.so` in `/home/user/workspace/`.
2. **Fix the Python 3 string/bytes migration issues**:
   - In `security_tool.py`, the `create_token` method must return `bytes` instead of a Python 3 `str`.
   - The C function `parse_token` modifies its input string in-place. Passing an immutable Python 3 `bytes` object directly via `ctypes` will cause a segmentation fault. You must use `ctypes.create_string_buffer` to safely pass a mutable copy to the C library.
   - Configure the correct `argtypes` and `restype` for the C function in the Python class constructor.
3. **Fix the Mock Test Fixtures**: 
   - In `test_security_tool.py`, the `mock_open` fixture is currently returning a `str` when it simulates reading binary data. Update it to return `bytes` so it behaves correctly in a Python 3 environment.
4. **Run the Tests**: Once you have fixed all the issues, run the test suite and redirect the output (both stdout and stderr) to `/home/user/workspace/test_report.txt`. The test report must indicate that 2 tests were run and passed (OK).

Do not change the underlying logic of the C parser state machine or the expected token format.