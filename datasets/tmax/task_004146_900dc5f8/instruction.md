You are an MLOps engineer debugging an experiment tracking pipeline. We have a simple C++ program that simulates model training and outputs the final evaluation loss. However, we've noticed a "silent conversion" issue similar to pandas pipeline bugs: the evaluation losses being tracked are mysteriously truncated, losing all decimal precision, which ruins our hyperparameter tuning.

Your task is to fix the pipeline:

1. Inspect the C++ source code located at `/home/user/train_model.cpp`. Find and fix the bug that causes the calculated loss or weights to silently lose their floating-point precision when outputting the final metric. 
2. Compile the fixed C++ program into an executable named `/home/user/model_trainer`. You must use standard C++11 (or higher) and no external libraries.
3. Write a bash script at `/home/user/run_experiments.sh` that acts as our experiment tracker. The script must:
   - Be executable.
   - Iterate over three learning rates exactly: `0.01`, `0.05`, and `0.1`.
   - Run the `/home/user/model_trainer` for each learning rate. The executable takes the learning rate as its first and only command-line argument.
   - Parse or capture the final output loss from the executable.
   - Append the results to an experiment tracking file at `/home/user/experiments.csv`.
4. Run your bash script to generate the final `experiments.csv`.

The `/home/user/experiments.csv` file must have exactly this format for each run (no headers, just the comma-separated values):
```
<learning_rate>,<final_loss>
```
For example:
```
0.01,45.1234
0.05,12.5678
0.1,6.7890
```

Ensure the C++ fix correctly restores the precision, and that the bash script automates the tracking correctly.