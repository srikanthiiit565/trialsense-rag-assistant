"""Evaluation datasets definitions."""
import json


DATASET_PATH = (
    "data/evaluation/golden_dataset.json"
)


def load_dataset():

    with open(
        DATASET_PATH,
        "r"
    ) as f:

        return json.load(f)



if __name__ == "__main__":

    data = load_dataset()

    print(
        f"Loaded {len(data)} evaluation samples"
    )