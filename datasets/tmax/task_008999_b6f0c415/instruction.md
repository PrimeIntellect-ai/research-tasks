You are a data engineer building an ETL pipeline to process raw tabular data and perform inference using a lightweight linear model. 

We have a C++ program at `/home/user/etl.cpp` that is supposed to read raw feature data from `/home/user/data.csv`, aggregate the data, run inference, and output the results to `/home/user/predictions.csv`.

Currently, the pipeline runs, but the output is completely wrong. It produces incorrect values much like a matplotlib script that produces blank plots due to a silent configuration error. Your job is to debug the C++ code, recompile it, and generate the correct predictions.

Here is the specification for the pipeline:
1. **Input**: Read `/home/user/data.csv` (contains a header `id,f1,f2`).
2. **Aggregation**: Group the rows by `id`. For each `id`, calculate the arithmetic **mean** of feature `f1` and the **mean** of feature `f2`.
3. **Inference**: Apply a linear model to the aggregated features. The model architecture is a simple dot product plus bias:
   - Weight for f1: `0.5`
   - Weight for f2: `1.2`
   - Bias: `0.1`
   - Equation: `prediction = (mean_f1 * 0.5) + (mean_f2 * 1.2) + 0.1`
4. **Output**: Write the results to `/home/user/predictions.csv` with the header `id,prediction`. 
   - The output must be sorted by `id` in ascending order.
   - The `prediction` values must be formatted to exactly 1 decimal place (e.g., `7.6`).

Identify the logical and numerical bugs in `/home/user/etl.cpp`, fix them, compile the code (`g++ -O3 etl.cpp -o etl`), and run it to produce the correct `/home/user/predictions.csv`.