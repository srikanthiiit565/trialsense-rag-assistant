from app.ingestion.clinical_trials_loader import _normalize_study


def test_normalize_study_handles_v2_payload():
    study = {
        "protocolSection": {
            "identificationModule": {
                "nctId": "NCT12345678",
                "briefTitle": "Example trial",
            },
            "descriptionModule": {
                "briefSummary": "Example summary",
            },
            "conditionsModule": {
                "conditions": ["Alzheimer Disease"]
            },
            "armsInterventionsModule": {
                "interventions": [{"name": "Drug A"}]
            },
            "designModule": {
                "phases": ["Phase 2"]
            },
        }
    }

    normalized = _normalize_study(study)

    assert normalized["NCTId"] == ["NCT12345678"]
    assert normalized["BriefTitle"] == ["Example trial"]
    assert normalized["Condition"] == ["Alzheimer Disease"]
    assert normalized["InterventionName"] == ["Drug A"]
    assert normalized["BriefSummary"] == ["Example summary"]
    assert normalized["Phase"] == ["Phase 2"]
