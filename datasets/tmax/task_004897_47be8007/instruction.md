You are a bioinformatics analyst tasked with analyzing the relationship between primer GC content and empirical binding efficiency. You have been provided with an experimental dataset of primer sequences and their corresponding binding scores. 

Your task is to write a Rust program that performs this analysis. 

Here are the requirements:
1. Read the dataset from `/home/user/binding_data.csv`. The CSV has two columns: `sequence` (a DNA string of length 20) and `score` (a floating-point experimental binding efficiency).
2. For each sequence, calculate the GC fraction (the number of 'G' and 'C' bases divided by the total sequence length).
3. Perform an Ordinary Least Squares (OLS) linear regression to fit a line `score = m * gc_fraction + c`. Calculate the slope (`m`) and the intercept (`c`).
4. Fit a normal distribution to the empirical `score` values by calculating their sample mean (`mu`) and sample standard deviation (`sigma` - use Bessel's correction, i.e., divide by N-1).
5. Output the results to a JSON file located at `/home/user/analysis_results.json` with exactly the following format (all float values rounded to 4 decimal places):
```json
{
  "slope": 1.2345,
  "intercept": -0.1234,
  "mean_score": 0.5678,
  "std_score": 0.1111
}
```

Write and execute your Rust code to generate the final JSON file. Ensure your Rust program compiles and runs successfully in the `/home/user` directory.