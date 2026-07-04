You are a performance engineer debugging a newly written Python microservice for graph analysis. The service calculates PageRank, but users are reporting that the results are inaccurate, and the iterative solver often fails to converge or suffers from severe precision loss.

Here is your task:
1. The research team sent a screenshot of the required algorithm parameters (damping factor and convergence tolerance). The image is located at `/app/config.png`. You will need to extract these values (hint: tesseract is available).
2. Inspect the buggy microservice located at `/app/pagerank.py`. You need to:
   - Fix the convergence failure. There is a mathematical flaw in the update step causing it to drift.
   - Fix the precision loss issue. The code is inappropriately truncating floats.
   - Update the code to use the exact `DAMPING` and `TOLERANCE` values extracted from `/app/config.png`.
3. The script `/app/pagerank.py` is an HTTP server. Fix it and run it so it listens on `127.0.0.1:8080`.
4. The server must expose a `POST /calculate` endpoint.
   - It should accept JSON in the format: `{"graph": {"A": ["B", "C"], "B": ["C"], "C": ["A"]}}`
   - It should return JSON in the format: `{"ranks": {"A": 0.4, "B": 0.2, "C": 0.4}, "iterations": 15}` (values are examples).

Ensure your fixed service remains running in the background or foreground so it can be tested. Do not change the overall framework of the server (using standard `http.server`), just fix the core logic and parameters.