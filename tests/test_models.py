"""Tests for jb_workhistory models and loader."""

from pathlib import Path

import pytest
from pydantic import ValidationError

from jb_workhistory.work_history.loader import load_yaml
from jb_workhistory.work_history.models import (
    Company,
    Environment,
    Project,
    Qualification,
    SelfPRSection,
    SideCompany,
    SideProject,
    SkillCategory,
    SkillItem,
    StandardCompany,
    StandardProject,
    StandardWorkHistory,
    StarCompany,
    StarProject,
    StarWorkHistory,
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


class TestStarProject:
    def test_valid(self):
        p = StarProject(
            period="2020年",
            name="テストプロジェクト",
            situation="既存システムが老朽化していた",
            task="新システムへの移行を完了させること",
            action=["要件定義を実施", "設計・開発を担当"],
            result=["予定通りリリース完了", "障害ゼロを達成"],
        )
        assert p.situation == "既存システムが老朽化していた"
        assert p.task == "新システムへの移行を完了させること"
        assert len(p.action) == 2
        assert len(p.result) == 2

    def test_missing_required_fields(self):
        with pytest.raises(ValidationError):
            StarProject(
                period="2020年",
                name="テスト",
                # situation, task, action, result are required
            )


class TestStarWorkHistory:
    def test_minimal(self):
        wh = StarWorkHistory(date="2024年1月1日現在", name="山田 太郎")
        assert wh.date == "2024年1月1日現在"
        assert wh.experience == []

    def test_full(self):
        wh = StarWorkHistory(
            date="2024年1月1日現在",
            name="山田 太郎",
            experience=[
                StarCompany(
                    company="テスト株式会社",
                    period="2020年4月～現在",
                    projects=[
                        StarProject(
                            period="2020年4月～現在",
                            name="テストプロジェクト",
                            situation="テスト状況",
                            task="テスト課題",
                            action=["行動1", "行動2"],
                            result=["結果1"],
                        )
                    ],
                )
            ],
        )
        assert len(wh.experience) == 1
        proj = wh.experience[0].projects[0]
        assert proj.situation == "テスト状況"
        assert proj.task == "テスト課題"


class TestSideProject:
    def test_minimal(self):
        p = SideProject(period="2023年", name="個人開発")
        assert p.period == "2023年"
        assert p.name == "個人開発"
        assert p.description == ""
        assert p.environment.languages == []

    def test_full(self):
        p = SideProject(
            period="2023年1月～現在",
            name="タスク管理アプリ",
            description="個人プロジェクトとして開発",
            environment=Environment(
                languages=["TypeScript"],
                frameworks=["Next.js"],
            ),
            team_size="1名",
            role="個人開発",
        )
        assert p.name == "タスク管理アプリ"
        assert p.description == "個人プロジェクトとして開発"
        assert p.environment.languages == ["TypeScript"]

    def test_extra_fields_forbidden(self):
        with pytest.raises(ValidationError):
            SideProject(period="2023年", name="テスト", unknown_field="NG")


class TestSideCompany:
    def test_minimal(self):
        sc = SideCompany(company="フリーランス", period="2023年～現在")
        assert sc.company == "フリーランス"
        assert sc.employment_type == ""
        assert sc.projects == []

    def test_full(self):
        sc = SideCompany(
            company="フリーランス",
            period="2023年1月～現在",
            employment_type="業務委託",
            projects=[
                SideProject(period="2023年", name="テストPJ"),
            ],
        )
        assert sc.employment_type == "業務委託"
        assert len(sc.projects) == 1

    def test_missing_required_fields(self):
        with pytest.raises(ValidationError):
            SideCompany()  # type: ignore[call-arg]


class TestSideExperienceInWorkHistory:
    def test_default_empty(self):
        wh = WorkHistory(date="2024年1月1日現在", name="山田 太郎")
        assert wh.side_experience == []

    def test_with_side_experience(self):
        wh = WorkHistory(
            date="2024年1月1日現在",
            name="山田 太郎",
            side_experience=[
                SideCompany(
                    company="フリーランス",
                    period="2023年～現在",
                    projects=[
                        SideProject(period="2023年", name="副業PJ"),
                    ],
                )
            ],
        )
        assert len(wh.side_experience) == 1
        assert wh.side_experience[0].projects[0].name == "副業PJ"

    def test_star_work_history_with_side_experience(self):
        wh = StarWorkHistory(
            date="2024年1月1日現在",
            name="山田 太郎",
            side_experience=[
                SideCompany(
                    company="フリーランス",
                    period="2023年～現在",
                )
            ],
        )
        assert len(wh.side_experience) == 1


class TestLoadYaml:
    def test_load_standard_sample(self):
        sample_path = Path(__file__).parent.parent / "sample" / "work_history_standard.yaml"
        if not sample_path.exists():
            pytest.skip("sample/work_history_standard.yaml not found")
        data = load_yaml(sample_path)
        assert data.name == "山田 太郎"
        assert len(data.experience) == 1
        assert len(data.experience[0].projects) == 3
        assert len(data.technical_skills) >= 1
        assert len(data.qualifications) >= 1
        assert len(data.self_pr) >= 1

    def test_load_star_sample(self):
        sample_path = Path(__file__).parent.parent / "sample" / "work_history_star.yaml"
        if not sample_path.exists():
            pytest.skip("sample/work_history_star.yaml not found")
        data = load_yaml(sample_path, content_format="star")
        assert data.name == "山田 太郎"
        assert len(data.experience) == 1
        assert len(data.experience[0].projects) == 3

    def test_star_yaml_fails_with_standard_format(self):
        """STAR形式YAMLを標準フォーマットで読むとバリデーションエラー."""
        sample_path = Path(__file__).parent.parent / "sample" / "work_history_star.yaml"
        if not sample_path.exists():
            pytest.skip("sample/work_history_star.yaml not found")
        with pytest.raises(ValidationError):
            load_yaml(sample_path, content_format="standard")

    def test_standard_yaml_fails_with_star_format(self):
        """標準形式YAMLをSTARフォーマットで読むとバリデーションエラー."""
        sample_path = Path(__file__).parent.parent / "sample" / "work_history_standard.yaml"
        if not sample_path.exists():
            pytest.skip("sample/work_history_standard.yaml not found")
        with pytest.raises(ValidationError):
            load_yaml(sample_path, content_format="star")

    def test_load_nonexistent(self):
        with pytest.raises(FileNotFoundError):
            load_yaml("/nonexistent/path.yaml")
