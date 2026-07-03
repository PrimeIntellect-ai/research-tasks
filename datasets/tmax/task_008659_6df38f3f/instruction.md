You are an integration developer tasked with testing a legacy API emulator. The emulator interprets a simple custom bytecode to make API calls, but the code you inherited is buggy, the Makefile is broken, and there is no test fixture.

You need to complete the following phases in `/home/user`:

**Phase 1: Setup and Repair**
Below is the inherited codebase. Save it to the respective files.

File: `/home/user/emulator.cpp`
```cpp
#include <iostream>
#include <vector>
#include <string>
#include <fstream>
#include <cstdlib>

using namespace std;

// Opcodes:
// 1 <val> : PUSH <val>
// 2       : ADD (pops two values, adds them, pushes result)
// 3       : CALL (pops value, calls /api/<value> on mock server, pushes numeric response)
// 4       : PRINT (pops value, writes it to /home/user/integration_result.txt)

int main(int argc, char** argv) {
    vector<int> stack;
    for (int i = 1; i < argc; ++i) {
        int op = stoi(argv[i]);
        if (op == 1) {
            stack.push_back(stoi(argv[++i]));
        } else if (op == 2) {
            int a = stack.back(); stack.pop_back();
            int b = stack.back(); stack.pop_back();
            stack.push_back(a - b); // BUG: Should add b + a
        } else if (op == 3) {
            int val = stack.back(); stack.pop_back();
            string cmd = "curl -s http://127.0.0.1:9090/api/" + to_string(val) + " > /tmp/out.txt"; // BUG: Wrong port, mock server runs on 8080
            system(cmd.c_str());
            ifstream infile("/tmp/out.txt");
            int res; infile >> res;
            stack.push_back(res);
        } else if (op == 4) {
            int val = stack.back(); stack.pop_back();
            ofstream outfile("/home/user/integration_result.txt");
            outfile << val << endl;
        }
    }
    return 0;
}
```

File: `/home/user/Makefile`
```makefile
emulator: emulator.cpp
	gcc -o emulator emulator.cpp
```
*Note: The Makefile is using the C compiler instead of the C++ compiler, which will cause link errors.*

**Phase 2: Test Fixture Setup**
1. Write a Python script at `/home/user/mock_server.py` that starts a basic HTTP server on port `8080`.
2. When the server receives a `GET` request to `/api/<id>` (where `<id>` is an integer), it must return a plain text response equal to `<id> * 100`. (e.g., `/api/42` returns `4200`).
3. Run this Python server in the background so it can receive requests.

**Phase 3: Integration Test**
1. Fix the bugs in `/home/user/emulator.cpp` as noted in the comments.
2. Fix `/home/user/Makefile` and run `make` to build the `emulator` executable.
3. Run the compiled `emulator` passing the following bytecode as space-separated command-line arguments:
   `PUSH 10`, `PUSH 32`, `ADD`, `CALL`, `PRINT`
   *(Remember to translate these instructions into their corresponding integer opcodes and arguments as defined in the source code).*

The final verification will check the contents of `/home/user/integration_result.txt`.