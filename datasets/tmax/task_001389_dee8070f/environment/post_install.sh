apt-get update && apt-get install -y python3 python3-pip ffmpeg tzdata
    pip3 install pytest scipy numpy

    mkdir -p /app
    # Generate 1 hour audio file
    ffmpeg -y -f lavfi -i sine=frequency=1000:duration=3600 -c:a pcm_s16le /app/radio_broadcast.wav

    mkdir -p /home/user
    cat << 'EOF' > /home/user/segments.log
2023-10-27T00:15:30.250Z - 2023-10-27T00:15:35.750+00:00
2023-10-27T00:45:10.1Z - 2023-10-27T00:45:12.900-04:00
EOF

    cat << 'EOF' > /home/user/process_broadcast.sh
#!/bin/bash
# Buggy script: drops precision and leaks memory by invoking ffmpeg in a loop

rm -f /home/user/final_output.wav
touch /home/user/file_list.txt

while read -r line; do
    start_str=$(echo "$line" | awk '{print $1}')
    end_str=$(echo "$line" | awk '{print $3}')

    # Bug 1: date +%s drops fractional seconds and mishandles some timezones
    start_sec=$(date -d "$start_str" +%s)
    end_sec=$(date -d "$end_str" +%s)

    # Base time is 2023-10-27T00:00:00Z
    base_sec=$(date -d "2023-10-27T00:00:00Z" +%s)

    offset=$((start_sec - base_sec))
    duration=$((end_sec - start_sec))

    # Bug 3: invoking ffmpeg iteratively for each segment
    out_file="/home/user/segment_${offset}.wav"
    ffmpeg -y -i /app/radio_broadcast.wav -ss "$offset" -t "$duration" -c copy "$out_file" 2>/dev/null

    echo "file '$out_file'" >> /home/user/file_list.txt
done < /home/user/segments.log

ffmpeg -y -f concat -safe 0 -i /home/user/file_list.txt -c copy /home/user/final_output.wav 2>/dev/null
EOF
    chmod +x /home/user/process_broadcast.sh

    cat << 'EOF' > /tmp/gen_ref.py
import sys
from datetime import datetime, timezone
import numpy as np
from scipy.io import wavfile

sr, data = wavfile.read("/app/radio_broadcast.wav")
t0 = datetime.strptime("2023-10-27T00:00:00+0000", "%Y-%m-%dT%H:%M:%S%z").timestamp()

out_data = []
with open("/home/user/segments.log") as f:
    for line in f:
        parts = line.strip().split(" - ")
        if len(parts) != 2: continue

        def parse_time(ts):
            ts = ts.replace("Z", "+00:00")
            if len(ts.rsplit("+", 1)) == 2:
                main, tz = ts.rsplit("+", 1)
                tz = "+" + tz.replace(":", "")
            elif len(ts.rsplit("-", 1)) > 1 and "T" in ts.rsplit("-", 1)[0]:
                main, tz = ts.rsplit("-", 1)
                tz = "-" + tz.replace(":", "")
            else:
                main = ts
                tz = "+0000"

            if "." not in main:
                main += ".0"

            base, frac = main.split(".")
            frac = frac.ljust(6, "0")
            dt_str = f"{base}.{frac}{tz}"
            dt = datetime.strptime(dt_str, "%Y-%m-%dT%H:%M:%S.%f%z")
            return dt.timestamp()

        t1 = parse_time(parts[0]) - t0
        t2 = parse_time(parts[1]) - t0

        s1 = int(round(t1 * sr))
        s2 = int(round(t2 * sr))
        s1 = max(0, min(len(data), s1))
        s2 = max(0, min(len(data), s2))
        out_data.append(data[s1:s2])

if out_data:
    final = np.concatenate(out_data)
else:
    final = np.array([], dtype=data.dtype)

wavfile.write("/tmp/reference_output.wav", sr, final)
EOF
    python3 /tmp/gen_ref.py

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user /tmp/reference_output.wav