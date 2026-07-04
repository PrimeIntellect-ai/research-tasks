You are an automation specialist tasked with creating a robust, parallelized log processing pipeline. We have a stream of JSON-Lines logs containing PII and timestamps, but our previous parser failed on complex Unicode escape sequences (specifically UTF-16 surrogate pairs) and processed logs too slowly. 

Your job is to write a high-performance Rust CLI tool that reads JSON-Lines from `stdin`, processes the logs in parallel while preserving order, and writes the output to `stdout`.

First, you must determine the processing rules by analyzing a calibration video located at `/app/calibration.mp4`. The video contains a sequence of solid colored frames.
1. Count the number of strictly red frames (RGB: 255, 0, 0). Let this number be `H`.
2. Count the number of strictly green frames (RGB: 0, 255, 0). Let this number be `N`.

Once you have your configuration, create a Rust project in `/home/user/log_processor` and build a binary named `anonymizer`. It must be compiled in release mode and copied to `/home/user/anonymizer`.

The `anonymizer` must do the following for each JSON line received on `stdin`:
- Parse the JSON object. Expected fields: `timestamp` (ISO-8601 string), `user_name` (string), and `message` (string). The `user_name` and `message` fields may contain complex Unicode characters and escaped surrogate pairs (e.g., `\uD83D\uDE00`).
- **Timestamp Alignment:** Parse the `timestamp`, add exactly `H` hours to it, and re-format it as an ISO-8601 string with a `Z` suffix.
- **Data Masking:** Replace the entire string value of `user_name` with exactly `N` repetitions of the Unicode block character '█' (`U+2588`).
- **Parallel Processing:** You must process the lines in parallel (e.g., using `rayon`) but the output lines on `stdout` must be in the exact same order as they appeared in `stdin`.
- Unrecognized fields should be passed through unchanged.

Your final binary will be automatically tested against a reference oracle with thousands of randomized JSON lines containing complex Unicode inputs. Any deviation in the stdout output will result in failure.