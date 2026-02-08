"""Tests for jpcv models and loader."""

from pathlib import Path

import pytest
from pydantic import ValidationError

from jpcv.loader import load_yaml
from jpcv.models import (
    Company,
    Environment,
    Project,
    Qualification,
    SelfPRSection,
    SkillCategory,
    SkillItem,
    WorkHistory,
)


class TestWorkHistory:
    def test_minimal(self):
        wh = WorkHistory(date="2024年1月1日現在", name="山田 太郎")
        assert wh.date == "2024年1月1日現在"
        assert wh.name == "山田 太郎"
        assert wh.summary == ""
        assert wh.highlights == []
        assert wh.experience == []

    def test_missing_required_fields(self):
        with pytest.raises(ValidationError):
            WorkHistory()  # type: ignore[call-arg]

    def test_full(self):
        wh = WorkHistory(
            date="2024年1月1日現在",
            name="山田 太郎",
            summary="要約テスト",
            highlights=["スキル1", "スキル2"],
            experience=[
                Company(
                    company="テスト株式会社",
                    period="2020年4月～現在",
                    projects=[
                        Project(
                            period="2020年4月～現在",
                            name="テストプロジェクト",
                            environment=Environment(
                                languages=["Python"],
                                db=["PostgreSQL"],
                            ),
                            team_size="全5名",
                            role="リーダー",
                        )
                    ],
                )
            ],
            technical_skills=[
                SkillCategory(
                    category="言語",
                    items=[
                        SkillItem(name="Python", period="3年", level="上級"),
                    ],
                )
            ],
            qualifications=[
                Qualification(name="基本情報技術者試験", date="2020年4月合格"),
            ],
            self_pr=[
                SelfPRSection(title="テスト力", content="テスト内容"),
            ],
        )
        assert len(wh.experience) == 1
        assert len(wh.experience[0].projects) == 1
        assert wh.experience[0].projects[0].environment.languages == ["Python"]
        assert len(wh.technical_skills) == 1
        assert len(wh.qualifications) == 1
        assert len(wh.self_pr) == 1


class TestProject:
    def test_minimal(self):
        p = Project(period="2020年", name="テスト")
        assert p.period == "2020年"
        assert p.name == "テスト"
        assert p.environment.languages == []

    def test_with_environment(self):
        p = Project(
            period="2020年",
            name="テスト",
            environment=Environment(
                languages=["Go", "Python"],
                os=["Linux"],
                db=["MySQL"],
                frameworks=["Gin"],
                tools=["Docker"],
            ),
        )
        assert p.environment.languages == ["Go", "Python"]
        assert p.environment.tools == ["Docker"]


class TestLoadYaml:
    def test_load_sample(self):
        sample_path = Path(__file__).parent.parent / "sample" / "data.yaml"
        if not sample_path.exists():
            pytest.skip("sample/data.yaml not found")
        data = load_yaml(sample_path)
        assert data.name == "山田 太郎"
        assert len(data.experience) == 1
        assert len(data.experience[0].projects) == 3
        assert len(data.technical_skills) >= 1
        assert len(data.qualifications) >= 1
        assert len(data.self_pr) >= 1

    def test_load_nonexistent(self):
        with pytest.raises(FileNotFoundError):
            load_yaml("/nonexistent/path.yaml")
