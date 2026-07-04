You are a data analyst tasked with building a reproducible Bash pipeline to process a batch of matrix data stored in CSV files. 

Your raw data is located in `/home/user/data/raw/`. Each file is a CSV containing a square matrix of floating-point numbers (no headers).

You need to write a standalone, executable Bash script at `/home/user/process_matrices.sh` that performs the following steps:

1. **Dependency Management**: The script must create a Python virtual environment at `/home/user/venv`, activate it, and install `numpy`.
2. **Storage Management**: Create a directory `/home/user/data/processed/`.
3. **Linear Algebra Analysis**: For every `.csv` file in `/home/user/data/raw/`, compute the *trace* of the matrix (the sum of the elements on the main diagonal). You should use Python with `numpy` invoked from within your Bash script to do this computation.
4. **Filtering and Logging**: If the trace is greater than or equal to `20.0`:
   - Copy the CSV file to `/home/user/data/processed/`.
   - Append a line to `/home/user/data/processed/summary.log` in the exact format: `filename.csv: <trace>`, where `<trace>` is rounded to exactly two decimal places (e.g., `matrix_3.csv: 22.45`). The files in the log should be sorted alphabetically.
5. **Archiving**: Compress the entire `/home/user/data/processed/` directory into a tarball at `/home/user/archive.tar.gz` (the tarball should extract to `processed/...` or `home/user/data/processed/...`).

Requirements:
- Your Bash script must be fully self-contained, reproducible, and executable (`chmod +x`).
- Execute your script to process the raw data and produce the final `archive.tar.gz`.
- Do not hardcode the names of the files in your script; it should discover any `.csv` files in the raw directory dynamically.