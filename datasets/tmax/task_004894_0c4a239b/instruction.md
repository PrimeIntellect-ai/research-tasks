You are acting as a data analyst. You have been provided with a dataset of company financials in `/home/user/company_data.csv`. The CSV has the following columns: `Company_ID`, `R&D_Spend`, `Total_Expenses`, `Profit`.

Your task is to write and execute a Rust program that performs the following analysis:
1. Create a new Cargo project in `/home/user/analysis` and configure your `Cargo.toml` to use necessary numerical and CSV parsing crates (e.g., `csv`, `serde`, `statrs` or simply implement the math yourself).
2. Read the dataset and engineer a new feature: `R&D_Ratio`, which is calculated as `R&D_Spend / Total_Expenses`.
3. Compute the Pearson correlation coefficient ($r$) between `R&D_Ratio` and `Profit`.
4. Perform a hypothesis test on this correlation by calculating the t-statistic for the correlation coefficient. The formula is: $t = r \sqrt{\frac{n-2}{1-r^2}}$, where $n$ is the number of data points.
5. Track your experiment by outputting a summary report to `/home/user/report.txt`. 

The file `/home/user/report.txt` must exactly match the following format (replace the bracketed placeholders with your calculated values rounded to 4 decimal places, and the top 3 IDs):

```
Correlation: [r_value]
T-statistic: [t_value]
Top 3: [ID1], [ID2], [ID3]
```
Note: `Top 3` refers to a comma-separated list of the 3 `Company_ID`s with the highest `R&D_Ratio`, sorted in descending order of `R&D_Ratio`.

You must write the solution in Rust and run it to produce the final `report.txt`.