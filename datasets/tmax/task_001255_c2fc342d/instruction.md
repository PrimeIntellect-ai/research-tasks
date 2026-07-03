We are building a robust data processing pipeline for our audio event logs. I have an audio recording at `/app/instruction.wav` that contains a spoken instruction regarding a numeric adjustment we need to apply to our data.

Your task is to write a Python script at `/home/user/pipeline.py` that processes a CSV stream. 

First, recover the spoken instruction from `/app/instruction.wav` (it will be a short sentence telling you to add or subtract a specific integer amount from our values).

Next, write the script `/home/user/pipeline.py` so that it:
1. Reads a CSV from standard input (`stdin`). The CSV will have the columns: `id`, `event_name`, `timestamp`, `value`.
2. Some rows will have missing (empty) entries in the `value` column. Fill these missing values with the floor of the mean of the existing `values`.
3. Apply the numeric adjustment extracted from the audio file to all `value` entries.
4. Ensure the `value` column is represented as integers (a common pandas gotcha is that NaNs silently convert the column to floats, so make sure your final output has standard integers, not floats).
5. Write the resulting CSV to standard output (`stdout`), without the dataframe index.

Ensure your script is executable (`chmod +x`) and uses `#!/usr/bin/env python3`.
Your script must be strictly reproducible and will be tested against a reference implementation with multiple random CSV inputs.