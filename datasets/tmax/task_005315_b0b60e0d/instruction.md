You are a data scientist tasked with cleaning a dataset and building a predictive model. You have been given a raw dataset and an image containing notes from a recent methodology meeting. 

Here is your multi-stage workflow:

1. **Extract Information**: Read the image at `/app/transformation.png`. It contains a 2x2 transformation matrix written on a whiteboard. Use OCR tools (like `tesseract`, which is preinstalled) to extract the four numerical values of this matrix.
2. **Data Transformation (Linear Algebra)**: Write a pipeline (using Bash, `awk`, or a Python script) to read `/app/raw_data.csv` (which has columns `id,X1,X2,Y`). Apply the 2x2 matrix from the image to the feature vector `[X1, X2]` for each row to compute a new set of orthogonal features `[Z1, Z2]`. (Standard matrix-vector multiplication: `Z_i = M_{i,1}*X1 + M_{i,2}*X2`).
3. **Data Schema Enforcement**: Clean the transformed dataset by strictly enforcing the following rules:
   - Drop any row that contains missing (empty) values in any column.
   - Drop any row where the newly computed `Z1` is strictly less than `-50.0`.
4. **Model Training**: Train an Ordinary Least Squares (OLS) Linear Regression model predicting `Y` from the engineered features `Z1` and `Z2` using your cleaned dataset.
5. **Evaluation**: Apply your full pipeline (transformation and model prediction) to the holdout dataset `/app/test_data.csv` (which contains `id,X1,X2`). 
6. **Integration**: Save your final predictions to `/home/user/predictions.csv`. The file must contain exactly two columns, formatted as:
```csv
id,Y_pred
1,45.213
2,-12.345
...
```

To pass this task, your predictions must achieve a Mean Squared Error (MSE) of less than `2.0` when compared to the hidden ground-truth target values for the test set.