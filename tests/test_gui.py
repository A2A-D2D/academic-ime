"""Tests for gui.py and domain_profiles.py."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

import pytest


class TestDomainProfiles:
    """Tests for domain_profiles.py."""

    def test_all_domains_have_words(self):
        from academic_ime.domain_profiles import DOMAINS
        assert len(DOMAINS) == 14
        for did, domain in DOMAINS.items():
            assert len(domain["words"]) > 0, f"Domain {did} has no words"
            assert domain["name"], f"Domain {did} has no name"
            assert domain["icon"], f"Domain {did} has no icon"

    def test_get_domain_list(self):
        from academic_ime.domain_profiles import get_domain_list
        domains = get_domain_list()
        assert len(domains) == 14
        for d in domains:
            assert "id" in d
            assert "name" in d
            assert "icon" in d

    def test_weight_multiplier(self):
        from academic_ime.domain_profiles import get_domain_weight_multiplier
        assert get_domain_weight_multiplier("test", 1) == 3.0
        assert get_domain_weight_multiplier("test", 2) == 2.0
        assert get_domain_weight_multiplier("test", 3) == 1.5
        assert get_domain_weight_multiplier("test", 4) == 1.3
        assert get_domain_weight_multiplier("test", 5) == 1.1
        assert get_domain_weight_multiplier("test", 6) == 1.0
        assert get_domain_weight_multiplier("test", None) == 0.5

    def test_build_domain_lexicon(self):
        from academic_ime.domain_profiles import build_domain_lexicon
        # Use two domains with different priorities
        entries = build_domain_lexicon([
            ("daily", 1),    # 3.0x
            ("cs_chip", 3),  # 1.5x
        ])
        assert len(entries) > 0
        for entry in entries:
            assert len(entry) == 3  # (term, pinyin, weight)
            assert isinstance(entry[0], str)
            assert isinstance(entry[1], str)
            assert isinstance(entry[2], int)
            assert entry[2] > 0

    def test_build_domain_lexicon_empty(self):
        from academic_ime.domain_profiles import build_domain_lexicon
        entries = build_domain_lexicon([])
        assert entries == []


class TestGUIApp:
    """Tests for the Flask GUI app."""

    @pytest.fixture
    def client(self):
        from academic_ime.gui import gui_app
        gui_app.config["TESTING"] = True
        with gui_app.test_client() as c:
            yield c

    def test_index_returns_html(self, client):
        resp = client.get("/")
        assert resp.status_code == 200
        assert b"AcademicIME" in resp.data
        assert b"domain" in resp.data.lower()

    def test_api_domains(self, client):
        resp = client.get("/api/domains")
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert len(data) == 14
        assert "word_count" in data[0]
        assert data[0]["word_count"] > 0

    def test_api_build_no_domains(self, client):
        resp = client.post("/api/build",
                           data=json.dumps({"data_dir": "data", "domains": []}),
                           content_type="application/json")
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert data["ok"] is False

    def test_api_build_bad_dir(self, client):
        resp = client.post("/api/build",
                           data=json.dumps({"data_dir": "/nonexistent/path", "domains": ["daily"]}),
                           content_type="application/json")
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert data["ok"] is False

    def test_api_build_with_domains(self, client):
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a small sample file
            sample = Path(tmpdir) / "sample.txt"
            sample.write_text("This is a test meeting document about semiconductor design.", encoding="utf-8")

            resp = client.post("/api/build",
                               data=json.dumps({
                                   "data_dir": tmpdir,
                                   "domains": ["daily", "cs_chip"]
                               }),
                               content_type="application/json")
            assert resp.status_code == 200
            data = json.loads(resp.data)
            assert data["ok"] is True
            assert "构建完成" in data["message"]

            # Verify CSV and Rime dict were created
            csv_path = Path("output/candidates.csv")
            rime_path = Path("output/academic_ime.dict.yaml")
            assert csv_path.exists()
            assert rime_path.exists()
            assert csv_path.stat().st_size > 0
            assert rime_path.stat().st_size > 0
