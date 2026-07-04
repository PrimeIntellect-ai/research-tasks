You are a machine learning engineer preparing a training dataset for a similarity search model. 

As part of your data ingestion pipeline, you must extract features from raw text files. We have a proprietary feature extractor provided as a compiled executable at `/app/legacy_embedder`. This executable takes a single file path as an argument and prints a 128-dimensional embedding vector (as space-separated floating-point numbers) to standard output. 

Unfortunately, some of the incoming training data is corrupted or maliciously crafted. When the `/app/legacy_embedder` processes these bad files, it outputs vectors that either:
1. Contain one or more `NaN` (Not-a-Number) values.
2. Have an L2 norm (Euclidean length) strictly greater than `10.0`.

Your task is to write a C++ program that acts as a filter for our dataset.
1. Create your source file at `/home/user/filter.cpp`.
2. Compile it to an executable named `/home/user/filter`.
3. Your executable must take exactly one command-line argument: the absolute path to a text file.
4. Your program must execute `/app/legacy_embedder <file_path>` as a subprocess and read its output.
5. Parse the 128-dimensional vector. 
6. Calculate its L2 norm.
7. If the vector contains any `NaN` values or its L2 norm is > 10.0, your program must terminate with exit code `1` (reject).
8. If the vector is valid and its L2 norm is <= 10.0, your program must terminate with exit code `0` (accept).

You can use standard C++ libraries. There are sample datasets you can test against in `/app/data/clean/` and `/app/data/evil/`.