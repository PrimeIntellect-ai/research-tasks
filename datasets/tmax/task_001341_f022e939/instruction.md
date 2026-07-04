You are an ML Engineer reviewing the results of a recent cross-validation grid search for hyperparameter tuning. The results have been saved to a CSV file at `/home/user/cv_results.csv`. 

Due to an out-of-memory issue during training, some folds failed and silently produced empty values for the `validation_loss` column instead of numeric values (similar to how some data pipelines silently introduce NaNs). 

Your task is to process this tabular data using only standard Linux shell tools (Bash, awk, sort, etc.) to find the best hyperparameter configuration.

Here are your instructions:
1. Read `/home/user/cv_results.csv`. The file has a header: `learning_rate,batch_size,fold,validation_loss`.
2. Filter out any rows where `validation_loss` is missing (empty string).
3. Aggregate the data by calculating the mean `validation_loss` for each unique combination of `learning_rate` and `batch_size`.
4. Identify the hyperparameter combination with the lowest average `validation_loss`.
5. Write the best configuration to a file named `/home/user/best_config.txt`. The output must be a single line formatted exactly as `learning_rate,batch_size,average_loss` (with the average loss rounded to exactly 4 decimal places).

Do not use Python, R, or any other external scripting languages; solve this entirely with command-line utilities.