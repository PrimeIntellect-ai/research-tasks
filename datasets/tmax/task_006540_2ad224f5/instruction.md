You are a performance engineer profiling a spectroscopy data processing application. The application frequently crashes or hangs when performing matrix factorizations on certain "near-singular" signal datasets. 

After some analytical solution validation, you've discovered that the application fails whenever a signal dataset has an extreme dynamic range. Specifically, a signal dataset causes a crash if the ratio of its maximum amplitude to its minimum **strictly positive** (greater than 0) amplitude is **strictly greater than 1000**.

You have a directory of raw signal files located at `/home/user/signals/`. Each file is named `signal_*.dat` and contains space-separated tabular data. The first column is the frequency, and the second column is the amplitude (which is always non-negative).

Your task:
1. Create a reproducible Bash pipeline or script (you can use standard tools like `awk`, `grep`, `sort`, etc.).
2. Analyze all `.dat` files in `/home/user/signals/`.
3. Identify which files are "near-singular" according to the rule above.
4. Output the **basenames** only (e.g., `signal_1.dat`, not the full path) of the near-singular files to a log file at `/home/user/singular.log`.
5. The list of filenames in `/home/user/singular.log` must be sorted alphabetically, with one filename per line.

Use only Bash and standard POSIX shell utilities (no Python, Perl, etc.).