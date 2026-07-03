You are an MLOps engineer tasked with analyzing experiment artifacts. You have a set of model configurations and their corresponding multi-dimensional metrics stored in two CSV files. 

Your objective is to write and run a C++ program that joins these data sources, computes a composite score using a linear algebra operation (dot product) with a provided weight vector, aggregates the results by model family, and outputs a summary report.

**Data sources (to be created by you based on the description, or assume they exist, but actually I will provide the files in the environment)**:
Actually, I have already placed the following files in `/home/user/`:
- `/home/user/configs.csv`: Contains `run_id` and `model_type` (comma-separated, with header `run_id,model_type`).
- `/home/user/metrics.csv`: Contains `run_id` and 5 numerical performance indicators (comma-separated, with header `run_id,m1,m2,m3,m4,m5`).
- `/home/user/weights.txt`: Contains exactly 5 floating-point weights, one per line.

**Your task**:
1. Write a C++ program (e.g., `/home/user/analyze.cpp`).
2. The program must read `configs.csv` and `metrics.csv`, joining the rows on `run_id`.
3. Read the 5 weights from `weights.txt` into a vector.
4. For each run, compute the "Composite Score" as the dot product of the run's 5 metrics and the weight vector. Ensure double precision is used for numerical accuracy.
5. Aggregate the runs by `model_type`, computing the mean Composite Score for each model type.
6. Write the results to `/home/user/report.csv` without a header row. Each line should be formatted as `model_type,mean_score`.
7. The output must be sorted in descending order of the mean score.
8. Format the mean score to exactly 4 decimal places.
9. Compile and run your program to produce the final `report.csv`.

You may use standard C++ libraries. No external libraries (like Eigen or Boost) are required or provided, but you may install them if you wish. Standard `std::vector` and `<fstream>` are sufficient.