You are a data engineer building a real-time ETL processing service.

We have an audio file located at `/app/auth_token.wav`. This file contains a single spoken English word. 
First, transcribe the audio file (you may use any available tools like Python's `SpeechRecognition` or `ffmpeg` to assist you). The lowercase version of this spoken word is the secret authentication token for your service.

Next, write and start an HTTP server in Go. The source file should be saved at `/home/user/etl_server.go` and the service must listen on `127.0.0.1:9090`.

Your Go server must implement a single endpoint:
`POST /process`

**Authentication:**
The endpoint must require an `Authorization: Bearer <secret_token>` header, where `<secret_token>` is the transcribed lowercase word from the audio file. If the token is missing or incorrect, return a `401 Unauthorized` status code.

**Payload & Processing (ETL Pipeline):**
The endpoint will receive a `multipart/form-data` request with a file field named `dataset`.
This dataset is a large CSV file with the following characteristics:
1.  **Character Encoding:** The file is encoded in `ISO-8859-1`, NOT UTF-8.
2.  **Wide Format:** The CSV has a header row: `EmployeeID,FullName,Jan_Sales,Feb_Sales,Mar_Sales`
3.  **Data constraints:** It may contain duplicate records and missing data.

Your Go server must stream-read this uploaded file (do not load the entire file into memory at once) and perform the following transformations:
1.  **Decoding:** Convert the text from ISO-8859-1 to UTF-8.
2.  **Reshaping (Wide to Long):** Transform the data from the wide format into a long format with the logical columns: `EmployeeID`, `FullName`, `Month`, `Sales`. (Month should be "Jan", "Feb", or "Mar").
3.  **Cleaning & Normalization:**
    *   Convert the `FullName` field to uppercase.
    *   Drop any long-format record where the `Sales` value is empty or missing.
4.  **Deduplication:** Ensure the output contains only unique records based on the composite key `(EmployeeID, Month)`. If duplicates exist for the same employee and month, keep the first one encountered in the stream and discard subsequent ones.

**Response:**
Return a `200 OK` status with the processed dataset as a JSON array of objects. The JSON keys must be `employee_id`, `full_name`, `month`, and `sales`. E.g.,
```json
[
  {"employee_id": "101", "full_name": "JANE DOE", "month": "Jan", "sales": "4500"},
  ...
]
```

Run the server in the background once it is ready so it can be verified.