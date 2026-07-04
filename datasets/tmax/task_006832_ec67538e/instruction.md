You are an open-source maintainer reviewing a broken Pull Request for a data processing pipeline. The contributor provided a pre-compiled binary `/home/user/repo/data_tool` and an archive of candidate shared library plugins `/home/user/repo/plugins.tar.gz`. 

The PR description claims that exactly one of the plugins in the archive satisfies the current ABI constraints of `data_tool` (specifically, it exports the symbol `process_record_v2`), but the contributor forgot to include the bash test orchestration script to verify this.

Your task is to fix the PR by writing and executing a test orchestration script using bash and standard shell tools. 

Perform the following steps:
1. Extract `/home/user/repo/plugins.tar.gz` into `/home/user/repo/plugins/`.
2. Write a bash script at `/home/user/repo/run_tests.sh` that automates the following end-to-end workflow:
   - Analyzes the `.so` files in `/home/user/repo/plugins/` to find the exact library that exports the global text/code symbol `process_record_v2`.
   - Creates a directory `/home/user/repo/lib/`.
   - Creates a symbolic link in `/home/user/repo/lib/` named `libprocessor.so` that points to the matching plugin.
   - Executes `/home/user/repo/data_tool`, ensuring the dynamic linker can find `libprocessor.so` in your newly created `lib/` directory.
   - Redirects the standard output of `data_tool` to `/home/user/repo/test_output.txt`.
3. Make `run_tests.sh` executable and run it so that `/home/user/repo/test_output.txt` is successfully generated.

The automated verification will check the contents of `/home/user/repo/test_output.txt` and the correctness of your `run_tests.sh` script.