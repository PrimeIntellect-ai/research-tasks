As an MLOps engineer, we have a legacy experiment tracking pipeline that parses artifact metadata. Recently, a bug was introduced where integer metadata keys were silently being converted to floats due to missing values (NaNs) in our data pipelines, causing hashing mismatches downstream.

We need you to build a C++ program that corrects this metadata processing and performs a robust statistical aggregation. 
First, look at the image located at `/app/experiment_schema.png`. Use OCR to extract the exact schema definition and the target tolerance value for our hypothesis testing module.

Next, implement a C++ program at `/home/user/pipeline.cpp`. This program must:
1. Read input data from standard input. The input will be sequences of metadata records (experiment ID, timestamp, artifact size, metric value).
2. Handle missing metrics appropriately without casting artifact sizes (which are integers) to floats.
3. Compute a dense embedding representation of the experiment features using basic linear algebra operations (projection matrix will be provided as input).
4. Perform a simple cross-validation split and output the confidence interval of the metrics.

Your C++ program must compile to `/home/user/pipeline`. We have a reference oracle binary at `/opt/oracle/pipeline_ref` that processes these artifact streams correctly. Your compiled program must produce bit-exact equivalent output to this oracle when given the same standard input.