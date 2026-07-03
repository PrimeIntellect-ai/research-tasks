You are a data scientist who needs to clean and merge user activity logs from two different systems: a legacy forum and a new mobile app. 

You must write a pure Bash script (using standard CLI tools like `awk`, `sed`, `iconv`, `date`, `grep`, etc. - NO Python, Perl, or Ruby) located at `/home/user/process.sh` that processes the following two datasets and outputs a single cleaned CSV file at `/home/user/cleaned_logs.csv`.

**Input Datasets:**
1. `/home/user/data/legacy.csv`
   - Encoding: ISO-8859-1
   - Fields: `Timestamp,Name,Email,IP,Age,Score`
   - Timestamp format: `YYYY/MM/DD HH:MM:SS` (Assumed UTC)
   - Note: Contains non-ASCII characters (like accented names).

2. `/home/user/data/app.csv`
   - Encoding: UTF-8
   - Fields: `Timestamp,Name,Email,IP,Age,Score`
   - Timestamp format: `YYYY-MM-DDTHH:MM:SSZ` (ISO 8601, UTC)

**Processing Requirements:**
1. **Character Encoding:** Unify everything to UTF-8. 
2. **Timestamp Alignment:** Convert all timestamps to standard Unix Epoch seconds.
3. **Data Masking (Anonymization):**
   - **Name:** Drop the `Name` column entirely from the final output.
   - **Email:** Mask the username portion (everything before the `@`) with `***`. (e.g., `john.doe@example.com` becomes `***@example.com`).
   - **IP Address:** Mask the last octet of the IPv4 address with `0` (e.g., `192.168.1.45` becomes `192.168.1.0`).
4. **Constraint-based Validation:** 
   - Keep only rows where `Age` is a valid integer between 18 and 100 (inclusive).
   - Keep only rows where `Score` is a valid integer between 0 and 1000 (inclusive).
   - Drop any row that fails these validation rules.
5. **Output Formatting:**
   - The final file `/home/user/cleaned_logs.csv` must be a headerless CSV.
   - The output columns must be: `EpochTime,MaskedEmail,MaskedIP,Age,Score`.
   - The final file must be sorted chronologically by the `EpochTime` (ascending).

**Example:**
An input row in `legacy.csv`:
`2023/10/05 14:00:00,José,jose123@mail.com,203.0.113.42,30,850`
Should become:
`1696514400,***@mail.com,203.0.113.0,30,850`

Create and run the script `/home/user/process.sh` to generate the final cleaned dataset.