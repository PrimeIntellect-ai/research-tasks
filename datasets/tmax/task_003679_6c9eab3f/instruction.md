You are a support engineer tasked with investigating a series of system hangs caused by our log processing utility. 

You have been provided with the source code for the vendored package located at `/app/vendored/log-processor-2.0`. Currently, the package fails to build. 

Your tasks are:
1. Diagnose and fix the build failure in the vendored package so that it compiles successfully using `make`.
2. Analyze the source code to understand how it processes binary log files. You will notice that certain malformed logs cause the program's worker threads to enter an infinite loop or trigger race conditions due to cyclic offsets in the binary structure.
3. Write a standalone C program at `/home/user/classifier.c` and compile it to `/home/user/classifier`. 
   - This program must act as a filter/sanitiser for incoming logs before they reach the vulnerable `log-processor`.
   - Your program should take exactly one argument: the file path to a log file.
   - Example invocation: `/home/user/classifier /path/to/logfile.bin`
   - It must exit with code `0` if the log file is perfectly safe (structurally sound).
   - It must exit with code `1` if the log file contains the cyclic reference flaw or other structural anomalies that would trigger the hang/crash in the processor.

You are provided with a sample safe log at `/app/sample_clean.log` and a sample malicious log at `/app/sample_evil.log` to help you reverse-engineer the exact conditions of the loop and test your classifier.