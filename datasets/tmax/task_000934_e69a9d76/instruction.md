You are acting as a localization engineer. We have a legacy translation scoring engine provided as a stripped binary at `/app/scorer`. It evaluates the quality of translated text, but we don't have its source code. We need to build a new localization processing pipeline around it.

Your task is to write a C++ HTTP service that processes translation updates, scores them in parallel, maintains rolling statistics, and samples data for human review.

Requirements:
1. **Network Service**: Create a C++ HTTP server listening on `127.0.0.1:8080`. You may use a header-only library like `cpp-httplib` (you can download it into your workspace).
2. **Scoring via Stripped Binary**: The binary at `/app/scorer` expects two arguments: the original text and the translated text. You must figure out its exact CLI usage to get the float score it outputs. (Use tools like `strings` or run it to understand its input format).
3. **Parallel Processing**: 
   - Endpoint: `POST /translations`
   - Payload: A JSON array of translation objects, e.g., `[{"lang": "es", "orig": "Hello", "trans": "Hola"}, ...]`.
   - Your service must process these entries in parallel, invoking the `/app/scorer` binary for each to compute the score. Ensure it correctly handles Unicode multi-language text.
4. **Rolling Statistics**:
   - Keep a rolling average of the translation scores for the last 5 processed translations per language.
   - Endpoint: `GET /stats`
   - Response: JSON object mapping language codes to their rolling average score, e.g., `{"es": 0.85, "fr": 0.92}`.
5. **Data Sampling & Stratification**:
   - For translations scoring strictly less than 0.5, store exactly 1 sample per language in a file `/home/user/low_quality_samples.json`. This file should be updated atomically and contain a JSON array of these sampled translation objects. Keep only the most recent sample per language.
6. **Pipeline Scheduling**:
   - Write a shell script at `/home/user/flush_pipeline.sh` that makes a `POST /flush` request to your server. 
   - Set up a user crontab entry that runs this script every minute. The `/flush` endpoint in your server should just clear the rolling statistics.

Build your C++ server as `/home/user/loc_server` and leave it running in the background.

Constraints:
- Use standard C++17 or later.
- Handle multi-byte Unicode strings properly when passing to the binary.
- Ensure thread-safe access to your statistics and sampling data structures.