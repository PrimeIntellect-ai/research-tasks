You are a performance engineer analyzing the latency of a critical microservice under varying CPU and Memory loads. You have collected observational data but need to determine the underlying scaling law to better provision your infrastructure. 

Two hypotheses have been proposed for how Latency ($L$) scales with CPU load ($C$) and Memory usage ($M$):
- **Hypothesis A (Linear):** $L = \alpha \cdot C + \beta \cdot M$
- **Hypothesis B (Quadratic CPU):** $L = \gamma \cdot C^2 + \delta \cdot M$

Your task is to write a Go program at `/home/user/profiler.go` that does the following:
1. **Reshape Observational Data:** Read the dataset located at `/home/user/metrics.csv`. The file has a header `cpu,mem,latency` and comma-separated float values.
2. **Optimization (Gradient Descent):** Implement standard Batch Gradient Descent from scratch in Go to find the optimal parameters $(\alpha, \beta)$ for Hypothesis A, and $(\gamma, \delta)$ for Hypothesis B. 
   - Initialize all weights to `0.0`.
   - Use a learning rate of `0.0005`.
   - The loss function should be the Mean Squared Error (MSE).
3. **Convergence Testing:** For each hypothesis, run the gradient descent loop until the absolute change in the MSE between consecutive epochs is strictly less than $10^{-5}$, or until you reach $50,000$ epochs.
4. **Statistical Hypothesis Comparison:** Compare the final MSE of Hypothesis A and Hypothesis B. The hypothesis with the lower MSE is the winner.
5. **Output:** Write a JSON file to `/home/user/best_model.json` containing the winning hypothesis. The file must strictly follow this format:
```json
{
  "hypothesis": "A" // or "B"
}
```

Run your Go program to generate the `/home/user/best_model.json` file. Ensure you have properly parsed the CSV and applied the algorithms exactly as specified.