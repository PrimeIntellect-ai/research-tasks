apt-get update && apt-get install -y python3 python3-pip ffmpeg sqlite3 cargo
    pip3 install pytest numpy opencv-python-headless

    mkdir -p /app

    python3 -c "
import cv2
import numpy as np
import sqlite3

# Generate video
out = cv2.VideoWriter('/app/experiment.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 1, (100, 100))
active_frames = [2, 5, 10, 15, 20]
for i in range(30):
    if i in active_frames:
        frame = np.full((100, 100, 3), 255, dtype=np.uint8)
    else:
        frame = np.zeros((100, 100, 3), dtype=np.uint8)
    out.write(frame)
out.release()

# Generate DB
conn = sqlite3.connect('/app/graph.db')
c = conn.cursor()
c.execute('CREATE TABLE edges(source INTEGER, target INTEGER)')
edges = [
    (2, 5), (5, 2),
    (2, 10), (10, 2),
    (5, 10), (10, 5),
    (15, 20), (20, 15),
    (2, 15), (15, 2),
    (1, 2), (2, 1),
    (3, 4), (4, 3)
]
c.executemany('INSERT INTO edges VALUES (?, ?)', edges)
conn.commit()
conn.close()
"

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user
    chmod -R 777 /app