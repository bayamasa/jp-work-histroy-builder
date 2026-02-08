"""Tests for jp_tenshoku_docs_builder.resume models and loader."""

from pathlib import Path

import pytest
import yaml
from pydantic import ValidationError

from jp_tenshoku_docs_builder.resume.loader import load_resume_yaml
from jp_tenshoku_docs_builder.resume.models import HistoryEntry, Resume


class TestHistoryEntry:
    def test_minimal(self):
        e = HistoryEntry(value="入学")
        assert e.value == "入学"
        assert e.year == ""
        assert e.month == ""

    def test_full(self):
        e = HistoryEntry(year="2020", month="4", value="○○大学 入学")
        assert e.year == "2020"
        assert e.month == "4"
        assert e.value == "○○大学 入学"

    def test_missing_value(self):
        with pytest.raises(ValidationError):
            HistoryEntry(year="2020", month="4")  # type: ignore[call-arg]

    def test_extra_fields_forbidden(self):
        with pytest.raises(ValidationError):
            HistoryEntry(value="テスト", unknown="NG")


class TestResume:
    def test_minimal(self):
        r = Resume(
            date="2024年1月1日現在",
            name_kana="やまだ たろう",
            name="山田 太郎",
            birth_day="1990年1月1日 (満 34 歳)",
        )
        assert r.date == "2024年1月1日現在"
        assert r.name_kana == "やまだ たろう"
        assert r.name == "山田 太郎"
        assert r.birth_day == "1990年1月1日 (満 34 歳)"
        assert r.education == []
        assert r.experience == []
        assert r.licences == []
        assert r.hobby == ""

    def test_missing_required_fields(self):
        with pytest.raises(ValidationError):
            Resume()  # type: ignore[call-arg]

    def test_missing_name(self):
        with pytest.raises(ValidationError):
            Resume(
                date="2024年",
                name_kana="やまだ",
                birth_day="1990年",
            )  # type: ignore[call-arg]

    def test_full(self):
        r = Resume(
            date="2024年1月1日現在",
            name_kana="やまだ たろう",
            name="山田 太郎",
            birth_day="1990年1月1日 (満 34 歳)",
            gender="男",
            cell_phone="090-1234-5678",
            email="test@example.com",
            address_kana="とうきょうと",
            address="東京都千代田区",
            address_zip="100-0001",
            tel="03-1234-5678",
            education=[
                HistoryEntry(year="2008", month="4", value="○○大学 入学"),
                HistoryEntry(year="2012", month="3", value="○○大学 卒業"),
            ],
            experience=[
                HistoryEntry(year="2012", month="4", value="株式会社テスト 入社"),
                HistoryEntry(value="現在に至る"),
            ],
            licences=[
                HistoryEntry(year="2010", month="11", value="普通自動車免許"),
            ],
            commuting_time="1時間",
            dependents="0人",
            spouse="無",
            supporting_spouse="無",
            hobby="プログラミング",
            motivation="志望動機テスト",
            request="特になし",
        )
        assert len(r.education) == 2
        assert len(r.experience) == 2
        assert len(r.licences) == 1
        assert r.gender == "男"
        assert r.commuting_time == "1時間"

    def test_extra_fields_forbidden(self):
        with pytest.raises(ValidationError):
            Resume(
                date="2024年",
                name_kana="やまだ",
                name="山田",
                birth_day="1990年",
                unknown_field="NG",
            )


class TestLoadResumeYaml:
    def test_load_sample_with_credential(self):
        sample_dir = Path(__file__).parent.parent / "sample"
        resume_path = sample_dir / "resume.yaml"
        credential_path = sample_dir / "credential.yaml"
        if not resume_path.exists() or not credential_path.exists():
            pytest.skip("sample/resume.yaml or sample/credential.yaml not found")
        data = load_resume_yaml(resume_path, credential_path=credential_path)
        assert data.name == "山田　太郎"
        assert data.name_kana == "やまだ　たろう"
        assert len(data.education) == 4
        assert len(data.experience) == 5
        assert len(data.licences) == 3

    def test_load_nonexistent(self):
        with pytest.raises(FileNotFoundError):
            load_resume_yaml("/nonexistent/path.yaml")

    def test_credential_merge(self, tmp_path):
        resume_data = {
            "date": "2024年1月1日現在",
            "education": [],
            "hobby": "テスト",
        }
        credential_data = {
            "name_kana": "てすと たろう",
            "name": "テスト 太郎",
            "birth_day": "2000年1月1日 (満 24 歳)",
        }
        resume_file = tmp_path / "resume.yaml"
        credential_file = tmp_path / "credential.yaml"
        resume_file.write_text(yaml.dump(resume_data, allow_unicode=True))
        credential_file.write_text(yaml.dump(credential_data, allow_unicode=True))

        result = load_resume_yaml(resume_file, credential_path=credential_file)
        assert result.date == "2024年1月1日現在"
        assert result.name == "テスト 太郎"
        assert result.name_kana == "てすと たろう"
        assert result.birth_day == "2000年1月1日 (満 24 歳)"
        assert result.hobby == "テスト"

    def test_credential_overrides_resume(self, tmp_path):
        resume_data = {
            "date": "2024年1月1日現在",
            "name_kana": "ふるい なまえ",
            "name": "古い 名前",
            "birth_day": "1990年",
        }
        credential_data = {
            "name_kana": "あたらしい なまえ",
            "name": "新しい 名前",
            "birth_day": "2000年",
        }
        resume_file = tmp_path / "resume.yaml"
        credential_file = tmp_path / "credential.yaml"
        resume_file.write_text(yaml.dump(resume_data, allow_unicode=True))
        credential_file.write_text(yaml.dump(credential_data, allow_unicode=True))

        result = load_resume_yaml(resume_file, credential_path=credential_file)
        assert result.name == "新しい 名前"
        assert result.name_kana == "あたらしい なまえ"
        assert result.birth_day == "2000年"

    def test_load_without_credential(self, tmp_path):
        resume_data = {
            "date": "2024年1月1日現在",
            "name_kana": "やまだ たろう",
            "name": "山田 太郎",
            "birth_day": "1990年",
        }
        resume_file = tmp_path / "resume.yaml"
        resume_file.write_text(yaml.dump(resume_data, allow_unicode=True))

        result = load_resume_yaml(resume_file)
        assert result.name == "山田 太郎"

    def test_credential_nonexistent(self, tmp_path):
        resume_data = {
            "date": "2024年",
            "name_kana": "やまだ",
            "name": "山田",
            "birth_day": "1990年",
        }
        resume_file = tmp_path / "resume.yaml"
        resume_file.write_text(yaml.dump(resume_data, allow_unicode=True))

        with pytest.raises(FileNotFoundError):
            load_resume_yaml(resume_file, credential_path="/nonexistent/cred.yaml")
