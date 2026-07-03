You are a data scientist tasked with fitting and comparing spatial models across a partitioned 2D domain. We have a dataset of spatial observations, but a single global model does not fit well. You need to implement a reproducible pipeline that performs domain decomposition, fits two competing models using numerical optimization, and performs a statistical hypothesis comparison based on Mean Squared Error (MSE) to select the best model for each sub-domain.

Here are your instructions:

1. **Input Data**: You will find a dataset at `/home/user/spatial_data.csv` containing three columns: `x`, `y`, and `z`. `x` and `y` are coordinates in the range [0, 1], and `z` is the observed value.

2. **Domain Decomposition**: Partition the data into a 2x2 grid (4 quadrants) based on `x` and `y` coordinates:
   - `Q1`: x < 0.5 and y < 0.5
   - `Q2`: x >= 0.5 and y < 0.5
   - `Q3`: x < 0.5 and y >= 0.5
   - `Q4`: x >= 0.5 and y >= 0.5

3. **Optimization / Model Fitting**: For each quadrant, fit two competing models to predict `z` from `x` and `y`:
   - **Model A (Linear)**: $\hat{z} = \theta_0 x + \theta_1 y + \theta_2$
   - **Model B (Quadratic)**: $\hat{z} = \theta_0 x^2 + \theta_1 y^2 + \theta_2 x y + \theta_3$
   
   To fit the models, write a Python script that uses `scipy.optimize.minimize` with the **Nelder-Mead** method to find the parameters ($\theta$) that minimize the Mean Squared Error (MSE) between the predicted $\hat{z}$ and the actual $z$ in that quadrant. 
   - Use an initial guess of `0.0` for all parameters ($\theta$).
   - Use the default tolerances for the optimizer.

4. **Hypothesis Comparison**: For each quadrant, compare the minimized MSE of Model A and Model B. Select the model with the strictly lower MSE as the "best_model".

5. **Output**: Your script must output a JSON file at `/home/user/results.json` containing the best model and its corresponding MSE (rounded to 4 decimal places) for each quadrant. 

The JSON must follow this exact structure:
```json
{
  "Q1": {
    "best_model": "A",
    "mse": 0.1234
  },
  "Q2": {
    "best_model": "B",
    "mse": 0.0456
  },
  "Q3": {
    "best_model": "A",
    "mse": 0.0678
  },
  "Q4": {
    "best_model": "B",
    "mse": 0.0890
  }
}
```

Write and execute the Python pipeline to produce this output file.