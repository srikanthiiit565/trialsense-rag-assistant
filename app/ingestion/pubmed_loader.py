"""PubMed ingestion utilities."""
import os
import time
from urllib.error import HTTPError

from Bio import Entrez
from Bio import Medline

Entrez.email = "your_email@example.com"


def search_pubmed(
    query: str,
    max_results: int = 50,
):

    handle = Entrez.esearch(
        db="pubmed",
        term=query,
        retmax=max_results,
    )

    record = Entrez.read(handle)

    return record["IdList"]


def fetch_articles(pmids):

    articles = []

    for pmid in pmids:
        for attempt in range(3):
            try:
                handle = Entrez.efetch(
                    db="pubmed",
                    id=pmid,
                    rettype="medline",
                    retmode="text",
                )
                article = Medline.read(handle)
                articles.append(article)
                break
            except HTTPError as exc:
                if exc.code in {429, 500, 502, 503, 504} and attempt < 2:
                    time.sleep(1)
                    continue
                break
            except Exception:
                break

    return articles


def save_articles(
    articles,
    output_dir="data/raw/pubmed",
):

    os.makedirs(output_dir, exist_ok=True)

    for article in articles:

        pmid = article.get("PMID", "unknown")

        with open(
            f"{output_dir}/{pmid}.json",
            "w",
            encoding="utf-8",
        ) as f:

            import json

            json.dump(article, f, indent=4)

    print("PubMed Articles Saved")