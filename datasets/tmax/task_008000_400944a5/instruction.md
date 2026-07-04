You are tasked with building a data processing pipeline to clean and normalize raw configuration change logs. As a configuration manager, you have received a messy log file at `/home/user/raw_changes.txt`. A previous CSV-based pipeline silently dropped records that contained embedded newlines in their notes, so we are moving to a custom parser that outputs JSON Lines.

Your goal is to parse the text file, extract the structured information, apply data masking, impute missing values, and output a clean JSON Lines file and a pipeline log.

### Input Data Format
`/home/user/raw_changes.txt` contains multiple configuration change records. 
Each record is separated by a line containing exactly three dashes: `---`.
Within a record, fields are listed as `Key: Value`. The possible keys are `Ticket`, `Date`, `IP`, `Password`, and `Notes`.
The `Notes` field may span multiple lines (embedded newlines). It will always be the last field in a record if it exists.

### Processing Requirements
Write a script in any language to process the file and generate `/home/user/processed_changes.jsonl`. For each record, create a JSON object with the following rules:

1. **Extraction & Normalization**:
   - `ticket_id`: String. The value of `Ticket`.
   - `notes`: String. The value of `Notes`. Normalize this by replacing any newline characters *within* the notes with a single space. Strip leading/trailing whitespace.
2. **Imputation**:
   - `timestamp`: String. The value of `Date`. If the `Date` field is missing or empty in a record, impute it by using the `timestamp` from the *immediately preceding* record. (The first record will always have a valid Date).
3. **Data Masking & Anonymization**:
   - `target_ip`: String. The value of `IP`. Mask the first two octets of the IPv4 address with `X`. For example, `192.168.1.50` becomes `X.X.1.50`.
   - `password`: String. If a `Password` field exists, its value must be replaced entirely with the literal string `[REDACTED]`. If it doesn't exist, omit the key or set to null.

### Pipeline Logging
Your script must also generate a log file at `/home/user/pipeline.log` containing exactly three lines detailing the pipeline's execution:
1. `Total records processed: <N>` (Total number of valid records parsed)
2. `Records with imputed dates: <M>` (Count of records where the Date was missing and had to be copied from the previous record)
3. `Records with masked passwords: <P>` (Count of records where a Password field was found and redacted)

Ensure your script handles the embedded newlines in the Notes field properly without splitting records incorrectly.