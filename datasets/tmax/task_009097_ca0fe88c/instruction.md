You are acting as an MLOps engineer. We have a C-based evaluation pipeline that processes experiment artifacts, specifically joining ground truth data with model predictions to calculate evaluation metrics. 

Currently, our pipeline is broken. The script generates an empty report and throws compilation errors due to a misconfigured numerical library backend, similar to how a plotting library might produce blank plots if the backend is missing. 

Your task is to fix the pipeline in `/home/user/experiment/`:

1. Examine `/home/user/experiment/truth.csv` and `/home/user/experiment/preds.csv`. Both have a header `id,value`. Note that the rows might not be in the same order.
2. We use the GNU Scientific Library (GSL) to compute statistics. The file `/home/user/experiment/evaluate.c` attempts to read these files, join them by `id`, calculate the squared errors for each matched sample, and then use GSL to compute the Mean Squared Error (MSE). It also calculates classification Accuracy (treating `value >= 0.5` as positive class 1, and `< 0.5` as negative class 0).
3. The `Makefile` in the directory is missing the correct linker flags for GSL. Fix it.
4. The `evaluate.c` file has a bug in its data joining logic and GSL vector allocation, causing it to crash or output nothing. Fix the C code so it correctly joins the data by `id`, computes the MSE using `gsl_stats_mean`, and computes the Accuracy.
5. Compile the program using `make` and run it. 
6. The program must write the results to `/home/user/experiment/metrics_report.txt` in exactly this format:
```
Total Samples: [integer]
MSE: [float with 4 decimal places]
Accuracy: [float with 4 decimal places]
```

Ensure your final compiled executable is named `evaluate` and successfully produces the `metrics_report.txt` file.