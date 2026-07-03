You are an MLOps engineer investigating a mysterious data leakage issue in our legacy experiment tracking pipeline. We use a proprietary tool to tokenize and encode text artifacts from our machine learning experiments. We suspect the tool has a bug similar to calling `fit_transform` on test data—it seems to be updating its internal token dictionary even when processing "evaluation" stage artifacts, causing train/test leakage.

Unfortunately, the original source code for this tokenization encoder is lost. All we have is a stripped binary located at `/app/leaky_encoder`. 

Your task is to reverse-engineer the exact behavior of this binary (either via black-box testing with bash scripts or reverse engineering) and reimplement it perfectly in Go. 

The binary operates as follows:
- It reads a newline-separated list of JSON objects from standard input.
- Each JSON object has two fields: `"stage"` (either `"train"` or `"eval"`) and `"text"` (a string of space-separated alphanumeric words).
- It outputs a space-separated sequence of integer tokens for each line.

You must create a Go program at `/home/user/replicate.go` that, when compiled to `/home/user/replicate`, behaves **exactly** like `/app/leaky_encoder` for any valid sequence of input JSONs. 

Requirements:
1. Set up your Go environment and necessary packages to handle standard I/O and JSON parsing.
2. Analyze `/app/leaky_encoder` to deduce how it maps words to integers, how it manages its internal dictionary, and critically, how the "eval" stage leakage bug manifests. (You will notice it assigns integer IDs starting from 1 to new words it encounters).
3. Write your Go solution in `/home/user/replicate.go`.
4. Build your program to `/home/user/replicate`. 
5. Ensure that your program's stdout exactly matches the binary's stdout for identical stdin. It must process the input stream line by line.

An automated fuzzer will run your compiled `/home/user/replicate` alongside `/app/leaky_encoder` with thousands of randomized inputs to ensure bit-exact equivalence.