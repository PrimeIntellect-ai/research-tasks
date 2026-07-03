You are helping a researcher organize and process historical clinical datasets. 

The researcher has left a photo of the required dataset schema in `/app/schema.png`. It contains a table with three columns: `Column`, `Type`, and `Nullable`. 
They also left a linear transformation matrix in `/app/transform_matrix.csv` to project features into a new space.

Currently, their data pipeline silently converts integer columns with missing values into floats, which breaks downstream tools. They need a robust web service that enforces the schema, prevents this int-to-float conversion, applies the matrix transformation, and returns the cleaned data.

Your task is to build and run an HTTP REST API using Python (FastAPI or Flask are recommended) that does the following:

1. **Extract the Schema**: Use OCR (e.g., `pytesseract`) to read `/app/schema.png`. Parse the table to determine the expected columns, their strict data types (`int` or `float`), and whether they allow nulls (`True` or `False`).
2. **Schema Enforcement**: 
   - When a dataset is uploaded, you must enforce the extracted schema.
   - **Crucial Rule**: Integer columns that allow nulls must remain integers and NOT be cast to floats (e.g., use pandas' `Int64` dtype). 
   - Missing values should be represented as standard JSON nulls in the output.
3. **Linear Algebra Transformation**:
   - Load `/app/transform_matrix.csv`.
   - Take the numeric columns from the dataset (in the exact order they appear in the schema from top to bottom, excluding any identifier columns like `patient_id` which you can assume is the first column).
   - Multiply this $N \times K$ feature matrix by the $K \times 2$ transformation matrix. Treat missing values as `0` *only* for the purpose of this matrix multiplication.
   - Append the resulting two columns to the dataset as `proj_1` and `proj_2`.
4. **Expose the Web Service**:
   - Listen on `0.0.0.0:8000`.
   - Implement a `POST /process` endpoint.
   - The endpoint must require an `Authorization` header with the exact value: `Bearer ds-secret-token`. Return `401 Unauthorized` otherwise.
   - The endpoint expects a `multipart/form-data` upload with a file field named `dataset` containing a CSV.
   - Return the processed dataset as a JSON array of objects (records format), e.g., `[{"patient_id": 1, "age": null, "weight": 70.5, "proj_1": 12.3, "proj_2": 4.5}, ...]`.

Leave the service running in the foreground or background so it can be tested. You have full freedom to install any Python packages you need.