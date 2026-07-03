You are a data engineer building an ETL pipeline and a lightweight embedding retrieval service. You must implement the entire logic using Bash and standard Linux tools.

Your tasks:
1. **ETL Pipeline Script**: Create a Bash script at `/home/user/run_etl.sh` that performs the following:
   - Creates the directory `/home/user/processed/frames/`.
   - Uses `ffmpeg` to extract frames from the video file located at `/app/data/source.mp4` at a rate of exactly 1 frame per second. Name the output files as `frame_0001.jpg`, `frame_0002.jpg`, etc.
   - For each extracted frame, run the provided tool `/app/bin/get_embedding <path_to_frame>` to generate a vector embedding.
   - Save the results to `/home/user/processed/embeddings.csv`. Each line should be formatted exactly as `frame_XXXX.jpg, <embedding_output>`.

2. **Retrieval Service**: Create a Bash script at `/home/user/serve.sh` that acts as a TCP server:
   - It must listen on `127.0.0.1:8888`.
   - You may use `socat` or `nc` (you might need to install them).
   - When a client connects via TCP and sends a 4-digit frame number (e.g., `0005\n`), the server should look up `frame_0005.jpg` in the `embeddings.csv` file, send back ONLY the `<embedding_output>` corresponding to that frame, followed by a newline, and then close the connection.
   - The server must remain running to handle multiple sequential requests.

Run both scripts. The ETL pipeline must finish, and the retrieval service must be actively listening on port 8888 when you complete the task.