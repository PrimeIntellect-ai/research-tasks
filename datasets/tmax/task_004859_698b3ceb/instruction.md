You are a mobile build engineer troubleshooting our automated pipeline analytics. We recently started embedding encoded build metrics directly into our pipeline recording videos, but the extraction and evaluation tooling is broken. 

You need to fix our C-based evaluation library, extract the encoded equations from the video, and expose a rate-limited API to serve the results.

Here is the situation:
1. **Video Extraction**: There is a video at `/app/build_metrics.mp4`. The video encodes mathematical expressions via solid colored frames. Most frames are gray, but specific frames flash colors that map to characters:
   - Red (#FF0000) = `+`
   - Green (#00FF00) = `-`
   - Blue (#0000FF) = `*`
   - Yellow (#FFFF00) = `1` (Consecutive yellow frames sum together, e.g., 3 yellow frames = `3`)
   - White (#FFFFFF) = `(`
   - Black (#000000) = `)`
   - Cyan (#00FFFF) = `=` (Indicates the end of an expression sequence)
   You must use `ffmpeg` and Python to extract these expressions in order. Every expression ends with a Cyan frame.

2. **C Library Fixes**: We use a C utility located at `/home/user/matheval/` to evaluate these expressions. However, `make` currently fails due to a linking error. Even if you fix the Makefile, the code in `evaluate.c` has a buffer overflow and a use-after-free bug that causes a segfault on complex expressions. Fix the `Makefile` and `evaluate.c`, then compile it to a shared library `libmatheval.so`.

3. **API Orchestration**: Create a Python HTTP API using your preferred framework (e.g., Flask or FastAPI) that binds to `127.0.0.1:8000`. 
   - It must have an endpoint `POST /api/v1/query`.
   - It should accept JSON: `{"expression_index": N}` (where N is the 0-based index of the expression found in the video).
   - It must validate requests by requiring an `Authorization: Bearer build-ops-xyz-99` header. Return 401 if missing/invalid.
   - It must implement rate limiting: maximum of 3 requests per minute per IP address. Return HTTP 429 if exceeded.
   - For valid requests, it should call into your fixed `libmatheval.so` using Python's `ctypes`, evaluate the Nth expression extracted from the video, and return JSON: `{"index": N, "expression": "extracted_string", "result": <evaluated_int>}`.

Leave the API server running in the background. Write your API server code to `/home/user/server.py` and start it. You can log your extracted expressions to `/home/user/extracted_expressions.txt` (one per line) for your own debugging.