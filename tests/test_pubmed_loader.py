from urllib.error import HTTPError

from app.ingestion import pubmed_loader


class FakeHandle:
    def __init__(self, payload):
        self.payload = payload

    def read(self):
        return self.payload


def test_fetch_articles_retries_after_transient_error(monkeypatch):
    calls = {"count": 0}

    class FakeEntrez:
        email = None

        def efetch(self, **kwargs):
            calls["count"] += 1
            if calls["count"] == 1:
                raise HTTPError("https://example.test", 500, "temp fail", None, None)
            return FakeHandle("PMID- 123\nTI - Example title\nAB - Example summary\n")

    class FakeMedline:
        @staticmethod
        def read(handle):
            return {"PMID": "123", "TI": "Example title", "AB": "Example summary"}

    monkeypatch.setattr(pubmed_loader, "Entrez", FakeEntrez())
    monkeypatch.setattr(pubmed_loader, "Medline", FakeMedline)
    monkeypatch.setattr(pubmed_loader.time, "sleep", lambda *_args, **_kwargs: None)

    articles = pubmed_loader.fetch_articles(["123"])

    assert len(articles) == 1
    assert articles[0]["PMID"] == "123"
