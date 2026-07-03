You are an engineer troubleshooting a long-running mathematical service written in Bash. The service, located at `/home/user/calc_service.sh`, reads commands from a named pipe `/tmp/calc_in`, computes results, and writes them to `/tmp/calc_out`. 

Currently, the service suffers from two critical bugs:
1. **Formula Implementation Correction:** The service is supposed to calculate factorials when receiving a command like `fact 5`, but it always outputs `0` due to a mathematical logic error in the loop.
2. **Memory Leak / State Accumulation:** Because it is a long-running daemon, it logs its operations. However, it incorrectly accumulates log entries in a continuously growing string variable (`LOG_BUFFER`) inside the loop, causing the bash process's memory to grow indefinitely over time. It overwrites `/home/user/service.log` with this entire accumulated string on every request.

Your task is to fix the service and implement a regression test:

**Step 1: Fix the Service**
- Modify `/home/user/calc_service.sh`.
- Correct the factorial formula so that, for example, `fact 5` outputs `120` and `fact 0` outputs `1`. (You may assume inputs will be non-negative integers $\le 20$).
- Fix the memory leak: Remove the accumulating `LOG_BUFFER` variable. The script should instead append the current log line directly to `/home/user/service.log` without storing the history of all logs in memory.

**Step 2: Construct a Regression Test**
- Create a bash script at `/home/user/test_calc.sh` (ensure it is executable).
- The script must do the following in order:
  1. Start `/home/user/calc_service.sh` in the background.
  2. Send the command `fact 5` to `/tmp/calc_in` and read the result from `/tmp/calc_out`.
  3. Send the command `fact 6` to `/tmp/calc_in` and read the result from `/tmp/calc_out`.
  4. Send the command `QUIT` to `/tmp/calc_in` to gracefully terminate the service.
  5. Wait for the background service process to exit.
  6. Verify that the results read were exactly `120` and `720`.
  7. If both results are correct, print "PASS" to stdout and exit with code `0`.
  8. If any result is incorrect (or a timeout occurs), print "FAIL" to stdout and exit with code `1`.

*Note: The service script already contains the pipe setup (`mkfifo`) and gracefully exits when it receives `QUIT`. You only need to fix the bugs and write the test.*