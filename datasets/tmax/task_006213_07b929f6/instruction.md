You are a data scientist tasked with cleaning a messy dataset, joining multiple sources, testing a hypothesis, and building a baseline regression model.

Your workspace contains three data sources in the `/home/user/data/` directory (which you should assume exists and is populated):
1. `customers.csv`: Contains `CustomerID`, `Age`, and `Region`.
2. `transactions.csv`: Contains `TransactionID`, `CustomerID`, and `Amount`.
3. `support.db`: A local SQLite database with a table named `tickets` containing `CustomerID` and `TicketCount`.

**Step 1: Data Schema Enforcement & Cleaning**
You must load and clean the datasets according to the following strict schema rules. Any row failing these rules must be completely dropped from its respective dataset *before* any joining or aggregation occurs.
* `CustomerID`: Must be an integer > 0.
* `Age`: Must be an integer between 18 and 100 (inclusive).
* `Region`: Must be exactly one of: 'North', 'South', 'East', 'West'.
* `Amount`: Must be a float >= 0.0.
* `TicketCount`: Must be an integer >= 0.

**Step 2: Multi-source Data Joining & Aggregation**
1. Filter the raw datasets using the rules above.
2. Join the cleaned transactions with the cleaned customers. Drop any transactions that do not match a valid customer.
3. Aggregate the data to the customer level to compute:
   - `Total_Spend`: Sum of `Amount` for the customer.
   - `Average_Spend`: Mean of `Amount` for the customer.
4. Left join the `tickets` data from the SQLite database to this aggregated customer data. If a valid customer has no record in the `tickets` table, impute their `TicketCount` as 0.

**Step 3: Hypothesis Testing**
Using your aggregated customer dataset, perform a Welch's two-sample t-test (unequal variances) to determine if customers in the 'North' region have a significantly different `Average_Spend` than customers in the 'South' region.
* Note: Test if `Average_Spend` of North != `Average_Spend` of South (two-tailed).

**Step 4: Baseline Regression**
Using the final cleaned, aggregated customer dataset, train a Ridge regression model to predict `Total_Spend` based on two features: `Age` and `TicketCount`.
* Use `sklearn.linear_model.Ridge` with `alpha=1.0`.
* Train the model on the entire valid aggregated dataset.
* Calculate the Mean Squared Error (MSE) of the predictions on this same training set.

**Step 5: Reporting**
Save your results to the following files:
1. Save the aggregated customer dataset to `/home/user/cleaned_customers.csv` (Columns: `CustomerID`, `Age`, `Region`, `Total_Spend`, `Average_Spend`, `TicketCount`). Do not include the pandas index.
2. Create a JSON report at `/home/user/report.json` with exactly the following structure:
```json
{
  "num_valid_customers": <int: the number of rows in the final aggregated dataset>,
  "north_south_ttest_pvalue": <float: the p-value from the t-test>,
  "ridge_mse": <float: the MSE of the Ridge model>
}
```
Round the floats to 4 decimal places in the JSON.