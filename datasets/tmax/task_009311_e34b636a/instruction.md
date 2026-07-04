You are acting as a machine learning engineer preparing a training dataset. We have a raw dataset `/home/user/raw_data.csv` containing four columns: `id,f1,f2,f3` (all floats except `id` which is an integer).

We previously trained a simple linear regression model to predict a quality score $y$ from these features. The model weights are:
- Intercept (bias): 2.0
- w1 (for f1): 0.5
- w2 (for f2): -1.2
- w3 (for f3): 0.8

Your task is to write a C program `/home/user/filter_data.c` that performs the following steps:
1. Reconstructs this model architecture (calculates $y = bias + w_1f_1 + w_2f_2 + w_3f_3$).
2. Reads the CSV file (skipping the header row) and computes the predicted score $y$ for each row.
3. Filters the dataset: keeps only the rows where $y > 0.0$.
4. Writes the kept rows to `/home/user/filtered_data.csv` with the format `id,f1,f2,f3,y` (include a header `id,f1,f2,f3,y` and format floats to 4 decimal places).
5. Calculates the 95% Confidence Interval for the mean of the predicted scores ($y$) of the *filtered* rows. Use the large-sample approximation ($Z = 1.96$).
   - $Mean = \sum y / N$
   - $Variance = \sum (y - Mean)^2 / (N - 1)$
   - $Standard Error = \sqrt{Variance} / \sqrt{N}$
   - $Lower = Mean - 1.96 \times Standard Error$
   - $Upper = Mean + 1.96 \times Standard Error$
6. Writes these statistics to `/home/user/stats.txt` in exactly this format (floats to 4 decimal places):
```
Mean: <mean>
CI_Lower: <lower>
CI_Upper: <upper>
```

Compile your code using `gcc /home/user/filter_data.c -o /home/user/filter_data -lm` and execute it to generate the required output files.