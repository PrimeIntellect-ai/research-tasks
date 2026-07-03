You are helping a researcher organize and analyze an experimental dataset using only standard Linux command-line tools. 

The researcher previously tried to write a shell pipeline to join two datasets and flag statistically significant outliers based on a linear model. However, much like a misconfigured plotting library that silently outputs blank images, their `join` commands silently failed and produced empty outputs because they didn't account for the fact that standard Unix tools expect sorted inputs.

Your task is to properly process the data from scratch using Bash (e.g., `awk`, `join`, `sort`, `bc`, etc.).

**Data Sources (in `/home/user/`):**
1. `model.conf`: Contains the parameters of a simple linear model (`bias`, `w1`, `w2`) in `key=value` format.
2. `data_A.csv`: Contains `id,f1` (header included, unsorted).
3. `data_B.csv`: Contains `id,f2` (header included, unsorted).

**Requirements:**
1. **Multi-source Data Joining**: Join `data_A.csv` and `data_B.csv` on the `id` column. Make sure to handle the headers correctly and account for the unsorted nature of the files.
2. **Model Inference**: For each joined row, calculate the predicted value $y$ using the formula:
   $$y = \text{bias} + (w_1 \times f_1) + (w_2 \times f_2)$$
3. **Hypothesis Testing (Outlier Detection)**:
   - Calculate the population mean ($\mu$) and population standard deviation ($\sigma$) of all the predicted $y$ values.
   - Identify the `id`s of all rows where the predicted value is significantly higher than the rest, defined as: $y > \mu + 1.96 \times \sigma$.
4. **Output**: Write the `id`s of the outliers, sorted numerically, one per line, to `/home/user/outliers.txt`.

Work exclusively in the terminal using Bash tools to parse, join, compute, and filter the data.