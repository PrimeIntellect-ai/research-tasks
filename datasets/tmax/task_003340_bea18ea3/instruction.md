You are an engineer tasked with porting a high-performance signal processing module into a minimal containerized REST API. 

We have a legacy C library, `libfilter.so`, located at `/home/user/libfilter.so`. It contains a highly optimized mathematical filtering function, but we lack the original source code. The C function signature is known to be:
`void apply_filter(double* input, int width, int height, double* kernel, double* output);`
- `input`: 1D array representing a 2D matrix of size `width` x `height` (row-major).
- `kernel`: 1D array representing a 3x3 filter kernel (row-major, 9 elements).
- `output`: 1D array where the resulting filtered matrix of size `width` x `height` will be written.

Additionally, the specific 3x3 kernel matrix you must use for this deployment is documented in an image file located at `/app/kernel.png`.

Your objectives are:
1. Extract the 3x3 numerical kernel from `/app/kernel.png` using OCR (tesseract is installed) or another vision technique.
2. Build a Python REST API using Flask or FastAPI. The server must run on `127.0.0.1` at port `8000`.
3. Create a POST endpoint `/process` that accepts a JSON payload of the form:
   `{"width": W, "height": H, "data": [val1, val2, ...]}`
   where `data` is a flat list of `W * H` floats.
4. The `/process` endpoint must parse the input, invoke `apply_filter` from `libfilter.so` via Python's `ctypes` (handling ABI types correctly), using the 3x3 kernel you extracted from the image.
5. The endpoint must return a JSON response: `{"result": [out1, out2, ...]}` containing the flat output array.
6. Write a unit test script `/home/user/test_api.py` to verify your endpoint functions correctly.

Ensure your API server is running in the background before completing the task. An automated test will evaluate your API by sending a large random matrix and computing the Mean Squared Error (MSE) between your API's output and the true expected output calculated using the exact kernel. To pass, the MSE must be strictly less than 0.05.