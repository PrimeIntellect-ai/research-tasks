I am a researcher organizing a massive JSONL dataset of atmospheric sensor readings. I have a custom Go-based data parser that uses a vendored JSON parsing library to extract specific fields and convert them into a compressed CSV format, but the environment is currently broken.

Here is what you need to do:
1. I have a vendored package located at `/app/vendor/github.com/buger/jsonparser`. However, the build is failing because a deliberate perturbation was introduced: the main `parser.go` file has a corrupted import path (using `math/rand/v2` instead of `math/rand`) and a broken symlink for the internal `bytesafe` module located in `/app/vendor/github.com/buger/jsonparser/bytesafe`.
2. Fix the source code and rebuild my parsing tool located at `/home/user/workspace/dataparser`.
3. The dataset is located at `/home/user/raw_data/sensors.jsonl`. However, the files have some macro-inserted boilerplate lines starting with `DEBUG_MACRO::` that break the JSON parser. Strip these lines out using standard command-line text editing tools.
4. Run the compiled Go tool on the cleaned JSONL file to extract the `timestamp`, `sensor_id`, and `reading_value` fields. 
5. The tool outputs a CSV. You must compress this CSV using gzip and save it to `/home/user/organized_datasets/latest_readings.csv.gz`.
6. Create a symbolic link to this compressed file at `/home/user/latest.csv.gz`.

Please execute these steps. The final success will be measured by evaluating the size and structural integrity of `/home/user/latest.csv.gz`.