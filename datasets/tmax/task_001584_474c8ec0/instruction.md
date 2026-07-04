You are tasked with finding a regression in a Go coordinate transformation utility. 

A precision loss bug was recently introduced somewhere in the repository located at `/home/user/geo-transform`. The program reads a list of floating-point values from an input file and computes their sum. Historically, this tool processed high-precision coordinate offsets perfectly, but recent versions suffer from precision loss (silent truncation/rounding errors) due to an internal type or parsing change.

We have a test input file with slightly irregular (but valid) coordinate data located at `/home/user/input.txt`. 
If you run `go run main.go /home/user/input.txt`, the output should accurately reflect the high-precision sum of the values. In the buggy version, the output loses precision.

- The commit tagged `v1.0` is known to be **good** (calculates with high precision).
- The commit tagged `v2.0` (which is current `HEAD`) is known to be **bad** (loses precision).

Your task:
1. Use `git bisect` or write a custom delta-debugging script to test the commits between `v1.0` and `v2.0`.
2. Identify the **first bad commit** that introduced the precision loss.
3. Write the exact, full 40-character commit hash of the first bad commit to a file named `/home/user/result.txt`.

Ensure your final answer in `/home/user/result.txt` contains *only* the 40-character hash and a trailing newline.