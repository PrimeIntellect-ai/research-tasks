I am a researcher organizing a messy dataset from our latest lab runs, and I need an automated pipeline to extract the correct data and serve it. 

Here is what you need to do:

1. **Identify the Target Experiment:** 
   I scanned the lab label for the current batch. It's located at `/app/experiment_label.png`. Read the text from this image (you can use OCR tools like `tesseract` which are available on the system). Find the experiment identifier, which is written in the format `EXP_ID: <IDENTIFIER>`. The `<IDENTIFIER>` is the target experiment ID you will use for the next steps.

2. **Filter the Metadata:**
   The raw dataset is stored in `/app/raw_data/`. It contains a deep directory structure with various metadata files in JSON, CSV, and XML formats. 
   You must search through all files in `/app/raw_data/` and parse them to find the ones that belong to the target experiment:
   - For `.json` files, look for the top-level key `"experiment_id"`.
   - For `.csv` files, look for a column named `experiment_id`. A file matches if any row has the target experiment ID.
   - For `.xml` files, look for an `<experiment_id>` tag.

3. **Organize the Dataset:**
   Create a new directory at `/home/user/organized_dataset/<IDENTIFIER>/` (replace `<IDENTIFIER>` with the actual ID you found). 
   Copy all the matching files you found in step 2 into this new directory. Do not preserve the original directory structure from `/app/raw_data/`; just place all matching files directly into the new `<IDENTIFIER>` directory. (You may assume there are no filename collisions among the matching files).

4. **Generate a Manifest:**
   Inside `/home/user/organized_dataset/<IDENTIFIER>/`, create a file named `manifest.json`. 
   This file must contain a single JSON object where the keys are the base filenames of the copied files (e.g., `data1.json`) and the values are their SHA-256 checksums (as lowercase hex strings).
   *Do not include `manifest.json` itself in the manifest.*

5. **Serve the Dataset:**
   Bring up an HTTP server listening on `0.0.0.0:8000` that serves the root directory `/home/user/organized_dataset/`. Keep this server running so that my verification scripts can fetch the files over the network.

Ensure the server is running as your final step.