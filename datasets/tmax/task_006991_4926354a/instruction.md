A junior data scientist has written a bash script, `/home/user/pipeline.sh`, to process a dataset. The script joins features and targets, imputes missing values using the mean, splits the data into training and test sets, and evaluates a simple heuristic model on the test set.

However, the script suffers from a severe methodological flaw: **Data Leakage**. It calculates the mean for imputation across the *entire* joined dataset before making the train/test split. 

Your task is to fix `/home/user/pipeline.sh` so that:
1. The join operation remains the same.
2. The shuffling and splitting (80% train, 20% test) happen *before* any statistics are calculated. (Preserve the exact `shuf` command using `/home/user/seed.dat` so the splits remain deterministic).
3. The mean of the feature column (column 2) is computed **only** from the training set.
4. Missing values (empty fields in column 2) in **both** the training and test sets are imputed using this *training* mean.
5. The final evaluation metric is computed on the properly imputed test set, outputting exactly to `/home/user/metric.txt` as it originally did.

Modify `/home/user/pipeline.sh` to correct this data leakage, preserving the exact filenames and metric calculation logic. Run your fixed script so that the correct value is written to `/home/user/metric.txt`. 

Everything you need is in `/home/user/`. Do not alter `/home/user/features.csv`, `/home/user/targets.csv`, or `/home/user/seed.dat`.