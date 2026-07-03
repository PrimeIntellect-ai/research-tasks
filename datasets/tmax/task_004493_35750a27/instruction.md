I'm working on a C++ parallel execution engine in my workspace at `/home/user/workspace/async_engine`, but our CI pipeline is failing during the test phase. 

When you run `make test`, the `test_cancellation` binary crashes. It seems to happen when the engine is cancelled immediately after startup, but I can't figure out why it's faulting.

Your task is to:
1. Diagnose the build/test failure by determining why `test_cancellation` is crashing (hint: it might be related to how statistics are calculated upon cancellation).
2. Fix the bug in the C++ source code so that `make test` passes successfully without crashing.
3. Create a brief summary of the root cause in `/home/user/workspace/bug_report.txt`. The file must contain the name of the function where the crash occurred and a short explanation of the mathematical/numerical error that caused it.

The workspace contains:
- `Makefile`
- `engine.cpp`
- `engine.h`
- `test_cancellation.cpp`

You can use `gdb` or any other tool to get the stack trace and diagnose the issue. Do not modify the test file (`test_cancellation.cpp`); you must fix the underlying bug in the engine code itself.