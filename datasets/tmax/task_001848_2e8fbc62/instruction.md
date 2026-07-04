You are a web developer building a fast backend service in Python. For a high-performance data sanitization endpoint, you are using a compiled binary written in C and C++. 

Currently, the integration tests are failing because the compiled binary crashes on long inputs. You need to fix the memory safety issue, orchestrate the build, and ensure the tests pass.

Here is your task:
1. Examine `/home/user/app/src/sanitize.c`. It contains a buffer overflow vulnerability that causes a segmentation fault when processing inputs longer than 15 characters. Fix this memory safety issue so it can safely handle inputs up to 100 characters. Do not change the standard output format of the program.
2. Create a polyglot build and test script at `/home/user/app/build_and_test.sh` (ensure it has executable permissions).
3. The script `/home/user/app/build_and_test.sh` must:
    - Create the directory `/home/user/app/bin/` if it doesn't exist.
    - Compile `/home/user/app/src/utils.cpp` (using `g++`) and `/home/user/app/src/sanitize.c` (using `gcc`) and link them into a single executable located at `/home/user/app/bin/sanitize`.
    - Run the Python integration test suite using `python3 -m pytest /home/user/app/test_processor.py -v` and redirect its standard output to `/home/user/app/test_results.log`.
4. Run your `build_and_test.sh` script so that the `test_results.log` is generated and the tests pass.

Ensure the final `test_results.log` reflects 100% passing tests and the C program is no longer memory-unsafe.