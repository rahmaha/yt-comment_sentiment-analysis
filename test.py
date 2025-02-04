import requests

host = "127.0.0.1:9696"
url = f"http://{host}/predict"

text = ["i like the video"]

# Make a POST request
try:
    response = requests.post(url, json={"text": text})
    response.raise_for_status()  # Raise an error for bad HTTP responses
    result = response.json()
    print('Results: ')
    print('Original comment', text)
    print(result)
except requests.exceptions.RequestException as e:
    print(f"HTTP error occurred: {e}")
except ValueError as e:
    print(f"Invalid JSON response: {e}")
