You are a data analyst setting up a reproducible data pipeline. We have encountered an issue where adversarial "leaky" data is entering our system, skewing our downstream classification and regression models. We have encoded the precise rejection criteria for our pipeline in an image located at `/app/reference_spec.png`.

Your task:
1. Extract the reference embedding vector and the numerical similarity threshold from the image `/app/reference_spec.png` (using OCR tools like `tesseract`, which is preinstalled).
2. Write a C program at `/home/user/detector.c` and compile it to an executable at `/home/user/detector`.
3. The compiled program must accept exactly one command-line argument: the path to a CSV file.
4. The input CSV files will have a header row `id,f1,f2,f3,f4,f5`, followed by multiple rows of data. The columns `f1` through `f5` represent a 5-dimensional feature embedding.
5. For each data row, your program must compute the Cosine Similarity between that row's feature vector and the reference embedding extracted from the image. 
6. **Filtering logic:** If *any* row in the CSV file has a cosine similarity greater than or equal to the threshold, your program must immediately terminate and exit with status code `1` (REJECT). 
7. If all rows are strictly below the threshold, the program must exit with status code `0` (ACCEPT).

Requirements:
- Parse the CSV accurately (skip the header).
- Compute cosine similarity using standard single-precision floats (`float`).
- Compile your code with standard math libraries (e.g., `gcc -O2 /home/user/detector.c -o /home/user/detector -lm`).
- Do not output anything to stdout/stderr in your final version; the verifier strictly relies on the exit code.

The automated verification suite will test your executable `/home/user/detector` against two hidden corpora: `/app/clean/` (which must be accepted) and `/app/evil/` (which must be rejected).