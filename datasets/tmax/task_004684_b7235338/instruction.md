You are a localization engineer at a software company. The translation system has a bug where it occasionally corrupts character encodings (Mojibake) and fails to populate certain translation keys, leaving them as `null`.

Your manager has recorded a short video presentation containing the exact rules for fixing the encodings and imputing the missing translations. The video is located at `/app/loc_rules.mp4`.

Your task is to:
1. Extract and analyze the video frames to read the encoding fixes and imputation rules. (Tools like `ffmpeg` and `tesseract-ocr` are available on the system).
2. Write a Python script at `/home/user/process_loc.py` that acts as a robust data processing filter. 

The script `/home/user/process_loc.py` must behave as follows:
- It should read a single line of JSON from Standard Input.
- The input JSON will have the following schema:
  ```json
  {
    "name": "User Name",
    "strings": {
      "greeting": null,
      "farewell": "Au revoir, l'Ã©tudiant",
      "error": null
    }
  }
  ```
- Apply the character encoding fixes (found in the video) to all string values inside the `"strings"` dictionary.
- Impute any `null` values inside the `"strings"` dictionary using the rules from the video. If the imputation rule contains `{name}`, you must interpolate it using the value of the top-level `"name"` field.
- Compute summary statistics and add a `"stats"` object to the top level of the JSON:
  - `total_keys`: The total number of keys in the `"strings"` dictionary.
  - `null_keys`: The number of `null` values in the `"strings"` dictionary *before* any imputation occurred.
- Pipeline logging: For every processed JSON, print a log message to Standard Error in the exact format: `[INFO] Processed user: <name>, nulls: <null_keys>`.
- Finally, print the resulting JSON string to Standard Output on a single line, and exit cleanly.

Ensure your code handles Unicode correctly and relies solely on the standard library for the JSON manipulation. Your script will be tested against a massive suite of randomized inputs to ensure bit-exact equivalence with our internal reference implementation.