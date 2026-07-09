"""Text cleaning utilities."""
# converts different sources into one common schema
from typing import Dict


def clean_clinical_trial(trial: Dict):

    return {

        "source": "clinical_trials",

        "id": trial["NCTId"][0] if trial["NCTId"] else "",

        "title": (
            trial["BriefTitle"][0]
            if trial["BriefTitle"]
            else ""
        ),

        "summary": (
            trial["BriefSummary"][0]
            if trial["BriefSummary"]
            else ""
        ),

        "phase": (
            trial["Phase"][0]
            if trial["Phase"]
            else ""
        ),
    }


def clean_pubmed(article):

    return {

        "source": "pubmed",

        "id": article.get("PMID", ""),

        "title": article.get("TI", ""),

        "summary": article.get("AB", ""),

        "authors": article.get("AU", []),

        "journal": article.get("JT", ""),
    }