import requests
import time

# Use exact lowercase EB URL
BASE_URL = "http://ece444-pra5-env.eba-epmhvzp3.us-east-2.elasticbeanstalk.com"

# Test cases: 2 fake news, 2 real news
test_cases = {
    "fake_1": "Scientists discover a potion that lets people fly and live forever, available next week in stores worldwide!",
    "fake_2": "Elon Musk announces the purchase of the moon to build a new Tesla factory.",
    "real_1": "The United Nations held a summit to discuss global climate change and carbon reduction goals.",
    "real_2": "The central bank announced an increase in interest rates to curb rising inflation.",
}

# Settings
TIMEOUT = 20  # seconds
MAX_RETRIES = 3  # retry if connection fails
RETRY_DELAY = 5  # seconds between retries

print("=== Functional Testing Results ===")

for name, text in test_cases.items():
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = requests.post(
                f"{BASE_URL}/predict",
                json={"message": text},
                timeout=TIMEOUT,
                verify=False  # ignore SSL cert issues for testing
            )
            data = resp.json()
            print(f"{name}: HTTP {resp.status_code}, Response: {data}")
            break  # success, exit retry loop
        except requests.exceptions.RequestException as e:
            print(f"{name}: Attempt {attempt} failed → {e}")
            if attempt < MAX_RETRIES:
                print(f"Retrying in {RETRY_DELAY} seconds...")
                time.sleep(RETRY_DELAY)
            else:
                print(f"{name}: All {MAX_RETRIES} attempts failed.\n")
