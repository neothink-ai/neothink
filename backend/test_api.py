import requests
import json

def test_generate_tasks():
    url = "http://localhost:6876/tasker/generate-tasks"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    data = {
        "project_description": "Create a simple website",
        "userid": "test123"
    }
    
    try:
        print(f"Sending request to {url} with data:", json.dumps(data, indent=2))
        response = requests.post(url, json=data, headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print(f"Response Body: {response.text}")
        
        if response.status_code == 404:
            print("\nAvailable routes:")
            print(requests.get("http://localhost:6876/docs").text)
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_generate_tasks()
