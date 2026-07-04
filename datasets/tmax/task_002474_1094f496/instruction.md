You are a release manager preparing a high-throughput deployment router. Currently, incoming traffic is routed to the new deployment based on complex parameter evaluation rules (e.g., checking if user weight and score combinations exceed certain thresholds). 

We have a Python script `/home/user/baseline_router.py` that parses a list of request URLs, extracts the parameters, and evaluates a routing expression using pure Python `eval()`. However, `eval()` is far too slow and poses security risks. We need to process a dataset of 200,000 URLs very quickly.

To fix this, we want to use `tinyexpr`, a fast C-based mathematical expression evaluator. We have vendored the source code for `tinyexpr` in `/app/tinyexpr/`.

Your task is to:
1. Examine the vendored `tinyexpr` package in `/app/tinyexpr/`. You will need to compile it into a shared library (`libtinyexpr.so`) so it can be loaded via Python. Note: The provided Makefile might have a configuration issue that prevents compiling it as a position-independent shared object. You must identify and fix this issue, then compile the shared library.
2. Write a new Python script `/home/user/fast_router.py`. This script must:
   - Accept two arguments: the path to the input dataset and the output file path. (e.g., `python3 fast_router.py /home/user/requests.txt /home/user/results.txt`)
   - Read the mathematical routing rule from `/home/user/rule.txt`.
   - Read the dataset of incoming URLs from `/home/user/requests.txt`.
   - For each URL, parse the path and the query parameters (e.g., `/deploy/v2?a=12.5&b=4.2`).
   - Use Python's `ctypes` module to load `libtinyexpr.so` and evaluate the rule using the extracted parameters. The `tinyexpr` function `te_interp` evaluates an expression string.
   - For each URL, evaluate the expression. If the result is greater than 0, the request is routed (write `1` to the output file). Otherwise, write `0`.
   - The output file should contain exactly one integer (1 or 0) per line, corresponding to the input URLs.

Your script must be highly optimized. It will be timed. To pass, `fast_router.py` must complete the processing of 200,000 URLs in under **1.5 seconds**, and the outputs must exactly match the expected ground truth.

To test your script, you can run the baseline:
`python3 /home/user/baseline_router.py /home/user/requests.txt /home/user/baseline_results.txt`
And compare its output to yours. Ensure your script output is identical, but runs significantly faster.