You are an AI assistant acting as a technical compliance officer. We are auditing a financial system for circular transaction patterns (indicative of money laundering) and system deadlock vulnerabilities.

You have been provided with an artefact at `/app/compliance_log.mp4`. This video is a screen recording of a terminal outputting batch transaction logs that were lost from the main database. 

Your task is to:
1. **Extract Data:** Use `ffmpeg` to extract frames from the video and an OCR tool (like `tesseract`) to read the transaction records. The records follow the format: `TXN: <SENDER_ID> -> <RECEIVER_ID> : <AMOUNT>`.
2. **Reconstruct Database:** Create a SQLite database at `/home/user/audit.db` with a table `transactions (tx_id TEXT, sender TEXT, receiver TEXT, amount REAL)`. Insert the extracted records.
3. **Graph Analysis (Recursive Queries):** Write a Python script using SQLite recursive CTEs to find all circular transaction chains of exact length 3 (e.g., A -> B -> C -> A). 
4. **Deadlock Simulation:** Write a Python function `trigger_deadlock()` that intentionally deadlocks two concurrent SQLite connections by updating rows involved in one of the discovered cycles in reverse order.
5. **Expose an API:** Create and run a Python web service (e.g., using Flask or FastAPI) that listens on `127.0.0.1:9090`. 
    - The API must require the HTTP header `X-Compliance-Key: alpha-audit-99`.
    - Endpoint `GET /api/cycles`: Returns a JSON array of arrays, where each inner array is a sequence of 3 `sender` IDs forming a cycle, ordered alphabetically by the first ID in the cycle.
    - Endpoint `POST /api/deadlock`: Invokes your `trigger_deadlock()` function and returns `{"status": "deadlocked"}` once the database lock error is caught.

Make sure your web service remains running in the foreground or background so our automated verifier can query it. You may install any Python packages you need (e.g., `fastapi`, `uvicorn`, `pytesseract`, `opencv-python`).