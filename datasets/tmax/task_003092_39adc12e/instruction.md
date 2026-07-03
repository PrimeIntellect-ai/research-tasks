You are an MLOps engineer tasked with fixing our experiment tracking pipeline. 

We have two issues:
1. **Blank Plots:** Our experiment visualization script at `/home/user/plot_experiments.py` is generating a blank/empty image file (`/home/user/experiment_plot.png`) when run in our headless CI environment. Please fix the script so that it successfully renders and saves the line plot showing our training metrics.
2. **Legacy Metric Oracle:** We track a custom "Model Drift Score" for numerical accuracy testing. The current calculator is a compiled, stripped legacy binary located at `/app/drift_oracle`. It takes two command-line arguments: both are comma-separated strings of non-negative integers representing expected and predicted values (e.g., `/app/drift_oracle "10,20,30" "12,18,33"`). 
   
   Because this binary is a black box and unsupported on our new ARM nodes, you need to write a replacement script at `/home/user/new_oracle.py`. Your script can be in Python, Bash, C++, or any language of your choice, but it must be invoked exactly as `python3 /home/user/new_oracle.py <actual_csv> <predicted_csv>` (if Python) or as an executable `/home/user/new_oracle <actual> <predicted>`. It must exactly replicate the behavior and standard output of `/app/drift_oracle` for any valid input arrays of equal length.

Investigate the outputs of `/app/drift_oracle` to deduce the mathematical function it computes. Implement the exact same mathematical metric in your replacement.