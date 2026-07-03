I am a researcher organizing some legacy scientific logs, and I need your help setting up my processing pipeline.

First, I have a custom log extraction tool located in `/app/fast-extractor-1.0`. I need to build it, but it crashes when I run it on my data because the maximum line length is set too small in the Makefile (it is currently set to `10`, but it should be `1024`). Please fix the Makefile, compile the tool by running `make` in that directory, and ensure the `fast-extract` binary is successfully built.

Second, I need a standalone bash script at `/home/user/transform.sh` that will process the extracted logs. The script must read lines from standard input. The input data will be encoded in `Windows-1252`. 
Your script must:
1. Convert the input stream from `Windows-1252` to `UTF-8`.
2. Parse the converted text as colon-separated fields (`:`).
3. Filter the lines: only keep lines where the exact value of the second field is `CRITICAL`.
4. For those matching lines, replace the second field's value with `RESOLVED`.
5. Print the resulting lines to standard output, maintaining the colon separation.

Please ensure `/home/user/transform.sh` is executable and works perfectly as a standard Unix filter (reading from stdin, writing to stdout).