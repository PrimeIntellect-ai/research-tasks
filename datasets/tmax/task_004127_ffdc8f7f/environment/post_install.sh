apt-get update && apt-get install -y python3 python3-pip gawk ffmpeg wget curl

    # Install python dependencies, using CPU-only torch to prevent massive downloads and timeouts
    pip3 install --no-cache-dir pytest gTTS
    pip3 install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu
    pip3 install --no-cache-dir openai-whisper

    mkdir -p /app/data /app/.hidden

    # Generate nodes
    gawk 'BEGIN{
      srand(42);
      types[1]="Gateway"; types[2]="Switch"; types[3]="Router"; types[4]="Database";
      for(i=1;i<=1000;i++){
        t = types[int(rand()*4)+1];
        print i "," t;
      }
    }' > /app/data/nodes.csv

    # Generate edges
    gawk 'BEGIN{
      srand(42);
      for(i=1;i<=5000;i++){
        s = int(rand()*1000)+1;
        t = int(rand()*1000)+1;
        if(s!=t) print s "," t;
      }
    }' > /app/data/edges.csv

    # Generate true result (Golden output)
    gawk -F, '
      NR==FNR { type[$1]=$2; next }
      {
        edges[$1][$2] = 1;
      }
      END {
        for (a in edges) {
          if (type[a] == "Gateway") {
            for (b in edges[a]) {
              for (c in edges[b]) {
                if (type[c] == "Database") {
                  print a "," b "," c
                }
              }
            }
          }
        }
      }
    ' /app/data/nodes.csv /app/data/edges.csv | sort > /app/.hidden/true_paths.csv

    # Generate audio using gTTS (clearer than espeak for Whisper transcription)
    python3 -c "
from gtts import gTTS
text = \"Hey, so the old script was doing a cross join and crashing. We need to find all valid two-hop paths. Specifically, we need to find paths where node A connects to node B, and node B connects to node C. The critical requirement is that the starting node, node A, must have the type 'Gateway', and the final node, node C, must have the type 'Database'. The intermediate node B can be anything. Just output the three node IDs separated by commas.\"
tts = gTTS(text)
tts.save('/app/bug_report.mp3')
"
    # Convert to wav as requested
    ffmpeg -i /app/bug_report.mp3 -ar 16000 -ac 1 -c:a pcm_s16le /app/bug_report.wav
    rm /app/bug_report.mp3

    # Create evaluator script
    cat << 'EOF' > /app/.hidden/eval.py
import sys

def load_set(path):
    try:
        with open(path, 'r') as f:
            return set([line.strip() for line in f.readlines() if line.strip()])
    except FileNotFoundError:
        return set()

truth = load_set('/app/.hidden/true_paths.csv')
pred = load_set('/home/user/result.csv')

if not truth and not pred:
    print(1.0)
    sys.exit(0)

tp = len(truth.intersection(pred))
fp = len(pred - truth)
fn = len(truth - pred)

if tp == 0:
    print(0.0)
    sys.exit(0)

precision = tp / (tp + fp)
recall = tp / (tp + fn)
f1 = 2 * (precision * recall) / (precision + recall)

print(f"{f1:.4f}")
EOF

    # Create user and set permissions
    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user
    chmod -R 755 /app