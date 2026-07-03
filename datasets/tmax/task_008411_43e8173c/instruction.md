You are an MLOps engineer tasked with consolidating and analyzing hyperparameter tracking logs from distributed training runs. Our experiment tracking system has dumped several CSV logs into `/home/user/experiments/logs/`.

Your task is to write a C++ program that acts as a custom ETL pipeline to join, transform, and aggregate these logs. 

Specifically, you need to create a C++ source file at `/home/user/experiments/process_logs.cpp` and compile it to `/home/user/experiments/process_logs`. When run, the program should read all CSV files in the `/home/user/experiments/logs/` directory and produce a single aggregated output file at `/home/user/experiments/summary.csv`.

Here are the requirements for the data processing pipeline:
1. **Multi-source Data Joining**: Read all `.csv` files in `/home/user/experiments/logs/`. Each file contains the same header: `experiment_id,learning_rate,batch_size,optimizer,val_accuracy,training_time`.
2. **Feature Engineering (Encoding)**: The `optimizer` column is categorical (`adam` or `sgd`). Encode `adam` as `1` and `sgd` as `0`.
3. **Transformation and Aggregation**: Group the data by `learning_rate` and `batch_size`. For each group, calculate:
   - `mean_val_accuracy`: The average of `val_accuracy`
   - `total_training_time`: The sum of `training_time`
   - `mean_optimizer`: The average of the encoded `optimizer` values.
4. **Output formatting**: Write the aggregated results to `/home/user/experiments/summary.csv` with the header `learning_rate,batch_size,mean_val_accuracy,total_training_time,mean_optimizer`.
5. **Sorting**: Sort the output rows by `mean_val_accuracy` in strictly descending order. If there is a tie, sort by `learning_rate` descending.
6. All floating-point numbers in the output CSV must be formatted to exactly 4 decimal places (e.g., `0.8500`).

Once you write the code, compile it using standard C++17 (e.g., `g++ -std=c++17 -o process_logs process_logs.cpp`) and run it so that `summary.csv` is generated.