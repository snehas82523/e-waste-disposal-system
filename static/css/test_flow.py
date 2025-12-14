import requests
import time

BASE_URL = 'http://127.0.0.1:5001/api'

def test_flow():
    print("Testing Employee Creation...")
    unique_email = f"john_verify_{int(time.time())}@example.com"
    emp_payload = {
        "name": "John Verify",
        "email": unique_email,
        "role": "Collector",
        "phone": "555-0199"
    }
    r = requests.post(f"{BASE_URL}/employees", json=emp_payload)
    if r.status_code == 201:
        emp_id = r.json()['id']
        print(f"PASS: Created Employee ID {emp_id}")
    else:
        print(f"FAIL: Employee Creation {r.text}")
        return

    print("Testing Pickup Request Creation...")
    req_payload = {
        "user_id": 1,
        "item_description": "Old Printer"
    }
    r = requests.post(f"{BASE_URL}/requests", json=req_payload)
    if r.status_code == 201:
        req_id = r.json()['id']
        print(f"PASS: Created Request ID {req_id}")
    else:
        print(f"FAIL: Request Creation {r.text}")
        return

    print("Testing Assignment...")
    assign_payload = {
        "employee_id": emp_id
    }
    r = requests.put(f"{BASE_URL}/requests/{req_id}/assign", json=assign_payload)
    if r.status_code == 200:
        data = r.json()
        # Verify against the name we created
        if data['assigned_employee'] == emp_payload['name'] and data['status'] == "Assigned":
             print(f"PASS: Assigned Request {req_id} to {emp_payload['name']}")
        else:
             print(f"FAIL: Assignment Data Mismatch {data}")
    else:
        print(f"FAIL: Assignment Request {r.text}")

    print("Testing Full Workflow (Pickup -> Recycled -> Reward)...")
    
    # 1. Employee Picked Up
    r = requests.put(f"{BASE_URL}/requests/{req_id}/status", json={"status": "Picked Up"})
    if r.status_code == 200 and r.json()['status'] == "Picked Up":
        print("PASS: Status Picked Up")
    else:
        print(f"FAIL: Status Picked Up {r.text}")

    # 2. Verify Initial Points (Should be 0)

    # 3. Center Recycled
    r = requests.put(f"{BASE_URL}/requests/{req_id}/status", json={"status": "Recycled"})
    if r.status_code == 200 and r.json()['status'] == "Recycled":
        print("PASS: Status Recycled")
        # Check Points if possible (We need a way to check, added GET /api/users/1)
    else:
        print(f"FAIL: Status Recycled {r.text}")
    
    # 4. Reward Delivered
    r = requests.put(f"{BASE_URL}/requests/{req_id}/status", json={"status": "Reward Delivered"})
    if r.status_code == 200 and r.json()['status'] == "Reward Delivered":
        print("PASS: Status Reward Delivered")
    else:
        print(f"FAIL: Status Reward Delivered {r.text}")

    print("Testing Employee List...")
    r = requests.get(f"{BASE_URL}/employees")

    if len(r.json()) > 0:
        print("PASS: Retrieved Employee List")
    else:
        print("FAIL: Employee List Empty")

if __name__ == "__main__":
    # Wait a bit for server to start if running immediately after spawn
    time.sleep(2)
    try:
        test_flow()
    except Exception as e:
        print(f"CRITICAL FAIL: {e}")
