You are a machine learning engineer preparing synthetic training data for a new model. You have been given a reference dataset from an older, undocumented pipeline, and you need to reproduce the mathematical model that generated it to create more data.

The legacy pipeline used a mathematical model of the form:
`y = sin(a * x) + b * cos(c * x)`
where `a`, `b`, and `c` are unknown integers between 1 and 10 (inclusive). 

You have a reference dataset located at `/home/user/reference_data.csv` containing two columns: `x` and `y`. This data was generated using the true values of `a`, `b`, and `c`, with no noise added.

Your task is to:
1. Reconstruct the model architecture and tune the hyperparameters (`a`, `b`, `c`) to find the exact integer values that perfectly reproduce the reference data (Mean Squared Error should be essentially 0).
2. Save the discovered hyperparameters in a JSON file at `/home/user/params.json` with the keys `"a"`, `"b"`, and `"c"`.
3. Use your reconstructed pipeline to generate *new* training data for `x` values starting from 10.0 up to 19.9 inclusive, with a step size of 0.1 (exactly 100 points).
4. Save this new data to `/home/user/new_training_data.csv`. The CSV must have a header `x,y`. The `x` values should be formatted to 1 decimal place (e.g., `10.0`), and the `y` values should be formatted to 4 decimal places (e.g., `3.1415`).

Ensure your pipeline is completely reproducible and mathematically exact.