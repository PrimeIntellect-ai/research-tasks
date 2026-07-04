You are a localization engineer managing a pipeline that receives translated strings from an external vendor. The vendor's files often have inconsistent key formatting and occasionally contain anomalous data (e.g., extremely long strings caused by encoding errors or translator notes left in the text).

Your task is to write a Python script that processes an incoming French translation file against the English master file, and then set up a cron schedule for this script.

**1. Create the Data Processing Script**
Write a Python script at `/home/user/process_loc.py` that does the following:
*   **Inputs:** 
    *   Master English JSON: `/home/user/master_en.json`
    *   Incoming French JSON: `/home/user/incoming_fr.json`
*   **Normalization:** The vendor often messes up the translation keys. Before processing, normalize all keys in the incoming French JSON by converting them to completely lowercase and replacing any space characters (` `) with underscores (`_`).
*   **Validation & Anomaly Detection:** Compare the normalized incoming French keys/values against the master English keys/values.
    *   *Missing Keys:* Identify any keys present in the master file that are missing from the normalized incoming file.
    *   *Length Anomalies:* A translation is considered anomalous if its string length is strictly greater than 3 times the length of the corresponding English string in the master file.
*   **Outputs:**
    *   Generate a validation report at `/home/user/loc_report.json` with the following exact structure:
        ```json
        {
          "anomalies": ["list_of_anomalous_keys_here"],
          "missing": ["list_of_missing_keys_here"]
        }
        ```
        *(Sort both lists alphabetically).*
    *   Generate an approved translations file at `/home/user/approved_fr.json` containing only the normalized keys that are present in the incoming file, match a key in the master file, and are **not** flagged as length anomalies.

**2. Define the Pipeline Schedule**
The script needs to run daily at exactly 2:00 AM. Since we don't want to modify the actual system crontab in this environment, write the exact crontab line (using `python3 /home/user/process_loc.py` as the command) into a file named `/home/user/cron_schedule.txt`.

Ensure your Python script runs cleanly and generates the exact required output files.