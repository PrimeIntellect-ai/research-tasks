You are a DevOps engineer supporting a machine learning team. They are training a distributed mathematical model across 5 nodes. The training process runs for 100 epochs. 

Recently, the automated monitoring pipeline triggered an alert: the model appears to suffer from a sudden convergence failure and catastrophic variance explosion around Epoch 50, followed by `NaN` values.

However, the ML researchers suspect the model is actually converging fine, and the issue lies within the log aggregation pipeline. 

Your environment contains:
- `/home/user/logs/`: A directory containing 5 log files (`node_1.log` through `node_5.log`).
- `/home/user/aggregate.sh`: A shell script that reads these logs and computes the average loss per epoch, outputting to standard output.

Your investigation must accomplish the following:
1. Identify the statistical anomalies in the aggregated metrics.
2. Find the root cause in the raw logs (look for format parsing edge-cases, locale-specific formatting issues, or floating-point precision drops).
3. Fix `/home/user/aggregate.sh` so that it correctly parses all numeric formats present in the logs, avoids precision loss/underflow, and accurately computes the mean loss across all 5 nodes for each epoch.
4. Run your fixed script and redirect the output to `/home/user/fixed_epoch_averages.txt`.

The output in `/home/user/fixed_epoch_averages.txt` MUST exactly match this format:
```
Epoch 1: 0.954321
Epoch 2: 0.843210
...
Epoch 100: 0.000042
```
Ensure all averages are printed with exactly 6 decimal places of precision.

Do not manually hardcode the averages; you must fix the aggregation script so it dynamically computes the correct values from the log files.