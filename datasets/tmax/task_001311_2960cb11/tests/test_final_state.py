# test_final_state.py
import socket
import pytest

def query_oracle(node_id: str) -> str:
    try:
        with socket.create_connection(("localhost", 9000), timeout=5) as s:
            s.sendall(f"{node_id}\n".encode("utf-8"))
            response = s.recv(1024).decode("utf-8").strip()
            return response
    except ConnectionRefusedError:
        pytest.fail("TCP service is not running on localhost:9000 or refused the connection.")
    except socket.timeout:
        pytest.fail("TCP service on localhost:9000 timed out.")
    except Exception as e:
        pytest.fail(f"Unexpected error communicating with TCP service: {e}")

def test_tcp_service_node_a():
    """
    Test 2-hop paths for node A.
    A->C: A->B->C min(10,5)=5, A->D->C min(8,12)=8. Max is 8.0.
    Oracle score: 8.0 * 1.5 = 12.00.
    """
    response = query_oracle("A")
    assert response == "12.00", f"Expected '12.00' for node A, but got '{response}'"

def test_tcp_service_node_b():
    """
    Test 2-hop paths for node B.
    B->E: B->C->E min(5,20)=5. Max is 5.0.
    Oracle score: 5.0 * 1.5 = 7.50.
    """
    response = query_oracle("B")
    assert response == "7.50", f"Expected '7.50' for node B, but got '{response}'"

def test_tcp_service_node_d():
    """
    Test 2-hop paths for node D.
    D->E: D->C->E min(12,20)=12. Max is 12.0.
    Oracle score: 12.0 * 1.5 = 18.00.
    """
    response = query_oracle("D")
    assert response == "18.00", f"Expected '18.00' for node D, but got '{response}'"

def test_tcp_service_node_c():
    """
    Test 2-hop paths for node C.
    There are no 2-hop paths starting from C in the dataset.
    Oracle score: 0.0 * 1.5 = 0.00.
    """
    response = query_oracle("C")
    assert response == "0.00", f"Expected '0.00' for node C, but got '{response}'"