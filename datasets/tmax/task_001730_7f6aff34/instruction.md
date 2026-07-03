I am a machine learning engineer trying to prepare a reproducible training dataset, but my pipeline is broken. I have a multi-service setup running locally:

1. A data generation server running on `127.0.0.1:8081` (provides a continuous stream of raw sensor data).
2. A Redis instance on `127.0.0.1:6379`.
3. A visualization reporting service managed by a script at `/home/user/pipeline/start_report_service.sh`.

Right now, two things are wrong. 

First, the C++ data processor at `/home/user/pipeline/processor.cpp` is incomplete. It currently fetches 1000 floating-point numbers from `http://127.0.0.1:8081/data` but writes them raw. You need to implement the missing value and outlier handling directly in `processor.cpp`:
- Identify missing values (represented exactly as `-9999.0`).
- Replace these missing values with the mean of all *valid* values in the 1000-point batch.
- After handling missing values, clamp any outliers to the range `[-10.0, 10.0]` (i.e., values > 10.0 become 10.0, values < -10.0 become -10.0).
- Save the resulting 1000 cleaned floating-point numbers to `/home/user/pipeline/cleaned_data.csv`, with one number per line, formatted to 4 decimal places.
- Compile and run this C++ program. Use `g++ -O3 processor.cpp -o processor -lcurl` to compile.

Second, the reporting service (`/home/user/pipeline/start_report_service.sh`) starts a Python script that reads `cleaned_data.csv` and generates a plot. However, it currently produces blank plots or crashes because of a missing backend misconfiguration for Matplotlib in a headless server environment. Fix the startup script so the Python service successfully generates the plot.

After fixing both components, ensure the C++ processor has generated `/home/user/pipeline/cleaned_data.csv` and execute `./start_report_service.sh` to produce `/home/user/pipeline/report.png`.