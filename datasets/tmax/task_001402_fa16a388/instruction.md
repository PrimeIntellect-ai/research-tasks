You are a Data Engineer building out custom high-performance ETL pipelines in C. Your current task involves debugging a data leakage issue in a numerical processing pipeline and setting up an experiment tracking script.

You have been provided with a dataset at `/home/user/data.csv` containing 1000 rows of single float values. 
There is also a buggy pipeline program located at `/home/user/pipeline.c`. 

Currently, `pipeline.c` reads the dataset, calculates the global mean and standard deviation to standardize the data, and *then* performs a pseudo-random 80/20 train/test split. This is a classic data leakage bug, as information from the test set is leaking into the training set's feature scaling phase.

Your task is to fix this leakage and run an experiment suite:

1. **Fix the Data Leakage:** Modify `/home/user/pipeline.c` so that the mean and standard deviation are calculated **strictly on the training split**. Standardize both the train and test splits using *only* the train split's mean and standard deviation.
    * *Constraint:* Do not change the random seed logic, and do not change the split condition (`rand() % 100 < 80`). The assignment of data points to Train or Test must occur *before* any statistical computations are made so you know which points belong to the train set.
    * *Constraint:* The printed output format must remain exactly the same: `Seed: %d, Train_Mean: %.4f, Test_Mean: %.4f\n`.

2. **Compilation:** Compile your fixed program into an executable named `/home/user/pipeline`. You will need to link the math library.

3. **Experiment Tracking:** Write a bash script at `/home/user/track.sh` that loops through the following random seeds in order: `10, 20, 30, 40, 50`. 
    * For each seed, execute the `/home/user/pipeline` program.
    * Append the standard output of the pipeline directly to a log file located at `/home/user/experiment.log`.

Ensure `/home/user/track.sh` is executable and run it so that `experiment.log` is fully populated.