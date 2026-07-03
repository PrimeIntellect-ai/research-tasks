You are a Machine Learning Engineer preparing training data for an anomaly detection model. You have been given raw API access logs and node metadata. You need to engineer statistical features that capture the reliability and latency profile of each server node.

Your task is to write a Python script that processes these files and outputs a final feature set. 

**Inputs:**
1. `/home/user/api_logs.csv`: Contains API requests. Columns: `log_id`, `node_id`, `latency_ms`, `status` ('success' or 'fail').
2. `/home/user/node_info.json`: Contains node metadata. Format: `[{"node_id": "N1", "datacenter": "us-east"}, ...]`.

**Processing Steps:**
1. **Data Aggregation**: Group the logs by `node_id`. Calculate the total number of requests and the number of failed requests for each node. Merge this with the datacenter information.
2. **Bayesian Inference**: Some nodes have very few requests, making raw failure rates unreliable. Calculate the posterior mean failure rate for each node using a Beta-Binomial conjugate model. Assume a prior of Beta(α=2, β=10). 
   *Recall: The posterior mean for Beta(α, β) with $k$ failures out of $n$ trials is $\frac{\alpha + k}{\alpha + \beta + n}$.*
3. **Hypothesis Testing**: For each node, extract the `latency_ms` of all **successful** requests. Perform a 1-sample two-sided T-test (`scipy.stats.ttest_1samp`) against a baseline population mean latency of `120.0` ms. 
   *Note: If a node has fewer than 2 successful requests, assign a p-value of `1.0`.*
4. **Target Label Creation**: Create an integer column `is_anomalous` set to `1` if the node is deemed anomalous, and `0` otherwise. A node is anomalous if:
   - Its `bayes_failure_rate` > `0.15` OR
   - Its successful request latency is statistically significantly higher than the baseline (i.e., p-value < `0.05` AND the sample mean latency > `120.0`).

**Output:**
Save the resulting dataset to `/home/user/training_features.csv`.
The CSV must be sorted alphabetically by `node_id` and contain exactly the following columns in this order:
`node_id`, `datacenter`, `total_requests`, `bayes_failure_rate`, `latency_pvalue`, `is_anomalous`

Round `bayes_failure_rate` to 4 decimal places, and `latency_pvalue` to 4 decimal places before saving. Do not include an index column in the CSV.