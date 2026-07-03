# test_final_state.py
import socket
import sqlite3
import threading
import time
import pytest

def test_database_index_exists():
    db_path = "/app/data/graph.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Get all indexes for the edges table
    cursor.execute("PRAGMA index_list('edges');")
    indexes = cursor.fetchall()

    assert len(indexes) > 0, "No index found on the 'edges' table. You must create an index to optimize the query."

    index_on_parent_id = False
    for idx in indexes:
        idx_name = idx[1]
        cursor.execute(f"PRAGMA index_info('{idx_name}');")
        columns = cursor.fetchall()
        # columns format: (seqno, cid, name)
        if any(col[2] == 'parent_id' for col in columns):
            index_on_parent_id = True
            break

    assert index_on_parent_id, "No index found specifically on the 'parent_id' column in the 'edges' table."
    conn.close()

def send_request(node_id):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5.0)
    s.connect(('127.0.0.1', 8888))
    s.sendall(f"{node_id}\n".encode('utf-8'))
    data = s.recv(1024).decode('utf-8').strip()
    s.close()
    return data

def test_service_responses():
    try:
        resp1 = send_request(1)
        assert resp1 == "7", f"Expected descendant count '7' for node 1, got '{resp1}'"
    except Exception as e:
        pytest.fail(f"Failed to communicate with the service for node 1: {e}")

    try:
        resp2 = send_request(2)
        assert resp2 == "4", f"Expected descendant count '4' for node 2, got '{resp2}'"
    except Exception as e:
        pytest.fail(f"Failed to communicate with the service for node 2: {e}")

def test_concurrency():
    def worker(node_id, results, index):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5.0)
            s.connect(('127.0.0.1', 8888))
            # Sleep slightly to ensure multiple connections are open simultaneously
            time.sleep(0.5)
            s.sendall(f"{node_id}\n".encode('utf-8'))
            data = s.recv(1024).decode('utf-8').strip()
            s.close()
            results[index] = data
        except Exception as e:
            results[index] = str(e)

    results = [None, None]
    t1 = threading.Thread(target=worker, args=(1, results, 0))
    t2 = threading.Thread(target=worker, args=(2, results, 1))

    t1.start()
    t2.start()

    t1.join(timeout=10)
    t2.join(timeout=10)

    assert not t1.is_alive() and not t2.is_alive(), "Threads hung, likely due to a deadlock. Did you add 'fork' to the socat command?"
    assert results[0] == "7", f"Concurrent request 1 failed or returned wrong result: {results[0]}"
    assert results[1] == "4", f"Concurrent request 2 failed or returned wrong result: {results[1]}"