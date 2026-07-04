You are a data researcher organizing and modeling a messy dataset of environmental sensor readings. 

You have been given a legacy, undocumented, and stripped binary executable located at `/app/sensor_oracle`. This binary acts as a black-box environmental model. It accepts a strictly formatted, clean CSV file of 5-dimensional numerical sensor features (with no header) and outputs a single calibrated regression target (one floating-point number per line) for each row.

Your goal is to reverse-engineer an approximation of this oracle by training a linear regression model in **C** from scratch using LAPACK, and using it to predict values for a new test set.

Here are your specific tasks:

1. **Environment Setup**: Install any necessary development libraries for C linear algebra (e.g., LAPACKE).
2. **Data Schema Enforcement**: You have a raw training dataset at `/app/data/raw_sensors.csv`. It is messy. Some rows contain invalid strings (like "N/A", "ERR"), and some have the wrong number of columns (it should be exactly 5 comma-separated floats). Write a script or command to strictly enforce this schema: filter out any invalid rows and produce a clean training CSV containing only valid 5-dimensional rows.
3. **Oracle Labeling**: Run the stripped binary `/app/sensor_oracle` on your cleaned training CSV to generate the ground-truth target labels.
4. **Linear Regression in C**: Write a C program (e.g., `model.c`) that reads the clean training features and the oracle's target labels, and uses linear algebra (specifically LAPACK/LAPACKE least squares solver, e.g., `dgels`) to compute the linear regression weights. 
5. **Prediction**: A test dataset is located at `/app/data/test_sensors.csv` (this dataset is already clean). Have your C program (or a separate C program) apply the learned linear weights to this test dataset.
6. **Output**: Save the test set predictions to `/home/user/predictions.csv`. This file must contain exactly one floating point number per line, corresponding to the predictions for the test set.

Your final model must closely approximate the oracle's internal logic. An automated system will evaluate your `/home/user/predictions.csv` against the true outputs of the oracle for the test set.

*Constraints*:
- The primary modeling code MUST be written in C.
- You must use C to solve the regression (no Python libraries for the modeling step, though you may use shell utilities or Python for data cleaning if desired).
- Do not add headers to your CSV files.