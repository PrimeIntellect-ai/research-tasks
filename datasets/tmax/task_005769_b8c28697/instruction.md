You are an integration developer responsible for testing a new data processing API. You have been given a C++ CMake project located at `/home/user/tester` that acts as an API client, but the project is currently broken.

Your task consists of three parts:

1. **Fix the Build System**: The project fails to link against a pre-compiled shared library `libmetric.so` located in `/home/user/tester/lib`. Fix `/home/user/tester/CMakeLists.txt` so that it correctly links this library.

2. **Implement the API Logic**: Open `/home/user/tester/src/analyzer.cpp` and complete the `main` function. The program must:
   - Accept a single command-line argument (`argv[1]`) representing an API request URL.
   - Parse this URL routing string, which will always strictly follow this format: 
     `schema://hostname/path?data=x,y,z...&threshold=T`
     (where `x,y,z...` is a comma-separated list of integers, and `T` is an integer).
   - Implement a constraint satisfaction / numerical algorithm to find the total number of valid pairs. A valid pair is defined as a pair of indices `(i, j)` where `i < j` and `data[i] + data[j] == threshold`.
   - Call the `initialize_metrics()` function (provided by `libmetric.so` and declared in `metric.h`).
   - Multiply the number of valid pairs by the integer returned by `initialize_metrics()`.
   - Write this final calculated integer alone on a single line to `/home/user/tester/result.txt`.

3. **Execute the Test**: Build the project using CMake and `make`. Then, run the compiled executable `analyzer` with the following test URL:
   `"api://test/run?data=12,18,5,25,15,15,30,0&threshold=30"`

Ensure that `/home/user/tester/result.txt` is successfully created with the correct computed value. Note: you may need to configure your `LD_LIBRARY_PATH` when running the executable so it can find `libmetric.so` at runtime.