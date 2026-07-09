"""Clinical trial ingestion utilities."""
import json
import os
from typing import Any, Dict, List

import requests
from loguru import logger

BASE_URL = "https://clinicaltrials.gov/api/v2/studies"


def _normalize_study(study: Dict[str, Any]) -> Dict[str, List[str]]:
    protocol = study.get("protocolSection", {})
    identification = protocol.get("identificationModule", {})
    description = protocol.get("descriptionModule", {})
    conditions = protocol.get("conditionsModule", {}).get("conditions", [])
    interventions = protocol.get("armsInterventionsModule", {}).get("interventions", [])
    phases = protocol.get("designModule", {}).get("phases", [])

    return {
        "NCTId": [identification.get("nctId", "")] if identification.get("nctId") else [],
        "BriefTitle": [identification.get("briefTitle", "")] if identification.get("briefTitle") else [],
        "Condition": conditions if isinstance(conditions, list) else [conditions],
        "InterventionName": [
            intervention.get("name", "")
            for intervention in interventions
            if isinstance(intervention, dict) and intervention.get("name")
        ],
        "BriefSummary": [description.get("briefSummary", "")] if description.get("briefSummary") else [],
        "Phase": phases if isinstance(phases, list) else [phases],
    }


def fetch_trials(
    condition: str,
    max_results: int = 100,
):
    params = {
        "query.term": condition,
        "pageSize": max_results,
        "format": "json",
    }

    response = requests.get(BASE_URL, params=params, timeout=30)
    response.raise_for_status()

    payload = response.json()
    studies = [_normalize_study(study) for study in payload.get("studies", [])]

    logger.info(f"Downloaded {len(studies)} Clinical Trials")

    return studies


def save_trials(
    studies,
    output_dir="data/raw/clinical_trials",
):
    os.makedirs(output_dir, exist_ok=True)

    for study in studies:

        trial_id = (
            study["NCTId"][0]
            if study["NCTId"]
            else "unknown"
        )

        with open(
            f"{output_dir}/{trial_id}.json",
            "w",
            encoding="utf-8",
        ) as f:
            json.dump(study, f, indent=4)

    logger.info("Clinical Trials saved successfully.")