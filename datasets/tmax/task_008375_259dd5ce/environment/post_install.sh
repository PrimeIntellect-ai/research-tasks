apt-get update && apt-get install -y python3 python3-pip sqlite3 libsqlite3-dev gcc
pip3 install pytest

useradd -m -s /bin/bash user || true

sqlite3 /home/user/corporate.db <<EOF
CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER);
CREATE TABLE roles (user_id INTEGER PRIMARY KEY, role TEXT, clearance INTEGER);
CREATE TABLE events (event_id INTEGER PRIMARY KEY, event_data TEXT);

-- Insert Users
INSERT INTO users (id, name, dept_id) VALUES 
(1, 'Alice Manager', 1),
(2, 'Bob Intern', 2),
(3, 'Charlie Dev', 2),
(4, 'Diana Director', 1),
(5, 'Eve Contractor', 3);

-- Insert Roles
INSERT INTO roles (user_id, role, clearance) VALUES 
(1, 'Manager', 6),
(2, 'Intern', 2),
(3, 'Developer', 4),
(4, 'Director', 9),
(5, 'Contractor', 1);

-- Insert Events
INSERT INTO events (event_data) VALUES ('{"action": "READ", "resource": "vault", "timestamp": 1680000000}');
INSERT INTO events (event_data) VALUES ('{"action": "READ", "resource": "vault", "timestamp": 1680000100, "user_id": 2}');
INSERT INTO events (event_data) VALUES ('{"action": "READ", "resource": "vault", "timestamp": 1680000500, "user_id": 2}');
INSERT INTO events (event_data) VALUES ('{"action": "READ", "resource": "lobby", "timestamp": 1680000600, "user_id": 2}');
INSERT INTO events (event_data) VALUES ('{"action": "READ", "resource": "vault", "timestamp": 1680000300, "user_id": 3}');
INSERT INTO events (event_data) VALUES ('{"action": "WRITE", "resource": "vault", "timestamp": 1680000400, "user_id": 3}');
INSERT INTO events (event_data) VALUES ('{"action": "READ", "resource": "vault", "timestamp": 1680000900, "user_id": 5}');
EOF

cat << 'EOF' > /tmp/expected_flagged_audits.csv
user_id,name,role,violation_time
2,Bob Intern,Intern,1680000500
3,Charlie Dev,Developer,1680000300
5,Eve Contractor,Contractor,1680000900
EOF

chmod -R 777 /home/user