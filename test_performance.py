import requests
import time
import csv
import os
import numpy as np
import matplotlib.pyplot as plt

BASE_URL = "http://ece444-pra5-env.eba-epmhvzp3.us-east-2.elasticbeanstalk.com"

test_cases = {
    "fake_1": "Scientists discover a potion that lets people fly and live forever, available next week in stores worldwide!",
    "fake_2": "Elon Musk announces the purchase of the moon to build a new Tesla factory.",
    "real_1": "The United Nations held a summit to discuss global climate change and carbon reduction goals.",
    "real_2": "The central bank announced an increase in interest rates to curb rising inflation.",
}

os.makedirs("results", exist_ok=True)

for name, text in test_cases.items():
    csv_path = f"results/{name}_latency.csv"
    print(f"Running 100 requests for: {name}")

    latencies = []
    with open(csv_path, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["iteration", "latency_seconds"])
        for i in range(1, 101):
            start = time.time()
            try:
                resp = requests.post(
                    f"{BASE_URL}/predict",  # <-- must include /predict
                    json={"message": text},
                    timeout=20
                )
                resp.raise_for_status()
            except Exception as e:
                print(f"Request {i} failed: {e}")
                continue
            end = time.time()
            latency = end - start
            latencies.append(latency)
            writer.writerow([i, latency])


    print(f"Saved {csv_path}. Average latency: {np.mean(latencies):.4f}s")

# === Generate Boxplot ===
data = []
labels = []

for name in test_cases.keys():
    csv_path = f"results/{name}_latency.csv"
    with open(csv_path, "r") as f:
        next(f)
        times = [float(row.split(",")[1]) for row in f.readlines()]
        data.append(times)
        labels.append(name)

plt.figure(figsize=(10, 6))
plt.boxplot(data, labels=labels, patch_artist=True)
plt.ylabel("Latency (seconds)")
plt.title("API Latency per Test Case (100 Requests Each)")
plt.grid(axis="y")
plt.tight_layout()
plt.savefig("results/latency_boxplot.png")
plt.show()

# Compute averages
for name, latencies in zip(labels, data):
    print(f"{name}: average latency = {np.mean(latencies):.4f} seconds")
