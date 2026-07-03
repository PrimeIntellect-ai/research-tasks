You are an ML engineer preparing a graph training dataset for a Graph Neural Network that predicts latency bottlenecks in our microservices architecture. 

We have a local staging environment that simulates service traffic. In `/app/`, there is a startup script `start_services.sh` that launches three components:
1. A Redis instance (port 6379)
2. A simulated traffic API (port 8080)
3. A worker process that fetches raw observational traffic logs from the API and pushes them to a Redis list named `raw_traffic`.

Your task is to integrate these services, collect the observational data, process it into a robust graph dataset, and evaluate its distribution. 

Perform the following steps:
1. Start the services by running `/app/start_services.sh`. Wait a few seconds for the worker to populate Redis. 
2. Write a Python script `/home/user/prepare_data.py` to read all current items from the `raw_traffic` list in Redis (db=0). Each item is a JSON string: `{"src": "ServiceA", "dst": "ServiceB", "latency": 12.5}`. You should pull at least 1000 records.
3. Reshape this observational data into a directed graph structure, grouping all latency observations by their directed edge `(src, dst)`.
4. For each edge, use bootstrap resampling to calculate the 95% confidence interval of the **mean latency**. 
   - Perform convergence testing: start with `B=500` resamples and increase to `B=1000`. 
   - Use the `B=1000` resamples to compute the lower and upper bounds (2.5th and 97.5th percentiles).
5. Extract the bootstrap mean latency for each edge. Standardize these mean latencies across all edges (subtract the overall mean of the edge means, and divide by the standard deviation of the edge means).
6. Calculate the 1-Wasserstein distance between your standardized edge mean latencies and a standard normal distribution $\mathcal{N}(0, 1)$. (You can use `scipy.stats.wasserstein_distance` against a large sample from a standard normal, or its theoretical CDF).
7. Output the final dataset to `/home/user/processed_graph.json` with the following exact format:
```json
{
  "wasserstein_distance": 0.042,
  "edges": [
    {
      "src": "ServiceA",
      "dst": "ServiceB",
      "mean_latency": 12.6,
      "ci_lower": 11.2,
      "ci_upper": 14.1
    }
  ]
}
```

The automated test will evaluate the accuracy of your computed `wasserstein_distance` and confidence intervals against the true mathematical expected values based on the data dumped in Redis.