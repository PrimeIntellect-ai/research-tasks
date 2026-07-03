apt-get update && apt-get install -y \
        python3 \
        python3-pip \
        tesseract-ocr \
        libtesseract-dev

    pip3 install pytest rdflib Pillow

    mkdir -p /app

    cat << 'EOF' > /app/setup.py
import sqlite3
import json
import random
from PIL import Image, ImageDraw

# Create image
img = Image.new('RGB', (800, 400), color=(255, 255, 255))
d = ImageDraw.Draw(img)
text = """COMPLIANCE RULE SET:
Identify users matching ALL of the following criteria:
1. Relational DB (Users Table): `status` is 'active' AND `department` is 'finance'. (Join on `user_id`).
2. Document Store: The `tags` array contains 'offshore'. (Match `doc.user_id`).
3. Graph DB: The user has an `ex:ACCESSED` relationship to a resource node, 
   and that resource node has an `ex:hasType` of 'BlacklistedAccount'. (Match `ex:User_<user_id>`)."""
d.text((10,10), text, fill=(0,0,0))
img.save('/app/compliance_schema.png')

# Generate data
truth = [10, 20, 30, 40, 50]
with open('/app/hidden_truth.txt', 'w') as f:
    for t in truth:
        f.write(f"{t}\n")

# SQLite
conn = sqlite3.connect('/app/users.db')
c = conn.cursor()
c.execute('CREATE TABLE Users (user_id INTEGER PRIMARY KEY, status TEXT, department TEXT)')
for i in range(1, 101):
    if i in truth:
        c.execute('INSERT INTO Users VALUES (?, ?, ?)', (i, 'active', 'finance'))
    else:
        status = random.choice(['active', 'inactive'])
        dept = random.choice(['finance', 'hr', 'it'])
        if status == 'active' and dept == 'finance':
            dept = 'it' 
        c.execute('INSERT INTO Users VALUES (?, ?, ?)', (i, status, dept))
conn.commit()
conn.close()

# JSONL
with open('/app/profiles.jsonl', 'w') as f:
    for i in range(1, 101):
        if i in truth:
            doc = {"user_id": i, "tags": ["offshore", "vip"]}
        else:
            doc = {"user_id": i, "tags": ["local"]}
        f.write(json.dumps(doc) + '\n')

# RDF
with open('/app/activity.ttl', 'w') as f:
    f.write("@prefix ex: <http://example.org/> .\n\n")
    for i in range(1, 101):
        if i in truth:
            f.write(f"ex:User_{i} ex:ACCESSED ex:Resource_{i} .\n")
            f.write(f"ex:Resource_{i} ex:hasType 'BlacklistedAccount' .\n")
        else:
            f.write(f"ex:User_{i} ex:ACCESSED ex:Resource_{i} .\n")
            f.write(f"ex:Resource_{i} ex:hasType 'NormalAccount' .\n")
EOF

    python3 /app/setup.py
    rm /app/setup.py

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user /app