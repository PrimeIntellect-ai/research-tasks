You are helping a biomedical researcher organize and process their datasets for a predictive modeling task. 

The researcher has two CSV files located in `/home/user/data/`:
1. `patients.csv` with columns: `PatientID`, `Age`, `Condition`
2. `measurements.csv` with columns: `PatientID`, `BiomarkerA`, `BiomarkerB`

Write and execute a Go program that performs the following data processing steps:
1. Read both CSV files and join the data on `PatientID`.
2. Perform feature engineering by creating a new column called `RiskScore`. The formula for the risk score is: `(Age * BiomarkerA) / BiomarkerB`. 
   *Note: If `BiomarkerB` is 0, the `RiskScore` should be set to `0.00` to avoid division by zero.*
3. Write the joined and engineered data to a new CSV file at `/home/user/processed_data.csv`.
4. The output CSV must have the following header: `PatientID,Age,Condition,BiomarkerA,BiomarkerB,RiskScore`.
5. The output rows must be sorted in ascending order by `PatientID` (numerically).
6. Format the floating-point numbers (`BiomarkerA`, `BiomarkerB`, and `RiskScore`) strictly to 2 decimal places.

Your task is complete once the `/home/user/processed_data.csv` file has been correctly generated.