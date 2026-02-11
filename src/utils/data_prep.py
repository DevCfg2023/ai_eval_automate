import json


def harvest_failures(history_file="data/history.json", threshold=0.85, output_file="data/ready_to_train.json"):
    with open(history_file) as f:
        logs = json.load(f)

    ready_to_train = []
    for entry in logs:
        # Assume stats include 'accuracy'
        if entry["stats"].get("accuracy", 1.0) < threshold:
            ready_to_train.append(entry)

    with open(output_file, "w") as f:
        json.dump(ready_to_train, f, indent=2)
    print(f"[📦] Harvested {len(ready_to_train)} items → {output_file}")
