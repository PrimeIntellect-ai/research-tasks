You are a data scientist working on an embedded system where all data processing pipelines must be written in C. We have a raw tabular dataset exported from our sensors, but it contains a data quality issue similar to silent NaN conversions in pandas: missing numerical values were blindly exported as `-999`.

Your task is to write a C program that performs data cleaning, feature engineering, and computes Bayesian probabilities. 

Here are the requirements:
1. Read the dataset located at `/home/user/dataset.csv`. The file has a header: `id,feature_x,target`.
2. **Tabular Transformation**: Filter out and completely ignore any row where `feature_x` is exactly `-999` (these are missing values). 
3. **Feature Engineering**: For the valid rows, create a derived binary feature called `feat_bin`. Set `feat_bin = 1` if `feature_x > 50`, and `feat_bin = 0` otherwise (i.e., `feature_x <= 50`).
4. **Bayesian Inference**: Using *only the valid rows*, calculate the following probabilities:
   - The Prior probability of the target being 1: $P(Target=1)$
   - The Likelihood of the feature being 1 given the target is 1: $P(feat\_bin=1 | Target=1)$
   - The Likelihood of the feature being 1 given the target is 0: $P(feat\_bin=1 | Target=0)$
5. Write these three probabilities to an output file at `/home/user/bayes_results.txt`.

The output file `/home/user/bayes_results.txt` must contain exactly three lines formatted to 4 decimal places, like so:
```
Prior_T1: 0.XXXX
Likelihood_F1_given_T1: 0.XXXX
Likelihood_F1_given_T0: 0.XXXX
```

Write, compile, and run your C code to generate the final `bayes_results.txt` file.