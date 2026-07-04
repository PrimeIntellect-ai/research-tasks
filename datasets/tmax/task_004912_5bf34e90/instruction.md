You are a Data Engineer building a custom ETL and inference pipeline for processing optical signal recordings.

You have been provided with two assets:
1. `/app/signal.mp4`: A grayscale video recording of an optical sensor (10 seconds, 1 frame per second).
2. `/app/reference.db`: An SQLite database containing reference data, but the schema has been lost.

Your objective is to build a C++ pipeline that extracts data from the video, stores it, performs analytical queries to map the data, and serves the results over a custom TCP socket protocol.

**Step 1: Frame Extraction and Processing**
*   Extract the frames from `/app/signal.mp4`.
*   Write a C++ program that processes these frames. For each frame, calculate the average brightness of all pixels (0-255). 

**Step 2: Database Ingestion & Reverse Engineering**
*   Inspect `/app/reference.db` to understand its schema. It contains a table defining signal categories based on brightness ranges.
*   Have your C++ program connect to this SQLite database and create a new table called `frame_data` containing the frame number and the raw average brightness.
*   Insert your processed frame data into this table.

**Step 3: Analytical SQL Query (Window Functions & Mapping)**
*   Within your C++ program, execute a SQL query that:
    1.  Calculates a moving average of the brightness for each frame using a Window Function. The window should cover 3 frames: the preceding frame, the current frame, and the following frame. (For the first frame, average just itself and the following; for the last, itself and the preceding).
    2.  Joins the smoothed brightness value against the reverse-engineered table in `/app/reference.db` to determine the `signal_name` for that frame.

**Step 4: TCP Server Integration**
*   Your C++ program must stay running and listen for incoming TCP connections on `0.0.0.0:8000`.
*   When a client connects and sends the exact string `REPORT\n`, the server must respond with a JSON array of the results and then gracefully close the connection.
*   The JSON must exactly match this format:
    ```json
    [
      {"frame": 1, "raw_brightness": 12, "smoothed_brightness": 15.33, "signal_name": "background"},
      ...
    ]
    ```
    (Round `smoothed_brightness` to 2 decimal places).

**Constraints:**
*   You must use C++ (`g++` is available) as the primary language for processing, database querying, and the TCP server.
*   You may use `ffmpeg` via the shell to extract frames (e.g., to `/tmp`).
*   You may use the `sqlite3` C/C++ library (`libsqlite3-dev` is installed).
*   No external heavy C++ libraries (like Boost) are available; use standard POSIX sockets (`<sys/socket.h>`) for the TCP server.