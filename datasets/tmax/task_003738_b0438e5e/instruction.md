You are an operations engineer triaging a critical incident in our quantitative pricing pipeline. Our math engine service (written in C++) has been failing and producing erratic risk scores for the past few hours. We need you to diagnose the issue, fix the code, and re-run the pipeline.

Here is the situation:
1. **Logs & Timeline:** The data ingestion service writes to `/app/logs/ingest.log` and the C++ math engine writes to `/app/logs/engine.log`. The timestamps are in different timezones/formats. You need to reconstruct the timeline to figure out when the erratic outputs started, which corresponds to a subtle change in the upstream data format.
2. **Format Parsing Issue:** The upstream data provider recently started sending some floating-point numbers in a legacy format (e.g., using 'D' instead of 'E' for exponents, like `1.45D-03`). The C++ parser in `/app/src/engine.cpp` does not handle this edge case, causing truncation or parsing errors.
3. **Numerical Instability:** The core calculation `score = (x * y) / (x - y + alpha)` is experiencing numerical instability (blowups) when `x` and `y` are very close. 
4. **Missing Parameter:** The `alpha` regularization parameter was accidentally hardcoded to `0.0` during a recent refactor. The correct `alpha` value was noted in a screenshot of an old dashboard taken before the incident. This image is located at `/app/incident_artefacts/dashboard_snapshot.png`. You will need to extract this parameter (you can use `tesseract` which is installed on the system).

Your task:
1. Extract the `alpha` parameter from `/app/incident_artefacts/dashboard_snapshot.png`.
2. Inspect the logs in `/app/logs/` and the source code in `/app/src/engine.cpp` to understand how the parsing fails on the raw data `/app/data/input.csv`.
3. Fix the parsing logic in `/app/src/engine.cpp` to correctly handle the legacy exponent format.
4. Update the math logic in `/app/src/engine.cpp` to use the extracted `alpha` parameter to prevent numerical instability.
5. Recompile the C++ application (you can use `g++ -O3 /app/src/engine.cpp -o /app/bin/engine`).
6. Run the compiled engine on `/app/data/input.csv` and write the output to `/app/output/scores.csv`.

The output file `/app/output/scores.csv` must be a CSV with two columns: `id,score`.
The automated verifier will evaluate the Mean Squared Error (MSE) of your output scores against a private reference implementation. To pass, the MSE must be less than `1e-5`.