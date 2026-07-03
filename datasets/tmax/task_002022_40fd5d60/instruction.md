You are a data engineer validating an ETL pipeline. The pipeline processes large-scale numerical telemetry data and compresses the output. Before moving these files to cold storage, you need to perform a numerical accuracy and statistical test on the latest batch.

Two gzipped text files have been produced by the pipeline:
1. `/home/user/data/vector_a.txt.gz`
2. `/home/user/data/vector_b.txt.gz`

Each file contains exactly 10,000 lines of single-column floating-point numbers.

Your task is to compute two metrics using standard Linux utilities and/or a scripting language of your choice (you may install Python packages like `numpy` via pip if you prefer, or do it purely in bash/awk):
1. **Dot Product**: The linear algebra dot product of vector A and vector B.
2. **Correlation**: The Pearson correlation coefficient between vector A and vector B.

Write the final computed metrics to a log file located at `/home/user/etl_metrics.log`. The file must exactly match this format:
```
DOT_PRODUCT=<value_rounded_to_2_decimal_places>
CORRELATION=<value_rounded_to_4_decimal_places>
```

For example:
```
DOT_PRODUCT=1234567.89
CORRELATION=0.9876
```

Ensure you handle the gzipped files efficiently without permanently extracting them to disk if possible.