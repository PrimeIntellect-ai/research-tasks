You are an MLOps engineer tasked with verifying the reproducibility of two different machine learning regression pipelines. Large-scale artifacts from these pipelines have been exported as CSV files containing true and predicted values. To robustly test the pipeline reproducibility, you need to compute the bootstrap-estimated Mean Squared Error (MSE) for both runs.

Your task is to write a C program that calculates the bootstrap-estimated MSE for a given CSV file, and then write a shell script to generate a report for the two pipeline runs.

**Step 1: Write the C program**
Create a C program at `/home/user/bootstrap_mse.c` that does the following:
1. Accepts exactly two command-line arguments: the path to a CSV file and an integer random seed. Usage: `./bootstrap_mse <file.csv> <seed>`
2. Reads the CSV file. The file has no header and contains exactly 10,000 lines. Each line contains two comma-separated floating-point numbers: `true_value, predicted_value`.
3. Performs 1,000 bootstrap iterations. For each iteration:
   - Samples 10,000 pairs from the loaded data *with replacement*.
   - Computes the Mean Squared Error (MSE) for this bootstrap sample.
4. Computes the average of the 1,000 bootstrap MSEs.
5. Prints this final average MSE to standard output, formatted to exactly 6 decimal places (e.g., `printf("%.6f\n", final_mse);`).

**Important PRNG Requirement:**
To ensure strict cross-platform reproducibility, DO NOT use standard C `rand()`. You must implement and use the following Linear Congruential Generator (LCG) for your random index selection:
```c
unsigned long long state = seed; // Set once at start of program from argv[2]
unsigned int lcg_rand() {
    state = (state * 1103515245ULL + 12345ULL) % 2147483648ULL;
    return (unsigned int)state;
}
```
To pick a random index from 0 to 9999, use: `int idx = lcg_rand() % 10000;`

**Step 2: Generate the Report**
Compile your C program using `gcc -O3 /home/user/bootstrap_mse.c -o /home/user/bootstrap_mse`.
You are provided with two artifact files: `/home/user/run_A.csv` and `/home/user/run_B.csv`.

Run your compiled program on both files using the seed `42`.
Save the results to `/home/user/report.txt` in exactly the following format:
```
Run A Bootstrap MSE: <value>
Run B Bootstrap MSE: <value>
```

Replace `<value>` with the exact output from your C program. Ensure your program handles file I/O safely and uses standard libraries (`stdio.h`, `stdlib.h`).