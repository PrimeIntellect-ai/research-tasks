You are a systems programmer stepping in to debug a C library linking and build issue for a web authentication service. 

In `/home/user/auth_lib/`, you will find the source code for an authentication token validation library (`auth.c`) and a broken `Makefile`. The library is supposed to compile into a shared object `libauth.so`, but the build is currently failing or producing incorrect logic because it is missing critical compiler flags.

The previous developer left a screenshot of the build requirements in `/app/instructions.png`. 

Your task:
1. Extract the missing compilation flags from the text within the image `/app/instructions.png`. (You may use tools like `tesseract` to read the image).
2. Fix the `Makefile` in `/home/user/auth_lib/` and successfully compile `libauth.so`.
3. Write a Python script at `/home/user/solve.py` that acts as a bridge to this library. 
4. The Python script must read strings from standard input (stdin) line by line until EOF. For each line (stripped of trailing newlines), it should pass the string to the `validate_token(const char*)` function in `libauth.so` using the `ctypes` module, and print the returned integer result to standard output (stdout).

The automated verifier will pipe random token strings into your `solve.py` script and compare the outputs against a known good oracle. Ensure your Python script properly encodes the strings before passing them to the C library.