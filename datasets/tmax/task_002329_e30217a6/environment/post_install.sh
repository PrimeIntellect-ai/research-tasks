apt-get update && apt-get install -y python3 python3-pip python3-opencv gcc ffmpeg
    pip3 install pytest numpy opencv-python

    mkdir -p /app
    cd /app

    cat << 'EOF' > generate_video.py
import cv2
import numpy as np

# Create a fixed random graph over 10 frames
np.random.seed(42)
frames = 10
nodes = 128
video_writer = cv2.VideoWriter('/app/optical_graph.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 2, (nodes, nodes), isColor=False)

base_matrix = np.random.choice([0, 255], size=(nodes, nodes), p=[0.95, 0.05]).astype(np.uint8)

for i in range(frames):
    # Introduce some noise/temporal dropout to make the union meaningful
    noise = np.random.choice([0, 255], size=(nodes, nodes), p=[0.99, 0.01]).astype(np.uint8)
    frame_matrix = np.where(noise == 255, 0, base_matrix)
    video_writer.write(frame_matrix)

video_writer.release()

# Save the exact unioned ground truth for the oracle
union_matrix = np.where(base_matrix > 128, 1, 0).astype(np.int8)
union_matrix.tofile('/app/oracle_graph.bin')
EOF

    python3 generate_video.py

    cat << 'EOF' > /app/oracle_query_engine.c
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {
    if (argc != 2) return 1;
    FILE *f = fopen(argv[1], "rb");
    if (!f) return 1;
    char graph[128][128];
    fread(graph, 1, 16384, f);
    fclose(f);

    int n;
    while (scanf("%d", &n) == 1) {
        if (n < 0 || n > 127) {
            printf("ERROR\n");
        } else {
            int in_deg = 0, out_deg = 0;
            for (int i = 0; i < 128; i++) {
                if (graph[n][i] == 1) out_deg++;
                if (graph[i][n] == 1) in_deg++;
            }
            printf("%d|%d|%d\n", n, in_deg, out_deg);
        }
    }
    return 0;
}
EOF

    gcc -O3 /app/oracle_query_engine.c -o /app/oracle_query_engine
    chmod +x /app/oracle_query_engine

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user