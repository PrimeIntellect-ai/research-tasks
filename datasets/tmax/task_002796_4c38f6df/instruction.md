You are a data engineer maintaining an ETL pipeline that processes product feature vectors. We have been receiving corrupted datasets that break our downstream similarity search and recommendation systems. 

Your task is to write a dataset validator in **C** that filters out anomalous files.

An image containing the current pipeline configuration is located at `/app/config.png`. It contains two pieces of handwritten information you will need:
1. `REF_VECTOR`: A 3-dimensional reference vector `(x, y, z)`.
2. `THRESHOLD`: A minimum cosine similarity score.

(Note: `tesseract` is preinstalled on this system if you need to perform OCR).

Write a C program at `/home/user/validator.c` and compile it to `/home/user/validator`. 

**Program Specifications:**
- The program must take exactly one command-line argument: the path to a CSV file.
- The input CSV files will have a header `id,x,y,z` followed by rows of tabular data (where `id` is an integer, and `x,y,z` are floats).
- For each row, calculate the cosine similarity between the row's `(x,y,z)` vector and the `REF_VECTOR`.
- **Acceptance:** If ALL rows in the CSV have a cosine similarity $\ge$ `THRESHOLD`, the program must exit with status code `0` (Clean).
- **Rejection:** If ANY row in the CSV has a cosine similarity $<$ `THRESHOLD`, or if any row's vector has a magnitude of 0 (which makes cosine similarity undefined), the program must exit with status code `1` (Evil/Corrupted).

You must successfully compile `/home/user/validator`. The automated verifier will call your compiled binary directly against a suite of test CSV files to ensure it perfectly separates clean data from corrupted data. Ensure your program handles file reading efficiently and links against necessary numerical libraries.