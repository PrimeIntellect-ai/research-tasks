apt-get update && apt-get install -y python3 python3-pip ffmpeg gawk bc
pip3 install pytest pandas numpy

mkdir -p /app
ffmpeg -y -f lavfi -i "testsrc=duration=10:size=640x480:rate=30" -vf "hue=s='sin(t*2)+1',eq=brightness='sin(t)':contrast=1.2" -c:v libx264 /app/video.mp4

cat << 'EOF' > /tmp/verify.py
import pandas as pd
import numpy as np
import subprocess
import os
import sys

def generate_ground_truth():
    cmd = [
        "ffmpeg", "-i", "/app/video.mp4", "-vf", "signalstats",
        "-f", "null", "-"
    ]
    process = subprocess.Popen(cmd, stderr=subprocess.PIPE, text=True)

    data = []
    for line in process.stderr:
        if "Parsed_signalstats_" in line and "YAVG" in line:
            # Example line: [Parsed_signalstats_0 @ 0x...] YMIN:10 YLOMIN:12 YAVG:145 ... SAVG:120
            parts = line.split()
            yavg = None
            savg = None
            for p in parts:
                if p.startswith("YAVG:"):
                    yavg = float(p.split(":")[1])
                if p.startswith("SAVG:"):
                    savg = float(p.split(":")[1])
            if yavg is not None and savg is not None:
                data.append({'YAVG': yavg, 'SAVG': savg})

    df = pd.DataFrame(data)
    df['frame_num'] = np.arange(1, len(df) + 1)

    # Model parameters
    W_Y = 0.15
    W_S = -0.08
    B = -12.5

    df['Z'] = W_Y * df['YAVG'] + W_S * df['SAVG'] + B
    df['probability'] = 1 / (1 + np.exp(-df['Z']))
    return df[['frame_num', 'probability']]

def main():
    if not os.path.exists("/home/user/predictions.csv"):
        print("Metric: 1.0 (File not found)")
        sys.exit(1)

    try:
        agent_df = pd.read_csv("/home/user/predictions.csv")
        gt_df = generate_ground_truth()

        # Merge on frame_num
        merged = pd.merge(gt_df, agent_df, on="frame_num", suffixes=('_gt', '_agent'))
        if len(merged) == 0:
            print("Metric: 1.0 (No overlapping frames)")
            sys.exit(1)

        mse = np.mean((merged['probability_gt'] - merged['probability_agent'])**2)
        print(f"Metric: {mse}")

        if mse <= 0.0001:
            sys.exit(0)
        else:
            sys.exit(1)
    except Exception as e:
        print(f"Metric: 1.0 (Error: {e})")
        sys.exit(1)

if __name__ == "__main__":
    main()
EOF

useradd -m -s /bin/bash user || true
chmod -R 777 /home/user