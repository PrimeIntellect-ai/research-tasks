You are an engineer tasked with debugging a failing build pipeline that analyzes network packet capture (pcap) files.

In your workspace (`/home/user/`), there is a shell script `build_and_test.sh` that iterates over `.pcap` files in `/home/user/pcaps/`, compiles `analyzer.c`, and runs it on each file to calculate a convergence metric based on the packet count.

Currently, the pipeline is failing for multiple reasons:
1. The shell script is breaking when processing files with spaces in their names.
2. The C program (`analyzer.c`) has a system call that also fails to handle spaces in filenames.
3. The core analytical function in `analyzer.c` (`compute_convergence`) contains a mathematical bug that causes an infinite loop (a convergence failure) when calculating the iterative metric.

Your tasks:
1. **Fix the Shell Script**: Modify `/home/user/build_and_test.sh` so that it safely loops over all `.pcap` files in `/home/user/pcaps/`, even those containing spaces, and passes them correctly to the compiled `analyzer` binary. The script should redirect all outputs to `/home/user/output.log` (overwriting the file if it exists).
2. **Fix the C Program**: 
   - Modify `/home/user/analyzer.c` to properly quote the filename passed to the `tcpdump` command via `popen`.
   - Fix the `compute_convergence` function (which attempts to implement Newton's method for square roots) so that it converges correctly.
3. **Create a Minimal Reproducible Example (MRE)**: Create a new file `/home/user/mre.c` that isolates the `compute_convergence` function. Its `main()` function should call `compute_convergence(100.0)` and print only the resulting `float` formatted to 3 decimal places (e.g., `printf("%.3f\n", result);`), then exit.

After making the fixes, run `./build_and_test.sh`. Ensure `/home/user/output.log` contains the correct output and `/home/user/mre.c` compiles and works independently.