You are an MLOps engineer tasked with fixing and deploying a high-performance C-based ML inference service. We use a custom vendored library, `libcml`, for inference. 

Currently, the pipeline has three major issues:
1. **Performance/Build issues:** The inference benchmarking tests fail because the library runs extremely slowly. The build process seems to be ignoring optimization flags, and there might be a linker error preventing it from building at all in some environments.
2. **Reproducibility/Data Leak:** Our pipeline reproducibility tests are failing. We found that predictions for the exact same input features vary depending on the other items in the inference batch. This implies a data leak between items or a state issue where the server recalculates scaling statistics on the fly (a classic `fit_transform` applied to test data) instead of using the model's pre-computed parameters.
3. **Model Selection:** We have 3 trained models (`/app/models/model_A.bin`, `/app/models/model_B.bin`, `/app/models/model_C.bin`) but we don't know which has the best hyperparameters.

Your tasks:

**Step 1: Fix the Vendored Package**
Inspect the library source at `/app/vendored/libcml-0.4.2`. 
- Fix the `Makefile` so that it correctly links the standard math library and allows overriding `CFLAGS` (it must support compiling with `-O3` for our inference performance benchmarking to pass).
- Inspect `cml.c`. Fix the inference data leak so that the library properly uses the model's pre-computed mean/std via the existing `cml_transform_scale` function, rather than improperly fitting on the inference batch.

**Step 2: Cross-validation / Model Selection**
Using the fixed `libcml` library, evaluate the three models in `/app/models/` against the validation dataset at `/app/data/val.csv`. The CSV has no header; the first 4 columns are features, and the last column is the true target value.
Identify the model with the lowest Mean Squared Error (MSE). 

**Step 3: Deploy the Inference Service**
Create and run a C-based TCP inference server at `/home/user/infer_server.c`. 
Compile it (linking your fixed `libcml` and utilizing `-O3`).
The server must bind to `127.0.0.1:8888` and implement the following line-based TCP protocol:
1. Upon connection, the server must wait for an authentication line: `AUTH: m10ps_t0k3n\n`
   - If the token is incorrect or missing, close the connection immediately.
2. The client will send one or more prediction requests in the format: `PREDICT: f1,f2,f3,f4\n` (where f1..f4 are floating point numbers).
3. The server must load the single best model you identified in Step 2, run inference on the requested features using the fixed `libcml` functions, and respond with: `RESULT: <prediction>\n` (format as `%.4f`).
4. The client may send `QUIT\n` to cleanly close the connection.

Leave the server running in the background when you are finished.