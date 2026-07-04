You are a machine learning engineer tasked with replacing a legacy, black-box feature extraction pipeline with a native Python implementation to prepare training data more efficiently. 

We have a proprietary, compiled binary located at `/app/feature_extractor` (it is a stripped binary without debug symbols). This tool takes raw 50-dimensional continuous data and reduces it to a 5-dimensional embedding. However, the binary is too slow for our new real-time pipeline, and we need to reconstruct its underlying mathematical model.

Based on prior documentation, we know the binary performs dimensionality reduction via a linear projection, followed by a specific probabilistic scaling that can be estimated using Bayesian inference. 

Your tasks:
1. Use the binary `/app/feature_extractor` to generate embeddings for a set of random 50-dimensional vectors. You will need to write a script to generate raw inputs, pass them to the binary, and parse the outputs. The binary reads from standard input (comma-separated values, one 50-dimensional vector per line) and prints the 5-dimensional embedding to standard output.
2. Analyze the relationship between the inputs and outputs using dimensionality reduction techniques and probabilistic modeling to reconstruct the projection matrix and scaling factors. Use hypothesis testing to ensure your estimated parameters are statistically significant and robust to the binary's internal noise.
3. Write a Python module at `/home/user/reconstructed_pipeline.py` that implements a class `FeatureExtractor`. 
   - The class must have a method `transform(X: np.ndarray) -> np.ndarray`.
   - `X` will be an $N \times 50$ NumPy array.
   - The method must return an $N \times 5$ NumPy array of embeddings.
   - Ensure your pipeline is reproducible (e.g., handle random seeds if your implementation relies on any probabilistic approximation, though the expected transformation should capture the expected value of the binary's output).

An automated test suite will import your `FeatureExtractor` class, pass a held-out test set of 10,000 vectors, and compare your output to the original binary. Your goal is to achieve an extremely low Mean Squared Error (MSE).