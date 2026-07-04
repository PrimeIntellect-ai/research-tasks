As an MLOps engineer, you are tracking experiment artifacts for a series of model deployments. I have an experiment metadata file located at `/home/user/experiments.csv`. This file logs various hyperparameters, inference performance benchmarks (latency), and model evaluation metrics (accuracy).

The CSV file has the following header and structure:
`experiment_id,learning_rate,batch_size,latency_ms,accuracy`

I need you to write a C program that calculates the Pearson correlation coefficient between the inference latency (`latency_ms`) and the model evaluation metric (`accuracy`). 

Please do the following:
1. Write the C source code to `/home/user/analyze.c`.
2. The program must read `/home/user/experiments.csv`, extract the `latency_ms` and `accuracy` columns, and compute their Pearson correlation coefficient.
3. The program must output the final computed correlation to a file named `/home/user/correlation_result.txt` exactly in the following format:
`Correlation: X.XXXX` (where X.XXXX is the correlation coefficient rounded to 4 decimal places).
4. Compile your program using `gcc` and run it to produce the output file. You can use the standard math library (`-lm`).

Ensure your math handles standard floating-point operations. Assume the CSV is well-formed, does not contain empty lines, and has a header row.