You are an infrastructure engineer tasked with automating the provisioning of a new high-performance log ingestion pipeline. The previous pipeline used a slow combination of text processing pipelines (`awk`, `sed`, `grep`), and we need to replace the core normalization step with a fast C++ utility.

Your tasks are:
1. We have an image containing the business logic rules for the log normalizer located at `/app/pipeline_rules.png`. Read this image to understand the required log transformation logic.
2. Write a C++ program at `/home/user/parser.cpp` that reads text from standard input line by line, applies the exact transformation rules specified in the image, and writes the resulting formatted lines to standard output. 
3. Compile your C++ program to the executable path `/home/user/log_parser`.
4. Ensure your compiled executable is highly robust and handles varying numbers of columns, empty lines, and malformed spacing gracefully, matching the precise field-extraction logic of standard `awk`-style processing.

Your program will be rigorously tested against a reference implementation with thousands of randomized log lines. Ensure your binary strictly matches the expected output character-by-character.