apt-get update && apt-get install -y python3 python3-pip ffmpeg
    pip3 install pytest opencv-python-headless numpy Pillow

    cat << 'EOF' > /tmp/setup.py
import os
import cv2
import numpy as np
import csv

os.makedirs('/app', exist_ok=True)

# 1. Generate Video
width, height = 200, 200
fps = 1
duration = 60 # seconds
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('/app/reaction.mp4', fourcc, fps, (width, height))

np.random.seed(42)
temperatures = []
activities = []

with open('/app/conditions.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['second', 'temperature'])

    for sec in range(duration):
        # Generate random temperature
        temp = np.random.uniform(15.0, 25.0)
        temperatures.append(temp)
        writer.writerow([sec, round(temp, 2)])

        # Decide activity
        is_active = np.random.rand() > 0.5
        activities.append(is_active)

        # Create frame
        frame = np.zeros((height, width, 3), dtype=np.uint8)

        # The center 10x10 is x:100-109, y:100-109
        if is_active:
            # Active: red channel sum > 12000. 10x10 = 100 pixels. 121 * 100 = 12100.
            frame[100:110, 100:110, 2] = 130 # OpenCV uses BGR, so index 2 is Red.
        else:
            # Inactive
            frame[100:110, 100:110, 2] = 50

        out.write(frame)

out.release()

# Calculate Ground Truth Posteriors
alpha_H, beta_H = 1, 1
alpha_L, beta_L = 1, 1

for temp, active in zip(temperatures, activities):
    if temp >= 20.0:
        if active: alpha_H += 1
        else: beta_H += 1
    else:
        if active: alpha_L += 1
        else: beta_L += 1

# 2. Write Oracle
oracle_code = "import sys\nimport json\n\n"
oracle_code += "base_alpha_H = " + str(alpha_H) + "\n"
oracle_code += "base_beta_H = " + str(beta_H) + "\n"
oracle_code += "base_alpha_L = " + str(alpha_L) + "\n"
oracle_code += "base_beta_L = " + str(beta_L) + "\n"
oracle_code += """
def process():
    try:
        line = sys.stdin.read().strip()
        if not line: return
        data = json.loads(line)
        temp = data['temp']
        obs = data['obs']

        if temp >= 20.0:
            a = base_alpha_H
            b = base_beta_H
        else:
            a = base_alpha_L
            b = base_beta_L

        for o in obs:
            if o == 1:
                a += 1
            elif o == 0:
                b += 1

        print(json.dumps({"alpha": a, "beta": b}))
    except Exception as e:
        print(json.dumps({"error": str(e)}))

if __name__ == '__main__':
    process()
"""

with open('/app/oracle_update_model.py', 'w') as f:
    f.write(oracle_code)
EOF

    python3 /tmp/setup.py

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user /app