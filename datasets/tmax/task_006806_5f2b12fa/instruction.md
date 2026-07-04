I am organizing a messy project directory and need your help to consolidate some data processing using an existing C shared library. 

In `/home/user/project/`, there is a shared library `libstate.so` (in `/home/user/project/lib/`) and a data file `events.txt` (in `/home/user/project/data/`). The shared library exposes a C function that runs a state machine on a sequence of characters:
`int process_event(const char* event_seq);`

I need you to do the following:
1. **Organize the files**: Move `libstate.so` to `/home/user/project/bin/` and move `events.txt` to `/home/user/project/archive/`. Create these directories.
2. **Write a Python script**: Create `/home/user/project/process_events.py` that does the following:
   - Uses `ctypes` to load the `libstate.so` library from its *new* location (`/home/user/project/bin/libstate.so`).
   - Explicitly defines the argument (`ctypes.c_char_p`) and return type (`ctypes.c_int`) for `process_event`.
   - Parses the archived `events.txt` file. Each line in the text file is formatted as `ID: SEQUENCE` (e.g., `evt1: AABAB`).
   - For each line, passes the `SEQUENCE` (as a byte string) to the `process_event` C function.
   - Saves the structured results into `/home/user/project/results.json`. The JSON should be a dictionary mapping the string `ID` to the integer result returned by the C function.
3. **Add a Unit Test**: In the same `process_events.py` file, include a standard Python `unittest.TestCase` class named `TestFFIWrapper`. It should contain at least one test method that directly calls your `ctypes` wrapper with the sequence `"AAB"` and asserts that the result is an integer (do not worry about the exact value, just verify the FFI call executes successfully and returns an `int`). Include an `if __name__ == '__main__':` block that runs the tests if the script is executed directly or processes the file if a specific flag is passed (or just run both). Simply running `python3 /home/user/project/process_events.py` must generate the `results.json` file.

Please execute the necessary commands to organize the files, create the Python script, and run it so that `results.json` is generated.