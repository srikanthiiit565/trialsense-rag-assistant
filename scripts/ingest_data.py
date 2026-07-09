"""Data ingestion script entrypoint."""
from app.ingestion.clinical_trials_loader import (
    fetch_trials,
    save_trials,
)

from app.ingestion.pubmed_loader import (
    search_pubmed,
    fetch_articles,
    save_articles,
)

from app.ingestion.cleaner import (
    clean_clinical_trial,
    clean_pubmed,
)

import json
import os


SEARCH_TOPIC = "Alzheimer Disease"


def main():

    print("=" * 60)
    print("Clinical Trials")
    print("=" * 60)

    trials = fetch_trials(
        SEARCH_TOPIC,
        20,
    )

    save_trials(trials)

    print("=" * 60)
    print("PubMed")
    print("=" * 60)

    pmids = search_pubmed(
        SEARCH_TOPIC,
        20,
    )

    articles = fetch_articles(pmids)

    save_articles(articles)

    os.makedirs(
        "data/processed",
        exist_ok=True,
    )

    unified_docs = []

    for trial in trials:
        unified_docs.append(
            clean_clinical_trial(trial)
        )

    for article in articles:
        unified_docs.append(
            clean_pubmed(article)
        )

    with open(
        "data/processed/documents.json",
        "w",
        encoding="utf-8",
    ) as f:

        json.dump(
            unified_docs,
            f,
            indent=4,
        )

    print()
    print("=" * 60)
    print(f"Total Documents: {len(unified_docs)}")
    print("=" * 60)


if __name__ == "__main__":
    main()