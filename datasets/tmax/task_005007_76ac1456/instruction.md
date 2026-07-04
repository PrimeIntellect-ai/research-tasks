You are an MLOps engineer tasked with fixing a critical data leakage bug in a custom high-performance machine learning pipeline. 

Our team wrote a lightweight linear regression pipeline in C for embedded devices, located at `/home/user/src/train_model.c`. This program reads a dataset `/home/user/data/dataset.csv`, performs Z-score feature scaling, and estimates the model's generalization error using Out-Of-Bag (OOB) MSE over 100 bootstrap samples. 

However, we suspect there is a severe data leakage issue. The program calculates the scaling statistics (mean and standard deviation) on the *entire* dataset before doing the bootstrap sampling, meaning information from the OOB test sets is leaking into the training process. 

We have a stripped, closed-source reference binary at `/app/oracle_pipeline` that implements the exact same linear regression and bootstrap algorithm but *without* the data leak. It scales the features correctly (fitting the scaler only on the bootstrap sample, and applying it to the sample and the OOB set). You can use it to see what the true, non-leaking OOB MSE should roughly be.

Your tasks are:
1. Analyze `/home/user/src/train_model.c` and identify the data leak.
2. Refactor the C code so that feature scaling is calculated strictly *inside* the bootstrap loop, using only the training sample to compute the mean and standard deviation, and then applying those statistics to scale both the training sample and the OOB evaluation set.
3. Ensure the random seed (`srand(42)`) and bootstrap sampling logic remain exactly the same so results are reproducible.
4. Compile your fixed code to `/home/user/bin/train_model_fixed` (create the directory).
5. Run your fixed pipeline. It should output the corrected average OOB MSE. Save this single floating-point value to a file located at `/home/user/metrics.txt`.

The automated verifier will evaluate your success based on how close your reported OOB MSE in `metrics.txt` is to the theoretically correct non-leaking OOB MSE.