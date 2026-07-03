You are a data analyst optimizing an inference pipeline written in C. 

In `/home/user/workspace`, you will find a dataset `data.csv` containing 1000 rows (each row is a single floating-point number) and a C program `normalize.c`. 

Currently, `normalize.c` suffers from a classic data leakage issue: it computes the mean and standard deviation over the *entire* dataset (1000 rows) and uses those statistics to perform Z-score normalization. 

Your task is to fix the data leak, set up the tracking log, and benchmark the inference step:
1. Modify `normalize.c` so that it calculates the mean and standard deviation (population standard deviation, using $N$) strictly on the first 800 rows (the "training" set).
2. Use these training statistics to normalize ONLY the remaining 200 rows (the "inference" set). 
3. The program must write these 200 normalized inference values to `/home/user/workspace/inference_normalized.csv` (one value per line, formatted to 4 decimal places, e.g., `%.4f`).
4. The program must measure the time taken to normalize and write these 200 rows (the inference execution time) in microseconds.
5. The program must append an experiment tracking record to `/home/user/workspace/experiment_log.txt` strictly in this format:
   `TRAIN_MEAN: <mean>, TRAIN_STD: <std>, INFERENCE_TIME_US: <time>`
   (Format `<mean>` and `<std>` to 4 decimal places).

Make sure to compile your fixed C code with the math library (e.g., `gcc -O3 normalize.c -o normalize -lm`) and run it to produce the required output files.