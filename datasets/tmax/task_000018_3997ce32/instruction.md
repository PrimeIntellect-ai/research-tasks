You are a performance engineer profiling a spectroscopy data processing pipeline. During debugging, you noticed that the computed total energy of the spectrum varies across different runs. You suspect this is due to the non-reproducibility of floating-point reduction order. 

To prove this to the development team, you need to calculate the sum of the spectrum values in two different ways and show the difference caused purely by the order of addition (due to catastrophic cancellation and floating-point precision limits).

You are provided with a file at `/home/user/signal.txt` containing one floating-point number per line.

Your task is to write a bash script at `/home/user/evaluate_order.sh` that uses **only** standard POSIX shell tools (like `awk`, `sort`, `sed`, `cat`, etc. - do NOT use Python, Perl, Ruby, or bc) to do the following:
1. Compute the sum of the numbers in `/home/user/signal.txt` sequentially from top to bottom.
2. Compute the sum of the numbers in `/home/user/signal.txt` after sorting them strictly by their **absolute value** in ascending order (smallest absolute value first).
3. Compute the absolute difference between the sequential sum and the sorted sum.
4. Output *only* this final absolute difference to `/home/user/result.txt`.

Ensure your script `/home/user/evaluate_order.sh` is executable and writes the exact numeric difference to the result file. 

Example of sorting by absolute value:
If the input is:
-10.5
2.1
5.0
The sorted order for summation should be:
2.1
5.0
-10.5