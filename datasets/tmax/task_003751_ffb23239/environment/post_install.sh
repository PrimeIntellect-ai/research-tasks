apt-get update && apt-get install -y python3 python3-pip git g++
pip3 install pytest

useradd -m -s /bin/bash user || true

mkdir -p /home/user/logs
mkdir -p /home/user/pipeline_repo

# Create logs
cat << 'EOF' > /home/user/logs/ingest.log
[23:59:58] INGEST record_id=101 timestamp=1672531198
[23:59:59] INGEST record_id=102 timestamp=1672531199
[00:00:00] INGEST record_id=103 timestamp=1672531200
[00:00:01] INGEST record_id=104 timestamp=1672531201
EOF

cat << 'EOF' > /home/user/logs/transform.log
[23:59:58] TRANSFORM record_id=101 status=ok
[23:59:59] TRANSFORM record_id=102 status=ok
[00:00:01] TRANSFORM record_id=104 status=ok
EOF

cat << 'EOF' > /home/user/logs/export.log
[23:59:58] EXPORT record_id=101 dest=db
[23:59:59] EXPORT record_id=102 dest=db
[00:00:01] EXPORT record_id=104 dest=db
EOF

# Create repo
cd /home/user/pipeline_repo
git init
git config --global user.email "dev@example.com"
git config --global user.name "Dev"

cat << 'EOF' > processor.h
#pragma once
#include <string>

struct Record {
    std::string id;
    long timestamp;
};

bool isValidRecord(const Record& r, long window_start, long window_end);
EOF

cat << 'EOF' > processor.cpp
#include "processor.h"

bool isValidRecord(const Record& r, long window_start, long window_end) {
    // Original working code: inclusive of start boundary
    return r.timestamp >= window_start && r.timestamp < window_end;
}
EOF

git add processor.h processor.cpp
git commit -m "Initial commit"

# Introduce bug and secret
cat << 'EOF' > processor.cpp
#include "processor.h"

// API_KEY="SECRET_8841_XQ"
bool isValidRecord(const Record& r, long window_start, long window_end) {
    // BUG: changed >= to >
    return r.timestamp > window_start && r.timestamp < window_end;
}
EOF
git add processor.cpp
git commit -m "Update timestamp validation logic"
BUG_COMMIT=$(git rev-parse HEAD)

# Remove secret
cat << 'EOF' > processor.cpp
#include "processor.h"

bool isValidRecord(const Record& r, long window_start, long window_end) {
    // BUG: changed >= to >
    return r.timestamp > window_start && r.timestamp < window_end;
}
EOF
git add processor.cpp
git commit -m "Remove accidentally committed key"

# Save the expected truth values
echo "SECRET_8841_XQ" > /home/user/.expected_secret
echo "$BUG_COMMIT" > /home/user/.expected_commit
echo "103" > /home/user/.expected_record

chown -R user:user /home/user/logs /home/user/pipeline_repo /home/user/.expected_*

chmod -R 777 /home/user