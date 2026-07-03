You are an MLOps engineer tasked with building a lightweight, fast telemetry processor for experiment artifacts. To ensure minimal overhead on the training nodes, this tool needs to be written in C.

You have two log files from a recent hyperparameter sweep:
1. `/home/user/params.csv` - Contains the setup for each experiment.
   Columns: `exp_id,learning_rate,epochs,initial_loss`
2. `/home/user/metrics.csv` - Contains the outcomes.
   Columns: `exp_id,final_loss`

Write a C program named `/home/user/evaluate_experiments.c` that does the following:
1. **Multi-source Data Joining:** Read and join the data from both CSV files using `exp_id` as the key.
2. **Tokenization and Parsing:** Properly parse the comma-separated values.
3. **Data Schema Enforcement:** Validate the data for each joined experiment. An experiment is considered `Invalid` if it violates any of these rules:
   - `learning_rate` > 0
   - `epochs` >= 1
   - `initial_loss` >= 0
   - `final_loss` >= 0
4. **Classification:** For valid experiments, we want to classify if the run was a success compared to a theoretical baseline. 
   - Calculate `predicted_loss = initial_loss / epochs`
   - If `final_loss < predicted_loss`, classify the experiment as `Success`.
   - Otherwise, classify it as `Failure`.
5. **Reporting:** The program must generate a file at `/home/user/report.csv` with the headers exactly as `exp_id,status`. The rows should contain the `exp_id` and the assigned status (`Success`, `Failure`, or `Invalid`), sorted by `exp_id` in ascending integer order.

Compile your program and execute it so that `/home/user/report.csv` is generated with the correct results. You may use standard C libraries (`stdio.h`, `stdlib.h`, `string.h`, etc.).