You are acting as an AI assistant for a machine learning engineer preparing signal training data.

We need to standardize our raw mathematical sensor data using Z-score normalization before feeding it into our neural network. 

Your task is to implement the preprocessing step in C, ensure it passes our regression tests, and apply it to our raw dataset.

Specifically, you need to:
1. Write a C program at `/home/user/src/preprocess.c`. The program must take exactly two command-line arguments: an input file path and an output file path.
   - Example execution: `./preprocess input.txt output.txt`
2. The program should read the input file, which contains a sequence of numerical data (one double-precision float per line).
3. Compute the Population Mean ($\mu$) and Population Standard Deviation ($\sigma$) of the dataset. (Note: use $N$ in the denominator for variance, not $N-1$).
4. Apply Z-score normalization to every value: $z_i = (x_i - \mu) / \sigma$.
5. Write the normalized values to the output file, one per line, formatted to exactly 6 decimal places (e.g., `%.6f`).
6. Compile your program and place the executable at `/home/user/bin/preprocess`.
7. We have a regression test script at `/home/user/test/regression_test.sh`. Run it to verify your program against our reference dataset. The script expects your executable at `/home/user/bin/preprocess`.
8. Once your program passes the test, run it on our new training data located at `/home/user/raw_training_data.txt`.
9. Save the processed output to `/home/user/prepared_data.txt`.

Ensure your C program dynamically handles up to 10,000 lines of data. If the standard deviation is 0 (all values are identical), the program should output `0.000000` for all values to avoid division by zero.