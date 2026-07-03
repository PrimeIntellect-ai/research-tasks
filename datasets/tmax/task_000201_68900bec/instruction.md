You are an AI assistant acting as a Data Engineer. We have a data pipeline that processes transactional data. Recently, we discovered a silent bug: an upstream pandas pipeline sometimes converts strict integer `user_id` fields to floats (e.g., appending `.0`) or `NaN` due to sparse missing values in other columns.

We want to quantify the risk this poses to our fraud detection models using Bayesian inference. 

You have been provided with a recent batch of processed data located at `/home/user/processed/data.csv`. 
The CSV has a header: `tx_id,user_id,amount`.

Your task is to write and execute a Bash script (`/home/user/analyze_pipeline.sh`) that does the following:
1. **Data Scanning (Storage Management):** Read through `/home/user/processed/data.csv` (skipping the header) and count the total number of transactions and the number of "corrupted" transactions. A transaction is considered corrupted if the `user_id` column contains a decimal point (`.`) or the string `NaN`.
2. **Probability Calculation:** Calculate the overall probability of a transaction being corrupted, $P(\text{Corrupt})$, based on the counts from step 1.
3. **Bayesian Inference:** We know from historical data that the prior probability of any transaction being fraudulent, $P(\text{Fraud})$, is exactly `0.05`. We also know that the fraud rings exploit this data type conversion bug, so the probability of a transaction being corrupted given it is fraudulent, $P(\text{Corrupt}|\text{Fraud})$, is `0.80`.
   Use Bayes' theorem to calculate the posterior probability that a transaction is fraudulent given that it is corrupted: $P(\text{Fraud}|\text{Corrupt})$.
4. **Numerical Configuration:** You must use the `bc` command-line calculator to perform this math. Configure `bc` to use exactly 4 decimal places of precision (`scale=4`) for the final division. 

Once your script calculates this posterior probability, it must save strictly the final numeric value (e.g., `0.1234`) to a file named `/home/user/posterior.txt`. 

Do not include any text other than the 4-decimal-place number in the output file.